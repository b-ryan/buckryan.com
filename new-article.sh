#!/bin/bash
title="$1"
if [[ -z "$title" ]]; then
    echo "Usage: $0 article-title" >&2
    exit 1
fi

filename="content/$(echo "$title" | awk '{print tolower($0)}' | sed 's/ /-/g').md"
if [[ -f "$filename" ]]; then
    echo "File '$filename' already exists" >&2
    exit 1
fi

cat > "$filename" << EOF
Title: $title
Date: $(date +'%Y-%m-%d')
Category:
Tags:
Author: Buck Ryan
Summary:
Status: draft


EOF
