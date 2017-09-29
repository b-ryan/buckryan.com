#!/bin/bash
set -e

DIR=.pelican.dev
if [[ -d $DIR ]]; then
    rm -r $DIR
fi
mkdir $DIR

trap 'kill %1' SIGINT

# NB: the slash at the end of content/ is important!
pelican --debug --autoreload \
    --output $DIR/ \
    --settings pelicanconf.py \
    content/ &

cd $DIR
python -m pelican.server 8888
