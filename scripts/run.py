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
    """获取 skill 目录 - 优先从配置读取，支持自定义路径"""
    
    # 方式1: 尝试读取配置文件中的路径
    try:
        # 查找配置文件
        possible_configs = [
            Path.home() / '.openclaw' / 'workspace' / 'skills' / 'xhs-tech-blogger' / 'config.json',
            Path(__file__).parent.parent / 'config.json',
            Path(r'D:\apps\xhs_openclaw') / 'config.json',
        ]
        
        for config_path in possible_configs:
            if config_path.exists():
                import json
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                paths = config.get('paths', {})
                skill_root = paths.get('skill_root', '.')
                
                # 如果是绝对路径，直接使用
                if skill_root and Path(skill_root).is_absolute():
                    if Path(skill_root).exists():
                        return Path(skill_root)
                
                # 否则使用配置文件所在目录
                if config_path.parent.exists():
                    return config_path.parent
    except Exception:
        pass
    
    # 方式2: 通过当前文件位置
    this_file = Path(__file__).resolve()
    if this_file.parent.name == 'scripts':
        return this_file.parent.parent
    
    # 方式3: 通过 openclaw workspace
    workspace = Path.home() / '.openclaw' / 'workspace' / 'skills' / 'xhs-tech-blogger'
    if workspace.exists():
        return workspace
    
    # 方式4: 默认位置（可配置）
    default = Path(r'D:\apps\xhs_openclaw')
    if default.exists():
        return default
    
    # 最后回退到当前目录
    return Path.cwd()

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
