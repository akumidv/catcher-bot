#pylint: disable=C0111,protected-access
import pytest
from catcher_bot.core import bot_config
from conftest import bot_cfg, WORKING_DIR, CONFIG_PATH


def test__load_bot_config():
    bot_cfg: dict = bot_config._load_bot_config(CONFIG_PATH, WORKING_DIR)
    assert isinstance(bot_cfg, dict)
    assert 'config_type' in bot_cfg
    assert bot_cfg['config_type'] == 'bot'


def test___check_loaded_bot_config():
    bot_config._check_loaded_bot_config({'config_type': 'bot'})
    with pytest.raises(TypeError):
        bot_config._check_loaded_bot_config([{'config_type': 'bot'}])
    with pytest.raises(KeyError):
        bot_config._check_loaded_bot_config({'config_type_wrong': 'bot'})
    with pytest.raises(ValueError):
        bot_config._check_loaded_bot_config({'config_type': 'strategy'})


def test__verify_config_wrong_path(bot_cfg):
    cfg = bot_cfg.copy()
    del cfg['path']
    with pytest.raises(KeyError):
        bot_config._verify_config(cfg)
    with pytest.raises(TypeError):
        cfg['path'] = [{'config': './config'}]
        bot_config._verify_config(cfg)
    with pytest.raises(KeyError):
        cfg['path'] = {'wrong_config': './config'}
        bot_config._verify_config(cfg)
    cfg['path'] = {'config': './config'}
    bot_config._verify_config(cfg)
