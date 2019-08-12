rem must install nuitka in a venv
@echo off
python -m nuitka --remove-output --windows-disable-console --follow-imports --plugin-enable=tk-inter .\data_entry\main.py