#!/bin/bash
python -m nuitka \
        --standalone \
        --onefile \
        --remove-output \
        --nofollow-import-to=pytest \
        --python-flag=nosite,-O \
        --plugin-enable=anti-bloat,implicit-imports,data-files,pylint-warnings,tk-inter \
        --warn-implicit-exceptions \
        --warn-unusual-code \
        --prefer-source-code \
        data_entry/main.py
