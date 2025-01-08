#!/bin/bash

FOCUS="boids.py"
STEM=$(basename $FOCUS .py)


# extract the docstring from a file

function extract-docstring() {
    local input="$1"; shift
    python << EOF
import ast

with open('${input}') as f:
    code = ast.parse(f.read())

for node in ast.walk(code):
    # if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Module)):
    if isinstance(node, (ast.Module)):
        docstring = ast.get_docstring(node)
        if docstring:
            print(docstring)
EOF
}

function run-all() {
    local game
    for game in ${STEM}-[0-9]*.py $FOCUS; do
        echo ========== "$game"
        extract-docstring $game
        python $game "$@" 2>&1 | grep -v 'Warning: Expected'
    done
}

# call with one arg that is the function name
main() {
    case "$1" in
    "")
        # do e.g. ln -s utils.sh extract.sh
        # and invoke extract.sh to call the extract() function
        command=$(basename $0 .sh)
        $command "$@"
        ;;
    *)
        # or run ./util.sh extract
        "$@"
        ;;
    esac
}

main "$@"
