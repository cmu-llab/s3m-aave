#!/usr/bin/env bash
# Set bash to 'debug' mode, it will exit on :
# -e 'error', -u 'undefined variable', -o ... 'error in pipeline', -x 'print commands',
set -e
set -u
set -o pipefail

./asr.sh \
    --lang en \
    --stage 3 \
    --stop_stage 4 \
    --skip_train true \
    --gpu_inference true \
    --ngpu 1 \
    --nbpe 5000 \
    --use_lm false \
    --max_wav_duration 30 \
    --feats_normalize utt_mvn \
    --test_sets "test" "$@" 
