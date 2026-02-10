---
name: xhs-tech-blogger
description: |
  小红书AI技术博主工具 - 自动生成AI日报并发布到小红书
  触发词: "生成小红书日报", "发布到小红书", "xhs daily", "小红书AI新闻"
---

# XHS Tech Blogger - 小红书AI博主工具

自动生成AI热点日报并发布到小红书

## Usage

### 生成AI日报

```bash
npx openclaw skills run xhs-tech-blogger
```

### 生成并打开发布页面

```bash
npx openclaw skills run xhs-tech-blogger --publish
```

### 快捷触发词

在聊天中输入：
- "生成小红书日报"
- "发布到小红书"
- "xhs daily"
- "小红书AI新闻"

## Features

- 🔥 自动收集多源AI新闻（TechMeme, HN, ProductHunt等）
- 📝 生成小红书格式文章
- 🎨 支持 nano-banana-pro 生成封面图
- 📤 一键打开小红书创作平台

## Configuration

编辑 `config.json` 配置新闻源和小红书设置

## Output

生成的文件保存在 `output/` 目录：
- `xhs_ai_news_YYYYMMDD.txt` - 小红书格式文章

## Dependencies

- OpenClaw Browser（用于发布）
- nano-banana-pro（可选，用于封面图）

## License

MIT
