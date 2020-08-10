import datetime
import os, shutil
import yaml

def docsrc_prefix_path(*path, docsrc_path="docsrc"):
    return os.path.join(docsrc_path, *path)

def docdst_prefix_path(*path, docdst_path="docs"):
    return os.path.join(docdst_path, *path)

def write_str_into_file(docstr, *path):
    fpath = docsrc_prefix_path(*path)
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(docstr)

def create_new_doc(docname, doctitle=None, config_path='config'):
    """
    Create a new document and init it.
    """
    if not doctitle:
        doctitle = docname
    doc_path = docsrc_prefix_path(docname)
    if not os.path.isdir(doc_path):
        os.mkdir(doc_path)
        init_conf_py(docname, doctitle, config_path)  # Add conf.py
        init_index_rst(docname, doctitle)             # Add index.rst
        init_copy_files(docname, config_path)         # Add index.html & nojekyll
        print(f"Document '{docname}' has been initialized under '{doc_path}'.")
    else:
        print(f"Document folder '{docname}' already exist.")

def init_conf_py(docname, doctitle, configpath):
    """
    Initialize the new document folder with configuration files.
    """
    # Read the general conf.py settings from hyperconf.yaml
    hyperconf_path = os.path.join(configpath, "hyperconf.yaml")
    with open(hyperconf_path, 'r') as f:
        doc_conf = yaml.safe_load(f)
    ## Add doc-wise information & Sort
    doc_conf['year'] = int(f"{datetime.datetime.today():%Y}")
    doc_conf['project'] = doctitle
    doc_conf = {k: doc_conf[k] for k in sorted(doc_conf)}

    # Write the dict into a .py file
    def write_dict_value(dict_val):
        ## Dict value is either string or int/list
        if isinstance(dict_val, str):
            write_str = '"{}"'.format(dict_val.strip('"'))
        else:
            write_str = dict_val
        return write_str
    
    conf_str = '\n'.join([
        f"{k} = {write_dict_value(v)}" for k,v in doc_conf.items() 
    ])
    write_str_into_file(conf_str, docname, "conf.py")

def init_index_rst(docname, doctitle):
    """
    Initialize the index.rst for table of content of the document.
    """
    rst_str_lines = [
        doctitle,
        '=' * (len(doctitle) + 4), "",   # RST title format
        "Abstract paragraph", "",
        ".. toctree::",
        "   :maxdepth: 2",
        "   :caption: 目录", "",
        "   Intro.rst"
    ]
    rst_str = '\n'.join(rst_str_lines)
    write_str_into_file(rst_str, docname, "index.rst")

def init_index_html(docname, configpath):
    """
    Initialize the index.html for jumping to the built HTML file path.
    """
    src = os.path.join(configpath, "index.html")
    dst = docsrc_prefix_path(docname, "index.html")
    shutil.copy(src, dst)

def init_copy_files(docname, configpath):
    """
    Copy files:
    - "index.html" for jumping to the built HTML file path.
    """
    for f in ("index.html"):
        src = os.path.join(configpath, f)
        dst = docsrc_prefix_path(docname, f)
        shutil.copy(src, dst)

def sphinx_build(docname):
    """
    Build the Sphinx website and output files in specifc folder.
    """
    # Buld the HTML website
    build_dirname = "build"
    build_dir = docsrc_prefix_path(docname, build_dirname)
    src_dir = docsrc_prefix_path(docname)
    cmd = f"sphinx-build -M html {src_dir} {build_dir}"
    os.system(cmd)
    # Copy to /docs folder
    if docname != "_homepage":
        dst_dir = docdst_prefix_path(docname)
    else:
        dst_dir = docdst_prefix_path("")
    shutil.copytree(os.path.join(build_dir, "html"), dst_dir, dirs_exist_ok=True)
    # Delete the build folder from src directory
    shutil.rmtree(build_dir)
    print(f"HTML pages have been moved into {dst_dir}.")

sphinx_build('Matplotlib')
