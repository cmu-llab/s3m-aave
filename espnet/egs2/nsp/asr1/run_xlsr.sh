#!/usr/bin/env bash
# Set bash to 'debug' mode, it will exit on :
# -e 'error', -u 'undefined variable', -o ... 'error in pipeline', -x 'print commands',
set -e
set -u
set -o pipefail

test_sets="test"

frontend=xlsr
asr_config=conf/tuning/train_asr_${frontend}.yaml
inference_config=conf/decode_asr.yaml

./asr.sh \
    --lang en \
    --stage 12 \
    --skip_train true \
    --gpu_inference true \
    --ngpu 1 \
    --nbpe 5000 \
    --use_lm false \
    --max_wav_duration 30 \
    --feats_normalize utt_mvn \
    --asr_config "${asr_config}" \
    --inference_config "${inference_config}" \
    --inference_asr_model "valid.loss.ave.pth" \
    --test_sets "${test_sets}" "$@" 
