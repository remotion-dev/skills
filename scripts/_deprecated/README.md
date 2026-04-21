# Deprecated patch scripts

These scripts were sequential one-off patches applied April 18-21, 2026 during
the dashboard design iterations. Their effects are now baked into
`unify_final.py` (the single canonical post-processor) and the consolidated
stylesheet inside it.

Kept here for historical reference only. Do NOT run any of these against new
dashboards — use `scripts/unify_final.py --target <new-dashboard.html>` instead.

Order of original application (FYI):
1. patch_dashboards_render_status.py — Peter guide + render status JS injection
2. fix_copy_render_js.py — fixed unescaped newline bug in copyRender()
3. redesign_dashboard_v5.py — v5 hero, badges, research accordion
4. unify_dashboard_v6.py — first unified visual pass
5. fix_advanced_text_color.py — readable text inside <details class="u-advanced">
6. polish_v2.py — final consolidator (now lives as unify_final.py)
