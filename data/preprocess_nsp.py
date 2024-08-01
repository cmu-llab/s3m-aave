from preprocess import normalize_text
import pandas as pd
import re



nsp = pd.read_csv("nsp/transcript.csv")


# the same text normalization applied to CORAAL
nsp["clean_content"] = nsp["transcript"].map(normalize_text)
# note: the above will not change the transcripts since text normalization was done before alignment

nsp.to_csv('nsp/transcript_clean.csv', index=None)
