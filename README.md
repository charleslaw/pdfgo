# pdfgo

[![CI](https://github.com/charleslaw/pdfgo/actions/workflows/ci.yml/badge.svg)](https://github.com/charleslaw/pdfgo/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](pyproject.toml)
[![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](pyproject.toml)

A simple python package for editing pdfs via command line. A light wrapper around [pypdf](https://github.com/py-pdf/pypdf).

## Installation

```bash
uv pip install pdfgo
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
