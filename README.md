# pdfgo

[![CI](https://github.com/charleslaw/pdfgo/actions/workflows/ci.yml/badge.svg)](https://github.com/charleslaw/pdfgo/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](pyproject.toml)
[![Version](https://img.shields.io/badge/version-0.3.0-informational.svg)](pyproject.toml)

A simple python package for editing pdfs via command line. A light wrapper around [pypdf](https://github.com/py-pdf/pypdf).

## Installation

Since pdfgo is a command-line tool, we recommend installing it with [pipx](https://pipx.pypa.io/):

```bash
pipx install pdfgo
```

### From source

To install from source, use [uv](https://github.com/astral-sh/uv):

```bash
git clone https://github.com/charleslaw/pdfgo.git
cd pdfgo
uv tool install .
```

## Updating

```bash
pipx upgrade pdfgo
```

If you installed from source with `uv tool install .`, pull the latest changes and reinstall:

```bash
git pull
uv tool install --force .
```

## Usage

```bash
pdfgo --version
pdfgo merge output.pdf input1.pdf input2.pdf
```

## Development

This project uses [uv](https://github.com/astral-sh/uv) for dependency management.

```bash
uv sync
uv run pytest
```
