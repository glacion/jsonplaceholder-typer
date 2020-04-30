import jsonplaceholder.cmd.albums as albums
import typer.testing as test

runner = test.CliRunner()


def test_app():
    result = runner.invoke(albums.app, [])
    assert result.exit_code == 0
    assert 'Usage: ' in result.output


def test_help():
    result = runner.invoke(albums.app, ['--help'])
    assert result.exit_code == 0
    assert 'Usage: ' in result.output


def test_list():
    result = runner.invoke(albums.app, ['list'])
    assert result.exit_code == 0


def test_list_extra_args():
    result = runner.invoke(albums.app, ['list', 'asadf'])
    assert result.exit_code == 2


def test_list_userid():
    result = runner.invoke(albums.app, ['list', '--userid', '1'])
    assert result.exit_code == 0
    assert len(result.output.splitlines()) == 11


def test_list_out_of_range_userid():
    result = runner.invoke(albums.app, ['list', '--userid', '0'])
    assert result.exit_code == 2
    assert 'Error: Invalid value for \'--userid\':' in result.output


def test_create_missing_userid():
    result = runner.invoke(albums.app, ['create'])
    assert result.exit_code == 2
    assert 'Error: Missing option \'--userid\'' in result.output


def test_create_out_of_range_userid():
    result = runner.invoke(
        albums.app, ['create', '--userid', '0', '--title', 'test'])
    assert result.exit_code == 2
    assert 'Error: Invalid value for \'--userid\':' in result.output


def test_create_missing_title():
    result = runner.invoke(albums.app, ['create', '--userid', '123'])
    assert result.exit_code == 2
    assert 'Error: Missing option \'--title\'' in result.output


def test_create_successfully():
    result = runner.invoke(
        albums.app, ['create', '--userid', '123', '--title', 'test'])
    assert result.exit_code == 0
    assert 'id=101, userId=123, title=test' in result.output


def test_get_without_id():
    result = runner.invoke(albums.app, ['get'])
    assert result.exit_code != 0
    assert 'Error: Missing argument \'ID\'.' in result.output


def test_get_correct_id():
    result = runner.invoke(albums.app, ['get', '1'])
    assert result.exit_code == 0
    assert 'id=1, userId=1, title=quidem molestiae enim' in result.output


def test_get_incorrect_id():
    result = runner.invoke(albums.app, ['get', '12345'])
    assert result.exit_code == 127
    assert 'Failure to retrieve resource.' in result.output


def test_get_out_of_range_id():
    result = runner.invoke(albums.app, ['get', '0'])
    assert result.exit_code == 2
    assert 'Error: Invalid value for \'ID\':' in result.output


def test_update_incorrect_id():
    result = runner.invoke(albums.app, ['update', '12345'])
    assert result.exit_code == 127
    assert 'Failure to retrieve resource.' in result.output


def test_update_no_change():
    result = runner.invoke(albums.app, ['update', '1'])
    assert result.exit_code == 0
    assert 'id=1, userId=1, title=quidem molestiae enim' in result.output


def test_update_change_title():
    result = runner.invoke(albums.app, ['update', '1', '--title', 'test'])
    assert result.exit_code == 0
    assert 'id=1, userId=1, title=test' in result.output


def test_update_change_userid():
    result = runner.invoke(albums.app, ['update', '1', '--userid', '42'])
    assert result.exit_code == 0
    assert 'id=1, userId=42, title=quidem molestiae enim' in result.output


def test_update_change_all():
    result = runner.invoke(
        albums.app, ['update', '1', '--title', 'test', '--userid', '42'])
    assert result.exit_code == 0
    assert 'id=1, userId=42, title=test' in result.output


def test_update_out_of_range_id():
    result = runner.invoke(albums.app, ['update', '0'])
    assert result.exit_code == 2
    assert 'Error: Invalid value for \'ID\':' in result.output


def test_delete():
    result = runner.invoke(albums.app, ['delete', '12345'])
    assert result.exit_code == 0
    assert 'Resource deleted successfully.' in result.output


def test_delete_out_of_range_id():
    result = runner.invoke(albums.app, ['delete', '0'])
    assert result.exit_code == 2
    assert 'Error: Invalid value for \'ID\':' in result.output
