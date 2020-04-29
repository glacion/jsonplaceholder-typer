import cmd.albums
import cmd.comments
import cmd.photos
import cmd.posts
import cmd.todos
import cmd.users

import typer

app = typer.Typer()
app.add_typer(cmd.albums.app, name='albums', help='Manage albums')
app.add_typer(cmd.comments.app, name='comments', help='Manage comments')
app.add_typer(cmd.photos.app, name='photos', help='Manage photos')
app.add_typer(cmd.posts.app, name='posts', help='Manage posts')
app.add_typer(cmd.todos.app, name='todos', help='Manage todos')
app.add_typer(cmd.users.app, name='users', help='Manage users')


@app.callback()
def main():
    typer.echo(f"Main")


if __name__ == "__main__":
    app()
