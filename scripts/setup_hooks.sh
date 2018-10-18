#!/usr/bin/env bash

cp scripts/commit-msg .git/hooks/
cp scripts/pre-commit .git/hooks/

chmod +x .git/hooks/commit-msg
chmod +x .git/hooks/pre-commit
