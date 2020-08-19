#!/bin/bash
 # 'movie' 'waterbird' 'face' 'dog'


TASK=$1

for SUPERVISION in 0.1 0.9
do
  for FOLD in {1..10}
  do
    get-another-label/bin/get-another-label.sh \
      --categories ../data/categories/categories\_$TASK.txt \
      --input ../data/clean-tabbed/answer\_$TASK.csv \
      --eval ../data/kfolds/DS/eval_$TASK\_$SUPERVISION\_fold$FOLD\_tab.csv \
      --gold ../data/kfolds/DS/gold_$TASK\_$SUPERVISION\_fold$FOLD\_tab.csv 
    python3 results/process_predictions.py $TASK --semi-supervised $SUPERVISION --fold $FOLD
  done
done

for SUPERVISION in 0.2 0.8
do
  for FOLD in {1..5}
  do
    get-another-label/bin/get-another-label.sh \
      --categories ../data/categories/categories\_$TASK.txt \
      --input ../data/clean-tabbed/answer\_$TASK.csv \
      --eval ../data/kfolds/DS/eval_$TASK\_$SUPERVISION\_fold$FOLD\_tab.csv \
      --gold ../data/kfolds/DS/gold_$TASK\_$SUPERVISION\_fold$FOLD\_tab.csv 
    python3 results/process_predictions.py $TASK --semi-supervised $SUPERVISION --fold $FOLD
  done
done

for SUPERVISION in 0.5
do
  for FOLD in 1 2
  do
    get-another-label/bin/get-another-label.sh \
      --categories ../data/categories/categories\_$TASK.txt \
      --input ../data/clean-tabbed/answer\_$TASK.csv \
      --eval ../data/kfolds/DS/eval_$TASK\_$SUPERVISION\_fold$FOLD\_tab.csv \
      --gold ../data/kfolds/DS/gold_$TASK\_$SUPERVISION\_fold$FOLD\_tab.csv 
    python3 results/process_predictions.py $TASK --semi-supervised $SUPERVISION --fold $FOLD
  done
done

get-another-label/bin/get-another-label.sh \
    --categories ../data/categories/categories\_$TASK.txt \
    --input ../data/clean-tabbed/answer\_$TASK.csv \
    --eval ../data/clean-tabbed/truth\_$TASK.csv
python3 results/process_predictions.py $TASK
