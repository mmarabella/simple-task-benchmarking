import pandas as pd
from sklearn import metrics


labels_df = pd.read_csv('labels.csv', delimiter='\t')
eval_df = pd.read_csv('evaluation.csv', delimiter='\t').set_index('question')


with open('eval_clean.txt', 'w') as infile:
	for index, row in eval_df.iterrows():
		if row['question'] in labels_df['question'].values:
			infile.write(row['question'] + '\t' + row['answer'] + '\n')
