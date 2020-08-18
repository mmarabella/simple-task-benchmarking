#!/bin/bash
TASK=$1
TASK_TYPE=$2

LEVEL=0.0
FOLD=1
PREFIX=$TASK\_$LEVEL\_fold$FOLD
java -jar MACE_external_lib/MACE.jar \
    --prefix $PREFIX \
    ../data/MACE/answer\_$TASK.csv 
mv *.prediction ./results
mv *.competence ./results
python3 evaluate.py $TASK $TASK_TYPE results/$PREFIX.prediction ../data/MACE/truth_$TASK.csv


for LEVEL in 0.1 0.9
do
  for FOLD in {1..10}
  do
    PREFIX=$TASK\_$LEVEL\_fold$FOLD
    echo $LEVEL
    java -jar MACE_external_lib/MACE.jar \
        --prefix $PREFIX \
        --controls ../data/kfolds/MACE/gold\_$PREFIX.csv \
        ../data/MACE/answer_$TASK.csv 
        mv *.prediction ./results
        mv *.competence ./results
    python3 evaluate.py $TASK $TASK_TYPE results/$PREFIX.prediction ../data/kfolds/MACE/eval\_$PREFIX.csv --semi $LEVEL --fold $FOLD
  done
done


# for LEVEL in 0.2 0.8
# do
#   for FOLD in {1..5}
#   do
  # PREFIX=$TASK\_$LEVEL\_fold$FOLD
#     echo $LEVEL
#     java -jar MACE_external_lib/MACE.jar \
#         --prefix $PREFIX \
#         --controls ../data/kfolds/MACE/gold\_$PREFIX.csv \
#         ../data/MACE/answer_$TASK.csv 
#         mv *.prediction ./results
#         mv *.competence ./results
#     python3 evaluate.py $TASK $TASK_TYPE results/$PREFIX.prediction ../data/kfolds/MACE/eval\_$PREFIX.csv --semi $LEVEL --fold $FOLD
#   done
# done


# for LEVEL in 0.5
# do
#   for FOLD in {1..2}
#   do
  # PREFIX=$TASK\_$LEVEL\_fold$FOLD
#     echo $LEVEL
#     java -jar MACE_external_lib/MACE.jar \
#         --prefix $PREFIX \
#         --controls ../data/kfolds/MACE/gold\_$PREFIX.csv \
#         ../data/MACE/answer_$TASK.csv 
#         mv *.prediction ./results
#         mv *.competence ./results
#     python3 evaluate.py $TASK $TASK_TYPE results/$PREFIX.prediction ../data/kfolds/MACE/eval\_$PREFIX.csv --semi $LEVEL --fold $FOLD
#   done
# done
