import jsonplaceholder.cmd.photos as photos
import typer.testing as test

runner = test.CliRunner()


def test_app():
    result = runner.invoke(photos.app, [])
    assert result.exit_code == 0
    assert 'Usage: ' in result.output


def test_help():
    result = runner.invoke(photos.app, ['--help'])
    assert result.exit_code == 0
    assert 'Usage: ' in result.output


def test_list():
    result = runner.invoke(photos.app, ['list'])
    assert result.exit_code == 0


def test_list_extra_args():
    result = runner.invoke(photos.app, ['list', 'asadf'])
    assert result.exit_code == 2


def test_list_albumid():
    result = runner.invoke(photos.app, ['list', '--albumid', '1'])
    assert result.exit_code == 0
    assert len([line for line in result.output.splitlines()
                if line.startswith('id=')]) == 50


def test_list_out_of_range_albumid():
    result = runner.invoke(photos.app, ['list', '--albumid', '0'])
    assert result.exit_code == 2
    assert 'Error: Invalid value for \'--albumid\':' in result.output


def test_create_missing_albumid():
    result = runner.invoke(photos.app, ['create'])
    assert result.exit_code == 2
    assert 'Error: Missing option \'--albumid\'' in result.output


def test_create_out_of_range_albumid():
    result = runner.invoke(
        photos.app, ['create', '--albumid', '0', '--title', 'https://example.com/thumbnailimage', '--url', 'https://example.com/image', '--thumbnailurl', 'https://example.com/thumbnailimage'])
    assert result.exit_code == 2
    assert 'Error: Invalid value for \'--albumid\':' in result.output


def test_create_missing_title():
    result = runner.invoke(photos.app, [
                           'create', '--albumid', '1', '--url', 'https://example.com/image', '--thumbnailurl', 'https://example.com/thumbnailimage'])
    assert result.exit_code == 2
    assert 'Error: Missing option \'--title\'' in result.output


def test_create_successfully():
    result = runner.invoke(
        photos.app, ['create', '--albumid', '1', '--title', 'test', '--url', 'https://example.com/image', '--thumbnailurl', 'https://example.com/thumbnailimage'])
    assert result.exit_code == 0
    assert 'id=5001, albumId=1, title=test, url=https://example.com/image, thumbnailUrl=https://example.com/thumbnailimage' in result.output


def test_get_no_id():
    result = runner.invoke(photos.app, ['get'])
    assert result.exit_code == 2
    assert 'Error: Missing argument \'ID\'.' in result.output


def test_get_successfully():
    result = runner.invoke(photos.app, ['get', '1'])
    assert result.exit_code == 0
    assert 'id=1, albumId=1, title=accusamus beatae ad facilis cum similique qui sunt, url=https://via.placeholder.com/600/92c952, thumbnailUrl=https://via.placeholder.com/150/92c952' \
        in result.output


def test_get_incorrect_id():
    result = runner.invoke(photos.app, ['get', '12345'])
    assert result.exit_code == 127
    assert 'Failure to retrieve resource.' in result.output


def test_get_out_of_range_id():
    result = runner.invoke(photos.app, ['get', '0'])
    assert result.exit_code == 2
    assert 'Error: Invalid value for \'ID\':' in result.output


def test_update_incorrect_id():
    result = runner.invoke(photos.app, ['update', '12345'])
    assert result.exit_code == 127
    assert 'Failure to retrieve resource.' in result.output


def test_update_no_change():
    result = runner.invoke(photos.app, ['update', '1'])
    assert result.exit_code == 0
    assert 'id=1, albumId=1, title=accusamus beatae ad facilis cum similique qui sunt, url=https://via.placeholder.com/600/92c952, thumbnailUrl=https://via.placeholder.com/150/92c952' \
        in result.output


def test_update_change_single():
    result = runner.invoke(photos.app, [
                           'update', '1', '--thumbnailurl', 'https://example.com/thumbnailimage'])
    assert result.exit_code == 0
    assert 'id=1, albumId=1, title=accusamus beatae ad facilis cum similique qui sunt, url=https://via.placeholder.com/600/92c952, thumbnailUrl=https://example.com/thumbnailimage' in result.output


def test_update_change_double():
    result = runner.invoke(
        photos.app, ['update', '1', '--title', 'test', '--thumbnailurl', 'https://example.com/thumbnailimage'])
    assert result.exit_code == 0
    assert 'id=1, albumId=1, title=test, url=https://via.placeholder.com/600/92c952, thumbnailUrl=https://example.com/thumbnailimage' in result.output


def test_update_change_all():
    result = runner.invoke(
        photos.app, ['update', '1', '--albumid', '42', '--title', 'test', '--url', 'https://example.com/image', '--thumbnailurl', 'https://example.com/thumbnailimage'])
    assert result.exit_code == 0
    assert 'id=1, albumId=42, title=test, url=https://example.com/image, thumbnailUrl=https://example.com/thumbnailimage' in result.output


def test_update_out_of_range_id():
    result = runner.invoke(photos.app, ['update', '0'])
    assert result.exit_code == 2
    assert 'Error: Invalid value for \'ID\':' in result.output


def test_delete_successfully():
    result = runner.invoke(photos.app, ['delete', '12345'])
    assert result.exit_code == 0
    assert 'Resource deleted successfully.' in result.output


def test_delete_out_of_range_id():
    result = runner.invoke(photos.app, ['delete', '0'])
    assert result.exit_code == 2
    assert 'Error: Invalid value for \'ID\':' in result.output
