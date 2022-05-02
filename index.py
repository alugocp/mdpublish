"""
This tool converts a markdown project into a website that can be easily published on the web
"""
import re
import os
import sys
from markdown_it import MarkdownIt
PATH_REGEX = '(\.|\.\.|[\w\s\d])(/[\w\s\d])*'

def get_files(target):
    """
    This function recursively grabs markdown files
    """
    files = []
    dirs = [target]
    while len(dirs) > 0:
        test = dirs.pop(0)
        if os.path.isdir(test):
            dirs += list(map(lambda x: os.path.join(test, x), os.listdir(test)))
        elif re.search('\.md$', test):
            files.append(test)
    return files

# Validate arguments then initialize variables
l = len(sys.argv)
src = sys.argv[1] if l > 1 else None
dst = sys.argv[2] if l > 2 else None
if not (src and dst and re.search(PATH_REGEX, src) and re.search(PATH_REGEX, dst)):
    print('Usage: tool <src> <dst>')
    print('  src and dst should be project paths')
    sys.exit(1)
targets = get_files(sys.argv[1])
print(f'Found {len(targets)} markdown files to convert')
md = MarkdownIt()

# Run conversion loop
for file in targets:
    # Read input file
    with open(file, 'r', encoding = 'utf8') as markdown:
        html = md.render(markdown.read())

    # Create and write output file
    outpath = re.sub('\.md$', '.html', file)
    outpath = re.sub(f'^{sys.argv[1]}', sys.argv[2], outpath)
    print(f'Converted {file} -> {outpath}')
    parent = os.path.dirname(outpath)
    os.makedirs(parent, exist_ok = True)
    with open(outpath, 'w', encoding = 'utf8') as out:
        out.write(html)
        out.flush()
