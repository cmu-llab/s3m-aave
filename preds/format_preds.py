import pandas as pd
import sentencepiece as spm


sp = spm.SentencePieceProcessor(model_file='analysis/bpe.model')
for dataset in ["coraal_ddm", "coraal", "nsp"]:
    for method in ["hubert", "wav2vec2", "wavlm", "xlsr", "fbank"]:
        # words
        preds = pd.read_csv(f"preds/{dataset}/{method}", header=None, names=["temp"])
        # split on first space into filename and prediction
        preds[["segment_filename","prediction"]] = preds["temp"].str.split(" ", n=1, expand=True)
        preds = preds.drop(["temp"], axis=1)
        ref = pd.read_csv(f"preds/{dataset}/ref", header=None, names=["temp"])
        ref[["segment_filename","reference"]] = ref["temp"].str.split(" ", n=1, expand=True)
        ref = ref.drop(["temp"], axis=1)
        # convert reference to uppercase
        ref["reference"] = ref["reference"].str.upper()
        merged = preds.merge(ref, on='segment_filename')
        merged.to_csv(f"preds/{dataset}/{method}.csv", index=False)

        # tokens
        preds = pd.read_csv(f"preds/{dataset}/{method}-ter", header=None, names=["temp"])
        # split on first space into filename and prediction
        preds[["segment_filename","prediction"]] = preds["temp"].str.split(" ", n=1, expand=True)
        preds = preds.drop(["temp"], axis=1)
        
        # use word-level reference, already converted to uppercase
        def tokenize(ref_sent):
            return " ".join(sp.encode(ref_sent, out_type=str))
        ref["reference"] = ref["reference"].map(tokenize)
        
        full_ter = preds.merge(ref, on='segment_filename')
        full_ter.to_csv(f"preds/{dataset}/{method}_tokens.csv", index=False)
