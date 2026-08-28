import subprocess
import sys

from pypdf import PdfWriter

from pdfgo import __version__
from pdfgo.cli import build_parser, extract, merge, parse_page_ranges, split


def make_pdf(path, num_pages=1):
    writer = PdfWriter()
    for _ in range(num_pages):
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

    merge([str(pdf_a), str(pdf_b)], str(output))

    assert output.exists()
    with open(output, "rb") as f:
        from pypdf import PdfReader

        reader = PdfReader(f)
        assert len(reader.pages) == 2


def test_split(tmp_path):
    pdf = make_pdf(tmp_path / "doc.pdf", num_pages=3)
    out_dir = tmp_path / "pages"

    split(str(pdf), str(out_dir))

    assert sorted(p.name for p in out_dir.iterdir()) == [
        "doc_1.pdf",
        "doc_2.pdf",
        "doc_3.pdf",
    ]


def test_parse_page_ranges():
    assert parse_page_ranges("1-3,5,7-9", num_pages=9) == [0, 1, 2, 4, 6, 7, 8]


def test_parse_page_ranges_last():
    assert parse_page_ranges("2-last", num_pages=5) == [1, 2, 3, 4]
    assert parse_page_ranges("last", num_pages=5) == [4]


def test_parse_page_ranges_out_of_bounds():
    try:
        parse_page_ranges("1-5", num_pages=3)
        assert False, "expected ValueError"
    except ValueError:
        pass


def test_extract(tmp_path):
    pdf = make_pdf(tmp_path / "doc.pdf", num_pages=5)
    output = tmp_path / "extracted.pdf"

    extract(str(pdf), "2-3,5", str(output))

    assert output.exists()
    from pypdf import PdfReader

    reader = PdfReader(str(output))
    assert len(reader.pages) == 3
