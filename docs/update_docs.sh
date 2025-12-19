#!/bin/bash

# 快速更新文档脚本
# 用于后续更新文档时使用

echo "🔄 更新Bifrost文档..."
echo ""

cd /Users/egets/Downloads/Bifrost-master/docs

# 重新生成HTML
echo "📝 重新生成HTML文档..."
python3 generate_professional_html.py
echo ""

# 提交更新
echo "💾 提交更改..."
cd ..
git add docs/html/
git commit -m "📚 Update documentation - $(date '+%Y-%m-%d %H:%M:%S')" || {
    echo "没有更改需要提交"
    exit 0
}
echo ""

# 推送到main分支
echo "⬆️  推送到main分支..."
git push origin main
echo ""

# 更新gh-pages分支
echo "🚀 更新gh-pages分支..."
cd docs/html
git init
git add .
git commit -m "🚀 Update documentation - $(date '+%Y-%m-%d %H:%M:%S')"
git push -f $(git -C ../.. remote get-url origin) main:gh-pages
cd ../..
echo ""

echo "✅ 文档更新完成！"
echo "⏰ 等待1-2分钟后生效"
echo ""
