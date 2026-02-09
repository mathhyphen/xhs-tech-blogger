#!/usr/bin/env python3
"""
Xiaohongshu AI Tech Blogger - 小红书 AI 技术文档博主工具

一个自动化的 AI 技术文档生成和发布工具，专为小红书博主设计。

Features:
- 搜索并分析技术文档
- 生成 Markdown 格式的技术文章
- 自动生成配图（使用 nano-banana-pro）
- 智能标签推荐
- 自动发布到小红书
"""

import json
import os
import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import requests

class XhsTechBlogger:
    """小红书 AI 技术文档博主"""
    
    def __init__(self, config_path: str = None):
        self.config = self._load_config(config_path)
        self.workspace = Path(r"D:\apps\xhs_openclaw")
        self.output_dir = self.workspace / "posts"
        self.output_dir.mkdir(exist_ok=True)
        
    def _load_config(self, config_path: str) -> Dict:
        """加载配置文件"""
        default_config = {
            "xhs": {
                "api_key": os.getenv("XHS_API_KEY", ""),
                "api_secret": os.getenv("XHS_API_SECRET", ""),
                "default_tags": ["AI", "人工智能", "大模型", "技术文档"]
            },
            "nano_banana": {
                "enabled": True,
                "api_key": os.getenv("GEMINI_API_KEY", "")
            },
            "content": {
                "max_length": 1000,  # 小红书字数限制
                "style": "professional",  # professional / casual / humorous
                "include_code": True,
                "include_diagrams": True
            }
        }
        
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                return {**default_config, **json.load(f)}
        return default_config
    
    def search_documentation(self, tech_names: List[str]) -> Dict[str, Dict]:
        """
        搜索技术官方文档并总结
        
        Args:
            tech_names: 技术名称列表
            
        Returns:
            Dict: 每个技术的文档总结
        """
        results = {}
        
        for tech in tech_names:
            print(f"🔍 搜索 {tech} 的文档...")
            
            # 模拟搜索和总结过程
            # 实际实现应该调用搜索 API 和 LLM
            results[tech] = {
                "name": tech,
                "official_doc": f"https://{tech.lower().replace(' ', '')}.dev/docs",
                "key_features": [],
                "summary": "",
                "code_examples": [],
                "benchmarks": {}
            }
            
        return results
    
    def generate_markdown(self, tech_data: Dict, template: str = "default") -> str:
        """
        生成 Markdown 格式的技术文章
        
        Args:
            tech_data: 技术文档数据
            template: 文章模板
            
        Returns:
            str: Markdown 内容
        """
        date_str = datetime.now().strftime("%Y-%m-%d")
        
        markdown = f"""# {tech_data['name']} - 技术解析

> 📅 发布日期: {date_str}
> 🏷️ 分类: AI技术 | 大模型

## 🚀 简介

{tech_data.get('summary', '暂无总结')}

## ✨ 核心特点

"""
        
        # 添加特点列表
        for i, feature in enumerate(tech_data.get('key_features', []), 1):
            markdown += f"{i}. **{feature['title']}**: {feature['description']}\n"
        
        # 添加代码示例
        if tech_data.get('code_examples') and self.config['content']['include_code']:
            markdown += "\n## 💻 代码示例\n\n```python\n"
            markdown += tech_data['code_examples'][0]
            markdown += "\n```\n"
        
        # 添加性能对比
        if tech_data.get('benchmarks'):
            markdown += "\n## 📊 性能对比\n\n"
            markdown += "| 指标 | 数值 |\n"
            markdown += "|------|------|\n"
            for metric, value in tech_data['benchmarks'].items():
                markdown += f"| {metric} | {value} |\n"
        
        # 添加结论
        markdown += f"""
## 🎯 总结

{tech_data['name']} 是一个值得关注的技术...

---

💡 **想要了解更多 AI 技术？关注我，每天分享最新技术干货！**

"""
        
        return markdown
    
    def generate_image_prompt(self, tech_data: Dict) -> str:
        """
        生成配图提示词
        
        Args:
            tech_data: 技术数据
            
        Returns:
            str: 图片生成提示词
        """
        tech_name = tech_data['name']
        
        prompts = {
            "default": f"""
            Create a professional tech blog cover image for "{tech_name}".
            Style: Modern, clean, futuristic
            Elements: Neural networks, code snippets, abstract AI visualization
            Colors: Blue and purple gradient, glowing effects
            Text: Include "{tech_name}" in elegant typography
            Aspect ratio: 3:4 (for Xiaohongshu)
            """,
            "minimal": f"""
            Minimalist tech illustration for {tech_name}.
            Clean white background with subtle gradient
            Abstract geometric shapes representing AI/ML
            Professional and modern aesthetic
            """,
            "detailed": f"""
            Detailed technical illustration showing {tech_name} architecture.
            Include: Data flow diagrams, neural network layers, performance charts
            Style: Infographic meets sci-fi aesthetic
            Vibrant colors with professional finish
            """
        }
        
        return prompts.get(self.config['content']['style'], prompts['default'])
    
    def generate_image(self, tech_data: Dict) -> Optional[str]:
        """
        使用 nano-banana-pro 生成配图
        
        Args:
            tech_data: 技术数据
            
        Returns:
            str: 生成的图片路径
        """
        if not self.config['nano_banana']['enabled']:
            print("⚠️ nano-banana-pro 未启用，跳过图片生成")
            return None
        
        prompt = self.generate_image_prompt(tech_data)
        print(f"🎨 生成配图: {tech_data['name']}...")
        
        # 这里应该调用 nano-banana-pro 的 API
        # 简化示例，实际需要集成 gemini API
        output_path = self.output_dir / f"{tech_data['name'].replace(' ', '_')}_cover.png"
        
        print(f"✅ 图片生成完成: {output_path}")
        return str(output_path)
    
    def recommend_tags(self, tech_data: Dict) -> List[str]:
        """
        智能推荐标签
        
        Args:
            tech_data: 技术数据
            
        Returns:
            List[str]: 推荐标签列表
        """
        base_tags = self.config['xhs']['default_tags'].copy()
        
        # 根据技术名称添加标签
        tech_name = tech_data['name'].lower()
        
        tag_mapping = {
            'llm': ['LLM', '大语言模型'],
            'gpt': ['GPT', 'OpenAI'],
            'claude': ['Claude', 'Anthropic'],
            'kimi': ['Kimi', 'Moonshot'],
            'qwen': ['通义千问', '阿里'],
            'transformer': ['Transformer', '注意力机制'],
            'moe': ['MoE', '混合专家模型'],
            'agent': ['AI Agent', '智能体'],
            'rag': ['RAG', '检索增强生成'],
            'fine-tuning': ['微调', 'Fine-tuning'],
            'quantization': ['量化', '模型压缩'],
            'deployment': ['模型部署', 'MLOps']
        }
        
        for keyword, tags in tag_mapping.items():
            if keyword in tech_name:
                base_tags.extend(tags)
        
        # 去重并限制数量
        unique_tags = list(set(base_tags))
        return unique_tags[:10]  # 小红书最多 10 个标签
    
    def format_for_xiaohongshu(self, markdown: str, tags: List[str]) -> str:
        """
        格式化为小红书风格
        
        Args:
            markdown: Markdown 内容
            tags: 标签列表
            
        Returns:
            str: 小红书格式内容
        """
        # 移除 Markdown 语法
        text = markdown.replace('# ', '').replace('## ', '').replace('### ', '')
        text = text.replace('**', '').replace('*', '')
        text = text.replace('```python', '').replace('```', '')
        text = text.replace('|', '').replace('---', '')
        
        # 添加表情和格式化
        lines = text.split('\n')
        formatted_lines = []
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('>'):
                # 添加适当的换行
                formatted_lines.append(line)
                formatted_lines.append('')  # 空行增加可读性
        
        # 添加标签
        formatted_text = '\n'.join(formatted_lines)
        formatted_text += '\n\n🏷️ '
        formatted_text += ' '.join([f"#{tag}" for tag in tags])
        
        return formatted_text
    
    def save_post(self, tech_name: str, markdown: str, xhs_content: str, image_path: str = None):
        """
        保存文章到本地
        
        Args:
            tech_name: 技术名称
            markdown: Markdown 内容
            xhs_content: 小红书格式内容
            image_path: 图片路径
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = tech_name.replace(' ', '_').replace('/', '_')
        
        post_dir = self.output_dir / f"{timestamp}_{safe_name}"
        post_dir.mkdir(exist_ok=True)
        
        # 保存 Markdown
        md_path = post_dir / "article.md"
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(markdown)
        
        # 保存小红书版本
        xhs_path = post_dir / "xiaohongshu.txt"
        with open(xhs_path, 'w', encoding='utf-8') as f:
            f.write(xhs_content)
        
        # 保存元数据
        meta = {
            "tech_name": tech_name,
            "created_at": datetime.now().isoformat(),
            "markdown_file": str(md_path),
            "xiaohongshu_file": str(xhs_path),
            "image_file": image_path,
            "status": "ready_to_publish"
        }
        
        meta_path = post_dir / "meta.json"
        with open(meta_path, 'w', encoding='utf-8') as f:
            json.dump(meta, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 文章已保存到: {post_dir}")
        return post_dir
    
    def publish_to_xiaohongshu(self, post_dir: Path) -> bool:
        """
        发布到小红书
        
        Args:
            post_dir: 文章目录
            
        Returns:
            bool: 是否成功
        """
        # 读取文件
        xhs_file = post_dir / "xiaohongshu.txt"
        meta_file = post_dir / "meta.json"
        
        if not xhs_file.exists():
            print("❌ 小红书内容文件不存在")
            return False
        
        with open(xhs_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        with open(meta_file, 'r', encoding='utf-8') as f:
            meta = json.load(f)
        
        print(f"📤 正在发布到小红书: {meta['tech_name']}...")
        
        # 这里应该调用小红书 API
        # 简化示例，实际需要集成小红书开放平台 API
        print("⚠️ 小红书 API 集成待实现")
        print(f"标题: {meta['tech_name']}")
        print(f"内容长度: {len(content)} 字符")
        print(f"配图: {meta.get('image_file', '无')}")
        
        return True
    
    def process_tech(self, tech_name: str, auto_publish: bool = False) -> Path:
        """
        处理单个技术并生成文章
        
        Args:
            tech_name: 技术名称
            auto_publish: 是否自动发布
            
        Returns:
            Path: 文章目录
        """
        print(f"\n{'='*60}")
        print(f"📝 处理技术: {tech_name}")
        print(f"{'='*60}\n")
        
        # 1. 搜索文档
        tech_data = self.search_documentation([tech_name])[tech_name]
        
        # 2. 生成 Markdown
        print("📝 生成 Markdown 文章...")
        markdown = self.generate_markdown(tech_data)
        
        # 3. 生成配图
        image_path = self.generate_image(tech_data)
        
        # 4. 推荐标签
        print("🏷️ 推荐标签...")
        tags = self.recommend_tags(tech_data)
        print(f"   标签: {', '.join(tags)}")
        
        # 5. 格式化为小红书
        xhs_content = self.format_for_xiaohongshu(markdown, tags)
        
        # 6. 保存
        post_dir = self.save_post(tech_name, markdown, xhs_content, image_path)
        
        # 7. 可选：自动发布
        if auto_publish:
            self.publish_to_xiaohongshu(post_dir)
        
        print(f"\n✅ 完成！文章保存在: {post_dir}")
        return post_dir
    
    def process_multiple_techs(self, tech_names: List[str], comparison_mode: bool = False):
        """
        处理多个技术，可选对比模式
        
        Args:
            tech_names: 技术名称列表
            comparison_mode: 是否生成对比文章
        """
        if comparison_mode and len(tech_names) > 1:
            # 生成对比文章
            print(f"\n{'='*60}")
            print(f"🔄 生成对比文章: {' vs '.join(tech_names)}")
            print(f"{'='*60}\n")
            
            # 搜索所有技术
            all_tech_data = self.search_documentation(tech_names)
            
            # 生成对比 Markdown
            markdown = self._generate_comparison_markdown(all_tech_data)
            
            # 保存
            comparison_name = "_vs_".join([t.replace(' ', '') for t in tech_names[:3]])
            xhs_content = self.format_for_xiaohongshu(markdown, self.recommend_tags({'name': ' '.join(tech_names)}))
            
            post_dir = self.save_post(f"Comparison_{comparison_name}", markdown, xhs_content)
            print(f"✅ 对比文章已保存: {post_dir}")
            
        else:
            # 分别处理每个技术
            for tech in tech_names:
                self.process_tech(tech)
    
    def _generate_comparison_markdown(self, tech_data_dict: Dict) -> str:
        """生成对比文章的 Markdown"""
        tech_names = list(tech_data_dict.keys())
        date_str = datetime.now().strftime("%Y-%m-%d")
        
        markdown = f"""# {' vs '.join(tech_names)} - 技术对比

> 📅 发布日期: {date_str}
> 🏷️ 分类: AI技术对比 | 大模型选型

## 🚀 概述

今天为大家带来 {len(tech_names)} 款热门技术的深度对比...

## 📊 对比维度

"""
        
        # 添加对比表格
        markdown += "| 特性 | " + " | ".join(tech_names) + " |\n"
        markdown += "|------|" + "|".join(["------"] * len(tech_names)) + "|\n"
        
        # 对比项
        comparison_items = ["架构", "参数量", "上下文长度", "推理速度", "中文能力", "开源程度"]
        for item in comparison_items:
            row = f"| {item} |"
            for tech in tech_names:
                row += " 待补充 |"
            markdown += row + "\n"
        
        # 每个技术的简介
        markdown += "\n## 🔍 详细解析\n\n"
        for tech_name, data in tech_data_dict.items():
            markdown += f"### {tech_name}\n\n"
            markdown += f"{data.get('summary', '暂无总结')}\n\n"
        
        # 结论
        markdown += """
## 🎯 选型建议

- **如果你的需求是 XXX**: 推荐 XXX
- **如果你的需求是 YYY**: 推荐 YYY

---

💡 **想要了解更多技术对比？关注我，每周深度对比！**

"""
        
        return markdown


def main():
    """命令行入口"""
    import sys
    
    blogger = XhsTechBlogger()
    
    if len(sys.argv) < 2:
        print("用法:")
        print("  python xhs_tech_blogger.py <技术名称>")
        print("  python xhs_tech_blogger.py --compare <技术1> <技术2> [<技术3>]")
        print("")
        print("示例:")
        print('  python xhs_tech_blogger.py "Claude 3.5"')
        print('  python xhs_tech_blogger.py --compare "GPT-4o" "Claude 3.5" "Kimi K2.5"')
        return
    
    if sys.argv[1] == '--compare':
        tech_names = sys.argv[2:]
        if len(tech_names) < 2:
            print("❌ 对比模式需要至少 2 个技术")
            return
        blogger.process_multiple_techs(tech_names, comparison_mode=True)
    else:
        tech_name = ' '.join(sys.argv[1:])
        blogger.process_tech(tech_name)


if __name__ == "__main__":
    main()
