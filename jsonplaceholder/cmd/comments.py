from typing import Dict, Union

import typer

app = typer.Typer()
ENDPOINT = '/comments'


def view_comment(comment: Dict[str, Union[int, str]]) -> str:
    pass


@app.command
def list():
    pass


@app.command
def get():
    pass


@app.command
def delete():
    pass


@app.command
def update():
    pass


@app.command
def create():
    pass


@app.callback()
def main():
    """
    Manage Comments
    """


if __name__ == '__main__':
    app()
