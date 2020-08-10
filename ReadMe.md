# Self-contained: 一份个人博客随笔 <!-- omit in toc -->

本项目是 [wklchris](https://github.com/wklchris) 的个人博客迁移站点。

要进入本站，请点击右侧仓库简介中显示的 URL。

## 如何使用本模板

关键文件：
- `make.py`：原 `make.bat` / `Makefile` 的优化替代。
- `docs\`
  - `.nojekyll`：阻止 Github Pages 的 Jekyll 功能。
- `docsrc\`
  - `_homepage\`: 主网站页面的源文件夹。
    - `404.rst`：网站内的 404 错误提示页。
    - `conf.py`：屏蔽了 template，准备稍加自定义。
  - `_static\`：样式文件。
  - `_templates\layout.html`
    - 配置了侧边栏的“返回主页”按钮。
    - 配置了 Google Analytics。

### make.py 工具

尚在更新中……
