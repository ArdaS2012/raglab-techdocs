import pytest
import os

from raglab_techdocs.data_preprocessing.preprocess_utils import PreprocessUtils
from raglab_techdocs.chunking_utils.chunking import ChunkingStrategies, Chunk


class TestChunkingStrategies:
    def test_chunk_character(self):
        text = "This is a test document to be chunked into smaller pieces."
        cs = ChunkingStrategies(chunk_strategy="character", chunk_size=10, overlap=2)
        chunks = cs.chunk_data(text)
        assert len(chunks) == 8
        assert chunks[0].chunk_data == "This is a "
        assert chunks[1].chunk_data == "a test doc"
        assert chunks[2].chunk_data == "ocument to"
        assert chunks[3].chunk_data == "to be chun"
        assert chunks[4].chunk_data == "unked into"
        assert chunks[5].chunk_data == "to smaller"
        assert chunks[6].chunk_data == "er pieces."
        assert chunks[7].chunk_data == "s."

    def test_chunk_paragraph(self):
        text = "Paragraph one.\n\nParagraph two is a bit longer than the first one.\n\nParagraph three."
        cs = ChunkingStrategies(chunk_strategy="paragraph", chunk_size=20, overlap=5)
        chunks = cs.chunk_data(text)
        assert len(chunks) == 5
        assert chunks[0].chunk_data == "Paragraph one."
        assert chunks[1].chunk_data == "Paragraph two is a b"
        assert chunks[2].chunk_data == "s a bit longer than "
        assert chunks[3].chunk_data == "than the first one."
        assert chunks[4].chunk_data == "Paragraph three."

    def test_empty_chunking(self):
        text = ""
        cs = ChunkingStrategies(chunk_strategy="character", chunk_size=10, overlap=2)
        chunks = cs.chunk_data(text)
        assert len(chunks) == 0

    def test_empty_chunking_paragraph(self):
        text = ""
        cs = ChunkingStrategies(chunk_strategy="paragraph", chunk_size=20, overlap=5)
        chunks = cs.chunk_data(text)
        assert len(chunks) == 0

    # --- character chunking edge cases ---

    def test_chunk_character_shorter_than_chunk_size(self):
        text = "Hello"
        cs = ChunkingStrategies(chunk_strategy="character", chunk_size=20, overlap=5)
        chunks = cs.chunk_data(text)
        assert len(chunks) == 1
        assert chunks[0].chunk_data == "Hello"

    def test_chunk_character_exact_chunk_size_no_overlap(self):
        text = "0123456789"
        cs = ChunkingStrategies(chunk_strategy="character", chunk_size=10, overlap=0)
        chunks = cs.chunk_data(text)
        assert len(chunks) == 1
        assert chunks[0].chunk_data == "0123456789"

    def test_chunk_character_no_overlap(self):
        text = "ABCDEFGHIJ"
        cs = ChunkingStrategies(chunk_strategy="character", chunk_size=3, overlap=0)
        chunks = cs.chunk_data(text)
        assert len(chunks) == 4
        assert chunks[0].chunk_data == "ABC"
        assert chunks[1].chunk_data == "DEF"
        assert chunks[2].chunk_data == "GHI"
        assert chunks[3].chunk_data == "J"
        for i in range(len(chunks) - 1):
            assert chunks[i].chunk_data[-1] != chunks[i + 1].chunk_data[0]

    def test_chunk_character_single_char_chunks(self):
        text = "ABC"
        cs = ChunkingStrategies(chunk_strategy="character", chunk_size=1, overlap=0)
        chunks = cs.chunk_data(text)
        assert len(chunks) == 3
        assert chunks[0].chunk_data == "A"
        assert chunks[1].chunk_data == "B"
        assert chunks[2].chunk_data == "C"

    # --- paragraph chunking edge cases ---

    def test_chunk_paragraph_all_fit(self):
        text = "Short.\n\nAlso short."
        cs = ChunkingStrategies(chunk_strategy="paragraph", chunk_size=50, overlap=5)
        chunks = cs.chunk_data(text)
        assert len(chunks) == 2
        assert chunks[0].chunk_data == "Short."
        assert chunks[1].chunk_data == "Also short."

    def test_chunk_paragraph_single_long_paragraph(self):
        text = "Paragraph two is a bit longer than the first one."
        cs = ChunkingStrategies(chunk_strategy="paragraph", chunk_size=20, overlap=5)
        chunks = cs.chunk_data(text)
        assert len(chunks) == 3
        assert chunks[0].chunk_data == "Paragraph two is a b"
        assert chunks[1].chunk_data == "s a bit longer than "
        assert chunks[2].chunk_data == "than the first one."

    def test_chunk_paragraph_whitespace_only_paragraphs(self):
        text = "\n\n   \n\n"
        cs = ChunkingStrategies(chunk_strategy="paragraph", chunk_size=20, overlap=5)
        chunks = cs.chunk_data(text)
        assert len(chunks) == 0

    def test_chunk_paragraph_multiple_blank_lines(self):
        text = "Hello\n\n\n\nWorld"
        cs = ChunkingStrategies(chunk_strategy="paragraph", chunk_size=20, overlap=5)
        chunks = cs.chunk_data(text)
        assert len(chunks) == 2
        assert chunks[0].chunk_data == "Hello"
        assert chunks[1].chunk_data == "World"

    # --- metadata correctness ---

    def test_chunk_index_sequential(self):
        text = "One.\n\nTwo.\n\nThree."
        cs = ChunkingStrategies(chunk_strategy="paragraph", chunk_size=20, overlap=5)
        chunks = cs.chunk_data(text)
        for i, chunk in enumerate(chunks):
            assert chunk.metadata["chunk_index"] == i

    def test_source_filename_propagated(self):
        text = "Hello world"
        cs = ChunkingStrategies(chunk_strategy="character", chunk_size=5, overlap=1, source_filename="test.txt")
        chunks = cs.chunk_data(text)
        assert len(chunks) > 0
        for chunk in chunks:
            assert chunk.metadata["source_filename"] == "test.txt"

    def test_chunk_id_unique(self):
        text = "One.\n\nTwo.\n\nThree."
        cs = ChunkingStrategies(chunk_strategy="paragraph", chunk_size=20, overlap=5)
        chunks = cs.chunk_data(text)
        chunk_ids = [c.metadata["chunk_id"] for c in chunks]
        assert len(set(chunk_ids)) == len(chunk_ids)

    # --- error handling ---

    def test_unsupported_strategy_raises(self):
        cs = ChunkingStrategies(chunk_strategy="invalid")
        with pytest.raises(ValueError):
            cs.chunk_data("some text")

    # --- stateful reset ---

    def test_chunk_data_called_twice_does_not_accumulate(self):
        text = "Hello world."
        cs = ChunkingStrategies(chunk_strategy="character", chunk_size=5, overlap=0)
        first = cs.chunk_data(text)
        first_len = len(first)
        second = cs.chunk_data(text)
        assert len(second) == first_len
