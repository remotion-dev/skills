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
The skill orchestrates: read inputs, run this script, humanize the prose,
push to GitHub via direct git, create the Gmail draft.

WEEK-OVER-WEEK MODEL (added 2026-06-22)
---------------------------------------
The uploaded ShowingTime/Glide export is CUMULATIVE: it holds every showing and
disclosure pull since the listing went live, each stamped with a date. That single
file IS the running history. This script buckets every dated row into calendar
weeks (Mon-Sun) so the report can show the climb week 1 -> week 2 -> ... -> total
and emphasize the most recent week. No separate database is needed; prior published
reports serve only as a backup cross-check.

If a row has no parseable date, it falls into an "undated" bucket and is still
counted in the cumulative totals, so the report never loses an interaction — it
just cannot place it on the weekly curve.
"""

import argparse, calendar, json, re, sys
from datetime import datetime, timedelta
from pathlib import Path

try:
    import openpyxl
except ImportError:
    print("ERROR: openpyxl not installed. Run: pip install openpyxl --break-system-packages", file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------------------
# Text helpers
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Date helpers — used to bucket activity into weeks
# ---------------------------------------------------------------------------

def parse_dt(val):
    """Best-effort parse of a cell value into a date. Returns datetime or None."""
    if val is None:
        return None
    if isinstance(val, datetime):
        return val
    s = str(val).strip()
    if not s:
        return None
    # strip a trailing time if it confuses the parser
    s_main = s.split(' ')[0] if ' ' in s and '/' in s.split(' ')[0] or '-' in s.split(' ')[0] else s
    fmts = ['%m/%d/%Y', '%m/%d/%y', '%Y-%m-%d', '%m-%d-%Y', '%m-%d-%y',
            '%m/%d/%Y %H:%M', '%m/%d/%y %I:%M %p', '%Y-%m-%d %H:%M:%S']
    for f in fmts:
        try:
            return datetime.strptime(s, f)
        except ValueError:
            continue
    for f in ['%m/%d/%Y', '%m/%d/%y', '%Y-%m-%d']:
        try:
            return datetime.strptime(s_main, f)
        except ValueError:
            continue
    # last resort: pull the first date-looking token
    m = re.search(r'(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})', s)
    if m:
        mo, da, yr = m.groups()
        yr = int(yr)
        if yr < 100:
            yr += 2000
        try:
            return datetime(yr, int(mo), int(da))
        except ValueError:
            return None
    return None


def week_start(dt):
    """Monday of the week containing dt (date-only)."""
    d = datetime(dt.year, dt.month, dt.day)
    return d - timedelta(days=d.weekday())


def week_label(monday):
    return f"{calendar.month_abbr[monday.month]} {monday.day}"


def find_date_col(ws, header_keywords, exclude_idxs):
    """Scan the header row for a column whose header matches any keyword.
    Returns the 0-based column index, or None. Used additively so name/feedback
    columns keep their known-good fixed indices and only the date is auto-located."""
    header = next(ws.iter_rows(values_only=True, max_row=1), None)
    if not header:
        return None
    for idx, cell in enumerate(header):
        if idx in exclude_idxs or cell is None:
            continue
        h = str(cell).strip().lower()
        if any(k in h for k in header_keywords):
            return idx
    return None


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

def parse_showing_file(path):
    wb = openpyxl.load_workbook(path, data_only=True)
    supra_agents, glide_agents = [], []

    if 'Showing Activity (Suprashowing)' in wb.sheetnames:
        ws = wb['Showing Activity (Suprashowing)']
        # name=1, datetime=4, feedback=6 are the known-good Supra indices
        for row in ws.iter_rows(values_only=True, min_row=2):
            if row[1]:
                supra_agents.append({
                    'name': initial_format(row[1]),
                    'feedback': clean_feedback(row[6]) if len(row) > 6 else '',
                    'date': parse_dt(row[4]) if len(row) > 4 else None,
                    'kind': 'showing',
                })

    if 'Glide View Activity' in wb.sheetnames:
        ws = wb['Glide View Activity']
        # name=2, feedback=10 are known-good; date column is auto-located by header
        date_col = find_date_col(ws, ['date', 'time', 'viewed', 'accessed', 'activity'], exclude_idxs={2, 10})
        seen = set()
        for row in ws.iter_rows(values_only=True, min_row=2):
            if not row[2]:
                continue
            name_raw = str(row[2]).strip().replace('\n', ' ')
            if 'Invited by' in name_raw or name_raw in seen:
                continue
            seen.add(name_raw)
            dt = parse_dt(row[date_col]) if (date_col is not None and len(row) > date_col) else None
            glide_agents.append({
                'name': initial_format(name_raw),
                'feedback': clean_feedback(row[10]) if len(row) > 10 else '',
                'date': dt,
                'kind': 'disclosure',
            })

    all_records = supra_agents + glide_agents
    all_feedback = ' '.join([a['feedback'].lower() for a in all_records])
    themes = build_themes(all_feedback)

    return {
        'supra_agents': supra_agents,
        'glide_agents': glide_agents,
        'all_records': all_records,
        'counts': {
            'showings': len(supra_agents),
            'disclosures': len(glide_agents),
            'total_interactions': len(all_records),
        },
        'themes': themes,
    }


def build_themes(all_feedback):
    return {
        'tenant': count_mentions(all_feedback, ['tenant', 'occupied']),
        'price': count_mentions(all_feedback, ['price', 'negotiat', 'asking']),
        'neighbor': count_mentions(all_feedback, ['neighbor']),
        'location': count_mentions(all_feedback, ['location', 'east side', 'west side', 'surrounding']),
        'no_longer': count_mentions(all_feedback, ['no longer interested', 'not interested']),
        'lost_to_other': count_mentions(all_feedback, ['purchased', 'in contract', 'went into contract', 'closed deal', 'another property', 'different property']),
        'forgot': count_mentions(all_feedback, ['forgot', 'long time ago', 'doesnt remember', "doesn't remember"]),
    }


THEME_LABELS = {
    'tenant': 'Tenant occupancy',
    'price': 'Price / negotiation interest',
    'neighbor': 'Neighbor / street concern',
    'location': 'Location preference',
    'no_longer': 'No longer interested',
    'lost_to_other': 'Lost to competing inventory',
    'forgot': 'Forgot the property',
}


# ---------------------------------------------------------------------------
# Week-over-week bucketing
# ---------------------------------------------------------------------------

def build_weekly(all_records, recent_weeks=6):
    """Bucket records into calendar weeks. Returns ordered weekly rows plus
    this-week deltas, cumulative totals, and a momentum read."""
    buckets = {}
    undated = {'showings': 0, 'disclosures': 0, 'new_feedback': 0}
    for r in all_records:
        if not r['date']:
            undated['showings'] += 1 if r['kind'] == 'showing' else 0
            undated['disclosures'] += 1 if r['kind'] == 'disclosure' else 0
            undated['new_feedback'] += 1 if r['feedback'] else 0
            continue
        wk = week_start(r['date'])
        b = buckets.setdefault(wk, {'showings': 0, 'disclosures': 0, 'new_feedback': 0,
                                    'feedback': [], 'themes': ''})
        b['showings'] += 1 if r['kind'] == 'showing' else 0
        b['disclosures'] += 1 if r['kind'] == 'disclosure' else 0
        if r['feedback']:
            b['new_feedback'] += 1
            b['feedback'].append(r['feedback'].lower())

    ordered_keys = sorted(buckets.keys())
    weeks = []
    for k in ordered_keys:
        b = buckets[k]
        wk_themes = build_themes(' '.join(b['feedback']))
        top = max(wk_themes.items(), key=lambda kv: kv[1]) if any(wk_themes.values()) else (None, 0)
        weeks.append({
            'week_start': k.strftime('%Y-%m-%d'),
            'label': week_label(k),
            'showings': b['showings'],
            'disclosures': b['disclosures'],
            'new_feedback': b['new_feedback'],
            'interactions': b['showings'] + b['disclosures'],
            'top_theme': THEME_LABELS.get(top[0]) if top[1] else None,
        })

    this_week = weeks[-1] if weeks else None
    prior_week = weeks[-2] if len(weeks) >= 2 else None

    def delta(cur, prev, key):
        if prev is None:
            return None
        return cur[key] - prev[key]

    this_week_deltas = None
    if this_week:
        this_week_deltas = {
            'showings': delta(this_week, prior_week, 'showings'),
            'disclosures': delta(this_week, prior_week, 'disclosures'),
            'interactions': delta(this_week, prior_week, 'interactions'),
        }

    # momentum: most-recent week interactions vs trailing 3-week average
    momentum = 'steady'
    if len(weeks) >= 2:
        recent = this_week['interactions']
        trail = [w['interactions'] for w in weeks[-4:-1]]
        avg = sum(trail) / len(trail) if trail else 0
        if recent > avg * 1.25 and recent > 0:
            momentum = 'accelerating'
        elif recent < avg * 0.6:
            momentum = 'cooling'

    cumulative = {
        'showings': sum(w['showings'] for w in weeks) + undated['showings'],
        'disclosures': sum(w['disclosures'] for w in weeks) + undated['disclosures'],
    }
    cumulative['interactions'] = cumulative['showings'] + cumulative['disclosures']

    # collapse older weeks into an "Earlier" rollup for readability
    detailed = weeks[-recent_weeks:]
    older = weeks[:-recent_weeks]
    earlier_rollup = None
    if older:
        earlier_rollup = {
            'label': f"Earlier ({older[0]['label']}–{older[-1]['label']})",
            'showings': sum(w['showings'] for w in older),
            'disclosures': sum(w['disclosures'] for w in older),
            'new_feedback': sum(w['new_feedback'] for w in older),
            'interactions': sum(w['interactions'] for w in older),
        }

    return {
        'weeks': weeks,
        'detailed_weeks': detailed,
        'earlier_rollup': earlier_rollup,
        'undated': undated if (undated['showings'] or undated['disclosures']) else None,
        'this_week': this_week,
        'prior_week': prior_week,
        'this_week_deltas': this_week_deltas,
        'momentum': momentum,
        'cumulative': cumulative,
        'dated': bool(weeks),
    }


# ---------------------------------------------------------------------------
# Offers + warm leads
# ---------------------------------------------------------------------------

OFFER_KEYWORDS = ['accepted offer', 'offer accepted', 'submitted an offer', 'submitted offer',
                  'wrote an offer', 'made an offer', 'received an offer', 'offer received',
                  'offer in', 'will write', 'writing an offer', 'in escrow']


def detect_offer_signals(data):
    """Conservative scan for offer-relevant rows. These are CANDIDATES for the
    report's offer banner — Claude confirms and enriches (price, terms, status)
    from context or from the --offers argument. Deliberately excludes
    'in contract with ANOTHER property', which means a buyer lost elsewhere."""
    signals = []
    for agent in data['all_records']:
        fb = agent['feedback'].lower()
        if not fb:
            continue
        if any(k in fb for k in OFFER_KEYWORDS):
            # exclude buyers who went under contract elsewhere
            if 'another' in fb or 'different property' in fb or 'elsewhere' in fb:
                continue
            signals.append({'name': agent['name'], 'feedback': agent['feedback'],
                            'date': agent['date'].strftime('%Y-%m-%d') if agent['date'] else None})
    return signals


def detect_warm_leads(data):
    leads = []
    keywords = {
        'price-negotiation': ['interested but', 'wants to negotiate', 'negotiate price', 'room to negotiate'],
        'active-disclosure': ['accessed disclosures', 'discuss with my clients', 'will get back'],
        'tenant-investor': ['how many tenants', 'month to month', 'how much is the rent', 'is it still occupied'],
    }
    for agent in data['all_records']:
        fb_lower = agent['feedback'].lower()
        for signal, kws in keywords.items():
            if any(k in fb_lower for k in kws):
                leads.append({'name': agent['name'], 'signal': signal})
                break
    return leads


def determine_status(data, weekly, offers_count):
    if offers_count > 0:
        return {'level': 'green', 'headline': 'Status · Offer In Hand',
                'message': 'An offer is on the table. Decision and negotiation in focus.'}
    this_week = weekly['this_week']
    tw_showings = this_week['showings'] if this_week else 0
    warm = len(detect_warm_leads(data))
    if weekly['momentum'] == 'accelerating' and tw_showings >= 1:
        return {'level': 'green', 'headline': 'Status · Active',
                'message': 'Activity is picking up week over week, warm leads in motion.'}
    if tw_showings == 0 and warm < 2:
        return {'level': 'amber', 'headline': 'Status · Attention Needed',
                'message': 'Activity has cooled this week. A decision on next phase is due.'}
    return {'level': 'amber', 'headline': 'Status · Watch',
            'message': 'Some activity, no offers yet.'}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

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
    ap.add_argument('--recent-weeks', type=int, default=6,
                    help='How many most-recent weeks to show individually before rolling older ones into "Earlier".')
    ap.add_argument('--offers', default=None,
                    help='Optional JSON array of confirmed offers, e.g. '
                         '[{"agent":"Sheila S.","price":1050000,"status":"accepted","terms":"...","date":"2026-04-15"}]')
    ap.add_argument('--output', required=True, type=Path)
    args = ap.parse_args()

    report_date = datetime.now() if not args.report_date else datetime.strptime(args.report_date, '%Y-%m-%d')
    listed_date = datetime.strptime(args.listed_date, '%Y-%m-%d')
    dom = (report_date - listed_date).days

    data = parse_showing_file(args.showing_file)
    weekly = build_weekly(data['all_records'], recent_weeks=args.recent_weeks)

    # offers: explicit --offers wins; otherwise fall back to candidate signals
    offer_signals = detect_offer_signals(data)
    offers = []
    if args.offers:
        try:
            offers = json.loads(args.offers)
        except json.JSONDecodeError:
            print("WARN: --offers was not valid JSON; using detected signals instead.", file=sys.stderr)
    offers_count = len(offers) if offers else len(offer_signals)

    warm_leads = detect_warm_leads(data)
    status = determine_status(data, weekly, offers_count)
    ppsf = round(args.list_price / args.sqft)

    # dominant themes overall, sorted
    sorted_themes = sorted(
        [(THEME_LABELS.get(k, k), v) for k, v in data['themes'].items() if v > 0],
        key=lambda kv: kv[1], reverse=True
    )

    out = {
        'address': args.address,
        'report_date': report_date.strftime('%Y-%m-%d'),
        'dom': dom,
        'ppsf': ppsf,
        'status': status,
        'momentum': weekly['momentum'],
        'cumulative': weekly['cumulative'],
        'this_week': weekly['this_week'],
        'this_week_deltas': weekly['this_week_deltas'],
        'weeks': weekly['weeks'],
        'detailed_weeks': weekly['detailed_weeks'],
        'earlier_rollup': weekly['earlier_rollup'],
        'undated': weekly['undated'],
        'dated': weekly['dated'],
        'offers': offers,
        'offer_signals': offer_signals,
        'offers_count': offers_count,
        'warm_leads': [l['name'] for l in warm_leads],
        'themes_overall': sorted_themes,
        'counts': data['counts'],
    }
    print(json.dumps(out, indent=2, default=str))

    if not weekly['dated']:
        print("\nNOTE: No parseable dates found in the export, so the week-over-week "
              "curve could not be built. The report will fall back to a single 'this period' "
              "view. Check that the export includes Date/Time columns.", file=sys.stderr)


if __name__ == '__main__':
    main()
