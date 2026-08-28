import subprocess
import sys

from pypdf import PdfWriter

from pdfgo import __version__
from pdfgo.cli import build_parser, merge


def make_pdf(path):
    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)
    with open(path, "wb") as f:
        writer.write(f)
    return path


def test_version():
    result = subprocess.run(
        [sys.executable, "-m", "pdfgo.cli", "--version"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert __version__ in result.stdout


def test_parser_requires_command():
    parser = build_parser()
    try:
        parser.parse_args([])
        assert False, "expected SystemExit"
    except SystemExit:
        pass


def test_merge(tmp_path):
    pdf_a = make_pdf(tmp_path / "a.pdf")
    pdf_b = make_pdf(tmp_path / "b.pdf")
    output = tmp_path / "merged.pdf"

    merge(str(output), [str(pdf_a), str(pdf_b)])

    assert output.exists()
    with open(output, "rb") as f:
        from pypdf import PdfReader

        reader = PdfReader(f)
        assert len(reader.pages) == 2
