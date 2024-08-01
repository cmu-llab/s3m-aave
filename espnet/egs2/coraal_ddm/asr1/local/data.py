import os
import tqdm
import pandas
from pathlib import Path
from collections import defaultdict


def write_data(utt_id, data, fp):
    fp.write(f"{utt_id} {data}\n")

csvfile = "/ocean/projects/cis210027p/kchang1/aal-ssl/data/coraal/DDM.csv"
df = pandas.read_csv(csvfile)
ddm_utt = set(df['segment_filename'])

# all utterances
    # note: a lot of the utterances annotated with DDM are not in the matched subset
csvfile = "/ocean/projects/cis210027p/kchang1/aal-ssl/data/coraal/CORAAL_transcripts_clean.csv"
df = pandas.read_csv(csvfile)
root = "/ocean/projects/cis210027p/kchang1/aal-ssl/data/coraal/CORAAL_audio_wav"
outdir = "data/test"
os.makedirs(outdir, exist_ok=True)

df = df[df["segment_filename"].isin(ddm_utt)]
# utt2spk needs to be sorted by speaker-id and utterance-id
# CORAAL sorts the utterances by timestamp but espnet wants the above
df = df.sort_values(by=["segment_filename"])

# spk2gender  spk2utt  text  utt2spk  wav.scp
utt2spk_file = open(f"{outdir}/utt2spk", "w")
text_file = open(f"{outdir}/text", 'w')
wavscp_file = open(f"{outdir}/wav.scp", 'w')
spk2utt_file = open(f"{outdir}/spk2utt", 'w')

spk2utt = defaultdict(list)


for index, row in tqdm.tqdm(df.iterrows()):
    text = row['clean_content']
    spk = row['basefile']
    # final number is the audio clip number, not the speaker
    spk = spk.rsplit('_', 1)[0]
    Id = row['segment_filename'].strip('.wav')
    # process filename
    subset = Id.split('_')[0].lower()
    fn = f"{root}/{subset}/{Id}.wav"

    # utt2spk
    # 1272-128104-0000 1272-128104 
    write_data(Id, spk, utt2spk_file)
    write_data(Id, text, text_file)
    write_data(Id, fn, wavscp_file)

    spk2utt[spk].append(Id)


with open(f"{outdir}/spk2utt", 'w') as f:
    for spk, utterances in spk2utt.items():
        f.write(f"{spk} {' '.join(sorted(utterances))}\n")

utt2spk_file.close()
text_file.close()
wavscp_file.close()
spk2utt_file.close()
