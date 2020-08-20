import pandas as pd

df_data = pd.read_csv('data_weather_ordinal_withzeros.csv', header=None, names=['question', 'worker', 'answer'])
df_truth = pd.read_csv('truth_weather_ordinal_withzeros.csv')

df_data['answer'] = df_data['answer'] + 1
df_truth['truth'] = df_truth['truth'] + 1

df_data.to_csv('data_weather_ordinal.csv', header=None, index=False)
df_truth.to_csv('truth_weather_ordinal.csv', index=False)