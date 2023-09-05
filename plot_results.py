import pandas as pd, seaborn as sns
import numpy as np
import matplotlib.pyplot as plt,
pd.set_option('display.max_rows', 500);pd.set_option('display.max_columns', 500);pd.set_option('display.width', 1000)
sns.set_style("darkgrid");


df = pd.read_csv('./all_metric.csv')
metrics = ['dice', 'fdr', 'miss', 'bAcc', 'f1', 'Sdis', 'SdisI', 'SdisMax', 'SdisIMax', 'clDice', 'Vol']
tissues = [ 'mean', 'GM', 'WM', 'CSF', 'cereb', 'deepGM', 'bstem', 'hippo']
model_order = ['Synth', 'SynthInh', 'SynthMot', 'SynthMotInh', 'DataT2',]


dfs = df[(df.GroundTruth=='drawEM') & (df.eval_on=='T2')]

for met in metrics:
    sel_metrics = [f'{met}_{tt}' for tt in tissues]
    dfmm = dfs.melt(id_vars=['scan_age', 'sujnum', 'model_name','eval_name','eval_on'], value_vars=sel_metrics, var_name='metric', value_name='y')

    fig = sns.catplot(data=dfmm, y='y', x='eval_on',hue='model_name', col='metric', kind='boxen', hue_order=model_order, col_wrap=4)
    #fig = sns.relplot(data=dfmm, y='y', x='sujnum', hue='eval_name', col='metric', col_wrap=4)

dfmm['age_label'] = pd.cut(dfmm.scan_age, bins=[26,32,36, 40, 46])
fig = sns.catplot(data=dfmm, y='y', x='age_label',hue='model_name', col='metric', kind='boxen', hue_order=model_order, col_wrap=4)


#tabel with average over the all subject or by age bins
df['age_label'] = pd.cut(df.scan_age, bins=[26,32,36, 40, 46])
df.groupby(['eval_name'])['dice_GM'].mean()
df.groupby(['age_label','eval_name'])['dice_GM'].mean()

#compute volume ratio
label_volume = [f'occupied_volume_{tt}' for tt in tissues]
prediction_volume = [f'predicted_occupied_volume_{tt}' for tt in tissues]

for (labvol,predvol,tis) in zip(label_volume, prediction_volume,tissues):
    new_keys = f'Vol_{tis}'
    df[new_keys] = df[predvol]/df[labvol]
#compute average by metric
def compute_mean(df, met):
    for ii, col in enumerate(met):
        if ii==0:
            dfmean = df[col]
        else:
            dfmean = dfmean + df[col]
    return dfmean/len(met)

for met in metrics:
    ymet = [f'{met}_{tt}' for tt in tissues]
    df[f'{met}_mean'] = df.apply(lambda x:  compute_mean(x, ymet), axis=1)

ymet = ['average'] + ymet
