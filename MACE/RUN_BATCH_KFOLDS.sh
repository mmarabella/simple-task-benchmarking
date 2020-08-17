#!/bin/bash
TASK=$1

java -jar MACE.jar \
    --prefix $TASK\_0.0\_fold1 \
    ../data/MACE/answer\_$TASK.csv 
mv *.prediction ./results
python3 results/evaluate_semisupervised.py $TASK categorical 0.0 1


for LEVEL in 0.1 0.9
do
  for FOLD in {1..10}
  do
    echo $LEVEL
    java -jar MACE.jar \
        --prefix $TASK\_$LEVEL\_fold$FOLD \
        --controls ../data/kfolds/MACE/gold\_$TASK\_$LEVEL\_fold$FOLD.csv \
        ../data/MACE/answer_$TASK.csv 
        mv *.prediction ./results
    python3 results/evaluate_semisupervised.py $TASK categorical $LEVEL $FOLD
  done
done


for LEVEL in 0.2 0.8
do
  for FOLD in {1..5}
  do
    echo $LEVEL
    java -jar MACE.jar \
        --prefix $TASK\_$LEVEL\_fold$FOLD \
        --controls ../data/kfolds/MACE/gold\_$TASK\_$LEVEL\_fold$FOLD.csv \
        ../data/MACE/answer_$TASK.csv 
        mv *.prediction ./results
    python3 results/evaluate_semisupervised.py $TASK categorical $LEVEL $FOLD
  done
done


for LEVEL in 0.5
do
  for FOLD in {1..2}
  do
    echo $LEVEL
    java -jar MACE.jar \
        --prefix $TASK\_$LEVEL\_fold$FOLD \
        --controls ../data/kfolds/MACE/gold\_$TASK\_$LEVEL\_fold$FOLD.csv \
        ../data/MACE/answer_$TASK.csv 
        mv *.prediction ./results
    python3 results/evaluate_semisupervised.py $TASK categorical $LEVEL $FOLD
  done
done


rm *.competence
mv results/*.prediction results/predictions
