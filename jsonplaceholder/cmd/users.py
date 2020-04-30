import typer

app = typer.Typer()
ENDPOINT = '/users'


def view_user(user: Dict[str, Union[int, str]]) -> str:
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
    Manage Users
    """


if __name__ == '__main__':
    app()
