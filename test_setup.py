#!/usr/bin/env python3
"""
XHS Tech Blogger v2.0 测试脚本
验证配置和依赖是否正确
"""

import subprocess
import sys
from pathlib import Path

def check_skill(skill_name):
    """检查skill是否安装"""
    skill_path = Path.home() / '.openclaw' / 'workspace' / 'skills' / skill_name
    return skill_path.exists()

def main():
    print("=" * 70)
    print("XHS Tech Blogger v2.0 环境检查")
    print("=" * 70)
    print()
    
    # 检查Skills
    print("[1/4] 检查OpenClaw Skills...")
    skills = {
        'ai-news-collectors': 'AI新闻收集器',
        'news-aggregator-skill-2': '多源新闻聚合器',
        'nano-banana-pro': 'AI图片生成'
    }
    
    all_ok = True
    for skill, desc in skills.items():
        if check_skill(skill):
            print(f"  [OK] {desc} ({skill})")
        else:
            print(f"  [Missing] {desc} ({skill})")
            print(f"      安装: npx clawhub@latest install {skill}")
            all_ok = False
    
    print()
    
    # 检查OpenClaw Browser
    print("[2/4] 检查OpenClaw Browser...")
    try:
        result = subprocess.run(
            ['openclaw', 'browser', 'status'],
            capture_output=True,
            text=True,
            timeout=10
        )
        if 'connected' in result.stdout.lower() or result.returncode == 0:
            print("  [OK] OpenClaw Browser 已连接")
        else:
            print("  [Warning] OpenClaw Browser 可能未连接")
            print("      请确保Chrome扩展已安装并配对")
    except:
        print("  [Error] 无法检查OpenClaw Browser状态")
    
    print()
    
    # 检查配置文件
    print("[3/4] 检查配置文件...")
    config_path = Path(__file__).parent / 'config.json'
    if config_path.exists():
        print(f"  [OK] 配置文件存在: {config_path}")
    else:
        print(f"  [Missing] 配置文件不存在")
        all_ok = False
    
    print()
    
    # 检查输出目录
    print("[4/4] 检查输出目录...")
    output_dir = Path(__file__).parent / 'output'
    output_dir.mkdir(exist_ok=True)
    print(f"  [OK] 输出目录: {output_dir}")
    
    print()
    print("=" * 70)
    if all_ok:
        print("[OK] 环境检查通过，可以开始使用！")
        print()
        print("快速开始:")
        print("  1. python daily_ai_news.py")
        print("  2. npx openclaw skills run nano-banana-pro --prompt 'AI news cover'")
        print("  3. python xhs_auto_publish.py --latest")
    else:
        print("[Warning] 部分依赖缺失，请按提示安装")
    print("=" * 70)

if __name__ == '__main__':
    main()
