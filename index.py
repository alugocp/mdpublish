from markdown_it import MarkdownIt
import sys
import os

# This function recursively grabs markdown files
def get_files(target):
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
    file = open(src, "r")
    content = file.read()
    html = md.render(content)
    file.close()

    # Write output file
    outpath = (src
        .replace(sys.argv[1], sys.argv[2])
        .replace(".md", ".html"))
    parent = os.path.dirname(outpath)
    os.makedirs(parent, exist_ok = True)
    out = open(outpath, "w")
    out.write(html)
    out.flush()
    out.close()