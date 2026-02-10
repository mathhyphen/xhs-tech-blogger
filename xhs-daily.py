#!/usr/bin/env python3
"""
XHS Tech Blogger - 命令行入口
可以直接运行: python xhs-daily.py
"""

import subprocess
import sys
from pathlib import Path

def main():
    skill_dir = Path(__file__).parent
    
    print("=" * 70)
    print("小红书AI日报生成器")
    print("=" * 70)
    print()
    
    # 生成日报
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
    
    # 检查是否需要发布
    if "--publish" in sys.argv:
        print("\n[2/2] 正在打开发布页面...")
        subprocess.run(
            [sys.executable, str(skill_dir / "xhs_auto_publish.py"), "--latest"],
            cwd=str(skill_dir)
        )
    else:
        print("\n[2/2] 日报已生成!")
        print("\n生成封面图:")
        print('  npx openclaw skills run nano-banana-pro --prompt "AI news cover"')
        print("\n发布到小红书:")
        print("  python xhs-daily.py --publish")
    
    print()
    print("=" * 70)
    return 0

if __name__ == "__main__":
    sys.exit(main())
