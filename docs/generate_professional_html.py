#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bifrost文档HTML生成器 - 修复版
修复中文锚点跳转问题
"""

import os
import re

# 文档配置
DOCS = [
    {
        'file': 'README.md',
        'title': '文档导航',
        'subtitle': '快速找到你需要的内容',
        'icon': '📚',
        'prev': None,
        'next': '01-什么是Bifrost.md'
    },
    {
        'file': '01-什么是Bifrost.md',
        'title': '第1章 什么是Bifrost',
        'subtitle': '了解Bifrost的背景和核心理念',
        'icon': '🎯',
        'prev': 'README.md',
        'next': '02-核心概念.md'
    },
    {
        'file': '02-核心概念.md',
        'title': '第2章 核心概念',
        'subtitle': '业务模块、代码依赖、三层架构',
        'icon': '💡',
        'prev': '01-什么是Bifrost.md',
        'next': '03-快速开始.md'
    },
    {
        'file': '03-快速开始.md',
        'title': '第3章 快速开始',
        'subtitle': '10分钟上手Bifrost',
        'icon': '🚀',
        'prev': '02-核心概念.md',
        'next': '04-路由系统详解.md'
    },
    {
        'file': '04-路由系统详解.md',
        'title': '第4章 路由系统详解',
        'subtitle': 'Router URL的使用和高级特性',
        'icon': '🗺️',
        'prev': '03-快速开始.md',
        'next': '05-远程API详解.md'
    },
    {
        'file': '05-远程API详解.md',
        'title': '第5章 远程API详解',
        'subtitle': 'Service协议设计和模块间通信',
        'icon': '🔌',
        'prev': '04-路由系统详解.md',
        'next': '06-模块开发指南.md'
    },
    {
        'file': '06-模块开发指南.md',
        'title': '第6章 模块开发指南',
        'subtitle': '完整的模块开发流程',
        'icon': '⚙️',
        'prev': '05-远程API详解.md',
        'next': '07-最佳实践.md'
    },
    {
        'file': '07-最佳实践.md',
        'title': '第7章 最佳实践',
        'subtitle': '命名规范、性能优化、常见问题',
        'icon': '✨',
        'prev': '06-模块开发指南.md',
        'next': '08-Demo项目解析.md'
    },
    {
        'file': '08-Demo项目解析.md',
        'title': '第8章 Demo项目解析',
        'subtitle': '通过实际项目深入理解',
        'icon': '🎓',
        'prev': '07-最佳实践.md',
        'next': None
    },
]

def md_to_html(md_file):
    """将md文件名转换为html文件名"""
    return md_file.replace('.md', '.html')

def process_markdown_links(content):
    """处理Markdown中的链接"""
    # 处理相对链接 [text](./file.md) -> [text](file.html)
    content = re.sub(r'\]\(\./([^)]+\.md)\)', r'](\1)', content)
    # 将 .md 链接转换为 .html
    content = re.sub(r'\]\(([^)]+)\.md\)', r'](\1.html)', content)
    return content

def generate_sidebar(current_file):
    """生成侧边栏导航"""
    html = '<nav class="sidebar"><div class="sidebar-content">'
    html += '<h3>📖 文档目录</h3><ul class="doc-nav">'

    for doc in DOCS:
        html_file = md_to_html(doc['file'])
        active = ' class="active"' if doc['file'] == current_file else ''
        html += f'<li><a href="{html_file}"{active}>{doc["icon"]} {doc["title"]}</a></li>'

    html += '</ul></div></nav>'
    return html

def generate_doc_page(doc):
    """生成文档页面"""

    # 读取Markdown内容
    with open(doc['file'], 'r', encoding='utf-8') as f:
        md_content = f.read()

    # 处理链接
    md_content = process_markdown_links(md_content)

    # 转义用于JavaScript
    md_content = md_content.replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${')

    # 生成导航按钮
    prev_btn = ''
    next_btn = ''

    if doc['prev']:
        prev_doc = next((d for d in DOCS if d['file'] == doc['prev']), None)
        if prev_doc:
            prev_btn = f'''
            <a href="{md_to_html(doc['prev'])}" class="nav-btn prev">
                <span class="nav-icon">←</span>
                <div class="nav-text">
                    <div class="nav-label">上一章</div>
                    <div class="nav-title">{prev_doc['title']}</div>
                </div>
            </a>
            '''

    if doc['next']:
        next_doc = next((d for d in DOCS if d['file'] == doc['next']), None)
        if next_doc:
            next_btn = f'''
            <a href="{md_to_html(doc['next'])}" class="nav-btn next">
                <div class="nav-text">
                    <div class="nav-label">下一章</div>
                    <div class="nav-title">{next_doc['title']}</div>
                </div>
                <span class="nav-icon">→</span>
            </a>
            '''

    sidebar = generate_sidebar(doc['file'])

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{doc['subtitle']}">
    <title>{doc['title']} - Bifrost文档</title>

    <script src="https://cdn.jsdelivr.net/npm/marked@11.1.0/marked.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10.6.0/dist/mermaid.min.js"></script>

    <style>
        :root {{
            --primary-color: #0366d6;
            --primary-dark: #0256c7;
            --bg-color: #f6f8fa;
            --text-color: #24292e;
            --border-color: #e1e4e8;
            --sidebar-width: 280px;
            --header-height: 60px;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.7;
            color: var(--text-color);
            background: var(--bg-color);
        }}

        /* 顶部栏 */
        .header {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: var(--header-height);
            background: white;
            border-bottom: 1px solid var(--border-color);
            z-index: 100;
            display: flex;
            align-items: center;
            padding: 0 2rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }}

        .header-content {{
            max-width: 1400px;
            width: 100%;
            margin: 0 auto;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}

        .logo {{
            font-size: 1.3rem;
            font-weight: 600;
            color: var(--primary-color);
            text-decoration: none;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .breadcrumb {{
            font-size: 0.9rem;
            color: #586069;
        }}

        .breadcrumb a {{
            color: var(--primary-color);
            text-decoration: none;
        }}

        .breadcrumb a:hover {{
            text-decoration: underline;
        }}

        /* 侧边栏 */
        .sidebar {{
            position: fixed;
            left: 0;
            top: var(--header-height);
            width: var(--sidebar-width);
            height: calc(100vh - var(--header-height));
            background: white;
            border-right: 1px solid var(--border-color);
            overflow-y: auto;
            z-index: 50;
        }}

        .sidebar-content {{
            padding: 2rem 1.5rem;
        }}

        .sidebar h3 {{
            font-size: 0.9rem;
            font-weight: 600;
            color: #586069;
            margin-bottom: 1rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .doc-nav {{
            list-style: none;
        }}

        .doc-nav li {{
            margin: 0.3rem 0;
        }}

        .doc-nav a {{
            display: block;
            padding: 0.6rem 1rem;
            color: var(--text-color);
            text-decoration: none;
            border-radius: 6px;
            font-size: 0.9rem;
            transition: all 0.2s;
        }}

        .doc-nav a:hover {{
            background: var(--bg-color);
            color: var(--primary-color);
        }}

        .doc-nav a.active {{
            background: var(--primary-color);
            color: white;
            font-weight: 500;
        }}

        /* 主内容区 */
        .main {{
            margin-left: var(--sidebar-width);
            margin-top: var(--header-height);
            padding: 3rem;
        }}

        .content-wrapper {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            padding: 3rem;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }}

        /* Markdown内容样式 */
        .markdown-body {{
            font-size: 16px;
        }}

        .markdown-body h1 {{
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 2rem;
            padding-bottom: 0.5rem;
            border-bottom: 3px solid var(--primary-color);
            color: var(--primary-color);
        }}

        .markdown-body h2 {{
            font-size: 1.8rem;
            font-weight: 600;
            margin-top: 3rem;
            margin-bottom: 1.5rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid var(--border-color);
        }}

        .markdown-body h3 {{
            font-size: 1.4rem;
            font-weight: 600;
            margin-top: 2rem;
            margin-bottom: 1rem;
        }}

        .markdown-body h4 {{
            font-size: 1.2rem;
            font-weight: 600;
            margin-top: 1.5rem;
            margin-bottom: 0.8rem;
            color: #586069;
        }}

        .markdown-body p {{
            margin: 1.2rem 0;
            line-height: 1.8;
        }}

        .markdown-body ul, .markdown-body ol {{
            margin: 1.2rem 0;
            padding-left: 2rem;
        }}

        .markdown-body li {{
            margin: 0.5rem 0;
            line-height: 1.7;
        }}

        .markdown-body a {{
            color: var(--primary-color);
            text-decoration: none;
            font-weight: 500;
        }}

        .markdown-body a:hover {{
            text-decoration: underline;
        }}

        .markdown-body code {{
            background: #f6f8fa;
            padding: 0.2em 0.4em;
            border-radius: 3px;
            font-family: "SF Mono", Monaco, Consolas, monospace;
            font-size: 0.9em;
            color: #e83e8c;
        }}

        .markdown-body pre {{
            background: #f6f8fa;
            padding: 1.2rem;
            border-radius: 6px;
            overflow-x: auto;
            margin: 1.5rem 0;
            border: 1px solid var(--border-color);
        }}

        .markdown-body pre code {{
            background: none;
            padding: 0;
            color: inherit;
            font-size: 0.9rem;
        }}

        .markdown-body table {{
            border-collapse: collapse;
            width: 100%;
            margin: 1.5rem 0;
        }}

        .markdown-body th, .markdown-body td {{
            border: 1px solid var(--border-color);
            padding: 0.8rem 1rem;
            text-align: left;
        }}

        .markdown-body th {{
            background: var(--bg-color);
            font-weight: 600;
        }}

        .markdown-body tr:hover {{
            background: #fafbfc;
        }}

        .markdown-body blockquote {{
            margin: 1.5rem 0;
            padding: 1rem 1.5rem;
            background: #f6f8fa;
            border-left: 4px solid var(--primary-color);
            border-radius: 0 6px 6px 0;
        }}

        .markdown-body img {{
            max-width: 100%;
            height: auto;
            border-radius: 6px;
            margin: 1.5rem 0;
        }}

        /* Mermaid图表 */
        .mermaid {{
            margin: 2rem 0;
            text-align: center;
        }}

        /* 页面导航 */
        .page-navigation {{
            margin-top: 4rem;
            padding-top: 2rem;
            border-top: 2px solid var(--border-color);
            display: flex;
            justify-content: space-between;
            gap: 1rem;
        }}

        .nav-btn {{
            flex: 1;
            max-width: 45%;
            padding: 1.5rem;
            background: white;
            border: 2px solid var(--border-color);
            border-radius: 8px;
            text-decoration: none;
            color: var(--text-color);
            display: flex;
            align-items: center;
            transition: all 0.3s;
        }}

        .nav-btn:hover {{
            border-color: var(--primary-color);
            background: var(--bg-color);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(3,102,214,0.1);
        }}

        .nav-btn.prev {{
            justify-content: flex-start;
        }}

        .nav-btn.next {{
            justify-content: flex-end;
            text-align: right;
        }}

        .nav-icon {{
            font-size: 1.5rem;
            color: var(--primary-color);
            font-weight: bold;
        }}

        .nav-text {{
            margin: 0 1rem;
        }}

        .nav-label {{
            font-size: 0.8rem;
            color: #586069;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 0.3rem;
        }}

        .nav-title {{
            font-size: 1rem;
            font-weight: 600;
            color: var(--text-color);
        }}

        /* 回到顶部 */
        .back-to-top {{
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            width: 50px;
            height: 50px;
            background: var(--primary-color);
            color: white;
            border-radius: 50%;
            display: none;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            font-size: 1.5rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            transition: all 0.3s;
            z-index: 1000;
        }}

        .back-to-top:hover {{
            background: var(--primary-dark);
            transform: translateY(-3px);
        }}

        .back-to-top.show {{
            display: flex;
        }}

        /* 响应式 */
        @media (max-width: 1024px) {{
            .sidebar {{
                transform: translateX(-100%);
            }}
            .main {{
                margin-left: 0;
            }}
        }}

        @media (max-width: 768px) {{
            .header {{
                padding: 0 1rem;
            }}
            .main {{
                padding: 1.5rem;
            }}
            .content-wrapper {{
                padding: 1.5rem;
            }}
            .markdown-body h1 {{
                font-size: 2rem;
            }}
            .page-navigation {{
                flex-direction: column;
            }}
            .nav-btn {{
                max-width: 100%;
            }}
        }}
    </style>
</head>
<body>
    <header class="header">
        <div class="header-content">
            <a href="index.html" class="logo">
                <span>📚</span>
                <span>Bifrost 文档</span>
            </a>
            <div class="breadcrumb">
                <a href="index.html">首页</a> / {doc['title']}
            </div>
        </div>
    </header>

    {sidebar}

    <main class="main">
        <div class="content-wrapper">
            <article class="markdown-body" id="content"></article>
            <nav class="page-navigation">
                {prev_btn if prev_btn else '<div></div>'}
                {next_btn if next_btn else '<div></div>'}
            </nav>
        </div>
    </main>

    <div class="back-to-top" id="backToTop">↑</div>

    <script>
        // 初始化Mermaid
        mermaid.initialize({{
            startOnLoad: false,
            theme: 'default',
            securityLevel: 'loose',
        }});

        // 自定义渲染器 - 修复中文锚点问题
        const renderer = new marked.Renderer();

        // 覆盖heading渲染，使用中文友好的ID生成
        renderer.heading = function(text, level, raw) {{
            // 移除markdown链接语法，只保留文本
            const plainText = text.replace(/<[^>]+>/g, '');

            // 生成ID：移除特殊字符，保留中文、英文、数字、-
            const id = plainText
                .toLowerCase()
                .replace(/[^\\u4e00-\\u9fa5a-z0-9\\s-]/g, '')
                .replace(/\\s+/g, '-')
                .replace(/-+/g, '-')
                .replace(/^-|-$/g, '');

            return `<h${{level}} id="${{id}}">${{text}}</h${{level}}>`;
        }};

        // 配置marked
        marked.setOptions({{
            renderer: renderer,
            breaks: true,
            gfm: true,
            headerIds: true,
            mangle: false,
            highlight: function(code, lang) {{
                if (lang && hljs.getLanguage(lang)) {{
                    return hljs.highlight(code, {{ language: lang }}).value;
                }}
                return hljs.highlightAuto(code).value;
            }}
        }});

        // Markdown内容
        const markdown = `{md_content}`;

        // 渲染
        const contentEl = document.getElementById('content');
        contentEl.innerHTML = marked.parse(markdown);

        // 处理Mermaid图表
        const mermaidBlocks = contentEl.querySelectorAll('pre code.language-mermaid');
        mermaidBlocks.forEach((block, index) => {{
            const pre = block.parentElement;
            const code = block.textContent;
            const div = document.createElement('div');
            div.className = 'mermaid';
            div.textContent = code;
            pre.replaceWith(div);
        }});

        // 渲染Mermaid
        mermaid.run();

        // 回到顶部
        const backToTop = document.getElementById('backToTop');
        window.addEventListener('scroll', () => {{
            backToTop.classList.toggle('show', window.pageYOffset > 300);
        }});
        backToTop.addEventListener('click', () => {{
            window.scrollTo({{ top: 0, behavior: 'smooth' }});
        }});

        // 修复锚点跳转 - 考虑固定头部的高度
        function scrollToAnchor(target) {{
            const headerOffset = 80; // 固定头部高度 + 额外间距
            const elementPosition = target.getBoundingClientRect().top;
            const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

            window.scrollTo({{
                top: offsetPosition,
                behavior: 'smooth'
            }});
        }}

        // 处理所有锚点链接点击
        document.addEventListener('click', function(e) {{
            const target = e.target.closest('a[href^="#"]');
            if (target) {{
                e.preventDefault();
                const id = target.getAttribute('href').substring(1);
                const element = document.getElementById(id);
                if (element) {{
                    scrollToAnchor(element);
                    // 更新URL但不跳转
                    history.pushState(null, null, '#' + id);
                }}
            }}
        }});

        // 页面加载时处理URL中的锚点
        window.addEventListener('DOMContentLoaded', function() {{
            if (window.location.hash) {{
                setTimeout(() => {{
                    const id = window.location.hash.substring(1);
                    const element = document.getElementById(id);
                    if (element) {{
                        scrollToAnchor(element);
                    }}
                }}, 100);
            }}
        }});
    </script>
</body>
</html>'''

    return html

def generate_index():
    """生成首页"""

    cards_html = ''
    for doc in DOCS:
        html_file = md_to_html(doc['file'])
        cards_html += f'''
        <a href="{html_file}" class="doc-card">
            <div class="card-icon">{doc['icon']}</div>
            <h3>{doc['title']}</h3>
            <p>{doc['subtitle']}</p>
            <div class="card-arrow">→</div>
        </a>
        '''

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Bifrost - iOS业务模块化架构完整指南">
    <title>Bifrost使用文档 - iOS模块化架构指南</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 3rem 1.5rem;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}

        .hero {{
            text-align: center;
            color: white;
            margin-bottom: 4rem;
            animation: fadeInDown 0.8s;
        }}

        .hero h1 {{
            font-size: 3.5rem;
            font-weight: 700;
            margin-bottom: 1rem;
            text-shadow: 0 4px 6px rgba(0,0,0,0.2);
        }}

        .hero .subtitle {{
            font-size: 1.4rem;
            opacity: 0.95;
            margin-bottom: 2rem;
            font-weight: 300;
        }}

        .hero .description {{
            font-size: 1.1rem;
            opacity: 0.9;
            max-width: 600px;
            margin: 0 auto 2rem;
            line-height: 1.6;
        }}

        .features {{
            display: flex;
            justify-content: center;
            gap: 2rem;
            margin-bottom: 3rem;
            flex-wrap: wrap;
        }}

        .feature {{
            background: rgba(255,255,255,0.15);
            backdrop-filter: blur(10px);
            padding: 1rem 1.5rem;
            border-radius: 8px;
            color: white;
            font-size: 0.95rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .doc-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 1.5rem;
            animation: fadeInUp 0.8s 0.3s both;
        }}

        .doc-card {{
            background: white;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            text-decoration: none;
            color: #24292e;
            display: block;
            transition: all 0.3s;
            position: relative;
            overflow: hidden;
        }}

        .doc-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #667eea, #764ba2);
            transform: scaleX(0);
            transition: transform 0.3s;
        }}

        .doc-card:hover {{
            transform: translateY(-8px);
            box-shadow: 0 12px 24px rgba(0,0,0,0.15);
        }}

        .doc-card:hover::before {{
            transform: scaleX(1);
        }}

        .card-icon {{
            font-size: 3rem;
            margin-bottom: 1rem;
            display: inline-block;
        }}

        .doc-card h3 {{
            font-size: 1.3rem;
            font-weight: 600;
            margin-bottom: 0.8rem;
            color: #667eea;
        }}

        .doc-card p {{
            color: #586069;
            line-height: 1.6;
            margin-bottom: 1.5rem;
        }}

        .card-arrow {{
            color: #667eea;
            font-size: 1.5rem;
            font-weight: bold;
            opacity: 0;
            transform: translateX(-10px);
            transition: all 0.3s;
        }}

        .doc-card:hover .card-arrow {{
            opacity: 1;
            transform: translateX(0);
        }}

        .footer {{
            text-align: center;
            color: white;
            margin-top: 4rem;
            padding: 2rem 0;
            border-top: 1px solid rgba(255,255,255,0.2);
            animation: fadeIn 1s 0.6s both;
        }}

        .footer a {{
            color: white;
            text-decoration: none;
            border-bottom: 1px solid rgba(255,255,255,0.5);
            transition: border-color 0.3s;
        }}

        .footer a:hover {{
            border-color: white;
        }}

        @keyframes fadeInDown {{
            from {{
                opacity: 0;
                transform: translateY(-30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        @keyframes fadeInUp {{
            from {{
                opacity: 0;
                transform: translateY(30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}

        @media (max-width: 768px) {{
            .hero h1 {{
                font-size: 2.5rem;
            }}
            .hero .subtitle {{
                font-size: 1.2rem;
            }}
            .doc-grid {{
                grid-template-columns: 1fr;
            }}
            .features {{
                flex-direction: column;
                align-items: center;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="hero">
            <h1>📚 Bifrost</h1>
            <p class="subtitle">iOS业务模块化架构完整指南</p>
            <p class="description">
                从零开始掌握Bifrost，打造可维护、可扩展的iOS应用架构
            </p>
            <div class="features">
                <div class="feature">✅ 完全解耦</div>
                <div class="feature">🚀 独立开发</div>
                <div class="feature">⚡ 高性能</div>
                <div class="feature">📖 详尽文档</div>
            </div>
        </div>

        <div class="doc-grid">
            {cards_html}
        </div>

        <div class="footer">
            <p>
                用心打造的iOS模块化架构文档<br>
                <a href="https://github.com/insignificance/Bifrost-docs" target="_blank">GitHub仓库</a> ·
                <a href="README.html">开始阅读</a>
            </p>
        </div>
    </div>
</body>
</html>'''

    return html

def main():
    """主函数"""
    output_dir = 'html'

    print("🔧 重新生成HTML文档（修复锚点跳转）...\n")

    # 生成文档页面
    for doc in DOCS:
        if not os.path.exists(doc['file']):
            print(f"⚠️  文件不存在: {doc['file']}")
            continue

        print(f"📝 生成: {doc['title']}")
        html = generate_doc_page(doc)

        output_file = os.path.join(output_dir, md_to_html(doc['file']))
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)

    # 生成首页
    print(f"\n🏠 生成首页")
    index_html = generate_index()
    index_file = os.path.join(output_dir, 'index.html')
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(index_html)

    print(f"\n✨ 完成！")
    print(f"📂 文档位置: {output_dir}/")
    print(f"🔧 已修复中文锚点跳转问题")

if __name__ == '__main__':
    main()
