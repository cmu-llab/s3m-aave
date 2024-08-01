# Propensity score matching

```
cd util
ln -s ../../data/coraal/CORAAL_transcripts_clean.csv CORAAL_transcripts_clean.csv
ln -s ../../data/nsp/nsp_transcript_clean.csv nsp_transcript_clean.csv
python propensity_matchingv2.py # generates matches.csv, propensity_match.png, effect_size.png
python filter_list.py # generates coraal_matched.csv, nsp_matched.csv
```
