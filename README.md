# Markdown Publisher
This is a small tool to render markdown (`.md`) files into websites that can be hosted online.
Use it for easily publishing your digital journals or project ideas.

## Installation
To install this package from GitHub, simply run the following:
```bash
pip install -e git+https://github.com/alugocp/publisher
```

## Usage
Here is how you run this tool:
```bash
python -m publisher <src> <dst> [style]
```
This command will recursively convert markdown (`.md`) files from an input directory into a presentable website in an output directory.
The parameters `src` and `dst` are the input and output directories, respectively.
The optional parameter `style` will select resulting website's stylesheet.
You can pass in a filepath (relative to your `src`) or choose from one of the various built-in stylesheets.
The stylesheet defaults to `charcoal` if none is provided from the command line.

## Development
These commands are to be run from within this directory for development purposes:
- `python -m pip install -r requirements.txt` - Install dependencies
- `python -m pylint ./*.py` - Lints the code
- `python __main__.py` - Runs the tool
- `python test.py` - Runs unit tests
