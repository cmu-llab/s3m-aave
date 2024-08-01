import json


def process(sslr):
    data = dict()
    # sclite output
    with open(f"analysis/coraal/wer-{sslr}") as f:
        lines = f.readlines()
        for i in range(len(lines)):
            if lines[i].startswith("id: ("):
                ID = lines[i].strip(')\n').split('-')[-1]
                ref, hyp = lines[i+2].lower(), lines[i+3].lower()

                ref = ref.split()[1:]
                hyp = hyp.split()[1:]

                assert len(ref) == len(hyp), f"{i}, {ref}, {hyp}"

                assert ID not in data, ID
                data[ID] = [ref, hyp]

    with open(f'wer-log/wer-{sslr}.json', 'w') as json_file: 
        json.dump(data, json_file)


for sslr in ["wavlm", "wav2vec2", "xlsr", "hubert"]:
    print(sslr)
    process(sslr)

