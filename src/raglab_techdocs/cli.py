import typer
from rich.console import Console
from raglab_techdocs.data_preprocessing.preprocess_utils import PreprocessUtils
from raglab_techdocs.chunking_utils.chunking import ChunkingStrategies
app = typer.Typer()
console = Console()
import os

@app.command()
def ingest(
    path: str,
    output_dir: str = typer.Option("data/processed/plain_text/", help="Output directory"),
    save_doc: bool = typer.Option(False, "--save-doc", help="Save normalized document to disk"),
):
    pu = PreprocessUtils(path, output_dir=output_dir if save_doc else None)
    content = pu.normalize_text()
    if save_doc:
        out_path = pu.save_document()
        console.print(f"Saved: {out_path}")
    else:
        console.print(content)
    #TODO: implement ingest function, currently only normalizes and optionally saves the document. Future: add support for ingesting into vector database.
    # Also add metadata of document to the db such as file name, original path, etc. for better traceability.
@app.command()
def question(query: str):
    #TODO: implement question function
    console.print(f"questioning data placeholder: {query}")

@app.command()
def chunk(path: str,
          chunk_size: int = typer.Option(1000, help="Chunk size in characters"),
          overlap: int = typer.Option(200, help="Overlap size in characters"),
          save_chunks: bool = typer.Option(False, "--save-chunks", help="Save chunks to disk"),
          chunk_strategy: str = typer.Option("character", "--chunk-strategy", help="Chunking strategy: character or paragraph")
):
    #TODO: test
    cs = ChunkingStrategies(chunk_strategy=chunk_strategy, chunk_size=chunk_size, overlap=overlap,source_filename=os.path.basename(path))
    text = PreprocessUtils(path).read_document()
    chunks = cs.chunk_data(text)
    if save_chunks:
        output_dir = "data/processed/chunks/"
        chunk_path = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(path))[0]}_{cs.chunk_strategy}_csize{chunk_size}_ov{overlap}.txt")
        os.makedirs(output_dir, exist_ok=True)
        with open(chunk_path, "w", encoding="utf-8") as file:
            for i, chunk in enumerate(chunks):
                    file.write(f"-----THIS IS CHUNK {i}-----\n{chunk.chunk_data}\n")
                    file.write(f"Metadata: {chunk.metadata}\n")
                    file.write(f"-----END OF CHUNK {i}-----\n\n")
            console.print(f"Saved: {chunk_path}")
    else:
        for chunk in chunks:
            console.print(f"Chunk Data: {chunk.chunk_data}")
            console.print(f"Metadata: {chunk.metadata}")

@app.command()
def run():
    #TODO: implement run function
    console.print("running raglab placeholder")

@app.command()
def info():
    console.print("raglab-techdocs: a RAG pipeline for technical documentation")
