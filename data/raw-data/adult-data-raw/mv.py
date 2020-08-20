import pandas as pd
from sklearn import metrics


def dict_to_sorted_list(d):
  return [d[key] for key in sorted(d.keys())]


def accuracy(gold_dict, pred_dict):
  return (metrics.accuracy_score(dict_to_sorted_list(gold_dict), dict_to_sorted_list(pred_dict)))

labels_df = pd.read_csv('csvs/labels.csv', delimiter='\t')
eval_df = pd.read_csv('csvs/evaluation.csv', delimiter='\t').set_index('question')
full_df = labels_df.join(eval_df, how='inner', on='question')

gold_dict = full_df.set_index('question')['truth'].to_dict()
baseline_df = full_df[['question', 'answer']].groupby('question').agg(lambda x: x.mode()[0])
baseline_dict = baseline_df['answer'].to_dict()


print(accuracy(gold_dict, baseline_dict))