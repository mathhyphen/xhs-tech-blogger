---
name: xhs-tech-blogger
description: |
  小红书AI技术博主工具 - 自动生成AI日报并发布到小红书
  
  功能：
  - 自动从多源收集AI新闻（TechMeme, HN, ProductHunt等）
  - 智能去重、筛选、排序
  - 生成小红书格式文章
  - 支持 nano-banana-pro 生成封面图
  - 一键打开小红书创作平台
  
  使用方式：
    npx openclaw skills run xhs-tech-blogger
    npx openclaw skills run xhs-tech-blogger --publish
  
  触发词：@xhs, @小红书, 生成小红书日报, xhs daily
---

# XHS Tech Blogger

自动生成AI热点日报并发布到小红书

## Installation

```bash
npx clawhub@latest install xhs-tech-blogger
```

## Usage

### 生成AI日报

```bash
npx openclaw skills run xhs-tech-blogger
```

### 生成并打开发布页面

```bash
npx openclaw skills run xhs-tech-blogger --publish
```

### 触发词（在聊天中使用）

- `@xhs 生成日报`
- `@小红书 今天AI新闻`
- `xhs daily`
- `生成小红书日报`

## Configuration

首次使用前，在 `~/.openclaw/openclaw.json` 中添加配置：

```json
{
  "skills": {
    "entries": {
      "xhs-tech-blogger": {
        "enabled": true
      }
    }
  }
}
```

## Features

- 🔥 **多源新闻**：TechMeme, Hacker News, ProductHunt, 36Kr
- 🔄 **智能去重**：自动去重、筛选、热度排序
- 📝 **小红书格式**：自动生成适合小红书的文案格式
- 🎨 **封面生成**：支持 nano-banana-pro 生成封面图
- 📤 **一键发布**：自动打开小红书创作平台

## Output

生成的文件保存在 skill 目录下的 `output/`：
- `xhs_ai_news_YYYYMMDD.txt` - 小红书格式文章

## Dependencies

- OpenClaw Browser（用于发布到小红书）
- nano-banana-pro（可选，用于生成封面图）

## License

MIT

## Author

mathhyphen
