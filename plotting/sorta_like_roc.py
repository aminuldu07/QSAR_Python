import pandas as pd, numpy as np
import config, os
from hepatotox_db import ANIMALDB
from stats import get_class_stats
from plotting.coverage_plots import calc_roc

import matplotlib.pyplot as plt


def calc_roc(data, metric, disease_name):
    covs = []
    mets = []
    for offset in np.arange(0, 0.41, 0.01):
        data_offset = data[(data.PREDICTION_MEAN < 0.5-offset) | (data.PREDICTION_MEAN >= 0.5+offset)]
        stats = get_class_stats(None, data_offset[disease_name], data_offset.PREDICTION_MEAN_CLASS)
        covs.append(data_offset.shape[0]/data.shape[0])
        mets.append(stats[metric])
    return covs, mets


diseases = ['NECROSIS', 'CHOLESTASIS', 'STEATOSIS']

d_name = diseases[0]
dfs = []
#
for i, d_name in enumerate(diseases):

    animals = pd.read_csv('../data_scratch/new_rat_data.csv', index_col=0)

    disease = animals[d_name]
    disease.index = animals.USUBJID

    txt_dir = os.path.join(config.TEXT_DIR, 'pls_results', d_name)
    img_dir = os.path.join(config.IMG_DIR, 'pls_results', d_name)

    if not os.path.exists(img_dir):
        os.mkdir(img_dir)

    cv_predictions = pd.read_csv(os.path.join(txt_dir, 'cv_predictions.csv'), index_col=0)
    params = pd.read_csv(os.path.join(txt_dir, 'params.csv'), index_col=0)

    prediction_data = params.merge(cv_predictions)
    prediction_data.loc[prediction_data.PREDICTION < 0.5, 'PREDICTION_CLASS'] = 0
    prediction_data.loc[prediction_data.PREDICTION >= 0.5, 'PREDICTION_CLASS'] = 1


    stats = []
    for gp, gp_data in prediction_data.groupby(['MDL_ID', 'N_COMPONENTS']):
        stats_dic = get_class_stats(None, disease.loc[gp_data.USUBJID], gp_data.PREDICTION_CLASS)
        stats_dic['MDL_ID'] = gp[0]
        stats_dic['N_COMPONENTS'] = gp[1]
        stats_dic['ID'] = gp_data.ID.iloc[0]
        stats.append(stats_dic)

    stats_df = pd.DataFrame(stats)

    datasets = prediction_data.groupby('MDL_ID').ngroups
    n_components = prediction_data.groupby('N_COMPONENTS').ngroups

    stats_df['BAL_ACC'] = (stats_df['Recall'] + stats_df['Specificity']) / 2


    best_models = stats_df.groupby('MDL_ID').apply(lambda g: g[g['BAL_ACC'] == g['BAL_ACC'].max()].iloc[0])
    best_models.to_csv(os.path.join(txt_dir, 'best_models.csv'))
    best_model_predictions = prediction_data[prediction_data.ID.isin(best_models.ID)]

    best_model_predictions['PREDICTION_MEAN'] = best_model_predictions.groupby('USUBJID')['PREDICTION'].transform('mean')
    best_model_predictions['PREDICTION_STD'] = best_model_predictions.groupby('USUBJID')['PREDICTION'].transform('std')

    best_model_predictions.loc[best_model_predictions.PREDICTION_MEAN < 0.5, 'PREDICTION_MEAN_CLASS'] = 0
    best_model_predictions.loc[best_model_predictions.PREDICTION_MEAN >= 0.5, 'PREDICTION_MEAN_CLASS'] = 1

    final_data = best_model_predictions.drop_duplicates(['USUBJID', 'PREDICTION_MEAN_CLASS'])

    final_data = final_data.merge(disease.reset_index()).rename({0: 'TRUE'}, axis=1)

    offset = 0
    final_data = final_data[(final_data.PREDICTION_MEAN < 0.5-offset) | (final_data.PREDICTION_MEAN >= 0.5+offset)]

    stat_dfs = []
    df = pd.DataFrame()
    for stat in ['Precision', 'Recall']:
        cov, stat_array = calc_roc(final_data, stat, d_name)
        df[stat] = stat_array
        df['Coverage'] = cov
        df['Distance'] = np.arange(0, 0.41, 0.01)


    # Convert the dataframe to long-form or "tidy" format
    df = pd.melt(df, id_vars=['Distance'])
    df['Disease'] = [d_name]*len(df)

    dfs.append(df)

df = pd.concat(dfs)

import seaborn as sns
# # Set up a grid of axes with a polar projection
# g = sns.FacetGrid(df, col="Disease",
# # subplot_kws=dict(projection='polar'),
#                   sharex=False, sharey=False, despine=False, ylim=(0, 1), size=5)
#
# # Draw a scatterplot onto each axes in the grid
# g.map(sns.lineplot, y="value", x="Distance")

sns.set_context(rc={"lines.linewidth": 2.5})
g = sns.relplot(
    data=df,
    x="Distance", y="value",
    hue="variable",
    kind="line", col='Disease',
    height=5, aspect=.75, facet_kws=dict(sharex=False), legend=False
)

for each in [0, 1, 2]:
    g.axes[0, each].set_xlabel('')
    g.axes[0, each].set_ylabel('')
    g.axes[0, each].set_ylim(0, 1)
    g.axes[0, each].set_yticks(np.arange(0, 1.1, 0.1))
    g.axes[0, each].set_yticklabels([round(t, 1) for t in g.axes[0, each].get_yticks()], fontsize=14)
    g.axes[0, each].set_xticklabels(g.axes[0, each].get_xticklabels(), fontsize=14)
    g.axes[0, each].set_title(g.axes[0, each].get_title(), fontsize=14)

# new_title = 'Statistic'
# g._legend.texts[0].set_text("")
# g._legend.set_title(new_title )
# g._legend._legend_box.sep = -5
# g._legend.remove()
# for l in g.ax.lines:
#     print(l.get_linewidth())
#     plt.setp(l, linewidth=10)

output_file = os.path.join(os.getenv('LIVER_TOX'), 'img', 'good_figures', 'line.png')
plt.savefig(output_file)

