# Overall

After running inference in ESPnet, copy the predictions and sclite output over
```
cd analysis
./copy_edit_dist.sh  # Copy sclite output (edit distance breakdown)

# generate CSVs in preds/
cd ../preds
./copy_preds.sh
./copy_ddm_preds.sh
./copy_ref.sh
cd ..
python preds/format_preds.py

# get WER from ESPnet's sclite outputs and update CSVs in preds/
python analysis/edit_dist.py --dataset coraal --store_wer --fbank
python analysis/edit_dist.py --dataset coraal_ddm --store_wer --fbank
python analysis/edit_dist.py --dataset nsp --store_wer --fbank
```

# DDM analysis

```
python analysis/dialect_density.py
```

# WER breakdown by region
```
python analysis/edit_dist.py --dataset coraal --region  # SSL models only
python analysis/edit_dist.py --dataset nsp --region  # SSL models only
```

# Common edits
```
python analysis/common_edits.py
python analysis/edit_dist_stats.py
```

# Acoustic distance
```
python word_cnt.py  # get common words that overlap between paired (CORAAL, NSP) utterances
python extract_word_from_wav.py  # extract common words from the wav file
python process_wer_file.py   # parse sclite output to get edit distance alignments
python acoustic_distance.py  # find correlation between acoustic distance and WER
```

# Segment-level analysis
* Get CMU Pronouncing Dictionary
```
wget https://raw.githubusercontent.com/Alexir/CMUdict/master/cmudict-0.7b
mv cmudict-0.7b cmudict-0.7b.txt
python phn_error.py
```
* Analyze common phoneme mistakes and final consonant cluster deletion
```
python g2p_phn_analysis.py
```

# Vowel formants
## CORAAL
* Go into data/coraal and get the full interviews (the TextGrid's are provided for the full interview)
```
./download_full.sh
```
* Generate CSV
```
cd ..  # should be at root of project
echo Filename > data/coraal/full/filenames.csv
find data/coraal/full -name "*.wav" -printf '%f\n' | sed 's/\.wav$//' >> data/coraal/full/filenames.csv
```
    * Manually filter out ROC_se0_ag2_m_01 (_1 ~ _4), ROC_se0_ag3_f_02_2, ROC_se0_ag3_f_02_3 since CORAAL notes that "For ROC, two speakers who were added in version 2020.05 are not included in the alignment"
* Install Praat in the root of this project: https://www.fon.hum.uva.nl/praat/download_linux.html (barren version is fine)
* Run Praat script to extract all vowel formants from the interviews
```
./praat_barren --run analysis/vowels/ExtractFormant.Praat 0 0 data/coraal/full/ data/coraal/aligned/ data/coraal/full/filenames.csv coraal ../../
```
* normalize per speaker with z-score
```
python analysis/vowels/normalize_formants.py
```
* Filter to only include the vowel formants for the word substitutions in the ASR mistakes and the correct substitutions:
```
python analysis/vowel_sub_formants.py --dataset coraal
```
* Plot the formants
```
python analysis/vowels/plot_formants.py
```

## NSP

* Create filenames.csv
```
import pandas as pd
df = pd.read_csv('data/nsp/demographics.txt', sep='\t')
for spk_id in df['Subject Number']:
    spk_id = spk_id.lower()
    print(spk_id + '/' + spk_id + 'I0')
```
* Extract vowel formants for all of NSP
```
./praat_barren --run analysis/vowels/ExtractFormant.Praat 1 2 data/nsp/spont/ data/nsp/spont_aligned/ data/nsp/filenames.csv NSP ../../
```
(word tier is 1, phone tier is 2)
