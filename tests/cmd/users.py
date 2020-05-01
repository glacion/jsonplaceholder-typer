import jsonplaceholder.cmd.users as users
import typer.testing as test

runner = test.CliRunner()


def test_app():
    result = runner.invoke(users.app, [])
    assert result.exit_code == 0
    assert 'Usage: ' in result.output


def test_help():
    result = runner.invoke(users.app, ['--help'])
    assert result.exit_code == 0
    assert 'Usage: ' in result.output


def test_list():
    result = runner.invoke(users.app, ['list'])
    assert result.exit_code == 0


def test_list_extra_args():
    result = runner.invoke(users.app, ['list', 'asadf'])
    assert result.exit_code == 2


def test_create_missing_name():
    result = runner.invoke(users.app, ['create'])
    assert result.exit_code == 2
    assert 'Error: Missing option \'--name\'' in result.output


def test_create_successfully():
    result = runner.invoke(
        users.app, ['create',
                    '--name', 'Ahmetcan',
                    '--username', 'glacion',
                    '--email', 'ahm@glacion.com',
                    '--street', 'teststreet',
                    '--suite', 'testsuite',
                    '--city', 'testcity',
                    '--zipcode', 'testzipcode',
                    '--latitude', '45.0',
                    '--longitude', '90.0',
                    '--phone', 'testphone',
                    '--website', 'https://glacion.com',
                    '--company-name', 'testcompany',
                    '--catch-phrase', 'testcatchPhrase',
                    '--bs', 'testbs'])
    assert result.exit_code == 0
    assert 'id=11, name=Ahmetcan, username=glacion, email=ahm@glacion.com' in result.output


def test_get_no_id():
    result = runner.invoke(users.app, ['get'])
    assert result.exit_code == 2
    assert 'Error: Missing argument \'ID\'.' in result.output


def test_get_successfully():
    result = runner.invoke(users.app, ['get', '1'])
    assert result.exit_code == 0
    assert 'id=1, name=Leanne Graham' in result.output


def test_get_incorrect_id():
    result = runner.invoke(users.app, ['get', '12345'])
    assert result.exit_code == 127
    assert 'Failure to retrieve resource.' in result.output


def test_get_out_of_range_id():
    result = runner.invoke(users.app, ['get', '0'])
    assert result.exit_code == 2
    assert 'Error: Invalid value for \'ID\':' in result.output


def test_update_incorrect_id():
    result = runner.invoke(users.app, ['update', '12345'])
    assert result.exit_code == 127
    assert 'Failure to retrieve resource.' in result.output


def test_update_no_change():
    result = runner.invoke(users.app, ['update', '1'])
    assert result.exit_code == 0
    assert 'id=1, name=Leanne Graham' in result.output


def test_update_change_single():
    result = runner.invoke(users.app, ['update', '1', '--username', 'glacion'])
    assert result.exit_code == 0
    assert 'id=1, name=Leanne Graham, username=glacion' in result.output


def test_update_change_double():
    result = runner.invoke(
        users.app, ['update', '1', '--name', 'test', '--username', 'glacion'])
    assert result.exit_code == 0
    assert 'id=1, name=test, username=glacion' in result.output


def test_update_change_all():
    result = runner.invoke(
        users.app, ['update', '1',
                    '--name', 'Ahmetcan',
                    '--username', 'glacion',
                    '--email', 'ahm@glacion.com',
                    '--street', 'teststreet',
                    '--suite', 'testsuite',
                    '--city', 'testcity',
                    '--zipcode', 'testzipcode',
                    '--latitude', '45.0',
                    '--longitude', '90.0',
                    '--phone', 'testphone',
                    '--website', 'https://glacion.com',
                    '--company-name', 'testcompany',
                    '--catch-phrase', 'testcatchPhrase',
                    '--bs', 'testbs'])
    assert result.exit_code == 0
    for item in ('id=1',
                 'name=Ahmetcan',
                 'username=glacion',
                 'email=ahm@glacion.com',
                 'street=teststreet',
                 'suite=testsuite',
                 'city=testcity',
                 'zipcode=testzipcode',
                 'lat=45',
                 'lng=90',
                 'phone=testphone',
                 'website=https://glacion.com',
                 'Company=name=testcompany',
                 'catchPhrase=testcatchPhrase',
                 'bs=testbs'):
        assert item in result.output


def test_update_out_of_range_id():
    result = runner.invoke(users.app, ['update', '0'])
    assert result.exit_code == 2
    assert 'Error: Invalid value for \'ID\':' in result.output


def test_delete_successfully():
    result = runner.invoke(users.app, ['delete', '12345'])
    assert result.exit_code == 0
    assert 'Resource deleted successfully.' in result.output


def test_delete_out_of_range_id():
    result = runner.invoke(users.app, ['delete', '0'])
    assert result.exit_code == 2
    assert 'Error: Invalid value for \'ID\':' in result.output
