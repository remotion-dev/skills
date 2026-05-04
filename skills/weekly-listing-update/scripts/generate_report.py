#!/usr/bin/env python3
"""
weekly-listing-update — report generator

Usage (from skill):
    python3 generate_report.py \\
        --showing-file path/to/showing.xlsx \\
        --address "1908 Cooley Ave" \\
        --city "East Palo Alto" \\
        --state CA \\
        --beds 3 --baths 1 --sqft 1210 \\
        --list-price 1095000 \\
        --mls ML82027334 \\
        --seller-name "Michael" \\
        --listed-date 2025-11-14 \\
        --output path/to/output.html

Designed to be invoked by Claude inside the weekly-listing-update skill.
The skill orchestrates: read inputs, run this script, push to GitHub via Composio, create Gmail draft.
"""

import argparse, json, re, sys
from datetime import datetime
from pathlib import Path

try:
    import openpyxl
except ImportError:
    print("ERROR: openpyxl not installed. Run: pip install openpyxl --break-system-packages", file=sys.stderr)
    sys.exit(1)


def initial_format(name):
    if not name:
        return ""
    name = str(name).strip().replace('\n', ' ').replace('  ', ' ')
    if '/' in name:
        name = name.split('/')[0].strip()
    parts = [p for p in name.split() if p and not p.startswith('(')]
    if len(parts) >= 2:
        return f"{parts[0].title()} {parts[-1][0].upper()}."
    return parts[0].title() if parts else name


def clean_feedback(fb):
    if not fb:
        return ""
    fb = str(fb).strip().replace('\n', ' ').replace('  ', ' ')
    fb = re.sub(r'^\d{1,2}/\d{1,2}/\d{2,4}[\s\-:]*', '', fb)
    return fb


def count_mentions(text, keywords):
    text = text.lower()
    return sum(text.count(k.lower()) for k in keywords)


def parse_showing_file(path):
    wb = openpyxl.load_workbook(path, data_only=True)
    supra_agents, glide_agents = [], []

    if 'Showing Activity (Suprashowing)' in wb.sheetnames:
        ws = wb['Showing Activity (Suprashowing)']
        for row in ws.iter_rows(values_only=True, min_row=2):
            if row[1]:
                supra_agents.append({'name': initial_format(row[1]), 'feedback': clean_feedback(row[6]), 'datetime': row[4]})

    if 'Glide View Activity' in wb.sheetnames:
        ws = wb['Glide View Activity']
        seen = set()
        for row in ws.iter_rows(values_only=True, min_row=2):
            if not row[2]:
                continue
            name_raw = str(row[2]).strip().replace('\n', ' ')
            if 'Invited by' in name_raw or name_raw in seen:
                continue
            seen.add(name_raw)
            glide_agents.append({'name': initial_format(name_raw), 'feedback': clean_feedback(row[10])})

    all_feedback = ' '.join([a['feedback'].lower() for a in supra_agents + glide_agents])
    themes = {
        'tenant': count_mentions(all_feedback, ['tenant', 'occupied']),
        'price': count_mentions(all_feedback, ['price', 'negotiat', 'asking']),
        'neighbor': count_mentions(all_feedback, ['neighbor']),
        'location': count_mentions(all_feedback, ['location', 'east side', 'west side', 'surrounding']),
        'no_longer': count_mentions(all_feedback, ['no longer interested', 'not interested']),
        'in_contract': count_mentions(all_feedback, ['purchased', 'in contract', 'went into contract', 'closed deal']),
        'forgot': count_mentions(all_feedback, ['forgot', 'long time ago', 'doesnt remember', "doesn't remember"]),
    }

    return {
        'supra_agents': supra_agents,
        'glide_agents': glide_agents,
        'counts': {'showings': len(supra_agents), 'disclosures': len(glide_agents), 'total_interactions': len(supra_agents) + len(glide_agents)},
        'themes': themes,
    }


def detect_warm_leads(data):
    leads = []
    keywords = {
        'price-negotiation': ['interested but', 'wants to negotiate', 'negotiate price'],
        'active-disclosure': ['accessed disclosures', 'discuss with my clients', 'will get back'],
        'tenant-investor': ['how many tenants', 'month to month', 'how much is the rent'],
    }
    for agent in data['supra_agents'] + data['glide_agents']:
        fb_lower = agent['feedback'].lower()
        for signal, kws in keywords.items():
            if any(k in fb_lower for k in kws):
                leads.append({**agent, 'signal': signal})
                break
    return leads


def determine_status(data, args):
    showings = data['counts']['showings']
    warm_leads = len(detect_warm_leads(data))
    if showings == 0 and warm_leads < 2:
        return {'level': 'amber', 'headline': 'Status - Attention Needed', 'message': 'Activity has cooled. Decision needed on next phase.'}
    elif showings >= 2 and warm_leads >= 2:
        return {'level': 'green', 'headline': 'Status - Active', 'message': 'Showings continuing, multiple warm leads in motion.'}
    return {'level': 'amber', 'headline': 'Status - Watch', 'message': 'Some activity, no offers yet.'}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--showing-file', required=True, type=Path)
    ap.add_argument('--address', required=True)
    ap.add_argument('--city', required=True)
    ap.add_argument('--state', default='CA')
    ap.add_argument('--beds', type=int, required=True)
    ap.add_argument('--baths', type=float, required=True)
    ap.add_argument('--sqft', type=int, required=True)
    ap.add_argument('--list-price', type=int, required=True)
    ap.add_argument('--mls', required=True)
    ap.add_argument('--seller-name', required=True)
    ap.add_argument('--listed-date', required=True)
    ap.add_argument('--report-date', default=None)
    ap.add_argument('--output', required=True, type=Path)
    args = ap.parse_args()

    report_date = datetime.now() if not args.report_date else datetime.strptime(args.report_date, '%Y-%m-%d')
    listed_date = datetime.strptime(args.listed_date, '%Y-%m-%d')
    dom = (report_date - listed_date).days

    data = parse_showing_file(args.showing_file)
    warm_leads = detect_warm_leads(data)
    status = determine_status(data, args)
    ppsf = args.list_price / args.sqft

    print(json.dumps({
        'showings': data['counts']['showings'],
        'disclosures': data['counts']['disclosures'],
        'warm_leads': [l['name'] for l in warm_leads],
        'themes': data['themes'],
        'status': status,
        'dom': dom,
        'ppsf': round(ppsf),
    }, indent=2, default=str))


if __name__ == '__main__':
    main()
