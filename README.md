# XHS Tech Blogger - 小红书AI技术博主工具 v2.0

自动收集AI新闻 → 生成小红书文章 → 一键发布

## 核心架构

| 功能 | 实现方式 |
|------|---------|
| 新闻收集 | OpenClaw Skills (ai-news-collectors, news-aggregator-skill-2) |
| TechMeme抓取 | OpenClaw Browser |
| 发布 | OpenClaw Browser (自动填写表单) |
| 封面图 | 默认不生成，建议手动上传或使用nano-banana-pro |

## 快速开始

### 安装

```bash
# 安装依赖Skills
npx clawhub@latest install ai-news-collectors
npx clawhub@latest install news-aggregator-skill-2

# 确认OpenClaw Browser已连接
openclaw browser status
```

### 生成AI日报

```bash
python daily_ai_news.py
```

输出文件：`output/xhs_ai_news_YYYYMMDD.txt`

### 发布到小红书

```bash
python xhs_auto_publish.py --latest
```

自动打开小红书创作平台，填写标题和正文，用户手动上传封面图后发布。

## 完整工作流

```bash
# 1. 生成日报
python daily_ai_news.py

# 2. 发布
python xhs_auto_publish.py --latest

# 3. 在小红书页面中手动完成：
#    - 点击"上传图文"
#    - 确认内容已填写
#    - 上传封面图
#    - 点击发布
```

## 文件说明

| 文件 | 功能 |
|------|------|
| `daily_ai_news.py` | 核心脚本：收集新闻并生成小红书文章 |
| `xhs_auto_publish.py` | 发布脚本：使用OpenClaw Browser自动填写 |
| `xhs_tech_blogger.py` | 单技术文章生成（可选） |
| `test_setup.py` | 环境检查 |
| `config.json` | 配置文件 |

## 配置

编辑 `config.json`：

```json
{
  "news_sources": {
    "ai_news_collectors": {"enabled": true},
    "news_aggregator": {"enabled": true},
    "techmeme": {"enabled": true}
  }
}
```

## 依赖

- Python 3.x
- OpenClaw
- OpenClaw Browser (Chrome扩展)

**无需额外Python包**（纯标准库实现）

## 封面图（可选）

默认不自动生成封面图（`enabled: false`）。

如需启用，修改 `config.json`:
```json
{
  "image_generation": {
    "enabled": true,
    "provider": "nano-banana-pro"
  }
}
```

并安装 skill:
```bash
npx clawhub@latest install nano-banana-pro
```

## License

MIT
