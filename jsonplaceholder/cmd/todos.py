import typer

app = typer.Typer()


@app.command()
def main():
    typer.echo("Todos")


if __name__ == '__main__':
    app()
