"""
This tool converts a markdown project into a website that can be easily published on the web
"""
import re
import os
import sys
import shutil
from markdown_it import MarkdownIt
from gitignore_parser import parse_gitignore
PATH_REGEX = '(\.|\.\.|[\w\s\d])(/[\w\s\d])*'

def get_files(target):
    """
    This function recursively grabs markdown files,
    except for those matched by .gitignore files
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
            for dir, matches in gitignores.items():
                if re.search(f'^{dir}', path) and matches(path):
                    ignore = True
                    break
            if not ignore:
                files.append(path)
    return files

# Validate arguments then initialize variables
l = len(sys.argv)
src = sys.argv[1] if l > 1 else None
dst = sys.argv[2] if l > 2 else None
style = sys.argv[3] if l > 3 else None
if not (src and dst and re.search(PATH_REGEX, src) and re.search(PATH_REGEX, dst)):
    print('Usage: tool <src> <dst> [stylesheet]')
    print('  src and dst should be project paths')
    sys.exit(1)
targets = get_files(src)
word = 'file' if len(targets) == 1 else 'files'
print(f'Found {len(targets)} markdown {word} to convert')
md = MarkdownIt()

# Copy over stylesheet (if any)
if style:
    os.makedirs(dst, exist_ok = True)
    outpath = f'{dst}/style.css'
    if os.path.exists(style):
        shutil.copyfile(style, outpath)
        print(f'Stylized after {style}')

# Run conversion loop
for file in targets:
    with open(file, 'r', encoding = 'utf8') as markdown:
        html = md.render(markdown.read())
    outpath = re.sub('\.md$', '.html', file)
    outpath = re.sub(f'^{src}', dst, outpath)
    print(f'Converted {file} -> {outpath}')
    parent = os.path.dirname(outpath)
    os.makedirs(parent, exist_ok = True)
    with open(outpath, 'w', encoding = 'utf8') as out:
        out.write(html)
        out.flush()
