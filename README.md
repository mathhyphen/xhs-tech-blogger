# XHS Tech Blogger - 小红书 AI 技术博主工具

**English** | [中文](#中文文档)

## Overview

An automated AI technology documentation tool for Xiaohongshu (Little Red Book) bloggers. 

This tool helps tech bloggers automatically:
- 🔍 Search and analyze official tech documentation
- 📝 Generate Markdown-formatted tech articles
- 🎨 Create cover images (using nano-banana-pro)
- 🏷️ Recommend trending hashtags
- 📤 Publish to Xiaohongshu

## Features

### 1. Intelligent Document Search
- Automatically searches official documentation
- Extracts key features and technical specifications
- Summarizes complex technical concepts

### 2. Article Generation
- Generates professional Markdown articles
- Multiple templates (single tech, comparison, tutorial)
- Optimized for Xiaohongshu's format

### 3. Auto Image Generation
- Uses nano-banana-pro (Gemini) to generate cover images
- Multiple style options (professional, minimal, detailed)
- Perfect 3:4 ratio for Xiaohongshu

### 4. Smart Hashtag Recommendation
- AI-powered hashtag suggestions
- Trending topic analysis
- Maximum 10 hashtags (Xiaohongshu limit)

### 5. One-Click Publishing
- Direct publishing to Xiaohongshu API
- Scheduled posting support
- Draft management

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/xhs-tech-blogger.git
cd xhs-tech-blogger

# Install dependencies
pip install -r requirements.txt

# Configure API keys
cp config.example.json config.json
# Edit config.json with your API keys
```

## Usage

### Single Tech Article

```bash
python xhs_tech_blogger.py "Claude 3.5"
```

### Tech Comparison

```bash
python xhs_tech_blogger.py --compare "GPT-4o" "Claude 3.5" "Kimi K2.5"
```

### Batch Processing

```bash
python batch_process.py tech_list.txt
```

## Configuration

Edit `config.json`:

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

## Output Structure

```
posts/
└── 20260209_143052_Claude_3.5/
    ├── article.md           # Markdown article
    ├── xiaohongshu.txt      # Xiaohongshu format
    ├── cover.png           # Cover image
    └── meta.json           # Metadata
```

## API Integration

### Xiaohongshu Open Platform
This tool uses the Xiaohongshu Open Platform API for publishing.
Apply for API access at: https://open.xiaohongshu.com

### nano-banana-pro
Image generation uses Gemini API through the nano-banana-pro skill.

## Workflow

```
Tech Topic → Document Search → Analysis → Article Generation 
    → Image Generation → Hashtag Optimization → Publishing
```

## License

MIT License

---

## 中文文档

### 简介

小红书 AI 技术文档博主工具 - 专为技术博主打造的自动化内容生成工具。

### 核心功能

1. **智能文档搜索**
   - 自动搜索官方技术文档
   - 提取关键特性和技术规格
   - 总结复杂技术概念

2. **文章自动生成**
   - 生成专业 Markdown 格式文章
   - 多种模板（单技术、对比、教程）
   - 针对小红书格式优化

3. **自动配图**
   - 使用 nano-banana-pro (Gemini) 生成封面图
   - 多种风格选择（专业、极简、详细）
   - 完美适配小红书 3:4 比例

4. **智能标签推荐**
   - AI 驱动的标签建议
   - 热门话题分析
   - 最多 10 个标签（小红书限制）

5. **一键发布**
   - 直接发布到小红书 API
   - 支持定时发布
   - 草稿管理

### 快速开始

```bash
# 克隆仓库
git clone https://github.com/yourusername/xhs-tech-blogger.git
cd xhs-tech-blogger

# 安装依赖
pip install -r requirements.txt

# 配置 API 密钥
cp config.example.json config.json
# 编辑 config.json 填入你的 API 密钥
```

### 使用方法

#### 单技术文章

```bash
python xhs_tech_blogger.py "Claude 3.5"
```

#### 技术对比

```bash
python xhs_tech_blogger.py --compare "GPT-4o" "Claude 3.5" "Kimi K2.5"
```

#### 批量处理

```bash
python batch_process.py tech_list.txt
```

### 输出结构

```
posts/
└── 20260209_143052_Claude_3.5/
    ├── article.md           # Markdown 文章
    ├── xiaohongshu.txt      # 小红书格式
    ├── cover.png           # 封面图片
    └── meta.json           # 元数据
```

### 工作流程

```
技术主题 → 文档搜索 → 分析 → 文章生成 
    → 图片生成 → 标签优化 → 发布
```

## Author

Created for AI Tech Bloggers
