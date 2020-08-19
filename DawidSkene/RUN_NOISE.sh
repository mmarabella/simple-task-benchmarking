#!/bin/bash
 # 'movie' 'waterbird' 'face' 'dog'


TASK=$1

# for NOISE in 0.35 0.45 0.55 0.65 0.75 0.85 0.95
for NOISE in 0.35
do
  # for SUPERVISION in 0.2 0.8
  for SUPERVISION in 0.2
  do
    
    # for FOLD in {1..5}
    for FOLD in 1
    do
      echo $NOISE
      echo $SUPERVISION
      bin/get-another-label.sh \
        --categories ../data/categories/categories\_$TASK.txt \
        --input ../data/noise/DS/answer\_$TASK\_noise$NOISE\_tab.csv \
        --eval ../data/kfolds/DS/eval_$TASK\_$SUPERVISION\_fold$FOLD\_tab.csv \
        --gold ../data/kfolds/DS/gold_$TASK\_$SUPERVISION\_fold$FOLD\_tab.csv 

      python3 results/process_predictions.py $TASK \
        --semi-supervised $SUPERVISION \
        --fold $FOLD \
        --noise $NOISE
    done
  done


  get-another-label/bin/get-another-label.sh \
      --categories ../data/categories/categories\_$TASK.txt \
      --input ../data/noise/DS/answer\_$TASK\_noise$NOISE\_tab.csv \
      --eval ../data/clean-tabbed/truth\_$TASK.csv
  python3 results/process_predictions.py $TASK --noise $NOISE
done