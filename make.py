import argparse
import datetime
import os, shutil
from os import read
import yaml

CONFIG = 'config'
CONFIG_DATABASE = os.path.join(CONFIG, "db.yaml")
DOCSRC, DOCDST = 'docsrc', 'docs'
ENCODING = 'utf-8'

def docsrc_prefix_path(*path, docsrc_path="docsrc"):
    return os.path.join(docsrc_path, *path)

def docdst_prefix_path(*path, docdst_path="docs"):
    return os.path.join(docdst_path, *path)

def write_str_into_file(docstr, *path):
    fpath = docsrc_prefix_path(*path)
    with open(fpath, 'w', encoding=ENCODING) as f:
        f.write(docstr)

def read_from_file(fpath, join=True):
    with open(fpath ,'r', encoding=ENCODING) as f:
        lines = f.readlines()
    return lines if not join else ''.join(lines)

def load_yaml(fpath):
    with open(fpath, 'r', encoding=ENCODING) as f:
        data = yaml.safe_load(f)
    return data

def create_new_doc(docname, doctitle=None):
    """
    Create a new document and init it.
    """
    if not doctitle:
        doctitle = docname
    doc_path = docsrc_prefix_path(docname)
    if not os.path.isdir(doc_path):
        os.mkdir(doc_path)
        init_new_doc(docname, doctitle) 
        print(f"Document '{docname}' has been initialized under '{doc_path}'.")
    else:
        print(f"Document folder '{docname}' already exist.")

def init_conf_py(docname, doctitle):
    """
    Initialize the new document folder with configuration files.
    """
    # Read the general conf.py settings from hyperconf.yaml
    hyperconf_path = os.path.join(CONFIG, "hyperconf.yaml")
    doc_conf = load_yaml(hyperconf_path)
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
    rst_config_template =read_from_file(os.path.join(CONFIG, "index.rst"))
    title_heading = "{}\n{}\n".format(doctitle, '='*(len(doctitle) + 4))
    rst_str = rst_config_template.replace("{{ title heading }}", title_heading)
    write_str_into_file(rst_str, docname, "index.rst")

def init_index_html(docname):
    """
    Initialize the index.html for jumping to the built HTML file path.
    """
    src = os.path.join(CONFIG, "index.html")
    dst = docsrc_prefix_path(docname, "index.html")
    shutil.copy(src, dst)

def init_new_doc(docname, doctitle):
    """
    Init/Copy files:
    + "conf.py"
    + "index.html"
    + "index.rst"
    """
    init_conf_py(docname, doctitle)    # Init conf.py
    init_index_html(docname)           # Copy index.html
    init_index_rst(docname, doctitle)  # Init index.rst

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
    print("---\nHTML pages have been moved into " + dst_dir)
    
    # Automatically update the database & homepage
    if docname != "_homepage":
        update_database(docname)
        update_homepage()

def update_yaml(yaml_file, key, value):
    d = load_yaml(yaml_file)
    # If value is None, delete the key
    if value:
        d[key] = value
    else:
        _ = d.pop(key, None)
    # Sort keys and write back to the yaml file
    d = {k: d[k] for k in sorted(d)}
    with open(yaml_file, 'w', encoding=ENCODING) as f:
        yaml.dump(d, f, allow_unicode=True)

def update_database(docname):
    """
    Update the metadata database after building cuurent document.
    """
    # Read the meta header of the source document RST
    doc_str_lines = read_from_file(docsrc_prefix_path(docname, "index.rst"), join=False)
    doc_meta = dict()
    for line in doc_str_lines[1:]:
        line = line.strip()
        if line.startswith(':'):
            key, value = line[1:].split(':', 1)
            doc_meta[key] = value.strip()
        else:
            break
    # Update modification date
    doc_meta["keywords"] = doc_meta["keywords"].split(',')
    doc_meta["last_modified"] = f"{datetime.datetime.today():%Y-%m-%d}"
    # Write into the database
    update_yaml(CONFIG_DATABASE, docname, doc_meta)
    print('Database has been updated.')

def update_homepage():
    """
    Update & build the homepage based on the latest updated document.
    """
    rst_str = read_from_file(os.path.join(CONFIG, "index-homepage.rst"))
    total_meta = load_yaml(CONFIG_DATABASE)    
    blog_list = [doc for doc in total_meta.keys() if not doc.startswith('_')]

    blog_str_group = dict()
    for docname in blog_list:
        doc_meta = total_meta[docname]
        category = doc_meta["category"]
        abstract = doc_meta['abstract']
        modify_date = doc_meta["last_modified"]
        item_str = f"  * `{docname} <{docname}/index.html>`_ （更新于{modify_date}）：{abstract}"
        if category in blog_str_group:
            blog_str_group[category] += "\n" + item_str
        else:
            blog_str_group[category] = f"\n* {category}\n\n{item_str}"
    blog_str_group = {k: blog_str_group[k] for k in sorted(blog_str_group)}
    blog_list_str = '\n'.join(blog_str_group.values())
    rst_str = rst_str.replace("{{ blog list }}", blog_list_str)

    # Write it to index.rst and build the homepage
    write_str_into_file(rst_str, "_homepage", "index.rst")
    sphinx_build("_homepage")

def remove_doc(docname):
    """
    Remove a doc from both local file and the database.
    """
    # Remove source & build directory, if exists
    doc_dir = docsrc_prefix_path(docname)
    build_dir = docdst_prefix_path(docname)
    for dirpath in (doc_dir, build_dir):
        if os.path.isdir(dirpath):
            shutil.rmtree(dirpath)
    # Remove docname key from the database 
    update_yaml(CONFIG_DATABASE, docname, None)
    update_homepage()
    print(f"Removed {docname} from the database, {doc_dir}, and {build_dir}.")

def enable_args():
    parser = argparse.ArgumentParser(
        description='Tool for making Sphinx HTML pages.'
    )
    args_help = {
        "docname": "Specify the docname (also project folder name).",
        "--create": "Create a new project. Won't overwrite existing ones. (Exclusive to --build)",
        "--build": "Build a project. (Exclusive to --create)",
        "--title": "Give a title to new project. Ignored in --build mode.",
        "--config": "Specific the config folder path.",
        "--remove": "Remove a document from the website."
    }

    parser.add_argument('docname')
    parser_group = parser.add_mutually_exclusive_group()
    parser_group.add_argument('--build', '-b', help=args_help['--build'], action='store_true')
    parser_group.add_argument('--create', '-c', dest='build', help=args_help["--create"], action='store_false')
    parser_group.add_argument('--remove', '-R', help=args_help["--remove"], action='store_true')
    parser_group.set_defaults(build=True, remove=False)
    parser.add_argument('--title', '-t', help=args_help['--title'], nargs='+', default=None)

    args = parser.parse_args()
    if args.remove:
        remove_doc(args.docname)
    else:
        # Either build or create. These two args can't be used at a same time.
        if args.build:
            sphinx_build(args.docname)
        else:
            title = ' '.join(args.title) if args.title else args.docname
            create_new_doc(args.docname, title)


# --- Main ---

enable_args()
