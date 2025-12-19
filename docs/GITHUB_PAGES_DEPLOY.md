# GitHub Pages 部署指南

## 方案一：部署HTML文档到GitHub Pages（推荐）

### 步骤1：初始化Git仓库

```bash
cd /Users/egets/Downloads/Bifrost-master

# 初始化git仓库
git init

# 添加所有文件
git add .

# 创建初始提交
git commit -m "Initial commit: Bifrost项目及完整文档"
```

### 步骤2：创建GitHub仓库

1. 访问 https://github.com/new
2. 仓库名称：`Bifrost-docs` 或 `bifrost`
3. 选择Public（公开）
4. 不要初始化README（我们已经有了）
5. 点击"Create repository"

### 步骤3：连接并推送到GitHub

```bash
# 连接到你的GitHub仓库（替换成你的用户名）
git remote add origin https://github.com/YOUR_USERNAME/Bifrost-docs.git

# 推送代码
git branch -M main
git push -u origin main
```

### 步骤4：配置GitHub Pages

#### 选项A：使用docs/html目录（最简单）

1. 在GitHub仓库页面，点击 `Settings`
2. 左侧菜单找到 `Pages`
3. Source选择：`Deploy from a branch`
4. Branch选择：`main` 分支
5. 文件夹选择：`/docs/html`
6. 点击 `Save`

等待1-2分钟，你的文档将发布到：
`https://YOUR_USERNAME.github.io/Bifrost-docs/`

#### 选项B：使用gh-pages分支（更专业）

```bash
# 创建gh-pages分支并只包含HTML文件
cd docs/html

# 初始化独立的git仓库
git init
git add .
git commit -m "Deploy documentation"

# 强制推送到gh-pages分支
git push -f https://github.com/YOUR_USERNAME/Bifrost-docs.git main:gh-pages

cd ../..
```

然后在GitHub Settings > Pages中：
- Branch选择：`gh-pages`
- 文件夹选择：`/ (root)`
- 点击Save

访问：`https://YOUR_USERNAME.github.io/Bifrost-docs/`

---

## 方案二：自动化部署脚本

我创建了一个自动化脚本，执行以下命令：

```bash
cd /Users/egets/Downloads/Bifrost-master/docs
chmod +x deploy_to_github.sh
./deploy_to_github.sh
```

---

## 自定义域名（可选）

如果你有自己的域名：

1. 在GitHub Pages设置中添加Custom domain
2. 在你的域名DNS设置中添加CNAME记录：
   ```
   docs.yourdomain.com  ->  YOUR_USERNAME.github.io
   ```
3. 在`docs/html/`目录下创建`CNAME`文件：
   ```
   echo "docs.yourdomain.com" > docs/html/CNAME
   ```

---

## 注意事项

1. **仓库必须是Public**才能使用免费的GitHub Pages
2. **首次发布需要等待1-2分钟**
3. **每次更新文档后**需要重新推送：
   ```bash
   cd docs
   python3 generate_professional_html.py
   git add html/
   git commit -m "Update documentation"
   git push
   ```

---

## 常见问题

### Q: 404错误？
- 检查分支和目录设置是否正确
- 等待几分钟让GitHub Pages构建完成

### Q: 样式或图片丢失？
- 确保所有资源使用相对路径
- 检查CDN链接是否可访问

### Q: 需要更新文档？
```bash
cd /Users/egets/Downloads/Bifrost-master/docs
python3 generate_professional_html.py
git add html/
git commit -m "Update docs"
git push
```

等待1-2分钟自动更新。

---

## 快速开始（一键部署）

执行我为你准备的自动化脚本：

```bash
cd /Users/egets/Downloads/Bifrost-master/docs
./deploy_to_github.sh YOUR_GITHUB_USERNAME
```
