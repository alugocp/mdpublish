# Markdown Publisher
This is a small tool to render markdown (`.md`) files into websites that can be hosted online.
Use it for easily publishing your digital journals or project ideas.

## Development
- `python index.py` - Runs the tool
- `pylint index.py` - Lints the code
- `pip install -r requirements.txt` - Install dependencies

## Todo
### Basic start point
- [x] Make sure you can convert a markdown file to HTML
- [x] Add support for recursive file directories
- [x] Make sure links work as expected
- [x] Structure the tool as a simple CLI with I/O directory args

### Flesh everything out
- [x] Restructure the code to feel better and be more organized/robust
- [x] Add a linter to the project
- [x] Validate arguments and all paths with regex
- [x] Throw some logging in there
- [x] Read `.gitignore` files and ignore the paths within
- [ ] Allow the tool to apply a stylesheet to the generated sites
- [ ] Write a few unit tests
- [ ] Test the installation and add info here