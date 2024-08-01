import os
import re
import json
from min_edit import min_edit_distance
from g2p_en import G2p 
from arpa2ipa import arpa_to_ipa
import tqdm

g2p = G2p()


def process_phns(phns):
    # remove number
    if type(phns) == str:
        phns = re.sub(r'\d', '', phns)
        #phns = re.sub(r'\s+', ' ', phns)
        phns = phns.replace("'", '') 
        phns = arpa_to_ipa(phns)
        return phns.split(' ')
    ret = []
    for phn in phns:
        if phn == "'":
            continue
        phn = re.sub(r'\d', '', phn)
        ret.append(arpa_to_ipa(phn))
    return ret 

def get_consonants(fn="cmudict-0.7b.phones"):
    consonants = set()
    with open(fn) as f:
        for line in f:
            ph, ph_type = line.strip('\n').split('\t')
            if ph_type != "vowel":
                consonants.add(ph)
    print("# of consonants:", len(consonants))
    return consonants

if __name__ == "__main__":
    consonants = get_consonants()

    # read wer-log
    cluster_del = dict()
    pairs = dict()

    for sslr in ["hubert"]: #, "wav2vec2", "wavlm", "xlsr"]:
        with open("wer-log/wer-hubert.json") as f:
            data = json.load(f)

        for key in tqdm.tqdm(data):
            ref, hyp = data[key]
            ref_text, hyp_text = ' '.join(ref), ' '.join(hyp)
            ref_phns, hyp_phns = g2p(ref_text), g2p(hyp_text)
            #ref_phns, hyp_phns = ' '.join(ref_phns), ' '.join(hyp_phns)
            ref_phns, hyp_phns = process_phns(ref_phns), process_phns(hyp_phns)

            distance, alignment = min_edit_distance(ref_phns, hyp_phns)
            """
            # final consonant cluster deletion
            if len(ref_phns) >= 2 and ref_phns[-2] in consonants and ref_phns[-1] in consonants and ref_phns[:-1] == hyp_phns:
                #print(ref_phns, hyp_phns)
                cluster = ref_phns[-2] + ' ' + ref_phns[-1]
                if cluster not in cluster_del:
                    cluster_del[cluster] = 0
                cluster_del[cluster] += 1
            """
            for j, pair in enumerate(alignment):
                if pair[0] != pair[1] and pair[0] != '' and pair[1] != '':
                    # any pair
                    if (pair[0], pair[1]) not in pairs:
                        pairs[(pair[0], pair[1])] = 0
                    pairs[(pair[0], pair[1])] += 1
                    # cluster deletion
                    if pair[1] == '*' and j > 0 and alignment[j-1][0] == alignment[j-1][1] and alignment[j-1][0] != '' and \
                        (j >= len(alignment)-1 or alignment[j+1][0] == ''):
                        if (alignment[j-1][0], pair[0]) not in cluster_del:
                            cluster_del[(alignment[j-1][0], pair[0])] = 0
                        cluster_del[(alignment[j-1][0], pair[0])] += 1

    #                    print(pair[1], " -> ", pair[0])
    #print(len(arr))
    #print(list(arr)[:10])

    pairs_info = [(val, key) for (key, val) in pairs.items()]
    pairs_info.sort(reverse=True)
    print("--- (frequency) ref phn -> hyp phn ---")
    for i in range(50):
        print(pairs_info[i])

    print('='*100)
    #print(cluster_del)
    cluster_info = [(val, key) for (key, val) in cluster_del.items()]
    cluster_info.sort(reverse=True)
    for c in cluster_info:
        print(c)

