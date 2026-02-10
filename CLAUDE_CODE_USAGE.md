# 使用 Claude Code 调用 XHS Tech Blogger Skill

## 方式一：直接运行脚本

```python
# 在Claude Code中运行
!python D:/apps/xhs_openclaw/daily_ai_news.py
```

## 方式二：使用 OpenClaw 命令

```bash
# 调用 AI 新闻收集 skills
npx openclaw skills run ai-news-collectors
npx openclaw skills run news-aggregator-skill-2

# 调用 nano-banana-pro 生成封面图
npx openclaw skills run nano-banana-pro

# 使用 OpenClaw Browser 发布
openclaw browser navigate https://creator.xiaohongshu.com/publish/publish
```

## 方式三：Python API 调用

```python
import subprocess

# 生成日报
result = subprocess.run(
    ['python', 'D:/apps/xhs_openclaw/daily_ai_news.py'],
    capture_output=True,
    text=True
)
print(result.stdout)

# 发布到小红书
subprocess.run([
    'python', 'D:/apps/xhs_openclaw/xhs_auto_publish.py', 
    '--latest'
])
```

## 完整工作流示例

```python
# 一键生成并准备发布
import subprocess
from pathlib import Path

# 1. 生成日报
print("正在生成AI日报...")
subprocess.run(['python', 'D:/apps/xhs_openclaw/daily_ai_news.py'])

# 2. 找到生成的文件
output_dir = Path('D:/apps/xhs_openclaw/output')
latest_file = sorted(output_dir.glob('xhs_ai_news_*.txt'))[-1]
print(f"生成文件: {latest_file}")

# 3. 读取内容
with open(latest_file, 'r', encoding='utf-8') as f:
    content = f.read()
print(f"内容长度: {len(content)} 字符")

# 4. 准备发布（打开浏览器）
print("正在打开小红书创作平台...")
subprocess.run([
    'python', 'D:/apps/xhs_openclaw/xhs_auto_publish.py', 
    '--latest'
])
```

## 配置文件说明

- `config.json`: 默认配置（已包含在GitHub仓库中）
- `config.local.json`: 用户本地配置（会被 .gitignore 忽略，不提交到GitHub）

如需自定义配置，创建 `config.local.json` 覆盖默认设置。
