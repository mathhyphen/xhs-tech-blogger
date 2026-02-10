#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
XHS Tech Blogger - OpenClaw Skill Entry
生成AI日报并准备发布到小红书

Usage as OpenClaw skill:
    npx openclaw skills run xhs-tech-blogger
    npx openclaw skills run xhs-tech-blogger --publish
"""

import subprocess
import sys
from pathlib import Path

def main():
    """主入口函数"""
    skill_dir = Path(__file__).parent.parent
    
    print("=" * 70)
    print("小红书AI日报生成器")
    print("=" * 70)
    print()
    
    # 1. 生成日报
    print("[1/2] 正在生成AI日报...")
    result = subprocess.run(
        [sys.executable, str(skill_dir / "daily_ai_news.py")],
        capture_output=True,
        text=True,
        cwd=str(skill_dir)
    )
    print(result.stdout[-500:] if len(result.stdout) > 500 else result.stdout)
    
    if result.returncode != 0:
        print("[Error] 生成失败")
        return 1
    
    # 2. 检查是否需要自动发布
    if "--publish" in sys.argv or "-p" in sys.argv:
        print()
        print("[2/2] 正在打开发布页面...")
        subprocess.run(
            [sys.executable, str(skill_dir / "xhs_auto_publish.py"), "--latest"],
            cwd=str(skill_dir)
        )
    else:
        print()
        print("[2/2] 日报已生成!")
        print()
        print("发布到小红书，请运行:")
        print("  npx openclaw skills run xhs-tech-blogger --publish")
        print()
        print("或手动访问:")
        print("  https://creator.xiaohongshu.com/publish/publish")
    
    print()
    print("=" * 70)
    return 0

if __name__ == "__main__":
    sys.exit(main())
