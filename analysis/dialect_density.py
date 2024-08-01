import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress


def ddm(utterance):
    # DDM = (phon_count + gram_count) / wordcount
    return (utterance["phon_count"] + utterance["gram_count"]) / utterance["wordcount"]
dialect_density_measures = pd.read_csv("data/coraal/DDM.csv")
dialect_density_measures["DDM"] = dialect_density_measures.apply(ddm, axis=1)
def tweak_filename(batch):
    return batch["segment_filename"].replace(".wav", "")
dialect_density_measures["segment_filename"] = dialect_density_measures.apply(tweak_filename, axis=1)
dialect_density_measures.set_index('segment_filename')
print(dialect_density_measures.head())

method_name = {
    'hubert': 'HuBERT',
    'wav2vec2': 'wav2vec 2.0',
    'wavlm': 'WavLM',
    'xlsr': 'XLS-R',
    'fbank': 'FBANK'
}

for method in ['hubert', 'wav2vec2', 'wavlm', 'xlsr', 'fbank']:
    preds = pd.read_csv(f'preds/coraal_ddm/{method}.csv')

    # merge with dialect_density_measures based on index
    #   only 150 utterances were annotated
    merged = dialect_density_measures.merge(preds, on='segment_filename', how='left')
    merged = merged[merged['prediction'].notnull()]

    print(merged.shape[0], "utterances")

    # TODO: CER and DDM - gather from edit_dist_stats.py

    # find the correlation with the DDM
    # WER is from sclite output from ESPnet
    wer_ddm = merged[['wer', 'DDM']]
    print('WER and DDM correlation')
    print(method, 'pearson', wer_ddm.corr(method='pearson'))
    print(method, 'spearman', wer_ddm.corr(method='spearman'))
    slope, _, r_value, p_value, _ = linregress(wer_ddm['DDM'], wer_ddm['wer'])
    print('slope, pearsonr, p value')
    print(slope, r_value, p_value)

    fig, ax = plt.subplots()
    ax.scatter(wer_ddm['DDM'], wer_ddm['wer'], linewidth=2.0)
    ax.set_ylim([None,1.2])
    plt.title(f"Robustness of {method_name[method]} to dialect density (AAVE)")
    plt.xlabel("Dialect Density Measure")
    plt.ylabel("WER")
    plt.savefig(f'analysis/ddm/{method}/wer_vs_ddm.png', bbox_inches='tight')
