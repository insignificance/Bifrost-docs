#!/bin/bash

# GitHub Pages 自动化部署脚本
# 用法: ./deploy_to_github.sh [github_username]

set -e

echo "🚀 Bifrost文档自动部署到GitHub Pages"
echo "======================================="
echo ""

# 检查参数
GITHUB_USERNAME="$1"
if [ -z "$GITHUB_USERNAME" ]; then
    read -p "请输入你的GitHub用户名: " GITHUB_USERNAME
fi

REPO_NAME="Bifrost-docs"
REPO_URL="https://github.com/${GITHUB_USERNAME}/${REPO_NAME}.git"

echo "📦 GitHub仓库: ${REPO_URL}"
echo ""

# 回到项目根目录
cd /Users/egets/Downloads/Bifrost-master

# 步骤1: 初始化Git仓库（如果还没有）
if [ ! -d ".git" ]; then
    echo "📝 初始化Git仓库..."
    git init
    echo ""
fi

# 步骤2: 创建.gitignore
echo "📝 创建.gitignore..."
cat > .gitignore << 'EOF'
# macOS
.DS_Store
._*

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.egg-info/

# 临时文件
*.tmp
*.bak
*.swp
*~

# IDE
.vscode/
.idea/
*.sublime-*

# 旧版本HTML（保留最新的html目录）
docs/html_v2/
docs/docs_html/
EOF
echo ""

# 步骤3: 添加并提交文件
echo "📝 提交代码..."
git add .
git commit -m "📚 Bifrost项目：iOS业务模块化架构及完整文档

- 核心Bifrost库代码
- 完整的Demo项目
- 9章详尽的使用文档（Markdown）
- 专业的HTML文档网站

文档包含：
✅ 什么是Bifrost
✅ 核心概念详解
✅ 快速开始指南
✅ 路由系统详解
✅ 远程API详解
✅ 模块开发指南
✅ 最佳实践
✅ Demo项目解析" || echo "已经提交过了"
echo ""

# 步骤4: 连接GitHub仓库
echo "🔗 连接到GitHub仓库..."
git remote remove origin 2>/dev/null || true
git remote add origin "$REPO_URL"
git branch -M main
echo ""

# 步骤5: 推送到GitHub
echo "⬆️  推送到GitHub..."
echo "如果这是第一次推送，你需要："
echo "1. 先在GitHub创建仓库: https://github.com/new"
echo "   - 仓库名: ${REPO_NAME}"
echo "   - 类型: Public"
echo "   - 不要初始化README"
echo ""
read -p "仓库已创建好了吗？按Enter继续..."
echo ""

git push -u origin main || {
    echo ""
    echo "❌ 推送失败！"
    echo "请检查："
    echo "1. GitHub仓库是否已创建"
    echo "2. 是否有推送权限"
    echo "3. 可能需要先登录: gh auth login"
    exit 1
}
echo ""

# 步骤6: 部署文档到gh-pages分支
echo "📄 部署文档到gh-pages分支..."
cd docs/html

# 临时初始化git仓库
rm -rf .git
git init
git add .
git commit -m "🚀 Deploy documentation to GitHub Pages"

# 推送到gh-pages分支
git push -f "$REPO_URL" main:gh-pages

cd ../..
echo ""

# 完成
echo "✅ 部署完成！"
echo ""
echo "📱 接下来的步骤："
echo "1. 访问: https://github.com/${GITHUB_USERNAME}/${REPO_NAME}/settings/pages"
echo "2. 在 'Build and deployment' 部分："
echo "   - Source: Deploy from a branch"
echo "   - Branch: gh-pages"
echo "   - Folder: / (root)"
echo "3. 点击 Save"
echo ""
echo "⏰ 等待1-2分钟后，文档将发布到:"
echo "🌐 https://${GITHUB_USERNAME}.github.io/${REPO_NAME}/"
echo ""
echo "🎉 完成！"
