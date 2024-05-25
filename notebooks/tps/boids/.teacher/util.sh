#!/bin/bash

#FOCUS="game.py"
FOCUS="boids.py"
STEM=$(basename $FOCUS .py)


function check-clean() {
    local stat=$(git diff --stat $FOCUS)
    [[ -n "$stat" ]] && {
        echo git repo not clean - aborting
        exit 1
    }
}

function extract() {
    check-clean
    local hashes=$(git log --reverse --format=%h)
    local hash
    local count=0
    for hash in $hashes; do
        echo ============ $hash
        git diff --name-only ${hash} ${hash}^ 2> /dev/null | grep -q "^${FOCUS}\$" && {
            count=$(($count+1))
            local filename=$(printf "${STEM}-%02d.py" $count)
            local message=$(printf "${STEM}-%02d.msg" $count)
            git archive $hash | tar xf - ${FOCUS}
            mv ${FOCUS} $filename
            git show -s --format=%B $hash > $message
            echo in $filename and $message
        }
    done
    git reset --hard
}

function run-all() {
    local game
    for game in ${STEM}-[0-9]*.py; do
        local message=$(sed -e s/.py/.msg/ <<< $game)
        echo ========== "$game"
        cat $message
        python $game "$@" 2>&1 | grep -v 'Warning: Expected'
    done
    game=game.py
    echo "final code - optional"
    python $game "$@" 2>&1 | grep -v 'Warning: Expected'
}

function clean() {
    rm ${STEM}-[0-9]*.{py,msg}
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
