#!/bin/bash

DRY_RUN=""

# find the current folder name without the teacher part

function find-stem() {
    while true; do
        stem=$(basename $(pwd))
        [[ "$stem" == "/" ]] && {
            echo "SLASH"
            return
        }
        ! [[ $stem =~ .*teacher.* ]] && {
            echo $stem
            return
        }
        cd ..
    done
}

STEM=$(find-stem)


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


function run-one() {
    local current="$1"; shift
    [[ -f $current ]] || {
        echo "File not found: $current"
        return
    }
    echo ========== "$current "
    extract-docstring $current
    # python $current  "$@" 2>&1 | grep -v 'Warning: Expected'
    [[ -z "$DRY_RUN" ]] && python $current
}

function run-all() {
    local current
    for current  in ${STEM}-[0-9]*.py $FOCUS; do
        [[ -f $current ]] || continue
        run-one $current
    done
}

function main() {
    while getopts "n" opt; do
        case $opt in
            n) DRY_RUN="yes";;
            *) echo "Unknown option: $opt";;
        esac
    done
    shift $((OPTIND-1))
    
    if [[ -z "$@" ]]; then
        run-all
    else
        for current in "$@"; do
            run-one $current
        done
    fi
}

main "$@"
