import typer


def panic(msg: str, exit_code: int = 127):
    typer.secho(
        msg, err=True, fg=typer.colors.BRIGHT_RED)
    raise typer.Exit(exit_code)
