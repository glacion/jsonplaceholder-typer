import typer

app = typer.Typer()


@app.command()
def main():
    typer.echo("Users")


if __name__ == '__main__':
    app()
