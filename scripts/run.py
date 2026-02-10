#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
XHS Tech Blogger - OpenClaw Skill Entry Point
Standard entry point for OpenClaw skill execution

Called by: npx openclaw skills run xhs-tech-blogger
"""

import subprocess
import sys
import os
from pathlib import Path

def get_skill_dir():
    """获取 skill 目录"""
    # 尝试多种方式找到 skill 目录
    
    # 方式1: 通过环境变量（OpenClaw 设置）
    skill_dir = os.environ.get('OPENCLAW_SKILL_DIR')
    if skill_dir:
        return Path(skill_dir)
    
    # 方式2: 通过当前文件位置
    # 脚本位于: <skill_dir>/scripts/run.py
    this_file = Path(__file__).resolve()
    if this_file.parent.name == 'scripts':
        return this_file.parent.parent
    
    # 方式3: 通过 openclaw workspace
    workspace = Path.home() / '.openclaw' / 'workspace' / 'skills' / 'xhs-tech-blogger'
    if workspace.exists():
        return workspace
    
    # 方式4: 默认位置
    return Path(r'D:\apps\xhs_openclaw')

def main():
    """主入口函数"""
    skill_dir = get_skill_dir()
    
    print("=" * 70)
    print("小红书AI日报生成器 (XHS Tech Blogger)")
    print("=" * 70)
    print()
    
    # 检查参数
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    
    # 1. 生成日报
    print("[1/2] 正在生成AI日报...")
    print(f"   Skill目录: {skill_dir}")
    
    daily_script = skill_dir / "daily_ai_news.py"
    
    if not daily_script.exists():
        print(f"[Error] 找不到脚本: {daily_script}")
        return 1
    
    result = subprocess.run(
        [sys.executable, str(daily_script)],
        capture_output=True,
        text=True,
        cwd=str(skill_dir)
    )
    
    if result.stdout:
        # 只显示最后一部分
        lines = result.stdout.strip().split('\n')
        if len(lines) > 10:
            print('\n'.join(lines[-10:]))
        else:
            print(result.stdout)
    
    if result.returncode != 0:
        print("[Error] 生成失败")
        if result.stderr:
            print(result.stderr)
        return 1
    
    # 2. 检查是否需要发布
    if "--publish" in args:
        print()
        print("[2/2] 正在打开发布页面...")
        publish_script = skill_dir / "xhs_auto_publish.py"
        if publish_script.exists():
            subprocess.run(
                [sys.executable, str(publish_script), "--latest"],
                cwd=str(skill_dir)
            )
        else:
            print("[Warning] 找不到发布脚本")
    else:
        print()
        print("[2/2] 日报已生成!")
        print()
        print("📄 文件位置:")
        output_dir = skill_dir / "output"
        if output_dir.exists():
            files = list(output_dir.glob("xhs_ai_news_*.txt"))
            if files:
                latest = max(files, key=lambda p: p.stat().st_mtime)
                print(f"   {latest}")
        print()
        print("📤 发布到小红书:")
        print("   npx openclaw skills run xhs-tech-blogger --publish")
        print()
        print("🎨 生成封面图:")
        print("   npx openclaw skills run nano-banana-pro --prompt 'AI news cover'")
    
    print()
    print("=" * 70)
    print("✅ 完成!")
    print("=" * 70)
    return 0

if __name__ == "__main__":
    sys.exit(main())
