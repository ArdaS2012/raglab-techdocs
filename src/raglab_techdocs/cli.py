import typer
from rich.console import Console
from raglab_techdocs.data_preprocessing.preprocess_utils import PreprocessUtils

app = typer.Typer()
console = Console()


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

@app.command()
def question(query: str):
    #TODO: implement question function
    console.print(f"questioning data placeholder: {query}")

@app.command()
def chunk(path: str):
    #TODO: implement chunk function
    console.print(f"chunking data placeholder: {path}")

@app.command()
def run():
    #TODO: implement run function
    console.print("running raglab placeholder")

@app.command()
def info():
    console.print("raglab-techdocs: a RAG pipeline for technical documentation")