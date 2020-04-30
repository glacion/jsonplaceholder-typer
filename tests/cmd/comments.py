import jsonplaceholder.cmd.comments as comments
import typer.testing as test

runner = test.CliRunner()


def test_app():
    result = runner.invoke(comments.app, [])
    assert result.exit_code == 0
    assert 'Usage: ' in result.output


def test_help():
    result = runner.invoke(comments.app, ['--help'])
    assert result.exit_code == 0
    assert 'Usage: ' in result.output


def test_list():
    result = runner.invoke(comments.app, ['list'])
    assert result.exit_code == 0


def test_list_extra_args():
    result = runner.invoke(comments.app, ['list', 'asadf'])
    assert result.exit_code == 2


def test_list_postid():
    result = runner.invoke(comments.app, ['list', '--postid', '1'])
    assert result.exit_code == 0
    assert len([line for line in result.output.splitlines()
                if line.startswith('id=')]) == 5


def test_list_out_of_range_postid():
    result = runner.invoke(comments.app, ['list', '--postid', '0'])
    assert result.exit_code == 2
    assert 'Error: Invalid value for \'--postid\':' in result.output


def test_create_missing_postid():
    result = runner.invoke(comments.app, ['create'])
    assert result.exit_code == 2
    assert 'Error: Missing option \'--postid\'' in result.output


def test_create_out_of_range_postid():
    result = runner.invoke(
        comments.app, ['create', '--postid', '0', '--name', 'test', '--email', 'test@example.com', '--body', 'test'])
    assert result.exit_code == 2
    assert 'Error: Invalid value for \'--postid\':' in result.output


def test_create_missing_name():
    result = runner.invoke(comments.app, [
                           'create', '--postid', '1', '--email', 'test@example.com', '--body', 'test'])
    assert result.exit_code == 2
    assert 'Error: Missing option \'--name\'' in result.output


def test_create_successfully():
    result = runner.invoke(
        comments.app, ['create', '--postid', '1', '--name', 'test', '--email', 'test@example.com', '--body', 'test'])
    assert result.exit_code == 0
    assert 'id=501, postId=1, name=test, email=test@example.com, body=test' in result.output


def test_get_no_id():
    result = runner.invoke(comments.app, ['get'])
    assert result.exit_code == 2
    assert 'Error: Missing argument \'ID\'.' in result.output


def test_get_successfully():
    result = runner.invoke(comments.app, ['get', '1'])
    assert result.exit_code == 0
    assert 'id=1, postId=1, name=id labore ex et quam laborum, email=Eliseo@gardner.biz, body=laudantium enim quasi est quidem magnam voluptate ipsam eos\ntempora quo necessitatibus\ndolor quam autem quasi\nreiciendis et nam sapiente accusantium' \
        in result.output


def test_get_incorrect_id():
    result = runner.invoke(comments.app, ['get', '12345'])
    assert result.exit_code == 127
    assert 'Failure to retrieve resource.' in result.output


def test_get_out_of_range_id():
    result = runner.invoke(comments.app, ['get', '0'])
    assert result.exit_code == 2
    assert 'Error: Invalid value for \'ID\':' in result.output


def test_update_incorrect_id():
    result = runner.invoke(comments.app, ['update', '12345'])
    assert result.exit_code == 127
    assert 'Failure to retrieve resource.' in result.output


def test_update_no_change():
    result = runner.invoke(comments.app, ['update', '1'])
    assert result.exit_code == 0
    assert 'id=1, postId=1, name=id labore ex et quam laborum, email=Eliseo@gardner.biz, body=laudantium enim quasi est quidem magnam voluptate ipsam eos\ntempora quo necessitatibus\ndolor quam autem quasi\nreiciendis et nam sapiente accusantium' \
        in result.output


def test_update_change_single():
    result = runner.invoke(comments.app, ['update', '1', '--body', 'test'])
    assert result.exit_code == 0
    assert 'id=1, postId=1, name=id labore ex et quam laborum, email=Eliseo@gardner.biz, body=test' in result.output


def test_update_change_double():
    result = runner.invoke(
        comments.app, ['update', '1', '--name', 'test', '--body', 'test'])
    assert result.exit_code == 0
    assert 'id=1, postId=1, name=test, email=Eliseo@gardner.biz, body=test' in result.output


def test_update_change_all():
    result = runner.invoke(
        comments.app, ['update', '1', '--postid', '42', '--name', 'test', '--email', 'test@example.com', '--body', 'test'])
    assert result.exit_code == 0
    assert 'id=1, postId=42, name=test, email=test@example.com, body=test' in result.output


def test_update_out_of_range_id():
    result = runner.invoke(comments.app, ['update', '0'])
    assert result.exit_code == 2
    assert 'Error: Invalid value for \'ID\':' in result.output


def test_delete_successfully():
    result = runner.invoke(comments.app, ['delete', '12345'])
    assert result.exit_code == 0
    assert 'Resource deleted successfully.' in result.output


def test_delete_out_of_range_id():
    result = runner.invoke(comments.app, ['delete', '0'])
    assert result.exit_code == 2
    assert 'Error: Invalid value for \'ID\':' in result.output
