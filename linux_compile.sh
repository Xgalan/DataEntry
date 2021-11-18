#!/bin/bash
python -m nuitka --remove-output --follow-imports --plugin-enable=tk-inter ./data_entry/__main__.py