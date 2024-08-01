import os
import re
import json
from min_edit import min_edit_distance

path = "cmudict-0.7b.txt"
dict_path = "cmudict-0.7b.json"


def process_phns(phns):
    # remove number
    return re.sub(r'\d', '', phns)

if os.path.exists(dict_path):
    # read dict json
    with open(dict_path) as f:
        eng_dict = json.load(f)
else:
    # read dictionary
    eng_dict = dict()
    cnt = 0 
    with open(path, encoding = "ISO-8859-1") as f:
        lines = f.readlines()

    for line in lines:
        if line[0] == ';':
            continue
        line = line.strip('\n')
        word, phns = line.split('  ')
        phns = process_phns(phns)
        assert word not in eng_dict 
        eng_dict[word] = phns.split()

    words_json = json.dumps(eng_dict)

    with open(dict_path, 'w') as f:
        f.write(words_json)

# read wer-log
with open("wer-log/wer-hubert.json") as f:
    data = json.load(f)

pairs = dict() 

#arr = set()
cnt = 0
for key in data:
    ref, hyp = data[key]
    for i in range(len(ref)):
        #if ref[i] not in eng_dict:
        #    arr.add(ref[i])
        #elif hyp[i] not in eng_dict:
        #    arr.add(hyp[i])

        if ref[i] != hyp[i] and ref[i][0] != '*' and hyp[i][0] != '*' and \
            ref[i].upper() in eng_dict and hyp[i].upper() in eng_dict:
            # only substitution errors
            ref_phns, hyp_phns = eng_dict[ref[i].upper()], eng_dict[hyp[i].upper()]
            #print(ref, ref_phns)
            #print(hyp, hyp_phns)
            distance, alignment = min_edit_distance(hyp_phns, ref_phns)
            phn_err = distance / len(ref_phns)
            if phn_err >= 1:
                #print(ref[i], ref_phns, '|||', hyp[i], hyp_phns, ';', phn_err, distance)
                cnt += 1
                continue
            # analyze
            for pair in alignment:
                if pair[0] != pair[1]:
                    if (pair[1], pair[0]) not in pairs:
                        pairs[(pair[1], pair[0])] = 0
                    pairs[(pair[1], pair[0])] += 1

#                    print(pair[1], " -> ", pair[0])
print(f"Skip {cnt} examples w/ phn err rate >= 1\n")
#print(len(arr))
#print(list(arr)[:10])
pairs_info = [(val, key) for (key, val) in pairs.items()]
pairs_info.sort(reverse=True)
print("--- (frequency) ref phn -> hyp phn ---")
for i in range(100):
    print(pairs_info[i])
