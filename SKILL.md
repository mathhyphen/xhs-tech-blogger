---
name: xhs-tech-blogger
version: 2.0.0
description: |
  小红书AI技术博主工具 - 多源新闻自动版
  自动从多新闻源收集AI热点、生成文章，使用OpenClaw Browser发布到小红书
---

# XHS Tech Blogger v2.0

自动收集AI新闻 → 生成小红书文章 → 一键发布

## 核心功能

- 🔥 **多源新闻收集**: ai-news-collectors + news-aggregator-skill-2 + TechMeme
- 🔄 **智能去重**: 自动去重、筛选、排序
- 📝 **文章生成**: 生成小红书格式的AI热点文章
- 📤 **一键发布**: 使用OpenClaw Browser自动发布

## 系统要求

- OpenClaw 已安装
- OpenClaw Browser 已连接（Chrome扩展）
- ai-news-collectors skill 已安装
- news-aggregator-skill-2 已安装

## 快速开始

### 1. 安装依赖Skills

```bash
npx clawhub@latest install ai-news-collectors
npx clawhub@latest install news-aggregator-skill-2

# 确认OpenClaw Browser已连接
openclaw browser status
```

### 2. 生成AI日报

```bash
python daily_ai_news.py
```

输出: `output/xhs_ai_news_YYYYMMDD.txt`

### 3. 发布到小红书

```bash
python xhs_auto_publish.py --latest
```

自动打开小红书创作平台并填写内容，用户手动上传封面图后发布。

## 完整工作流

```bash
# 1. 生成日报
python daily_ai_news.py

# 2. 发布（自动打开浏览器并填写内容）
python xhs_auto_publish.py --latest

# 3. 在小红书页面中：
#    - 点击"上传图文"
#    - 确认标题和正文已填写
#    - 手动上传封面图
#    - 点击发布
```

## 文件结构

```
xhs_openclaw/
├── config.json              # 配置文件
├── daily_ai_news.py         # AI日报生成器（核心）
├── xhs_auto_publish.py      # 一键发布脚本
├── xhs_tech_blogger.py      # 单技术文章生成（可选）
├── test_setup.py            # 环境检查
├── requirements.txt         # Python依赖（无特殊依赖）
├── README.md                # 使用说明
├── SKILL.md                 # 本文件
└── output/                  # 输出目录
    └── xhs_ai_news_*.txt    # 生成的日报
```

## 配置说明

编辑 `config.json`:

```json
{
  "news_sources": {
    "ai_news_collectors": {"enabled": true},
    "news_aggregator": {"enabled": true},
    "techmeme": {"enabled": true}
  },
  "xiaohongshu": {
    "default_tags": ["AI", "人工智能", "科技热点"]
  }
}
```

## 关于封面图

**默认不生成封面图**，原因：
- 小红书对图片风格有特定要求
- 用户通常有自己的封面模板

**如需封面图，建议**：
- 手动上传自己的封面模板
- 使用 nano-banana-pro skill 生成
- 使用其他AI图片工具

## 注意事项

1. **纯Python标准库**：无需安装playwright/Pillow
2. **浏览器操作**：全部使用OpenClaw Browser
3. **小红书发布**：自动填写内容，但需手动上传图片和点击发布（避免风控）

## License

MIT
