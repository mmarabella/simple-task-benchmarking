#!/bin/bash

TASK=$1
TASK_TYPE=$2

for NOISE in 0.35 0.45 0.55 0.65 0.75 0.85 0.95
# for NOISE in 0.35
do
  for SUPERVISION in 0.2 0.8
  # for SUPERVISION in 0.2
  do
    
    for FOLD in {1..5}
    # for FOLD in 1
    do
      PREFIX=$TASK\_$SUPERVISION\_fold$FOLD\_noise$NOISE
      echo $SUPERVISION
      java -jar MACE_external_lib/MACE.jar \
        --prefix $PREFIX \
        --controls ../data/kfolds/MACE/gold_$TASK\_$SUPERVISION\_fold$FOLD.csv \
        ../data/noise/MACE/answer\_$TASK\_noise$NOISE\_MACE.csv 
      mv *.prediction ./results
      mv *.competence ./results
      python3 evaluate.py $TASK $TASK_TYPE results/$PREFIX.prediction ../data/kfolds/MACE/eval\_$TASK\_$SUPERVISION\_fold$FOLD.csv \
        --semi $SUPERVISION \
        --fold $FOLD \
        --noise $NOISE
    done
  done

  SUPERVISION=0.0
  FOLD=1
  PREFIX=$TASK\_$SUPERVISION\_fold$FOLD\_noise$NOISE
  java -jar MACE_external_lib/MACE.jar \
      --prefix $PREFIX \
      ../data/noise/MACE/answer\_$TASK\_noise$NOISE\_MACE.csv
  mv *.prediction ./results
  mv *.competence ./results
  python3 evaluate.py $TASK $TASK_TYPE results/$PREFIX.prediction ../data/MACE/truth_$TASK.csv \
    --noise $NOISE
done
