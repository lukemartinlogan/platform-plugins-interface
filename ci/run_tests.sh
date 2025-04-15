#!/bin/bash
pip install coverage
pip install coverage-lcov
pip install pytest
coverage run -m pytest test
rm -rf "*.pyc"
coverage report
coverage-lcov
