import pytest
import os

from raglab_techdocs.data_preprocessing.preprocess_utils import PreprocessUtils


class TestIsSupportedFile:
    def test_txt_is_supported(self, tmp_path):
        f = tmp_path / "doc.txt"
        f.write_text("content")
        pu = PreprocessUtils(str(f))
        assert pu._is_supported_file() is True

    def test_md_is_supported(self, tmp_path):
        f = tmp_path / "doc.md"
        f.write_text("content")
        pu = PreprocessUtils(str(f))
        assert pu._is_supported_file() is True

    def test_pdf_is_not_supported(self, tmp_path):
        f = tmp_path / "doc.pdf"
        f.write_bytes(b"%PDF-1.4")
        pu = PreprocessUtils(str(f))
        assert pu._is_supported_file() is False

    def test_no_extension_is_not_supported(self, tmp_path):
        f = tmp_path / "README"
        f.write_text("content")
        pu = PreprocessUtils(str(f))
        assert pu._is_supported_file() is False


class TestGetOutputPath:
    def test_output_path_uses_filename(self, tmp_path):
        f = tmp_path / "notes.txt"
        f.write_text("hi")
        out_dir = str(tmp_path / "out")
        pu = PreprocessUtils(str(f), output_dir=out_dir)
        expected = os.path.join(out_dir, "notes.txt")
        assert pu._get_output_path() == expected

    def test_output_path_unsupported_raises(self, tmp_path):
        f = tmp_path / "file.pdf"
        f.write_bytes(b"%PDF")
        pu = PreprocessUtils(str(f))
        with pytest.raises(ValueError, match="Unsupported file type"):
            pu._get_output_path()


class TestNormalizeText:
    def test_lowercases_content(self, tmp_path):
        f = tmp_path / "doc.txt"
        f.write_text("Hello WORLD")
        out_dir = tmp_path / "out"
        pu = PreprocessUtils(str(f), output_dir=str(out_dir))
        pu.normalize_text()
        assert pu.loaded_document == "hello world"

    def test_collapses_whitespace(self, tmp_path):
        f = tmp_path / "doc.txt"
        f.write_text("foo   \n\n  bar\t\tbaz")
        out_dir = tmp_path / "out"
        pu = PreprocessUtils(str(f), output_dir=str(out_dir))
        pu.normalize_text()
        assert pu.loaded_document == "foo bar baz"

    def test_empty_file_produces_empty_string(self, tmp_path):
        f = tmp_path / "empty.txt"
        f.write_text("")
        out_dir = tmp_path / "out"
        pu = PreprocessUtils(str(f), output_dir=str(out_dir))
        pu.normalize_text()
        assert pu.loaded_document == ""

    def test_md_file_is_normalized(self, tmp_path):
        f = tmp_path / "doc.md"
        f.write_text("# Title\n\nSome   Content")
        out_dir = tmp_path / "out"
        pu = PreprocessUtils(str(f), output_dir=str(out_dir))
        pu.normalize_text()
        assert pu.loaded_document == "# title some content"

    def test_nonexistent_file_raises(self, tmp_path):
        pu = PreprocessUtils(str(tmp_path / "missing.txt"), output_dir=str(tmp_path / "out"))
        with pytest.raises(FileNotFoundError):
            pu.normalize_text()


class TestSaveDocument:
    def test_saves_to_output_dir(self, tmp_path):
        f = tmp_path / "input.txt"
        f.write_text("hello world")
        out_dir = tmp_path / "processed"
        pu = PreprocessUtils(str(f), output_dir=str(out_dir))
        pu.loaded_document = "hello world"
        out_path = pu.save_document()
        assert os.path.exists(out_path)
        assert open(out_path).read() == "hello world"

    def test_creates_output_dir_if_missing(self, tmp_path):
        f = tmp_path / "input.txt"
        f.write_text("data")
        out_dir = tmp_path / "nested" / "output"
        pu = PreprocessUtils(str(f), output_dir=str(out_dir))
        pu.loaded_document = "data"
        pu.save_document()
        assert out_dir.exists()

    def test_returns_correct_output_path(self, tmp_path):
        f = tmp_path / "report.txt"
        f.write_text("text")
        out_dir = tmp_path / "out"
        pu = PreprocessUtils(str(f), output_dir=str(out_dir))
        pu.loaded_document = "text"
        result = pu.save_document()
        assert result == str(out_dir / "report.txt")

    def test_overwrites_existing_file(self, tmp_path):
        f = tmp_path / "doc.txt"
        f.write_text("original")
        out_dir = tmp_path / "out"
        out_dir.mkdir()
        (out_dir / "doc.txt").write_text("old content")
        pu = PreprocessUtils(str(f), output_dir=str(out_dir))
        pu.loaded_document = "new content"
        pu.save_document()
        assert (out_dir / "doc.txt").read_text() == "new content"


class TestNormalizeTextEndToEnd:
    def test_full_pipeline_txt(self, tmp_path):
        f = tmp_path / "notes.txt"
        f.write_text("This   IS a TEST.\nWith  newlines.")
        out_dir = tmp_path / "out"
        pu = PreprocessUtils(str(f), output_dir=str(out_dir))
        out_path = pu.normalize_text()
        saved = open(out_path).read()
        assert saved == "this is a test. with newlines."

    def test_full_pipeline_md(self, tmp_path):
        f = tmp_path / "notes.md"
        f.write_text("## Header\n\nParagraph   text.")
        out_dir = tmp_path / "out"
        pu = PreprocessUtils(str(f), output_dir=str(out_dir))
        out_path = pu.normalize_text()
        assert os.path.isfile(out_path)
        assert open(out_path).read() == "## header paragraph text."
