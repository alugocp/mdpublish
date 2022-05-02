"""
This tool converts a markdown project into a website that can be easily published on the web
"""
import os
import sys
from markdown_it import MarkdownIt

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
        elif ".md" in test:
            files.append(test)
    return files

# Validate arguments then initialize variables
if len(sys.argv) < 3:
    print('Usage: tool src dst')
    sys.exit(1)
targets = get_files(sys.argv[1])
md = MarkdownIt()

# Run conversion loop
for src in targets:
    # Read input file
    with open(src, "r", encoding = "utf8") as file:
        html = md.render(file.read())

    # Create and write output file
    outpath = (src
        .replace(sys.argv[1], sys.argv[2])
        .replace(".md", ".html"))
    parent = os.path.dirname(outpath)
    os.makedirs(parent, exist_ok = True)
    with open(outpath, "w", encoding = "utf8") as out:
        out.write(html)
        out.flush()
