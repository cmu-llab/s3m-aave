#!/usr/bin/env bash
# Set bash to 'debug' mode, it will exit on :
# -e 'error', -u 'undefined variable', -o ... 'error in pipeline', -x 'print commands',
set -e
set -u
set -o pipefail

train_set="train_clean_100"
valid_set="dev"
test_sets="test_clean"

frontend=hubert_large
asr_config=conf/tuning/train_asr_${frontend}.yaml
inference_config=conf/decode_asr.yaml

./asr.sh \
    --lang en \
    --stage 6 \
    --ngpu 1 \
    --nbpe 5000 \
    --use_lm false \
    --max_wav_duration 30 \
    --speed_perturb_factors "0.9 1.0 1.1" \
    --feats_normalize utt_mvn \
    --asr_config "${asr_config}" \
    --asr_stats_dir "exp/asr_stats_raw_en_bpe5000_sp_${frontend}" \
    --inference_config "${inference_config}" \
    --inference_asr_model "valid.loss.ave.pth" \
    --train_set "${train_set}" \
    --valid_set "${valid_set}" \
    --test_sets "${test_sets}" \
    --lm_train_text "data/${train_set}/text data/local/other_text/text" \
    --bpe_train_text "data/${train_set}/text" "$@"

#--stop_stage 11 \
