from guruguru.constance import config


def test_write_and_read_config():
    data = {'token': 'nyknyknyk'}
    save_to = config.save(data)
    assert config.config_path == save_to
    assert config.exist_token

    loaded_data = config.load()
    assert data == loaded_data
    assert data == config.data

    assert config.get_token() == 'nyknyknyk'