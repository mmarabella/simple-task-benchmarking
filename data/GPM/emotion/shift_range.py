import pandas as pd

df_answer = pd.read_csv('data_emotion_withnegatives.csv')
df_answer['answer'] = df_answer['answer'] + 100

df_truth = pd.read_csv('truth_emotion_withnegatives.csv')
df_truth['truth'] = df_truth['truth'] + 100

df_answer.to_csv('data_emotion.csv', header=False, index=False)
df_truth.to_csv('truth_emotion.csv', header=False, index=False)
