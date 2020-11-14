#!/bin/sh
i="0"

while [ $i -lt 4 ]
do
echo "Running job\n"
pipenv run start --token 4dd18bdd-bd7d-4078-a173-d67284048070 --board 1 --logic Annoying &
pipenv run start --token bbc25e4f-068b-4147-9f3e-61896a0ca5ed --board 2 --logic Annoying &
pipenv run start --token 6e137175-a141-4527-9014-d29fc633fee2 --board 3 --logic Annoying &
pipenv run start --token 0c2c681b-457f-4043-bcb5-7224f90582bc --board 4 --logic Annoying &
pipenv run start --token 9e638916-b03a-4597-822c-3cdcc84e8fb8 --board 1 --logic Annoying &
pipenv run start --token ffaff538-8581-4c5d-ae9c-1b5b20f88590 --board 2 --logic Annoying &
pipenv run start --token 5e90739e-ed98-4bd4-97c2-409cfa9971ed --board 3 --logic Annoying &
pipenv run start --token a70a0f5a-2e1c-4283-a810-02414cbfcf10 --board 4 --logic Annoying &
i=$[$i+1]
sleep 65 
done

