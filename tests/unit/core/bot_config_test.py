#pylint: disable=C0111,protected-access, unused-import,
import pytest
from catcher_bot.core import bot_configurator
from tests.conftest import WORKING_FOLDER, CONFIG_BOT_FN


def test__load_bot_config():
    bot_cfg: dict = bot_configurator._load_bot_config(CONFIG_BOT_FN, WORKING_FOLDER)
    assert isinstance(bot_cfg, dict)
    assert 'config_type' in bot_cfg
    assert bot_cfg['config_type'] == 'bot'


def test___check_loaded_bot_config():
    bot_configurator._check_loaded_bot_config({'config_type': 'bot'})
    with pytest.raises(TypeError):
        bot_configurator._check_loaded_bot_config([{'config_type': 'bot'}])
    with pytest.raises(KeyError):
        bot_configurator._check_loaded_bot_config({'config_type_wrong': 'bot'})
    with pytest.raises(ValueError):
        bot_configurator._check_loaded_bot_config({'config_type': 'strategy'})


def test__verify_config_wrong_path(bot_config):
    bot_cfg = bot_config
    del bot_cfg['path']
    with pytest.raises(KeyError):
        bot_configurator._verify_config(bot_cfg)
    with pytest.raises(TypeError):
        bot_cfg['path'] = [{'config': './config'}]
        bot_configurator._verify_config(bot_cfg)
    with pytest.raises(KeyError):
        bot_cfg['path'] = {'wrong_config': './config'}
        bot_configurator._verify_config(bot_cfg)
    bot_cfg['path'] = {'config': './config'}
    bot_configurator._verify_config(bot_cfg)


def test___verify_config___working_dir(bot_config):
    bot_cfg = bot_config.copy()
    bot_configurator._verify_config(bot_cfg)
    with pytest.raises(KeyError):
        del bot_cfg['__working_dir']
        bot_configurator._verify_config(bot_cfg)
    with pytest.raises(FileExistsError):
        bot_cfg['__working_dir'] = '_is_not_exist_folder'
        bot_configurator._verify_config(bot_cfg)
