"""pdfgo: a light command-line wrapper around pypdf."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from pypdf.errors import PyPdfError

from pdfgo import __version__


class PdfGoError(Exception):
    """A user-facing error with a clear, non-traceback message."""


def _require_pdf(path: str) -> None:
    if not Path(path).is_file():
        raise PdfGoError(f"file not found: {path}")


def _write_pdf(writer: PdfWriter, output: str) -> None:
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    with open(output, "wb") as f:
        writer.write(f)


def parse_page_ranges(spec: str, num_pages: int) -> list[int]:
    """Parse a 1-indexed, comma-separated page range spec (e.g. "1-3,5,7-last")
    into a list of 0-indexed page numbers. "last" refers to the final page."""

    def parse_token(token: str) -> int:
        token = token.strip()
        return num_pages if token == "last" else int(token)

    pages: list[int] = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start, end = part.split("-", 1)
            start_i, end_i = parse_token(start), parse_token(end)
        else:
            start_i = end_i = parse_token(part)
        if start_i < 1 or end_i > num_pages or start_i > end_i:
            raise ValueError(f"invalid page range '{part}' for a {num_pages}-page document")
        pages.extend(range(start_i - 1, end_i))
    return pages


def merge(inputs: list[str], output: str) -> None:
    writer = PdfWriter()
    for pdf_path in inputs:
        _require_pdf(pdf_path)
        try:
            # Give each source file its own top-level outline entry. pypdf
            # imports the source outline beneath this entry, preserving its
            # existing bookmark hierarchy.
            writer.append(pdf_path, outline_item=Path(pdf_path).name)
        except PyPdfError as exc:
            raise PdfGoError(f"'{pdf_path}' is not a valid PDF") from exc
    _write_pdf(writer, output)


def split(input_path: str, output_dir: str) -> None:
    _require_pdf(input_path)
    try:
        reader = PdfReader(input_path)
    except PyPdfError as exc:
        raise PdfGoError(f"'{input_path}' is not a valid PDF") from exc
    stem = Path(input_path).stem
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    digits = len(str(len(reader.pages)))
    for i, page in enumerate(reader.pages):
        writer = PdfWriter()
        writer.add_page(page)
        out_path = out_dir / f"{stem}_{i + 1:0{digits}d}.pdf"
        with open(out_path, "wb") as f:
            writer.write(f)


def extract(input_path: str, pages: str, output: str) -> None:
    _require_pdf(input_path)
    try:
        reader = PdfReader(input_path)
    except PyPdfError as exc:
        raise PdfGoError(f"'{input_path}' is not a valid PDF") from exc
    page_indices = parse_page_ranges(pages, len(reader.pages))
    writer = PdfWriter()
    for i in page_indices:
        writer.add_page(reader.pages[i])
    _write_pdf(writer, output)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pdfgo",
        description="A light wrapper around pypdf for editing PDFs from the command line.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    subparsers = parser.add_subparsers(dest="command", required=True)

    merge_parser = subparsers.add_parser("merge", help="Merge multiple PDFs into one.")
    merge_parser.add_argument("inputs", nargs="+", help="PDF files to merge, in order.")
    merge_parser.add_argument("-o", "--output", required=True, help="Path to write the merged PDF to.")

    split_parser = subparsers.add_parser("split", help="Split a PDF into one file per page.")
    split_parser.add_argument("input", help="PDF file to split.")
    split_parser.add_argument(
        "-d", "--output-dir", required=True, help="Directory to write the split pages to."
    )

    extract_parser = subparsers.add_parser("extract", help="Extract a page range into a new PDF.")
    extract_parser.add_argument("input", help="PDF file to extract pages from.")
    extract_parser.add_argument(
        "pages", help="1-indexed page range(s) to extract, e.g. '1-3,5,7-last'."
    )
    extract_parser.add_argument("-o", "--output", required=True, help="Path to write the extracted PDF to.")

    return parser


def dispatch(args: argparse.Namespace) -> None:
    if args.command == "merge":
        merge(args.inputs, args.output)
    elif args.command == "split":
        split(args.input, args.output_dir)
    elif args.command == "extract":
        extract(args.input, args.pages, args.output)


_MENU_COMMANDS = ["merge", "split", "extract"]


def _prompt(label: str) -> str:
    return input(f"{label}: ").strip()


def run_interactive_menu() -> None:
    print("pdfgo - interactive mode")
    for i, name in enumerate(_MENU_COMMANDS, start=1):
        print(f"  {i}) {name}")
    choice = _prompt("Choose a command (number)")
    try:
        command = _MENU_COMMANDS[int(choice) - 1]
    except (ValueError, IndexError):
        print(f"Unknown option: {choice}")
        return

    if command == "merge":
        inputs = [p.strip() for p in _prompt("Input PDFs (comma-separated)").split(",") if p.strip()]
        output = _prompt("Output path")
        merge(inputs, output)
    elif command == "split":
        input_path = _prompt("Input PDF")
        output_dir = _prompt("Output directory")
        split(input_path, output_dir)
    elif command == "extract":
        input_path = _prompt("Input PDF")
        pages = _prompt("Pages to extract (e.g. 1-3,5,7-last)")
        output = _prompt("Output path")
        extract(input_path, pages, output)

    print("Done.")


def main(argv: list[str] | None = None) -> None:
    argv = sys.argv[1:] if argv is None else argv
    try:
        if not argv:
            run_interactive_menu()
            return

        parser = build_parser()
        args = parser.parse_args(argv)
        dispatch(args)
    except PdfGoError as exc:
        print(f"pdfgo: error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
