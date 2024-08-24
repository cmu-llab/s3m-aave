# Summary
* LibriSpeech: training
* CORAAL: zero-shot inference
* NSP: zero-shot inference
* CORAAL (DDM): zero-shot inference

# Instructions
* Setup ESPnet in another directory (https://espnet.github.io/espnet/installation.html ; conda setup is recommended)
* ```. ./activate_python.sh && ./installers/install_s3prl.sh``` to use SSLRs
```
./egs2/TEMPLATE/asr1/setup.sh egs2/coraal/asr1
./egs2/TEMPLATE/asr1/setup.sh egs2/nsp/asr1
./egs2/TEMPLATE/asr1/setup.sh egs2/coraal_ddm/asr1
```
Copy the files from the {coraal,coraal_ddm,librispeech,nsp} models in this repo to ESPnet.

Copy the wav files from data/nsp, data/coraal/
```
cd egs2/coraal/asr1
mkdir downloads
cp -r PATH_TO_aal-ssl_REPO/data/coraal/CORAAL_audio_wav downloads
cd ../../nsp/asr1
mkdir downloads
cp -r PATH_TO_aal-ssl_REPO/data/nsp/segmented/16000 downloads
```

```
cp /ocean/projects/cis230078p/kchang1/librispeech/asr1/data/en_token_list/bpe_unigram5000/bpe.model
```

Modify the basefiles in local/data.py for each dataset in ESPnet with your path.


For inference, the config.yaml and model file needs to be there
* Copy config.yaml
* Copy valid.loss.ave.path

```
. ./path.sh  # to activate conda env's python
python local/data.py  # to generate data/test
```

Format wav.scp: run stage 3 only (Kaldi formatting)
```
./run_wavscp.sh
```

Inference:
```
./run_fbank.sh
./run_hubert.sh
./run_xlsr.sh
./run_wavlm.sh
./run_wav2vec2.sh
```

# LibriSpeech training steps in ESPnet
https://github.com/espnet/espnet/tree/master/egs2/librispeech_100/asr1
* Copy our LibriSpeech training configurations in ```conf/tuning``` to ESPnet
* run.sh to prepare LibriSpeech data and train
