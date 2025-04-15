#!/bin/bash
pip install coverage
pip install coverage-lcov
coverage run -m pytest test
rm -rf "*.pyc"
coverage report
coverage-lcov
