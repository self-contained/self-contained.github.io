# Self-contained: 一份个人博客随笔 <!-- omit in toc -->

本项目是 [wklchris](https://github.com/wklchris) 的个人博客迁移站点。

要进入本站，请点击 [https://self-contained.github.io/](https://self-contained.github.io/) 链接，或者点击仓库简介中显示的 URL。

1. [模板结构](#模板结构)
2. [make.py 工具](#makepy-工具)
   1. [创建新文档](#创建新文档)
   2. [构建文档](#构建文档)
   3. [移除文档](#移除文档)

## 模板结构

本仓库的 Github Pages 功能定位于 master 分支的 `docs/` 文件夹，这可以在 Github 仓库的设置中进行配置。

关键文件：
- `make.py`：原 `make.bat` / `Makefile` 的优化替代。
- `config\`
  - `db.yaml`：全站的文档 meta 数据。
  - `hyperconf.yaml`，`index.html`，`index.rst`：用于初始化文档仓库的文件。
  - `index-homepage.rst`：用于更新主页的模板文件。
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

## make.py 工具

仓库中的 `make.py` 是本人编写的文档快速管理工具，用法是：

```sh
python make.py [-h] [--build | --create | --remove] [--title TITLE [TITLE ...]] docname
```

对于 Windows 用户，如果在 `PATH_EXT` 环境变量中加上对 `;.py` 的执行支持，并将 `.py` 文件的默认打开方式设置为了 Python 解释器，那么可以省略最前面的 `python` 前缀；在下述内容中，该前缀默认省略。

各参数：
- `-h`：显示帮助。
- 互斥参数组：以下三个参数最多只能同时传入1个。
  - `--build` / `-b`：（默认）网页构建模式。
  - `--create` / `-c`：创建模式。
    - `--title` / `-t`：指定文档一个与项目名称不同的标题。仅在创建模式生效。
  - `--remove` / `-R`：删除模式。
- `docname`：必选参数。文档项目名称，同时也是文档文件夹的名称。

以下样例均在 Windows 10，**Powershell 环境**中执行。请注意，在 CMD 中的表现很可能不同。

### 创建新文档

用 `--create/-c` 参数创建一个名为 `doc1` 的文档，路径在 `docsrc/doc1`。它会被自动初始化，加入 `index.rst`，`index.html` 与 `conf.py`。

```sh
./make.py doc1 --create
```

文档内标题默认与项目名相同。如果要指定一个文档内标题，使用 `-t` 参数：

```sh
./make.py doc1 -t title
```

### 构建文档

使用 `--build/-b` 参数（或者省略）来构建文档，将其转为 HTML。构建后的 HTML 会临时生成在 `docsrc/doc1/build` 文件夹中，随后 `docsrc/doc1/build/html` 中的所有文件会被移动到 `docs/doc1` 中，然后临时文件夹 `build` 会被删除。

```sh
./make.py doc1
```

同时，该命令还会尝试自动更新数据库 `db.yaml`，并自动构建主页（从 `docsrc/_hompage` 到 `docs/`）。因此用户会在控制台中观察到两次 sphinx 构建。

### 移除文档

使用 `--remove/-R` 参数来移除指定的文档。

```sh
./make.py doc1 -R
```

该文档的所有记录均会被删除，包括：
- 源文件：移除整个 `docsrc/doc1` 文件夹；
- 数据库记录：移除 `db.yaml` 中所有关于文档 `doc1` 的记录项；
- 主页的文档列表：在更新数据库后，主页会自动重编译，以保证 `doc1` 已经从列表中被移除。
