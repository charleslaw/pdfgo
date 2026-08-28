"""pdfgo: a light command-line wrapper around pypdf."""

from __future__ import annotations

import argparse
from pathlib import Path

from pypdf import PdfWriter

from pdfgo import __version__


def merge(output: str, inputs: list[str]) -> None:
    writer = PdfWriter()
    for pdf_path in inputs:
        writer.append(pdf_path)
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    with open(output, "wb") as f:
        writer.write(f)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pdfgo",
        description="A light wrapper around pypdf for editing PDFs from the command line.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    subparsers = parser.add_subparsers(dest="command", required=True)

    merge_parser = subparsers.add_parser("merge", help="Merge multiple PDFs into one.")
    merge_parser.add_argument("output", help="Path to write the merged PDF to.")
    merge_parser.add_argument("inputs", nargs="+", help="PDF files to merge, in order.")

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "merge":
        merge(args.output, args.inputs)


if __name__ == "__main__":
    main()
