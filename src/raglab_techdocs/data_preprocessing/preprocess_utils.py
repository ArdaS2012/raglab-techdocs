
class PreprocessUtils:
        """Utility class for preprocessing text files. Such as loading, normalizing, and saving processed documents."""

        def __init__(self, path: str):
            self.path = path
            self.loaded_document = ""

        def save_document(self):
            """Save the loaded document to a file in data/processed/ with a unique filename."""
            file_name = self.path.split("/")[-1]
            if self.path.endswith(".md"):
                 output_path = f"data/processed/plain_text/{file_name}"
            elif self.path.endswith(".txt"):
                output_path = f"data/processed/plain_text/{file_name}"
            elif self.path.endswith(".pdf"):
                output_path = f"data/processed/plain_text/{file_name}"
            else:
                raise ValueError("Unsupported file type. Only .md, .txt, and .pdf are supported.")
            with open(output_path, "w", encoding="utf-8") as file:
                file.write(self.loaded_document)

        def normalize_text(self):
            """Preprocess a md or txt file by reading its contents
            and normalizing. The processed text is saved in data/processed/ with the same filename."""
            with open(self.path, "r", encoding="utf-8") as file:
                text = file.read()
            # Normalize the text (e.g., convert to lowercase, remove extra whitespace)
            processed_text = " ".join(text.lower().split())
            self.loaded_document = processed_text
            
            # Save the processed text
            self.save_document()


if __name__ == "__main__":
    # Example usage
    processor = PreprocessUtils("data/raw/plain_text/example.txt")
    processor.normalize_text()