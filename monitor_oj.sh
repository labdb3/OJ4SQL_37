#!/bin/bash

while true
do
	monitor_kill=`ps -ef | grep "python killzombie.py" | grep -v grep| wc -l`
	if [ ${monitor_kill} -eq 0 ]
	then
		echo "kill connection programs is not running,restart killzombie.py"
		tmux kill-session -t killzombie 2>/dev/null
		tmux new-session -d -s killzombie \; send-keys 'conda activate web && python killzombie.py' Enter
	else
		echo "killzombie.py is running"
	fi
	sleep 5
done

