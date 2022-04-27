from markdown_it import MarkdownIt
md = MarkdownIt()

# Find files to render
file = open("test.md", "r")
content = file.read()
file.close()
html = md.render(content)
print(html)

out = open("tets.html", "w")
out.write(html)
out.flush()
out.close()