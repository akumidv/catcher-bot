#!/bin/bash

echo "Running tests"
cd ..
echo `pwd`
pytest --cov=catcher_bot --cov-config=.coveragerc tests/