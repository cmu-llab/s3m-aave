# Copy predictions for the 150 CORAAL utterances annotated with DDM


# DDM
cp /ocean/projects/cis210027p/kchang1/espnet/egs2/coraal_ddm/asr1/exp/asr_train_asr_hubert_large_lm_raw_en_bpe5000/decode_asr_asr_model_valid.loss.ave/test/text coraal_ddm/hubert
cp /ocean/projects/cis210027p/kchang1/espnet/egs2/coraal_ddm/asr1/exp/asr_train_asr_wav2vec2_large_lm_raw_en_bpe5000/decode_asr_asr_model_valid.loss.ave/test/text coraal_ddm/wav2vec2
cp /ocean/projects/cis210027p/kchang1/espnet/egs2/coraal_ddm/asr1/exp/asr_train_asr_wavlm_lm_raw_en_bpe5000/decode_asr_asr_model_valid.loss.ave/test/text coraal_ddm/wavlm
cp /ocean/projects/cis210027p/kchang1/espnet/egs2/coraal_ddm/asr1/exp/asr_train_asr_xlsr_lm_raw_en_bpe5000/decode_asr_asr_model_valid.loss.ave/test/text coraal_ddm/xlsr
cp /ocean/projects/cis210027p/kchang1/espnet/egs2/coraal_ddm/asr1/exp/asr_train_asr_fbank_lm_raw_en_bpe5000/decode_asr_asr_model_valid.loss.ave/test/text coraal_ddm/fbank


# TER
cp /ocean/projects/cis210027p/kchang1/espnet/egs2/coraal_ddm/asr1/exp/asr_train_asr_hubert_large_lm_raw_en_bpe5000/decode_asr_asr_model_valid.loss.ave/test/token coraal_ddm/hubert-ter
cp /ocean/projects/cis210027p/kchang1/espnet/egs2/coraal_ddm/asr1/exp/asr_train_asr_wav2vec2_large_lm_raw_en_bpe5000/decode_asr_asr_model_valid.loss.ave/test/token coraal_ddm/wav2vec2-ter
cp /ocean/projects/cis210027p/kchang1/espnet/egs2/coraal_ddm/asr1/exp/asr_train_asr_wavlm_lm_raw_en_bpe5000/decode_asr_asr_model_valid.loss.ave/test/token coraal_ddm/wavlm-ter
cp /ocean/projects/cis210027p/kchang1/espnet/egs2/coraal_ddm/asr1/exp/asr_train_asr_xlsr_lm_raw_en_bpe5000/decode_asr_asr_model_valid.loss.ave/test/token coraal_ddm/xlsr-ter
cp /ocean/projects/cis210027p/kchang1/espnet/egs2/coraal_ddm/asr1/exp/asr_train_asr_fbank_lm_raw_en_bpe5000/decode_asr_asr_model_valid.loss.ave/test/token coraal_ddm/fbank-ter
