#!/bin/bash
dirs=$(git ls-tree -rt HEAD:./ | awk '{if ($2 == "tree") print $4;}')
for dir in $dirs; do
    cd "$dir" || exit 1
    pip-compile "$@"
    cd - || exit 1
done
