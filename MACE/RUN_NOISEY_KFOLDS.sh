#!/bin/bash

TASK=$1

for NOISE in 0.35 0.45 0.55 0.65 0.75 0.85 0.95
# for NOISE in 0.35
do
  for SUPERVISION in 0.2 0.8
  # for SUPERVISION in 0.2
  do
    
    for FOLD in {1..5}
    # for FOLD in 1
    do
      echo $SUPERVISION
      java -jar MACE.jar \
        --prefix $TASK\_$SUPERVISION\_fold$FOLD\_noise$NOISE \
        --controls ../data/kfolds/MACE/gold_$TASK\_$SUPERVISION\_fold$FOLD.csv \
        ../data/noise/MACE/answer\_$TASK\_noise$NOISE\_MACE.csv 
      mv *.prediction ./results
      python3 results/evaluate_noise.py $TASK categorical $SUPERVISION $FOLD $NOISE
    done
  done


  java -jar MACE.jar \
    --prefix $TASK\_0.0\_fold1\_noise$NOISE \
    ../data/noise/MACE/answer\_$TASK\_noise$NOISE\_MACE.csv 
  mv *.prediction ./results
  python3 results/evaluate_noise.py $TASK categorical 0.0 1 $NOISE
done


rm *.competence
mv results/*.prediction results/predictions