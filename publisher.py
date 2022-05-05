"""
This tool converts a markdown project into a website
that can be easily published on the web.
"""
import re
import os
import sys
import shutil
from typing import List
from jinja2 import Template
from markdown_it import MarkdownIt
from gitignore_parser import parse_gitignore
PATH_REGEX = '(\.|\.\.|[\w\s\d])(/[\w\s\d])*'

builtin_styles = {
    'orange': {
        'background': '#ffa500',
        'main': '#ffffff',
        'text': '#000000'
    }
}

def get_files(target: str) -> List[str]:
    """
    This function recursively grabs markdown files,
    except for those matched by .gitignore files.
    """
    files = []
    dirs = [target]
    gitignores = {}
    while len(dirs) > 0:
        path = dirs.pop(0)
        if os.path.isdir(path):
            children = os.listdir(path)
            if '.gitignore' in children:
                gitignores[path] = parse_gitignore(os.path.join(path, '.gitignore'))
            dirs += list(map(lambda x: os.path.join(path, x), children))
        elif re.search('\.md$', path):
            ignore = False
            for folder, matches in gitignores.items():
                if re.search(f'^{folder}', path) and matches(path):
                    ignore = True
                    break
            if not ignore:
                files.append(path)
    return files

def read_file(filepath):
    """
    Reads the contents of a file
    """
    with open(filepath, 'r', encoding = 'utf8') as file:
        return file.read()

def write_file(filepath, body):
    """
    Writes some content to a file
    """
    with open(filepath, 'w', encoding = 'utf8') as file:
        file.write(body)
        file.flush()

def log(msg):
    """
    This function logs the tool's progress
    """
    print(msg)

def print_help():
    """
    This function prints tool usage info
    """
    log('Usage: tool <src> <dst> [stylesheet]')
    log('  src and dst should be project paths')

def main(args: List[str]) -> int:
    """
    This is the tool's main function. It holds the logic
    for converting markdown files into a website.
    """
    src = args[1] if len(args) > 1 else None
    dst = args[2] if len(args) > 2 else None
    style = args[3] if len(args) > 3 else None
    if not (src and dst and re.search(PATH_REGEX, src) and re.search(PATH_REGEX, dst)):
        print_help()
        return 1
    md = MarkdownIt()
    targets = get_files(src)
    log('Found 1 markdown file to convert' if len(targets) == 1 else
        f'Found {len(targets)} markdown files to convert')
    relative = lambda x: os.path.join(os.path.dirname(__file__), x)
    html_template = Template(read_file(relative('templates/page.html')))
    css_template = Template(read_file(relative('templates/style.css')))

    # Copy over stylesheet (if any)
    if style:
        os.makedirs(dst, exist_ok = True)
        outpath = f'{dst}/style.css'
        if os.path.exists(style):
            shutil.copyfile(style, outpath)
            log(f'Stylized after {style}')
        elif style in builtin_styles:
            write_file(outpath, css_template.render(style = builtin_styles[style]))
            log(f'Using style \'{style}\'')
        else:
            log(f'Unknown style \'{style}\'')
            return 1

    # Run conversion loop
    for file in targets:
        body = md.render(read_file(file))
        root = '/'.join(file[len(src):].split('/')[:-1])
        if root == "":
            root = "."
        html = html_template.render(body = body, style = style, root = root)
        outpath = re.sub('\.md$', '.html', file)
        outpath = re.sub(f'^{src}', dst, outpath)
        log(f'Converted {file} -> {outpath}')
        parent = os.path.dirname(outpath)
        os.makedirs(parent, exist_ok = True)
        write_file(outpath, html)
    return 0
