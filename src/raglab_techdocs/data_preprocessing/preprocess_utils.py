
import os

class PreprocessUtils:
        """Utility class for preprocessing text files. Such as loading, normalizing, and saving processed documents."""
        
        SUPPORTED_EXTENSIONS = [".md", ".txt"]

        def __init__(self, path: str, output_dir: str | None = None):
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
            if self.output_dir is None:
                raise ValueError("output_dir must be set before saving.")
            file_name = os.path.basename(self.path)
            return os.path.join(self.output_dir, file_name)

        def save_document(self):
            """Save the loaded document to a file in data/processed/ with a filename."""
            output_path = self._get_output_path()
            os.makedirs(self.output_dir, exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as file:
                file.write(self.loaded_document)
            return output_path

        def normalize_text(self) -> str:
            """Load a .txt or .md file, normalize its content, and return the normalized string.
            
            Call save_document() afterwards to optionally persist the result to disk.
            """
            if not self._is_supported_file():
                raise ValueError("Unsupported file type. Only .md and .txt are supported.")
            with open(self.path, "r", encoding="utf-8") as file:
                text = file.read()
            processed_text = " ".join(text.lower().split())
            self.loaded_document = processed_text
            return self.loaded_document