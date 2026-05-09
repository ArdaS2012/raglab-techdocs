import uuid

class Chunk:
    def __init__(self,
                 chunk_data: str,
                 chunk_index: int | None = None,
                 source_filename: str | None = None):
        
        self.chunk_data = chunk_data
        
        self.metadata = {
            "chunk_index": chunk_index,
            "source_filename": source_filename,
            "chunk_id": str(uuid.uuid4())
    
        }

class ChunkingStrategies:
    def __init__(self, chunk_strategy: str = "character",
                 chunk_size: int = 1000,
                 overlap: int = 200,
                 source_filename: str | None = None):
        
        self.chunk_strategy = chunk_strategy  # For now, we only implement character-based chunking. Future: add support for sentence and semantic chunking.
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.chunk_counter = 0
        self.source_filename = source_filename
        self.chunked_data = []

    def _chunk_character(self, text: str, drop_small_tail: bool = False) -> list[str]:
        """Chunk the input text into smaller pieces based on the specified chunk size and overlap."""
        start = 0
        while start < len(text):
            # In paragraph mode, skip a trailing tail fully covered by overlap.
            if drop_small_tail and start > 0 and (len(text) - start) <= self.overlap:
                break

            end = min(start + self.chunk_size, len(text))
            chunk = Chunk(text[start:end], chunk_index=self.chunk_counter, source_filename=self.source_filename)
            self.chunked_data.append(chunk)

            start += self.chunk_size - self.overlap
            self.chunk_counter += 1
        return self.chunked_data
    
    def _chunk_paragraph(self, text: str) -> list[str]:
        """Chunk the input text into paragraphs."""
        #TODO: For PDFs get start page and end page of chunk and add to metadata for better traceability
        for para in text.split("\n\n"):
            if not para.strip():
                continue
            if len(para.strip()) <= self.chunk_size:
                chunk = Chunk(para.strip(), chunk_index=self.chunk_counter, source_filename=self.source_filename)
                self.chunked_data.append(chunk)
                self.chunk_counter += 1
            else:
                self._chunk_character(para.strip(), drop_small_tail=True)

        return self.chunked_data
    
    def chunk_data(self, text: str) -> list[str]:
        """Choose the chunking strategy based on the chunk_strategy attribute."""
        #Reset chunked data and counter in case the same instance is used to chunk multiple documents
        self.chunked_data = []
        self.chunk_counter = 0

        if self.chunk_strategy == "character":
            return self._chunk_character(text)
        elif self.chunk_strategy == "paragraph":
            return self._chunk_paragraph(text)
        else:
            raise ValueError(f"Unsupported chunking strategy: {self.chunk_strategy}")