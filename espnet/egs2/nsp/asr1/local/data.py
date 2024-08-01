import os
import tqdm
import pandas
from pathlib import Path
from collections import defaultdict


# prereq: mkdir downloads
# prereq: cp -r PATH_TO_aal-ssl_REPO/data/nsp/segmented downloads

def write_data(utt_id, data, fp):
    fp.write(f"{utt_id} {data}\n")

# need to use the speaker matched version
csvfile = "/ocean/projects/cis210027p/kchang1/aal-ssl/matching/nsp_matched.csv"
df = pandas.read_csv(csvfile)
root = "downloads/segmented/16000"
outdir = "data/test"
os.makedirs(outdir, exist_ok=True)

# spk2utt  text  utt2spk  wav.scp
text_file = open(f"{outdir}/text", 'w')
wavscp_file = open(f"{outdir}/wav.scp", 'w')
utt2spk_file = open(f"{outdir}/utt2spk", 'w')

spk2utt = defaultdict(list)

# utt2spk needs to be sorted by speaker-id and utterance-id
df = df.sort_values(by=["wav"])

for index, row in tqdm.tqdm(df.iterrows()):
    text = row['transcript']
    spk = row['speaker']
    Id = row['wav'].split('.wav')[0]
    # process filename
    fn = f"{root}/{spk}/{Id}.wav"

    write_data(Id, text, text_file)
    write_data(Id, fn, wavscp_file)
    # utt2spk: at0_10872414_11447478 at0
    write_data(Id, spk, utt2spk_file)

    spk2utt[spk].append(Id)

with open(f"{outdir}/spk2utt", 'w') as f:
    for spk, utterances in spk2utt.items():
        f.write(f"{spk} {' '.join(sorted(utterances))}\n")


text_file.close()
wavscp_file.close() 
utt2spk_file.close()
