#!/usr/bin/env python3
import sys
import os
import json
import shutil
import datetime
import webbrowser

def generate_preview_html(lottie_json_path: str, output_html_path: str, version_name: str, versions: list):
    with open(lottie_json_path, 'r', encoding='utf-8') as f:
        lottie_data = json.load(f)

    width = lottie_data.get('w', 750)
    height = lottie_data.get('h', 720)
    fr = lottie_data.get('fr', 60)
    op = lottie_data.get('op', 180)
    ip = lottie_data.get('ip', 0)
    duration = (op - ip) / fr
    name = lottie_data.get('nm', '动画预览')

    json_str = json.dumps(lottie_data, ensure_ascii=False, separators=(',', ':'))

    version_links = ""
    for v in versions:
        active_style = "background: #4a5580; color: #fff;" if v['name'] == version_name else ""
        version_links += f'<a href="{v["path"]}" style="{active_style}">{v["name"]}</a>\n'

    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} - {version_name}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ background-color: #1a1a2e; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh; font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; color: #e0e0e0; }}
        .header {{ text-align: center; margin-bottom: 20px; }}
        h1 {{ font-size: 1.5rem; margin-bottom: 8px; color: #a8b2d1; font-weight: 400; }}
        .version-badge {{ background: #3a3f5c; padding: 4px 12px; border-radius: 12px; font-size: 0.85rem; }}
        .layout {{ display: flex; gap: 30px; align-items: flex-start; max-width: 1200px; width: 100%; padding: 0 20px; }}
        .sidebar {{ width: 250px; background: #16213e; padding: 20px; border-radius: 12px; border: 1px solid #3a3f5c; }}
        .sidebar h3 {{ margin-bottom: 15px; color: #a8b2d1; border-bottom: 1px solid #3a3f5c; padding-bottom: 10px; }}
        .versions {{ display: flex; flex-direction: column; gap: 8px; max-height: 380px; overflow-y: auto; padding-right: 5px; }}
        .versions::-webkit-scrollbar {{ width: 6px; }}
        .versions::-webkit-scrollbar-track {{ background: #16213e; border-radius: 4px; }}
        .versions::-webkit-scrollbar-thumb {{ background: #3a3f5c; border-radius: 4px; }}
        .versions::-webkit-scrollbar-thumb:hover {{ background: #4a5580; }}
        .versions a {{ padding: 10px; background: #1a1a2e; color: #a8b2d1; text-decoration: none; border-radius: 6px; border: 1px solid #3a3f5c; transition: all 0.2s; font-size: 0.9rem; box-sizing: border-box; }}
        .versions a:hover {{ background: #1a2744; border-color: #4a5580; }}
        .main-content {{ flex: 1; text-align: center; }}
        #lottie {{ background-color: #ffffff; border-radius: 12px; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3); overflow: hidden; display: inline-block; }}
        .info {{ margin-top: 16px; font-size: 0.85rem; color: #6b7394; }}
        .controls {{ margin-top: 16px; display: flex; gap: 12px; justify-content: center; }}
        .controls button {{ padding: 8px 20px; border: 1px solid #3a3f5c; background: #16213e; color: #a8b2d1; border-radius: 6px; cursor: pointer; font-size: 0.85rem; transition: all 0.2s; }}
        .controls button:hover {{ background: #1a2744; border-color: #4a5580; color: #ccd6f6; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{name}</h1>
        <span class="version-badge">当前版本: {version_name}</span>
    </div>
    
    <div class="layout">
        <div class="sidebar">
            <h3>版本历史</h3>
            <div class="versions">
                {version_links}
            </div>
        </div>
        
        <div class="main-content">
            <div id="lottie" style="width:{width}px;height:{height}px;"></div>
            <div class="info">{width} x {height}px | {fr}fps | {duration:.1f}s</div>
            <div class="controls">
                <button onclick="anim.stop()">Stop</button>
                <button onclick="anim.play()">Play</button>
                <button onclick="anim.pause()">Pause</button>
                <button onclick="anim.setDirection(anim.playDirection * -1); anim.play()">Reverse</button>
            </div>
        </div>
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/lottie-web/5.12.2/lottie.min.js"></script>
    <script>
        var anim = lottie.loadAnimation({{
            container: document.getElementById('lottie'),
            renderer: 'svg',
            loop: true,
            autoplay: true,
            animationData: {json_str}
        }});
    </script>
</body>
</html>"""

    with open(output_html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

def main():
    if len(sys.argv) < 3:
        sys.exit(1)
        
    source_json = sys.argv[1]
    version_desc = sys.argv[2] # e.g. "V1-初始肢体动画" or "V2-爱心轨迹修正"
    
    base_name = os.path.splitext(os.path.basename(source_json))[0]
    # 如果原名带“静态”等字眼，可以保留或者替换
    clean_name = base_name.replace('-静态', '')
    out_dir = f"/Users/user/Desktop/Skill专用/AI Lottie工具/_history_versions/{clean_name}_动画版本"
    
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    
    # 获取现有版本列表
    existing_versions = []
    if os.path.exists(out_dir):
        files = os.listdir(out_dir)
        html_files = [f for f in files if f.endswith('.html')]
        
        def get_v_num(filename):
            try:
                # "V14-侧导航折叠列表样式优化_135044.html" -> split('-')[0] -> "V14" -> [1:] -> 14
                return int(filename.split('-')[0][1:])
            except:
                return -1
                
        html_files.sort(key=get_v_num, reverse=True)
        
        for f in html_files:
            v_name = f.replace('.html', '')
            existing_versions.append({
                "name": v_name,
                "path": f # relative path for siblings
            })
            
    # Check existing versions to see if we are re-running the exact same version desc
    # If so, we should delete the old one and replace it rather than spawning a duplicate
    filtered_existing = []
    for ev in existing_versions:
        # e.g. ev["name"] = "V10-修复前臂阴影脱节错位_133241"
        # version_desc = "V10-修复前臂阴影脱节错位"
        if ev["name"].startswith(version_desc + "_"):
            # Old duplicate detected, trash the html and json
            old_html_path = os.path.join(out_dir, ev["name"] + ".html")
            old_json_path = os.path.join(out_dir, ev["name"] + ".json")
            if os.path.exists(old_html_path): os.remove(old_html_path)
            if os.path.exists(old_json_path): os.remove(old_json_path)
        else:
            filtered_existing.append(ev)
            
    # 新版本信息
    timestamp = datetime.datetime.now().strftime("%H%M%S")
    new_version_name = f"{version_desc}_{timestamp}"
    new_html_name = f"{new_version_name}.html"
    new_json_name = f"{new_version_name}.json"
    
    new_html_path = os.path.join(out_dir, new_html_name)
    new_json_path = os.path.join(out_dir, new_json_name)
    
    # 把当前版本加入列表顶部 (作为当前正在生成的版本)
    versions_for_render = [{"name": new_version_name, "path": new_html_name}] + filtered_existing

    # 复制当前的 JSON 到历史记录
    shutil.copy2(source_json, new_json_path)
    
    # helper: 生成完整的侧边栏链接 html snippet
    def build_sidebar_html(v_list, current_v_name):
        links = ""
        for v in v_list:
            active_style = "background: #4a5580; color: #fff;" if v['name'] == current_v_name else ""
            links += f'<a href="{v["path"]}" style="{active_style}">{v["name"]}</a>\n'
        return links

    # 生成当前的新版本
    generate_preview_html(new_json_path, new_html_path, new_version_name, versions_for_render)
    
    # 遍历已存在的老版本文件，替换掉其 version 标签里的内容
    for old_v in existing_versions:
        old_path = os.path.join(out_dir, old_v["path"])
        if os.path.exists(old_path):
            with open(old_path, 'r', encoding='utf-8') as f:
                old_html = f.read()
            
            # 使用简单的字符串替换。因为我们模板里有确切的 `<div class="versions">`
            # 我们只需要更新这部分里面的内容
            start_tag = '<div class="versions">'
            end_tag = '</div>'
            
            start_idx = old_html.find(start_tag)
            end_idx = old_html.find(end_tag, start_idx)
            
            if start_idx != -1 and end_idx != -1:
                old_html = old_html[:start_idx + len(start_tag)] + "\n                " + build_sidebar_html(versions_for_render, old_v["name"]) + "            " + old_html[end_idx:]
                with open(old_path, 'w', encoding='utf-8') as f:
                    f.write(old_html)
    
    print(f"Version saved: {new_html_path}")
    os.system(f'open "{os.path.abspath(new_html_path)}"')

if __name__ == '__main__':
    main()
