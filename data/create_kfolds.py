import pandas as pd
import numpy as np
import csv
from sklearn.model_selection import KFold

# tasks = ['temporal', 'movie', 'waterbird', 'face', 'dog', 'weather_ordinal', 'adult_ordinal', 'similarity', 'population', 'emotion']
folds = [10, 5, 2]
# folds = [10]
tasks = ['temporal', 'movie', 'waterbird', 'face', 'dog', 'weather_ordinal', 'adult_ordinal']
# tasks=['temporal']
for task in tasks:
	for k in folds:
		df_truth = pd.read_csv(f'same-index-separate/truth_{task}.csv')
		kf = KFold(n_splits = k, shuffle = True, random_state = None)

		i = 1
		for result in kf.split(df_truth):
			eval1 = df_truth.iloc[result[0]]
			gold1 =  df_truth.iloc[result[1]]
			gold2 = df_truth.iloc[result[0]]
			eval2 =  df_truth.iloc[result[1]]

			#DIST
			eval1.to_csv(f'kfolds/DIST/eval_{task}_{1/k}_fold{i}.csv', index=False)
			gold1.to_csv(f'kfolds/DIST/gold_{task}_{1/k}_fold{i}.csv', index=False)
			eval2.to_csv(f'kfolds/DIST/eval_{task}_{1-1/k}_fold{i}.csv', index=False)
			gold2.to_csv(f'kfolds/DIST/gold_{task}_{1-1/k}_fold{i}.csv', index=False)

			#DS
			eval1.to_csv(f'kfolds/DS/eval_{task}_{1/k}_fold{i}_tab.csv', index=False, sep='\t', header=None)
			gold1.to_csv(f'kfolds/DS/gold_{task}_{1/k}_fold{i}_tab.csv', index=False, sep='\t', header=None)
			eval2.to_csv(f'kfolds/DS/eval_{task}_{1-1/k}_fold{i}_tab.csv', index=False, sep='\t', header=None)
			gold2.to_csv(f'kfolds/DS/gold_{task}_{1-1/k}_fold{i}_tab.csv', index=False, sep='\t', header=None)


			################
			##### MACE #####
			################

			gold1_mace = df_truth.join(gold1.set_index('question'), on='question', how='left', lsuffix='_orig').sort_values('question').reset_index()[['question', 'truth']]
			with open(f'kfolds/MACE/gold_{task}_{1/k}_fold{i}.csv', 'w') as file:
				writer = csv.writer(file)
				for idx, val in gold1_mace['truth'].iteritems():
					if not(pd.isnull(val)):
						writer.writerow([int(val)])
					else:
						writer.writerow([])

			eval2_mace = gold1_mace[['truth']].dropna()
			eval2_mace.index.rename('question', inplace=True)
			eval2_mace['truth'] = eval2_mace['truth'].astype(int)
			eval2_mace.to_csv(f'kfolds/MACE/eval_{task}_{1-1/k}_fold{i}.csv')

			gold2_mace = df_truth.join(gold2.set_index('question'), on='question', how='left', lsuffix='_orig').sort_values('question').reset_index()[['question', 'truth']]
			with open(f'kfolds/MACE/gold_{task}_{1-1/k}_fold{i}.csv', 'w') as file:
				writer = csv.writer(file)
				for idx, val in gold2_mace['truth'].iteritems():
					if not(pd.isnull(val)):
						writer.writerow([int(val)])
					else:
						writer.writerow([])

			eval1_mace = gold2_mace[['truth']].dropna()
			eval1_mace.index.rename('question', inplace=True)
			eval1_mace['truth'] = eval1_mace['truth'].astype(int)
			eval1_mace.to_csv(f'kfolds/MACE/eval_{task}_{1/k}_fold{i}.csv')

			i += 1

