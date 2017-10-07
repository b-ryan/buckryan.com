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

sleep 3 # to give the pelican command in the background some time to write its
        # noise

cat <<EOF
#######################################################################
#               starting server: http://localhost:8888                #
#######################################################################
EOF

cd $DIR
python -m pelican.server 8888
