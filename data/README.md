
## CORAAL
```
cd data
python preprocess_coraal.py
./coraal/mp3_to_wav.sh
```


## NSP
* Please contact Cynthia Clopper to download NSP (https://u.osu.edu/nspcorpus/)
* Download MFA https://montreal-forced-aligner.readthedocs.io/en/latest/

```
cd data
cd nsp
./download.sh
./preprocess.sh
# forced alignment
mfa validate PATH_TO_aal-ssl/data/nsp/spont english_us_arpa english_us_arpa
mfa align PATH_TO_aal-ssl/data/nsp/spont english_us_arpa english_us_arpa ~/fairness/aal-ssl/data/nsp/spont_aligned --clean --beam 100 --config_path PATH_TO_aal-ssl/data/nsp/nsp.yaml
python segment.py
cd ..
python preprocess_nsp.py
# downsample from 48 kHz to 16 kHz
cd nsp
python resample.py
```
