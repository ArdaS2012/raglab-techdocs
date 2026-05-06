
import pathlib
import os

class PreprocessUtils:
        """Utility class for preprocessing text files. Such as loading, normalizing, and saving processed documents."""

        def __init__(self, path: str, output_dir: str = "data/processed/plain_text/"):
            self.SUPPORTED_EXTENSIONS = [".md", ".txt"]
            self.path = path
            self.output_dir = output_dir
            self.loaded_document = ""

        def _is_supported_file(self):
            """Check if the file has a supported extension."""
            return self.path.endswith(tuple(self.SUPPORTED_EXTENSIONS))
        
        def _get_output_path(self):
            """Generate the output path based on the input file name."""
            if not self._is_supported_file():
                raise ValueError("Unsupported file type. Only .md and .txt are supported.")
            file_name = os.path.basename(self.path)
            return os.path.join(self.output_dir, file_name)

        def save_document(self):
            """Save the loaded document to a file in data/processed/ with a unique filename."""
            output_path = self._get_output_path()
            os.makedirs(self.output_dir, exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as file:
                file.write(self.loaded_document)
            return output_path

        def normalize_text(self):
            """Preprocess a md or txt file by reading its content, normalizing it, and saving the processed text."""
            with open(self.path, "r", encoding="utf-8") as file:
                text = file.read()
            # Normalize the text (e.g., convert to lowercase, remove extra whitespace)
            processed_text = " ".join(text.lower().split())
            self.loaded_document = processed_text
            
            # Save the processed text
            return self.save_document()