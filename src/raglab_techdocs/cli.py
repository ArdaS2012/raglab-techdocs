import typer
from rich.console import Console

app = typer.Typer()
console = Console()


@app.command()
def ingest(path: str):
    #TODO: implement ingest function
    console.print(f"ingesting data placeholder: {path}")

@app.command()
def query(query: str):
    #TODO: implement query function
    console.print(f"querying data placeholder: {query}")

@app.command()
def chunk(path: str):
    #TODO: implement chunk function
    console.print(f"chunking data placeholder: {path}")

@app.command()
def run():
    #TODO: implement run function
    console.print("running raglab placeholder")