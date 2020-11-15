#!/bin/bash
collectortoken="9d4d7ffa-ed20-48c2-91d2-839ba8d2f0c5"
resettertoken="e89fa3cc-770c-46cd-b922-704e8592485b"
filename="plebtokens"
it=0

echo "Running script with $1 suiciders against board $2\n"
pipenv run start --token $resettertoken --board $2 --logic Resetter &
for next in `head -n $1 $filename`; do
	if [[ $((it * 2)) -eq $1 ]]
	then
		pipenv run start --token $collectortoken --board $2 --logic Collector &
		sleep 1
	fi
	((it++))
	pipenv run start --token $next --board $2 --logic Suicider &
	echo $next

done
exit 0
