import typer

app = typer.Typer()


@app.command()
def list():
    """
    List all Albums.
    """
    typer.echo("Listing...")


@app.command()
def get(id: int):
    """
    Get info about album by ID.
    """
    typer.echo(f"Getting id {id}")


@app.callback()
def main():
    """
    Manage Albums
    """


if __name__ == '__main__':
    app()
