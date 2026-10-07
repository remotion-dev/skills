#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lottie JSON 预览 HTML 生成器

用法:
    python generate_preview.py <lottie_json_path> <output_html_path>

功能:
    读取 Lottie JSON 文件，将其嵌入一个自包含的 HTML 页面中，
    使用 lottie-web CDN 播放动画。
"""

import sys
import os
import json


def generate_preview_html(lottie_json_path: str, output_html_path: str):
    """从 Lottie JSON 文件生成自包含的 HTML 预览页面"""

    # 读取 Lottie JSON
    with open(lottie_json_path, 'r', encoding='utf-8') as f:
        lottie_data = json.load(f)

    # 提取动画信息
    width = lottie_data.get('w', 750)
    height = lottie_data.get('h', 720)
    fr = lottie_data.get('fr', 25)
    op = lottie_data.get('op', 90)
    ip = lottie_data.get('ip', 0)
    duration = (op - ip) / fr
    name = lottie_data.get('nm', '动画预览')

    # 将 JSON 序列化为字符串
    json_str = json.dumps(lottie_data, ensure_ascii=False, separators=(',', ':'))

    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            background-color: #1a1a2e;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            color: #e0e0e0;
        }}
        .container {{
            text-align: center;
            padding: 20px;
        }}
        h1 {{
            font-size: 1.5rem;
            margin-bottom: 16px;
            color: #a8b2d1;
            font-weight: 400;
        }}
        #lottie {{
            background-color: #ffffff;
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            overflow: hidden;
            display: inline-block;
        }}
        .info {{
            margin-top: 16px;
            font-size: 0.85rem;
            color: #6b7394;
        }}
        .controls {{
            margin-top: 16px;
            display: flex;
            gap: 12px;
            justify-content: center;
        }}
        .controls button {{
            padding: 8px 20px;
            border: 1px solid #3a3f5c;
            background: #16213e;
            color: #a8b2d1;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.85rem;
            transition: all 0.2s;
        }}
        .controls button:hover {{
            background: #1a2744;
            border-color: #4a5580;
            color: #ccd6f6;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{name}</h1>
        <div id="lottie" style="width:{width}px;height:{height}px;"></div>
        <div class="info">
            {width} x {height}px | {fr}fps | {duration:.1f}s ({op - ip} frames)
        </div>
        <div class="controls">
            <button onclick="anim.stop()">Stop</button>
            <button onclick="anim.play()">Play</button>
            <button onclick="anim.pause()">Pause</button>
            <button onclick="anim.setDirection(anim.playDirection * -1); anim.play()">Reverse</button>
        </div>
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/lottie-web/5.12.2/lottie.min.js"></script>
    <script>
        var animationData = {json_str};
        var anim = lottie.loadAnimation({{
            container: document.getElementById('lottie'),
            renderer: 'svg',
            loop: true,
            autoplay: true,
            animationData: animationData
        }});
    </script>
</body>
</html>"""

    # 写入 HTML 文件
    with open(output_html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"[OK] HTML preview generated: {output_html_path}")
    print(f"     Animation: {name}")
    print(f"     Size: {width}x{height}, {fr}fps, {duration:.1f}s")

    # Auto open in browser
    import webbrowser
    webbrowser.open(os.path.abspath(output_html_path))


def main():
    if len(sys.argv) < 3:
        print("Usage: python generate_preview.py <lottie_json_path> <output_html_path>")
        print()
        print("Example:")
        print("  python generate_preview.py animation.json preview.html")
        sys.exit(1)

    lottie_json_path = sys.argv[1]
    output_html_path = sys.argv[2]

    if not os.path.exists(lottie_json_path):
        print(f"[ERROR] Lottie JSON file not found: {lottie_json_path}")
        sys.exit(1)

    generate_preview_html(lottie_json_path, output_html_path)


if __name__ == '__main__':
    main()
