import pandas as pd

coraal = pd.read_csv("CORAAL_transcripts_clean.csv")
nsp = pd.read_csv("nsp_transcript_clean.csv")

matches = pd.read_csv("matches.csv")

coraal = coraal[coraal['segment_filename'].isin(matches['matched_ID'])]
nsp = nsp[nsp['wav'].isin(matches['path'])]

coraal.to_csv("coraal_matched.csv")
nsp.to_csv("nsp_matched.csv")
