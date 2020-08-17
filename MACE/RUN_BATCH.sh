#!/bin/bash

#for task in 'dog' 'movie' 'temporal' 'waterbird' 'movie' 'face'
for task in 'waterbird'
do
  for level in 0.1 0.2
  do
    echo $task\_$level
    java -jar MACE.jar --prefix $task\_$level --controls data/honey_MACE_$task\_$level.csv data/answer_$task.csv
  done
done

rm *.competence
mv *.prediction ./results
