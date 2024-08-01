import torchaudio
import os
import pandas as pd
import tqdm


root, new_root = "segmented/spont", "segmented/16000"
csvfile = "transcript.csv"
df = pd.read_csv(csvfile)
resampler = torchaudio.transforms.Resample(44_100, 16_000)

for index, row in tqdm.tqdm(df.iterrows()):
    spk = row['speaker']
    Id = row['wav'].split('.wav')[0]
    path = f"{root}/{spk}/{spk}I0.wav/{Id}.wav"
    array, fs = torchaudio.load(path)
    assert fs == 44100
    
    new_path = f"{new_root}/{spk}/{Id}.wav"
    os.makedirs(f"{new_root}/{spk}", exist_ok=True)

    resampled = resampler(array) #.squeeze().numpy()
    torchaudio.save(new_path, resampled, 16_000)
