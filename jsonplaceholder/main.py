import jsonplaceholder.cmd.albums as albums
import jsonplaceholder.cmd.comments as comments
import jsonplaceholder.cmd.photos as photos
import jsonplaceholder.cmd.posts as posts
import jsonplaceholder.cmd.todos as todos
import jsonplaceholder.cmd.users as users
import typer

app = typer.Typer()
app.add_typer(albums.app, name='albums', help='Manage albums')
app.add_typer(comments.app, name='comments', help='Manage comments')
app.add_typer(photos.app, name='photos', help='Manage photos')
app.add_typer(posts.app, name='posts', help='Manage posts')
app.add_typer(todos.app, name='todos', help='Manage todos')
app.add_typer(users.app, name='users', help='Manage users')


@app.callback()
def main():
    """
    Command Line Interface for https://jsonplaceholder.typicode.com .
    """


if __name__ == "__main__":
    app()
