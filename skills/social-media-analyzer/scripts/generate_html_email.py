#!/usr/bin/env python3
"""
Generate branded HTML email report for Graeham Watts Social Media Performance.
This template is designed to be responsive, professional, and easy to scan quickly.
"""

import json
import sys
from datetime import datetime


def trend_arrow(value):
    """Return trend arrow based on value."""
    if value > 0:
        return "&#9650;"  # ▲
    elif value < 0:
        return "&#9660;"  # ▼
    return "&#9654;"  # ▶ (sideways = flat)


def trend_color(value):
    """Return color based on trend direction."""
    if value > 0:
        return "#2E7D32"  # green
    elif value < 0:
        return "#C62828"  # red
    return "#757575"  # gray


def score_color(score):
    """Return color based on health score."""
    if score >= 80:
        return "#2E7D32"
    elif score >= 60:
        return "#1B365D"
    elif score >= 40:
        return "#F57F17"
    else:
        return "#C62828"


def format_number(n):
    """Format large numbers with commas."""
    if isinstance(n, float):
        return f"{n:,.2f}"
    return f"{n:,}"


def generate_email(analysis_data):
    """Generate the full HTML email from analysis data."""
    overall = analysis_data.get("overall_health", {})
    platforms = analysis_data.get("platforms", {})
    report_date = analysis_data.get("report_date", datetime.now().strftime("%Y-%m-%d"))
    prev_date = analysis_data.get("previous_date", "")

    score = overall.get("score", 0)
    rating = overall.get("rating", "N/A")
    s_color = score_color(score)

    # Build platform sections
    ig = platforms.get("instagram", {})
    fb = platforms.get("facebook", {})
    yt = platforms.get("youtube", {})
    gb = platforms.get("google_business", {})

    def platform_row(name, icon, data):
        if data.get("status") != "ok":
            return f"""
            <tr>
                <td style="padding: 12px 16px; border-bottom: 1px solid #E0E0E0;">{icon} {name}</td>
                <td colspan="3" style="padding: 12px 16px; border-bottom: 1px solid #E0E0E0; color: #999;">Data not available</td>
            </tr>"""

        eng = data.get("avg_engagement_rate", 0)
        score = data.get("health_score", 0)
        wow = data.get("week_over_week", {})

        # Get the most relevant wow metric
        change_key = None
        for k in ["follower_change_pct", "subscriber_change_pct", "rating_change"]:
            if k in wow:
                change_key = k
                break

        change_val = wow.get(change_key, 0) if change_key else 0
        arrow = trend_arrow(change_val)
        t_color = trend_color(change_val)

        return f"""
            <tr>
                <td style="padding: 12px 16px; border-bottom: 1px solid #E0E0E0; font-weight: 600;">{icon} {name}</td>
                <td style="padding: 12px 16px; border-bottom: 1px solid #E0E0E0; text-align: center;">{eng}%</td>
                <td style="padding: 12px 16px; border-bottom: 1px solid #E0E0E0; text-align: center; color: {t_color};">{arrow} {change_val:+.1f}%</td>
                <td style="padding: 12px 16px; border-bottom: 1px solid #E0E0E0; text-align: center;">
                    <span style="background: {score_color(score)}; color: white; padding: 4px 12px; border-radius: 12px; font-size: 13px;">{score}</span>
                </td>
            </tr>"""

    platform_rows = (
        platform_row("Instagram", "📸", ig) +
        platform_row("Facebook", "👥", fb) +
        platform_row("YouTube", "🎬", yt) +
        platform_row("Google Business", "⭐", gb)
    )

    # Best performing content
    best_content_html = ""
    best_items = []
    if ig.get("best_post"):
        best_items.append(("Instagram", ig["best_post"].get("caption", "")[:100], f"{ig['best_post'].get('engagement_rate', 0)}%"))
    if fb.get("best_post"):
        best_items.append(("Facebook", fb["best_post"].get("text", "")[:100], f"{fb['best_post'].get('engagement_rate', 0)}%"))
    if yt.get("best_video"):
        best_items.append(("YouTube", yt["best_video"].get("title", "")[:100], f"{yt['best_video'].get('engagement_rate', 0)}%"))

    for platform, content, eng in best_items[:3]:
        best_content_html += f"""
        <div style="background: #F5F5F5; border-radius: 8px; padding: 16px; margin-bottom: 12px; border-left: 4px solid #C5A258;">
            <div style="font-size: 12px; color: #C5A258; font-weight: 700; text-transform: uppercase; margin-bottom: 4px;">{platform}</div>
            <div style="font-size: 14px; color: #333; margin-bottom: 4px;">{content}...</div>
            <div style="font-size: 13px; color: #1B365D; font-weight: 600;">Engagement: {eng}</div>
        </div>"""

    # Key insights
    insights = []
    if ig.get("status") == "ok":
        if ig.get("avg_engagement_rate", 0) >= 3.0:
            insights.append(("🏆", "Instagram engagement is excellent — above the 3% real estate benchmark"))
        elif ig.get("avg_engagement_rate", 0) < 1.5:
            insights.append(("⚠️", f"Instagram engagement at {ig['avg_engagement_rate']}% — below the 1.5% target"))
        ct = ig.get("content_type_avg_engagement", {})
        if ct:
            best_type = max(ct, key=ct.get)
            insights.append(("💡", f"{best_type.title()}s are your best-performing content type on Instagram"))

    if fb.get("status") == "ok" and fb.get("avg_engagement_rate", 0) >= 1.0:
        insights.append(("🏆", "Facebook engagement above 1% — excellent for real estate"))

    if gb.get("status") == "ok":
        if gb.get("average_rating", 0) >= 4.5:
            insights.append(("⭐", f"Google rating at {gb['average_rating']} — outstanding reputation"))
        if gb.get("response_rate", 0) < 80:
            insights.append(("⚠️", f"Google review response rate at {gb['response_rate']}% — aim for 80%+"))

    insights_html = ""
    for icon, text in insights[:5]:
        insights_html += f"""
        <div style="padding: 10px 0; border-bottom: 1px solid #F0F0F0;">
            <span style="font-size: 16px; margin-right: 8px;">{icon}</span>
            <span style="font-size: 14px; color: #333;">{text}</span>
        </div>"""

    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Weekly Social Media Report — {report_date}</title>
</head>
<body style="margin: 0; padding: 0; background: #F5F5F5; font-family: Arial, Helvetica, sans-serif;">
    <div style="max-width: 640px; margin: 0 auto; background: #FFFFFF;">

        <!-- Header -->
        <div style="background: #1B365D; padding: 32px 24px; text-align: center;">
            <h1 style="color: #FFFFFF; margin: 0 0 4px 0; font-size: 22px; font-weight: 700; letter-spacing: 0.5px;">
                SOCIAL MEDIA PERFORMANCE
            </h1>
            <div style="color: #C5A258; font-size: 14px; font-weight: 600;">
                Weekly Report &bull; {report_date}
            </div>
            <div style="color: rgba(255,255,255,0.6); font-size: 12px; margin-top: 4px;">
                Graeham Watts &mdash; Bay Area Real Estate
            </div>
        </div>

        <!-- Health Score -->
        <div style="text-align: center; padding: 32px 24px; border-bottom: 3px solid #C5A258;">
            <div style="font-size: 13px; color: #999; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">
                Overall Health Score
            </div>
            <div style="font-size: 64px; font-weight: 800; color: {s_color}; line-height: 1;">
                {score}
            </div>
            <div style="font-size: 16px; color: {s_color}; font-weight: 600; margin-top: 4px;">
                {rating}
            </div>
            <div style="font-size: 12px; color: #999; margin-top: 8px;">
                vs. previous week ({prev_date})
            </div>
        </div>

        <!-- Platform Summary Table -->
        <div style="padding: 24px;">
            <h2 style="font-size: 16px; color: #1B365D; margin: 0 0 16px 0; text-transform: uppercase; letter-spacing: 0.5px;">
                Platform Overview
            </h2>
            <table style="width: 100%; border-collapse: collapse; font-size: 14px;">
                <thead>
                    <tr style="background: #F5F5F5;">
                        <th style="padding: 10px 16px; text-align: left; font-size: 12px; color: #999; text-transform: uppercase;">Platform</th>
                        <th style="padding: 10px 16px; text-align: center; font-size: 12px; color: #999; text-transform: uppercase;">Eng. Rate</th>
                        <th style="padding: 10px 16px; text-align: center; font-size: 12px; color: #999; text-transform: uppercase;">Trend</th>
                        <th style="padding: 10px 16px; text-align: center; font-size: 12px; color: #999; text-transform: uppercase;">Score</th>
                    </tr>
                </thead>
                <tbody>
                    {platform_rows}
                </tbody>
            </table>
        </div>

        <!-- Key Insights -->
        <div style="padding: 0 24px 24px;">
            <h2 style="font-size: 16px; color: #1B365D; margin: 0 0 16px 0; text-transform: uppercase; letter-spacing: 0.5px;">
                Key Insights
            </h2>
            {insights_html if insights_html else '<div style="color: #999; font-size: 14px;">No insights available — need more data.</div>'}
        </div>

        <!-- Best Content -->
        <div style="padding: 0 24px 24px;">
            <h2 style="font-size: 16px; color: #1B365D; margin: 0 0 16px 0; text-transform: uppercase; letter-spacing: 0.5px;">
                Top Performing Content
            </h2>
            {best_content_html if best_content_html else '<div style="color: #999; font-size: 14px;">No content data available yet.</div>'}
        </div>

        <!-- Footer -->
        <div style="background: #1B365D; padding: 24px; text-align: center;">
            <div style="color: rgba(255,255,255,0.8); font-size: 13px; margin-bottom: 8px;">
                Full PDF report and data spreadsheet attached
            </div>
            <div style="color: #C5A258; font-size: 12px;">
                Generated by Social Media Analyzer &bull; Graeham Watts Real Estate
            </div>
        </div>

    </div>
</body>
</html>"""

    return html


if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            data = json.load(f)
    else:
        # Sample data for testing
        data = {
            "report_date": datetime.now().strftime("%Y-%m-%d"),
            "previous_date": "2026-03-25",
            "overall_health": {"score": 72, "rating": "Good"},
            "platforms": {
                "instagram": {"status": "ok", "avg_engagement_rate": 2.4, "health_score": 75,
                    "week_over_week": {"follower_change_pct": 1.2},
                    "best_post": {"caption": "Just listed! Beautiful 4BR home in Los Altos Hills", "engagement_rate": 4.2},
                    "content_type_avg_engagement": {"reel": 3.1, "carousel": 2.0, "image": 1.5}},
                "facebook": {"status": "ok", "avg_engagement_rate": 0.8, "health_score": 65,
                    "week_over_week": {"follower_change_pct": 0.3},
                    "best_post": {"text": "Market update: Bay Area spring inventory is up 12%", "engagement_rate": 1.5}},
                "youtube": {"status": "no_data"},
                "google_business": {"status": "ok", "average_rating": 4.8, "health_score": 90,
                    "response_rate": 92, "week_over_week": {"rating_change": 0.1}},
            }
        }

    html = generate_email(data)
    output_path = sys.argv[2] if len(sys.argv) > 2 else "weekly-email-report.html"
    with open(output_path, 'w') as f:
        f.write(html)
    print(f"Email report generated: {output_path}")
