#!/bin/bash


cd ../
xgettext -d base -k --keyword=_i18n -o src/catcher_bot/locales/core.pot src/catcher_bot/*.py
