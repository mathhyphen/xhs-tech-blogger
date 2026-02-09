---
name: xhs-tech-blogger
version: 1.0.0
description: |
  小红书 AI 技术文档博主工具
  自动搜索技术文档、生成文章、配图并发布到小红书
---

# XHS Tech Blogger - 小红书技术博主工具

## 功能

- 🔍 **智能搜索**: 自动搜索技术官方文档
- 📝 **文章生成**: 生成 Markdown 格式的技术文章
- 🎨 **自动配图**: 使用 nano-banana-pro 生成配图
- 🏷️ **标签推荐**: 智能推荐小红书标签
- 📤 **一键发布**: 自动发布到小红书

## 使用方式

### 单技术文章

```bash
# 生成单技术文章
python xhs_tech_blogger.py "Claude 3.5"

# 生成并自动发布
python xhs_tech_blogger.py "Claude 3.5" --publish
```

### 技术对比文章

```bash
# 生成对比文章
python xhs_tech_blogger.py --compare "GPT-4o" "Claude 3.5" "Kimi K2.5"
```

### 在 OpenClaw 中使用

```
@daily 帮我写一篇关于 Qwen 3.5 的小红书文章
```

## 配置

编辑 `config.json`:

```json
{
  "xhs": {
    "api_key": "your_xiaohongshu_api_key",
    "api_secret": "your_xiaohongshu_api_secret"
  },
  "nano_banana": {
    "enabled": true,
    "api_key": "your_gemini_api_key"
  }
}
```

## 输出

生成的内容保存在 `posts/` 目录：
- `article.md` - Markdown 原文
- `xiaohongshu.txt` - 小红书格式
- `cover.png` - 配图
- `meta.json` - 元数据

## 依赖

- Python 3.9+
- requests
- nano-banana-pro (可选，用于配图)

## 作者

AI Tech Blogger
