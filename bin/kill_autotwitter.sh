#!/bin/bash

SEARCH_STR="lgdd_autotweet.py"

if pgrep -f $SEARCH_STR; then
    pkill -f $SEARCH_STR
    echo "success"
else 
    echo "not running"
    exit 1
fi
