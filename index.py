from markdown_it import MarkdownIt
import os

# This function recursively grabs markdown files
def get_files(target):
    files = []
    dirs = [target]
    while len(dirs) > 0:
        test = dirs.pop(0)
        if os.path.isdir(test):
            dirs += list(map(lambda x: f'{test}/{x}', os.listdir(test)))
        elif ".md" in test:
            files.append(test)
    return files

# Initializes script variables
targets = get_files("test")
md = MarkdownIt()

# Run conversion loop
for src in targets:
    # Read input file
    file = open(src, "r")
    content = file.read()
    html = md.render(content)
    file.close()

    # Write output file
    out = open(src.replace(".md", ".html"), "w")
    out.write(html)
    out.flush()
    out.close()