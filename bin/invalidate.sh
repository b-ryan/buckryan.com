#!/bin/bash
set -eu
if [[ $# != 1 ]]; then
    echo >&1 "Usage: $0 space-separated-paths"
    exit 1
fi
response=$(aws cloudfront create-invalidation --distribution-id EULTW8OWMRXOD --paths "$1")
id=$(jq -r '.Invalidation.Id' <<<"$response")
while true; do
    status_response=$(aws cloudfront get-invalidation --distribution-id EULTW8OWMRXOD --id "$id")
    status_=$(jq -r '.Invalidation.Status' <<<"$status_response")
    echo "$status_"
    if [[ $status_ != InProgress ]]; then
        break
    fi
    sleep 5
done
