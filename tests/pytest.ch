#!/bin/bash

echo "Running tests"
cd ..
echo `pwd`
pytest --cov=catcher_bot --cov-config=.coveragerc -s -o log_cli=true  -o log_cli_level=DEBUG tests/