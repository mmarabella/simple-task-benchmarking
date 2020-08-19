import pandas as pd
import sys
import sklearn.metrics as metrics

task = sys.argv[1]
task_type = sys.argv[2]
truth_file = sys.argv[3]


def score_predictions(task, mode, round_bool):
	filename = f'res/{task}_predicted_mos_{mode}.csv'
	df_preds = pd.read_csv(filename, header=None, names=['question', 'preds']).set_index('question')
	if round_bool and mode == 'continuous':
		df_preds['preds'] = df_preds['preds'].map(lambda x: round(x))
	df_truth = pd.read_csv(truth_file).set_index('question')
	df_full = df_preds.join(df_truth, how='inner')
	mae = metrics.mean_absolute_error(df_full['truth'], df_full['preds'])
	df_full['score'] = abs(df_full['truth'] == df_full['preds'])
	return(mae)

if task_type == 'ordinal':
	mae_select = score_predictions(task, 'discrete', False)
	mae_merge = score_predictions(task, 'continuous', True)
	print(mae_select, mae_merge)

elif task_type == 'numerical':
	mae_select = score_predictions(task, 'discrete', False)
	mae_merge = score_predictions(task, 'continuous', False)
	print(mae_select, mae_merge)

elif task_type == 'categorical':
	mae_select = score_predictions(task, 'discrete', False)
	print(mae_select)

else:
	print('INVALID TASK TYPE')

mae_mean = score_predictions(task, 'MEAN', False)
# print("MEAN:", mae_mean)