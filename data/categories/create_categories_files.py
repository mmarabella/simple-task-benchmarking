import pandas as pd
import csv

tasks = ['temporal', 'movie', 'waterbird', 'face', 'dog', 'weather_ordinal', 'adult_ordinal', 'emotion', 'similarity', 'population']

for task in tasks:
  df_answer = pd.read_csv(f'answer_{task}.csv', header=None, sep='\t')
  df_truth = pd.read_csv(f'truth_{task}.csv', header=None, sep='\t')

  df_answer.columns = ['worker', 'question', 'answer']
  df_truth.columns = ['question', 'truth']

  answer_cats = df_answer['answer'].unique()
  truth_cats = df_truth['truth'].unique()

  aset = set(answer_cats)
  tset = set(truth_cats)

  combined_set = aset.union(tset)
  combined_list = list(combined_set)
  combined_list.sort()
  
  with open(f'categories_{task}.txt', 'w') as file:
    writer = csv.writer(file)
    for val in combined_list:
      writer.writerow([val])
