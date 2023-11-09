#pylint: disable=C0111,protected-access
import pytest
import argparse

from catcher_bot.core import bot_config


config_example_base = {
    'path': {'config': 'configs_example'}
}


def test__verify_config_correct():
    bot_config._verify_config(config_example_base)


def test__verify_config_wrong_path():
    cfg = config_example_base.copy()
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


def test___get_bot_config_from_args():
    args=argparse.Namespace
    bot_cfg = bot_config._load_bot_config()