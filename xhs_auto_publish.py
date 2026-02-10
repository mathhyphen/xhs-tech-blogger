#!/usr/bin/env python3
"""
XHS一键发布脚本 - OpenClaw Browser版
使用openclaw browser自动打开小红书并填写内容

Usage:
    python xhs_auto_publish.py <content_file>  # 发布指定文件
    python xhs_auto_publish.py --latest        # 发布最新的日报
"""

import argparse
import subprocess
import time
from pathlib import Path

def find_latest_content():
    """找到最新的内容文件"""
    output_dir = Path(__file__).parent / 'output'
    if not output_dir.exists():
        return None
    
    files = sorted(output_dir.glob('xhs_ai_news_*.txt'), reverse=True)
    return files[0] if files else None

def read_content(filepath):
    """读取内容文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def extract_title_and_content(full_content):
    """提取标题和正文"""
    lines = full_content.split('\n')
    title = lines[0].replace('标题：', '').strip() if lines[0].startswith('标题：') else lines[0]
    body = '\n'.join(lines[1:]).strip()
    return title, body

def publish_with_openclaw_browser(content_file):
    """使用OpenClaw Browser发布"""
    # 读取内容
    full_content = read_content(content_file)
    title, body = extract_title_and_content(full_content)
    
    print("=" * 70)
    print("XHS一键发布 - OpenClaw Browser版")
    print("=" * 70)
    print(f"\n标题: {title[:50]}...")
    print(f"正文长度: {len(body)} 字符")
    print()
    
    # 1. 打开小红书创作平台
    print("[1/3] 正在打开小红书创作平台...")
    subprocess.run([
        'openclaw', 'browser', 'navigate',
        'https://creator.xiaohongshu.com/publish/publish'
    ])
    time.sleep(5)
    
    # 2. 截图确认页面
    print("[2/3] 确认页面状态...")
    subprocess.run(['openclaw', 'browser', 'screenshot'])
    print("      请查看截图确认页面已加载")
    
    # 3. 填写内容（使用evaluate执行JavaScript）
    print("[3/3] 填写内容...")
    
    # 准备内容（转义特殊字符）
    title_js = title.replace("'", "\\'").replace('"', '\\"')
    body_js = body.replace("'", "\\'").replace('"', '\\"').replace('\n', '\\n')
    
    # 构建JavaScript代码
    js_code = f"""
    (function() {{
        // 填写标题
        const titleInputs = document.querySelectorAll('input, textarea');
        for (let input of titleInputs) {{
            if (input.placeholder && input.placeholder.includes('标题')) {{
                input.value = '{title_js}';
                input.dispatchEvent(new Event('input', {{ bubbles: true }}));
                break;
            }}
        }}
        
        // 填写正文
        const bodyInputs = document.querySelectorAll('textarea');
        for (let input of bodyInputs) {{
            if (input.placeholder && (input.placeholder.includes('正文') || input.placeholder.includes('内容'))) {{
                input.value = '{body_js}';
                input.dispatchEvent(new Event('input', {{ bubbles: true }}));
                break;
            }}
        }}
        
        return 'Content filled successfully';
    }})()
    """
    
    subprocess.run([
        'openclaw', 'browser', 'evaluate',
        '--fn', js_code
    ])
    
    print()
    print("=" * 70)
    print("[OK] 内容已自动填写到小红书创作平台")
    print()
    print("[下一步] 请手动完成:")
    print("  1. 点击'上传图文'标签（如需要）")
    print("  2. 使用 nano-banana-pro 生成并上传封面图")
    print("  3. 检查内容无误后点击发布")
    print("=" * 70)

def generate_cover_with_nano_banana(title):
    """使用nano-banana-pro skill生成封面"""
    print()
    print("=" * 70)
    print("生成封面图 - 使用 nano-banana-pro")
    print("=" * 70)
    
    prompt = f"A modern tech news cover for AI daily newsletter. Title: '{title}'. Dark blue gradient background, neon cyan glow effects, futuristic AI circuit patterns. Clean minimalist style, vertical 3:4 layout."
    
    print(f"生成提示词: {prompt[:80]}...")
    print()
    print("请运行以下命令生成封面图:")
    print(f'  npx openclaw skills run nano-banana-pro --prompt "{prompt}"')
    print()

def main():
    parser = argparse.ArgumentParser(description='XHS一键发布 - OpenClaw Browser版')
    parser.add_argument('file', nargs='?', help='内容文件路径')
    parser.add_argument('--latest', action='store_true', help='发布最新生成的日报')
    parser.add_argument('--cover', action='store_true', help='同时生成封面图')
    
    args = parser.parse_args()
    
    # 确定文件路径
    if args.latest:
        content_file = find_latest_content()
        if not content_file:
            print("[Error] 未找到内容文件，请先运行 daily_ai_news.py 生成")
            return
        print(f"使用最新文件: {content_file}")
    elif args.file:
        content_file = Path(args.file)
        if not content_file.exists():
            print(f"[Error] 文件不存在: {content_file}")
            return
    else:
        print("请指定文件路径或使用 --latest 参数")
        print(f"  示例: python xhs_auto_publish.py --latest")
        return
    
    # 读取内容获取标题
    full_content = read_content(content_file)
    title, _ = extract_title_and_content(full_content)
    
    # 生成封面（如果需要）
    if args.cover:
        generate_cover_with_nano_banana(title)
    
    # 发布
    try:
        publish_with_openclaw_browser(content_file)
    except Exception as e:
        print(f"[Error] 发布失败: {e}")
        print("\n备选方案:")
        print("1. 手动访问: https://creator.xiaohongshu.com/publish/publish")
        print(f"2. 复制文件内容: {content_file}")

if __name__ == '__main__':
    main()
