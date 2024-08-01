import pandas as pd
from collections import defaultdict
from min_edit import min_edit_distance
from textgrid import TextGrid
import re
import json
import argparse
from g2p_en import G2p
from scipy.io import wavfile
from pathlib import Path
from tqdm import tqdm


def load_pron_dict(dict_path):
    with open(dict_path) as f:
        return json.load(f)


def get_basefile(corpus, utt_id):
    if corpus == "coraal":
        # DCB_se1_ag2_f_01_1_1433172_1439219 -> 'DCB_se1_ag2_f_01_1'
        # remove the timestamps
        return utt_id.rsplit('_', 2)[0]
    elif corpus == "nsp":
        # we8_2948526_3996342 -> we8I0
        return utt_id.split('_')[0] + 'I0'

def get_spk_id(corpus, utt_id):
    if corpus == "coraal":
        # final number is the audio clip number, not the speaker
        # DCB_se1_ag2_f_01_1_1433172_1439219 -> 'DCB_se1_ag2_f_01'
        return utt_id.rsplit('_', 3)[0]
    elif corpus == "nsp":
        # we8_2948526_3996342 -> we8
        return utt_id.split('_')[0]


def get_region(corpus, utt_id):
    if corpus == "coraal":
        # 'DCB_se1_ag2_f_01_1_1433172_1439219' -> 'DCB'
        return utt_id.split('_')[0]
    elif corpus == "nsp":
        # we8_2948526_3996342 -> we
        return utt_id.split('_')[0][:2]


def get_textgrid(corpus, utt_id):
    if corpus == "coraal":
        # ex: data/coraal/aligned/DCB_se1_ag1_f_01_1.TextGrid
        file = "data/coraal/aligned/" + get_basefile(corpus, utt_id) + '.TextGrid'
    elif corpus == "nsp":
        # ex: data/nsp/spont_aligned/at0/at0I0.TextGrid
        file = "data/nsp/spont_aligned/" + get_region(corpus, utt_id) +\
            + "/" + get_spk_id(corpus, utt_id) + '.TextGrid'
    
    return TextGrid(open(file).read())


def is_vowel(phoneme):
    # http://www.speech.cs.cmu.edu/cgi-bin/cmudict
    # https://en.wikipedia.org/wiki/ARPABET
    vowel_set = {
        "AA", "AE", "AH", "AO", "AX", "EH", "IH", "IX", "IY", "UH", "UW", "UX"
    }
    # exclude diphthongs AW, AY, EY, OW, OY and rhotic AXR, ER for now
    return phoneme in vowel_set


def phoneme_error_rate(ref_phns, hyp_phns):
    """
    ref_phns: List[str]
    hyp_phns: List[str]
    """
    return min_edit_distance(ref_phns, hyp_phns) / len(ref_phns)


# def load_full_audio(corpus, utt_id):
#     if corpus == "coraal":
#         return wavfile.read("data/coraal/full/" + get_region(corpus, utt_id) + "/" + utt_id + '.wav')
#     elif corpus == "nsp":
#         return wavfile.read("data/nsp/spont/" + get_region(corpus, utt_id) + "/" + utt_id + '.wav')


def get_timestamp(corpus, utt_id):
    # get timestamp from utterance id
    elems = utt_id.split('_')
    st, end = elems[-2], elems[-1]
    st, end = int(st), int(end)

    if corpus == "coraal":
        # https://github.com/stanford-policylab/asr-disparities/blob/master/src/utils/snippet_generation.py
        # start_time = int((start_time-buffer_val)*1000)
        # end_time = int((end_time+buffer_val)*1000)
        return st / 1000, end / 1000
    
    elif corpus == "nsp":
        # data/nsp/segment.py
        # reported word start = actual word start * frequency
        return st / 44100, end / 44100

    return (st, end)


def get_intervals(corpus, utt_id):
    spk_id = get_spk_id(corpus, utt_id)
    grid = get_textgrid(corpus, utt_id)

    start, end = get_timestamp(corpus, utt_id)
    intervals = []

    if corpus == "coraal":
        phn_tier = list(filter(lambda x: x.nameid == f'{spk_id} - phones', grid.tiers))[0].simple_transcript
        for i, (phn_start, phn_end, phn) in enumerate(phn_tier):
            phn_start, phn_end = float(phn_start), float(phn_end)
            # linear search
            if start - 0.05 <= phn_start <= phn_end <= end + 0.05:
                # note: Praat tiers are 1-indexed, but Python is 0-indexed
                intervals.append((i + 1, phn_start, phn_end, phn))

    return intervals

def get_formants(corpus, formants_df, utt_id, vowel_index):
    # columns of interest:
        # speaker at "recording" - use utt_id base name to get (remove timestamp)
        # "vwl_index": index in the phone tier - might not need specific timestamp
        # "word_intvl": index in the word tier - might not need specific timestamp?
        # "word" - the actual word
    basefile = get_basefile(corpus, utt_id)
    # "vowel": the actual phoneme - note: remove the stress
    try:
        # there will only be one entry per vowel, so vowel_index is unique
        vowel = formants_df[formants_df['vwl_index'] == vowel_index].iloc[0]
    except IndexError:
        print(utt_id, vowel_index)
    return (vowel["f1_50"], vowel["f2_50"])


def investigate(corpus, utt_id, g2p, pron_dict, file):
    spk_id = get_spk_id(corpus, utt_id)
    grid = get_textgrid(corpus, utt_id)

    intervals = []

    start, end = get_timestamp(corpus, utt_id)
    word_tier = list(filter(lambda x: x.nameid == f'{spk_id} - words', grid.tiers))[0].simple_transcript
    phn_tier = list(filter(lambda x: x.nameid == f'{spk_id} - phones', grid.tiers))[0].simple_transcript
    for i, (word_start, word_end, word) in enumerate(word_tier):
        word_start, word_end = float(word_start), float(word_end)
        # linear search
        if start - 0.05 <= word_start <= word_end <= end + 0.05:
            # note: Praat tiers are 1-indexed, but Python is 0-indexed
            intervals.append((i + 1, word_start, word_end, word))

    for _, word_start, word_end, word in intervals:
        # g2p_phonemes = g2p(word)
        pd_phonemes = get_word_phonemes(g2p, pron_dict, word)
        mfa_phonemes = [phn for phn_start, phn_end, phn in phn_tier if word_start <= float(phn_start) < float(phn_end) <= word_end]
        mfa_phonemes = [phn for phn in mfa_phonemes if phn not in {'sp', 'spn', 'sil', 'rdx', ''}]

        if pd_phonemes != mfa_phonemes:
            file.write(word + '\t' + ' '.join(pd_phonemes) + '\t' + ' '.join(mfa_phonemes) + '\n')
            # print(word, g2p_phonemes, mfa_phonemes)


def get_pron_dict():
    file = "~/Documents/MFA/pretrained_models/dictionary/english_us_arpa.dict"
    pron_dict = pd.read_csv(file, sep='\t', header=None)
    return pron_dict


def get_word_phonemes(g2p, pron_dict, word):
    results = pron_dict[pron_dict[0] == word]
    # OOV
    if results.empty:
        return g2p(word)
    else:
        # take highest probability one and break ties using the first one
        return results.sort_values(by=1, ascending=False).iloc[0][5]


def get_hypothesis_phonemes(g2p, pron_dict, hypothesis):
    # use the english_us_arpa pronunciation dict and only fallback on g2p for OOV
    hypothesis = hypothesis.split(" ")
    hyp_phonemes = []
    for word in hypothesis:
        results = pron_dict[pron_dict[0] == word]
        # OOV
        if results.empty:
            hyp_phonemes += g2p(word)
        else:
            # take highest probability one and break ties using the first one
            hyp_phonemes += results.sort_values(by=1, ascending=False).iloc[0][5]
    return hyp_phonemes


if __name__ == "__main__":
    # REQUIRES: vowel formants have been normalized by speaker

    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--dataset", type=str, choices=["coraal", "nsp"], required=True)
    args = parser.parse_args()
    corpus = args.dataset

    # pron_dict = load_pron_dict("analysis/cmudict-0.7b.json")
    g2p = G2p()  # uses CMU Dict, falls back to neural G2P

    # Goal: get the vowel formants for substituted vowels and correct vowels
    #   go through the transcriptions and predictions to get the substituted and correct vowels

    f = open('pron_inconsistencies_english_us_arpa.txt', 'w')
    pron_dict = get_pron_dict()

    # aggregate across each model
    # map region to list of (F1 z-scored, F2 z-scored)
    wrong_vowels, correct_vowels = defaultdict(list), defaultdict(list)

    for sslr in ["wavlm", "wav2vec2", "xlsr", "hubert"]:
        preds_df = pd.read_csv(f"preds/{corpus}/{sslr}.csv")
        for _, row in tqdm(preds_df.iterrows()):
            utt_id, reference, hypothesis = row['segment_filename'], row['reference'], row['prediction']
            spk_id = get_spk_id(corpus, utt_id)
            region = get_region(corpus, utt_id)
            # audio = load_full_audio(corpus, utt_id)
            formants_df = pd.read_csv(f"analysis/vowels/{corpus}/{get_basefile(corpus, utt_id)}_formants.csv")

            # TODO: remove
            investigate(corpus, utt_id, g2p, pron_dict, f)
            continue

            # get phoneme intervals for the current utterance and their index (1-indexed) in the full TextGrid
            intervals = get_intervals(corpus, utt_id)

            hyp_phns = get_hypothesis_phonemes(g2p, hypothesis)
            # ref phones from CORAAL forced alignment
                # use timestamp to zero in on the TextGrid
                # even though reference comes from CMU Dict ref_phns will not be the same as the forced alignment b/c the latter contains silence
                # forced alignment also has OOVs, which drops many phones
                # just get the phones from CORAAL
            # ref_phns = g2p(reference)
            ref_phns = [phn for _, _, _, phn in intervals if phn not in {'sp', 'spn', 'sil', 'rdx', ''}]

            # remove stress
            hyp_phns = [re.sub(r'\d', '', p) for p in hyp_phns]
            ref_phns = [re.sub(r'\d', '', p) for p in ref_phns]

            # while we could keep spaces to preserve word boundaries, 
            # the spacing is not necessarily aligned between hyp, ref words
                # the predictions could break a word into two  
            # remove spaces
            hyp_phns = [p for p in hyp_phns if p != ' ']
            ref_phns = [p for p in ref_phns if p != ' ']

            _, phoneme_alignment = min_edit_distance(ref_phns, hyp_phns)

            # for ref_p, hyp_p in phoneme_alignment:
            #     if is_vowel(hyp_p) and is_vowel(ref_p) and hyp_p != ref_p:
            #         print(hyp_p, ref_p, 'substitution')

            # follow the forced alignment for the utterance and skip 'spn'
                # two pointers (one on the intervals, one on the ref)
            phoneme_idx = 0
            for interval_idx, _, _, phn in intervals:
                phn = re.sub(r'\d', '', phn)

                # silence (sil), out of vocab word (spn)
                if len(phn) == 0 or phn in {'spn', 'sil', 'sp'}:
                    # only move the intervals pointer
                    continue

                # forced alignment could be missing words due to OOV (spn)
                    # but we take the forced alignment as the reference - shouldn't be issues

                (ref_p, hyp_p) = phoneme_alignment[phoneme_idx]
                # focus on vowel substitutions; exclude deletions
                while (phoneme_idx < len(phoneme_alignment)) and (ref_p == "*" or ref_p == "sp"):
                    # move the ref pointer
                    phoneme_idx += 1
                    (ref_p, hyp_p) = phoneme_alignment[phoneme_idx]
                # exclude insertions
                if hyp_p == "*" or hyp_p == " " or not is_vowel(hyp_p) or not is_vowel(ref_p):
                    # move the ref pointer and the ref pointer?
                    phoneme_idx += 1
                    continue

                # convert phoneme index in the reference phoneme list to index in segment tier of TextGrid
                ref_f1, ref_f2 = get_formants(corpus, formants_df, utt_id, interval_idx)
                hyp_f1, hyp_f2 = get_formants(corpus, formants_df, utt_id, interval_idx)

                if ref_p == hyp_p:
                    correct_vowels[region].append((ref_p, ref_f1, ref_f2))
                else:
                    # substitution
                    wrong_vowels[region].append((hyp_p, hyp_f1, hyp_f2))

                # move the ref pointer
                phoneme_idx += 1

    # for region, formant_list in correct_vowels.items():
    #     Path(f"analysis/vowels/{corpus}/{region}").mkdir(parents=True, exist_ok=True)
    #     with open(f"analysis/vowels/{corpus}/{region}/correct.csv", "w") as f:
    #         f.write("phn,f1,f2\n")
    #         for p, f1, f2 in formant_list:
    #             f.write(p)
    #             f.write(",")
    #             f.write(str(f1))
    #             f.write(",")
    #             f.write(str(f2))
    #             f.write("\n")

    # for region, formant_list in wrong_vowels.items():
    #     Path(f"analysis/vowels/{corpus}/{region}").mkdir(parents=True, exist_ok=True)
    #     with open(f"analysis/vowels/{corpus}/{region}/substituted.csv", "w") as f:
    #         f.write("phn,f1,f2\n")
    #         for p, f1, f2 in formant_list:
    #             f.write(p)
    #             f.write(",")
    #             f.write(str(f1))
    #             f.write(",")
    #             f.write(str(f2))
    #             f.write("\n")
