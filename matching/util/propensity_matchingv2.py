from psmpy import PsmPy
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

coraal = pd.read_csv("CORAAL_transcripts_clean.csv")
nsp = pd.read_csv("nsp_transcript_clean.csv")

coraal = coraal[["segment_filename", "age", "gender", "duration"]]
coraal = coraal.rename(columns={"segment_filename":"path"})
nsp = nsp.rename(columns={"wav": "path"})
nsp = nsp[["path", "age", "gender", "duration"]]

coraal["gender"] = coraal["gender"].apply(lambda x: 1 if x == "Female" else 0)
nsp["age"] = nsp["age"].astype("float")
nsp["gender"] = nsp["gender"].apply(lambda x: 1 if x == "Female" else 0)
nsp["race"] = 1
coraal["race"] = 0

# natural log of the snippet length
# Koenecke's version uses log but we do not
# coraal["duration"] = np.log(coraal["duration"])
# nsp["duration"] = np.log(nsp["duration"])

# reproducibility
#   this controls the randomness of pandas' sample() and sklearn
np.random.seed(12345)

print(f"NSP: {len(nsp)}")
print(f"CORAAL: {len(coraal)}")
data = pd.concat([nsp, coraal])
#shuffle
data = data.sample(frac = 1)
#reset index
data = data.reset_index(drop=True)
#normalize
for c in data.columns[1:-1]:
    data[c] = (data[c]-data[c].mean())/data[c].std()
#for testing purposes
# data = data.head(100)

print(data.head())

psm = PsmPy(data, treatment='race', indx="path", exclude = [])
psm.logistic_ps(balance = True)
output = psm.predicted_data
print(output.head())
print(len(output))
psm.knn_matched(matcher='propensity_logit', replacement=False, caliper=None, drop_unmatched=True)

# plots
psm.effect_size_plot(title='Standardized Mean differences accross covariates before and after matching', before_color='#FCB754', after_color='#3EC8FB', save=True)
plt.clf()
psm.plot_match(Title='Side by side matched controls', Ylabel='Number ofpatients', Xlabel= 'Propensity logit', names = ['treatment', 'control'], colors=['#E69F00', '#56B4E9'] ,save=True)

matches = psm.df_matched
matches.dropna(subset='matched_ID', inplace=True)

print(matches.head())
print(len(matches))

matches.to_csv("matches.csv")
