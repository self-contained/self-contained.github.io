project = 'Homepage'
copyright = '2020, wklchris'
author = 'wklchris'

extensions = [
    'nbsphinx',
    'sphinx.ext.mathjax'
]

language = 'zh_CN'

exclude_patterns = [
    '_build',
    '**.ipynb_checkpoints'
]

html_theme = "sphinx_rtd_theme"
#templates_path = ['../_templates']

html_static_path = ['../_static']
html_css_files = ['style.css']