#!/bin/bash

sess=OJ4SQL
tmux has-session -t $sess 2>/dev/null
if [ $? == 0 ]; then
    read -p "The $sess session exists. Kill it?[y/N]" -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted."
        exit 1
else
        tmux kill-session -t $sess && echo $sess" killed"
    fi
fi


docker start pg_oj4db_backend
docker start my_oj_test
docker start pg_oj_test
docker start og_oj_test

tmux new-session -d -s $sess
tmux split-window -h
tmux select-pane -t 0
tmux send-keys 'cd ~/redis-6.0.8/src && ./redis-server ../redis.conf' C-m
tmux select-pane -t 1
tmux send-keys 'cd ~/redis-6.0.8/src && ./redis-server --port 6380' C-m
tmux split-window -v
tmux select-pane -t 2
tmux send-keys 'pipenv run python3 manage.py runserver 0.0.0.0:8000 --insecure' C-m
