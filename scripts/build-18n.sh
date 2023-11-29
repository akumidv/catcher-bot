#!/bin/bash

# Fedora dnf install gettext-devel intltool
# Ubuntu sudo apt-get install gettext

cd ../
DOMAIN_FN_BASE="catcher_bot"

declare -a LANGUAGES=("en")

LOCALES_PATH="src/catcher_bot/locales"
#xgettext -d base -k --keyword=_i18n -o src/catcher_bot/locales/${DOMAIN_FN_BASE}.pot src/catcher_bot/*/*.py
xgettext -d base -o "${LOCALES_PATH}/${DOMAIN_FN_BASE}.pot" src/catcher_bot/*.py src/catcher_bot/*/*.py

for lang in ${LANGUAGES[@]}; do
  echo "Language: ${lang}"
  lang_path="${LOCALES_PATH}/${lang}/LC_MESSAGES"
  mkdir -p "${lang_path}"

  # TODO replaced po - should be changed to join!
  if ! [ -f "${lang_path}/${DOMAIN_FN_BASE}.po" ]; then
    msginit --no-translator -i src/catcher_bot/locales/${DOMAIN_FN_BASE}.pot --locale=${lang} -o "${lang_path}/${DOMAIN_FN_BASE}.po"
  else
    msgmerge "${lang_path}/${DOMAIN_FN_BASE}.po" src/catcher_bot/locales/${DOMAIN_FN_BASE}.pot -o "${lang_path}/${DOMAIN_FN_BASE}.po"
  fi
  msgfmt "${lang_path}/${DOMAIN_FN_BASE}.po" -o "${lang_path}/${DOMAIN_FN_BASE}.mo"
done

