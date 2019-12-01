#!/bin/sh
pycodestyle webotron/
pydocstyle webotron/
pyflakes webotron/
read -p "Press enter to continue"