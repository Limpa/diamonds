#!/bin/bash
filename="plebtokens"

echo "Running script with $1 suiciders against board $2\n"
for next in `head -n $1 $filename`; do
	pipenv run start --token $next --board $2 --logic Suicider &
	echo $next

done
exit 0
