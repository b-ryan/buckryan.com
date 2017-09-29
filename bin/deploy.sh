#!/bin/bash
set -eu

GREEN='\033[0;32m'
NC='\033[0m'

PELICAN_OUTPUT_DIR=.pelican.prod

USER=buck
SERVER=104.131.52.54
SSH="$USER@$SERVER"
DEPLOY_DIR="/var/www/html"

_green() {
    echo -e "${GREEN}$@...${NC}"
}

build() {
    _green "Building Pelican"
    pelican \
        --delete-output-directory \
        --output $PELICAN_OUTPUT_DIR \
        --settings publishconf.py \
        content/ # NB: the slash at the end is important!
}

deploy() {
    _green "rsyncing code"
    aws s3 sync $PELICAN_OUTPUT_DIR/ s3://www.buckryan.com//
}

main() {
    build
    deploy
}

main "$@"
