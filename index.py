"""
This tool converts a markdown project into a website
that can be easily published on the web.
"""
import re
import os
import sys
import shutil
from typing import List
from markdown_it import MarkdownIt
from gitignore_parser import parse_gitignore
PATH_REGEX = '(\.|\.\.|[\w\s\d])(/[\w\s\d])*'

def log(msg):
    """
    This function logs the tool's progress
    """
    print(msg)

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

def main(args: List[str]) -> int:
    """
    This is the tool's main function. It holds the logic
    for converting markdown files into a website.
    """
    l = len(args)
    src = args[1] if l > 1 else None
    dst = args[2] if l > 2 else None
    style = args[3] if l > 3 else None
    if not (src and dst and re.search(PATH_REGEX, src) and re.search(PATH_REGEX, dst)):
        log('Usage: tool <src> <dst> [stylesheet]')
        log('  src and dst should be project paths')
        return 1
    targets = get_files(src)
    word = 'file' if len(targets) == 1 else 'files'
    log(f'Found {len(targets)} markdown {word} to convert')
    md = MarkdownIt()

    # Copy over stylesheet (if any)
    if style:
        os.makedirs(dst, exist_ok = True)
        outpath = f'{dst}/style.css'
        if os.path.exists(style):
            shutil.copyfile(style, outpath)
            log(f'Stylized after {style}')

    # Run conversion loop
    for file in targets:
        with open(file, 'r', encoding = 'utf8') as markdown:
            html = md.render(markdown.read())
        outpath = re.sub('\.md$', '.html', file)
        outpath = re.sub(f'^{src}', dst, outpath)
        log(f'Converted {file} -> {outpath}')
        parent = os.path.dirname(outpath)
        os.makedirs(parent, exist_ok = True)
        with open(outpath, 'w', encoding = 'utf8') as out:
            out.write(html)
            out.flush()
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
