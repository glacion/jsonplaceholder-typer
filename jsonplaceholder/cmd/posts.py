import typer

app = typer.Typer()


@app.command()
def main():
    typer.echo("Posts")


if __name__ == '__main__':
    app()
