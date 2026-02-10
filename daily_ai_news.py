#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
XHS AI日报生成器 v2.0 - OpenClaw Browser版
一键获取今日AI动态并生成小红书文章

Usage:
    python daily_ai_news.py              # 生成日报
    python daily_ai_news.py --publish    # 生成并准备发布
    python daily_ai_news.py --dry-run    # 测试模式，不保存
"""

import subprocess
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Dict

class XHSAIDailyPublisher:
    """小红书AI日报发布器"""
    
    def __init__(self, config_path: str = None):
        self.config = self._load_config(config_path)
        self.news_data = []
        
        # 处理输出目录（支持绝对路径）
        output_config = self.config.get('output', {})
        save_dir = output_config.get('save_directory', 'output')
        
        # 如果是绝对路径，直接使用；否则相对于脚本目录
        if Path(save_dir).is_absolute():
            self.output_dir = Path(save_dir)
        else:
            self.output_dir = Path(__file__).parent / save_dir
        
        self.output_dir.mkdir(exist_ok=True)
    
    def _load_config(self, config_path: str = None) -> dict:
        """加载配置文件"""
        if not config_path:
            config_path = Path(__file__).parent / 'config.json'
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"[Warning] 无法加载配置文件: {e}")
            return self._default_config()
    
    def _default_config(self) -> dict:
        """默认配置"""
        return {
            'news_sources': {
                'ai_news_collectors': {'enabled': True},
                'news_aggregator': {'enabled': True},
                'techmeme': {'enabled': True}
            },
            'xiaohongshu': {'enabled': True},
            'output': {'save_directory': 'output'}
        }
    
    def _run_openclaw_skill(self, skill_name: str, timeout: int = 120) -> str:
        """运行OpenClaw skill"""
        try:
            result = subprocess.run(
                ['npx', 'openclaw', 'skills', 'run', skill_name],
                capture_output=True,
                text=True,
                shell=True,
                timeout=timeout
            )
            return result.stdout + result.stderr
        except subprocess.TimeoutExpired:
            return f"[Timeout] Skill {skill_name} 运行超时"
        except Exception as e:
            return f"[Error] {e}"
    
    def collect_from_ai_news_collectors(self) -> List[Dict]:
        """从ai-news-collectors收集新闻"""
        print("[1/3] 正在运行 ai-news-collectors...")
        
        if not self.config.get('news_sources', {}).get('ai_news_collectors', {}).get('enabled'):
            print("      [Skip] 未启用")
            return []
        
        output = self._run_openclaw_skill('ai-news-collectors', timeout=180)
        
        # 解析输出
        news_list = self._parse_ai_news_output(output)
        print(f"      [OK] 收集到 {len(news_list)} 条")
        return news_list
    
    def collect_from_news_aggregator(self) -> List[Dict]:
        """从news-aggregator-skill-2收集新闻"""
        print("[2/3] 正在运行 news-aggregator-skill-2...")
        
        if not self.config.get('news_sources', {}).get('news_aggregator', {}).get('enabled'):
            print("      [Skip] 未启用")
            return []
        
        # 构建关键词
        keywords = self.config.get('news_sources', {}).get('news_aggregator', {}).get(
            'keywords', ['AI', 'LLM', 'GPT', 'OpenAI']
        )
        keyword_str = ','.join(keywords)
        
        try:
            # 运行fetch_news脚本
            skill_path = Path.home() / '.openclaw' / 'workspace' / 'skills' / 'news-aggregator-skill-2'
            result = subprocess.run(
                ['python', 'scripts/fetch_news.py', 
                 '--source', 'all',
                 '--limit', '10',
                 '--keyword', keyword_str],
                capture_output=True,
                text=True,
                shell=True,
                timeout=120,
                cwd=str(skill_path)
            )
            
            # 解析JSON输出
            try:
                data = json.loads(result.stdout)
                news_list = self._parse_news_aggregator_output(data)
                print(f"      [OK] 收集到 {len(news_list)} 条")
                return news_list
            except:
                print(f"      [Warning] 解析失败")
                return []
                
        except Exception as e:
            print(f"      [Error] {e}")
            return []
    
    def collect_from_techmeme(self) -> List[Dict]:
        """使用OpenClaw Browser从TechMeme收集AI新闻"""
        print("[3/3] 正在从 TechMeme 收集...")
        
        if not self.config.get('news_sources', {}).get('techmeme', {}).get('enabled'):
            print("      [Skip] 未启用")
            return []
        
        try:
            # 使用openclaw browser访问TechMeme
            subprocess.run(
                ['openclaw', 'browser', 'navigate', 'https://www.techmeme.com'],
                timeout=30
            )
            
            # 执行JavaScript提取新闻
            js_code = """
            (function() {
                const articles = document.querySelectorAll('div.hentry');
                const results = [];
                const aiKeywords = ['AI', 'artificial intelligence', 'ChatGPT', 'OpenAI', 
                                   'LLM', 'machine learning', 'Claude', 'model'];
                
                for (let article of articles.slice(0, 15)) {
                    const titleEl = article.querySelector('div.hed');
                    const sourceEl = article.querySelector('div.by');
                    
                    if (titleEl) {
                        const title = titleEl.innerText.trim();
                        const isAI = aiKeywords.some(kw => title.toLowerCase().includes(kw.toLowerCase()));
                        
                        if (isAI) {
                            results.push({
                                title: title,
                                source: sourceEl ? 'TechMeme - ' + sourceEl.innerText.trim() : 'TechMeme'
                            });
                        }
                    }
                }
                
                return JSON.stringify(results);
            })()
            """
            
            result = subprocess.run(
                ['openclaw', 'browser', 'evaluate', '--fn', js_code],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # 解析结果
            try:
                data = json.loads(result.stdout)
                news_list = []
                for item in data:
                    news_list.append({
                        'title': item['title'],
                        'source': item['source'],
                        'url': 'https://www.techmeme.com',
                        'date': datetime.now().strftime('%Y-%m-%d'),
                        'source_type': 'techmeme'
                    })
                print(f"      [OK] 收集到 {len(news_list)} 条")
                return news_list
            except:
                print(f"      [Warning] 解析失败")
                return []
                
        except Exception as e:
            print(f"      [Error] {e}")
            return []
    
    def _parse_ai_news_output(self, output: str) -> List[Dict]:
        """解析ai-news-collectors输出"""
        news_list = []
        lines = output.split('\n')
        current_news = {}
        
        for line in lines:
            if line.strip().startswith('**') and line.strip().endswith('**'):
                if current_news:
                    news_list.append(current_news)
                current_news = {
                    'title': line.strip().strip('*'),
                    'source': 'AI News Collectors',
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'source_type': 'ai_news_collectors'
                }
            elif 'http' in line and current_news:
                current_news['url'] = line.strip()
        
        if current_news:
            news_list.append(current_news)
        
        return news_list
    
    def _parse_news_aggregator_output(self, data: dict) -> List[Dict]:
        """解析news-aggregator输出"""
        news_list = []
        
        if isinstance(data, list):
            for item in data:
                news_list.append({
                    'title': item.get('title', ''),
                    'source': item.get('source', 'News Aggregator'),
                    'url': item.get('url', ''),
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'source_type': 'news_aggregator'
                })
        
        return news_list
    
    def deduplicate_and_rank(self, news_list: List[Dict]) -> List[Dict]:
        """去重并排序"""
        print("[汇总] 正在去重和排序...")
        
        # 去重
        seen = set()
        unique_news = []
        
        for news in news_list:
            key = news.get('title', '')[:20].lower()
            if key and key not in seen:
                seen.add(key)
                unique_news.append(news)
        
        # 限制数量
        final_news = unique_news[:10]
        
        # 添加emoji
        emojis = ['🎯', '📈', '🏦', '💰', '🎬', '⚖️', '⚡', '📹', '🔒', '🏗️']
        for i, news in enumerate(final_news):
            news['emoji'] = emojis[i % len(emojis)]
        
        print(f"       去重后: {len(final_news)} 条")
        return final_news
    
    def generate_xhs_content(self, news_list: List[Dict]) -> str:
        """生成小红书格式内容"""
        today = datetime.now()
        count = len(news_list)
        
        # 标题
        title_template = self.config.get('xiaohongshu', {}).get('post_format', {}).get(
            'title_template', '昨日AI圈{count}大热点'
        )
        title = title_template.format(
            date=today.strftime('%m月%d日'),
            count=count
        )
        
        # 头部
        header_template = self.config.get('xiaohongshu', {}).get('post_format', {}).get(
            'header', '{date} AI圈真实热点'
        )
        header = header_template.format(date=today.strftime('%Y年%m月%d日'))
        
        # 正文
        content_lines = [f'标题：{title}', '', header, '（来源：多源聚合，已去重）', '', '昨天AI圈发生了什么大事？', '我整理了最热资讯', '']
        
        for i, news in enumerate(news_list, 1):
            content_lines.append(f"{i}. {news['emoji']} {news['title']}")
            if news.get('summary'):
                content_lines.append(f"   {news['summary']}")
            content_lines.append(f"   来源：{news['source']}")
            content_lines.append(f"   链接：{news['url']}")
            content_lines.append('')
        
        # 尾部
        content_lines.extend([
            '——',
            '新闻来源：多源聚合（已去重）',
            '你最关注哪一条？评论区聊聊',
            '关注我，每天AI热点不错过',
            '',
            '#AI #人工智能 #科技热点 #OpenAI'
        ])
        
        return '\n'.join(content_lines)
    
    def save_content(self, content: str) -> Path:
        """保存内容"""
        today = datetime.now().strftime('%Y%m%d')
        filename = f"xhs_ai_news_{today}.txt"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return filepath
    
    def run(self, dry_run: bool = False) -> tuple:
        """运行完整流程"""
        print("=" * 70)
        print("XHS AI日报生成器 v2.0")
        print("=" * 70)
        print()
        
        # 收集新闻
        all_news = []
        all_news.extend(self.collect_from_ai_news_collectors())
        all_news.extend(self.collect_from_news_aggregator())
        all_news.extend(self.collect_from_techmeme())
        
        print()
        print(f"[汇总] 共收集 {len(all_news)} 条原始新闻")
        
        if not all_news:
            print("[Error] 未收集到任何新闻，请检查网络连接和skill配置")
            return None, None
        
        # 去重排序
        final_news = self.deduplicate_and_rank(all_news)
        
        # 生成内容
        content = self.generate_xhs_content(final_news)
        
        # 保存
        if not dry_run:
            filepath = self.save_content(content)
            print()
            print("=" * 70)
            print(f"生成完成！")
            print(f"文件: {filepath}")
            print(f"新闻数: {len(final_news)} 条")
            print("=" * 70)
        else:
            print()
            print("[Dry Run] 测试模式，未保存文件")
            filepath = None
        
        return content, filepath

def main():
    parser = argparse.ArgumentParser(description='XHS AI日报生成器')
    parser.add_argument('--publish', action='store_true', help='生成后准备发布到小红书')
    parser.add_argument('--dry-run', action='store_true', help='测试模式，不保存文件')
    parser.add_argument('--config', type=str, help='配置文件路径')
    
    args = parser.parse_args()
    
    # 创建发布器
    publisher = XHSAIDailyPublisher(config_path=args.config)
    
    # 运行
    content, filepath = publisher.run(dry_run=args.dry_run)
    
    if content and args.publish:
        print()
        print("准备发布到小红书...")
        print("运行: python xhs_auto_publish.py --latest")

if __name__ == '__main__':
    main()
