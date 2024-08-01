import jiwer
import pandas as pd
from pathlib import Path
from collections import Counter


def get_edits(reference, hypothesis, cer=False):
    """
    reference: str
    hypothesis: str

    Adapted from visualize_alignment, _construct_comparison_string (https://github.com/jitsi/jiwer/blob/master/jiwer/alignment.py)

    Returns (substitutions, insertions, deletions) where each is a list
        of (ref, hyp) words
    """
    if cer:
        # assumes '#' never shows up in predictions
        reference = reference.replace(" ", "#")
        reference = " ".join(reference).replace("#", "<space>")
        hypothesis = hypothesis.replace(" ", "#")
        hypothesis = " ".join(hypothesis).replace("#", "<space>")
    output = jiwer.process_words(reference, hypothesis)
    references = output.references
    hypothesis = output.hypotheses
    alignment = output.alignments

    substitutions, insertions, deletions = [], [], []
    for idx, (reference, hypothesis, chunks) in enumerate(zip(references, hypothesis, alignment)):
        for op in chunks:
            # use the indices of the edits to partition the string
            # ignore op.type == "equal"
            if op.type == "substitute":
                ref = reference[op.ref_start_idx : op.ref_end_idx]
                hyp = hypothesis[op.hyp_start_idx : op.hyp_end_idx]
                for r, h in zip(ref, hyp):
                    substitutions.append((r, h))
            elif op.type == "delete":
                ref = reference[op.ref_start_idx : op.ref_end_idx]
                hyp = ["*" for _ in range(len(ref))]
                for r, h in zip(ref, hyp):
                    deletions.append((r, h))
            elif op.type == "insert":
                hyp = hypothesis[op.hyp_start_idx : op.hyp_end_idx]
                ref = ["*" for _ in range(len(hyp))]
                for r, h in zip(ref, hyp):
                    insertions.append((r, h))

    return substitutions, insertions, deletions


def write_common_edits(filename, substitutions, insertions, deletions):
    with open(filename, 'w') as f:
        f.write('substitutions (ref -> hyp)\n')
        for sub, count in substitutions.most_common(60):
            (r, h) = sub
            f.write(r + ' -> ' + h)
            f.write('\t')
            f.write(str(count))
            f.write('\n')
        f.write('\n')
        f.write('insertions (ref -> hyp)\n')
        for ins, count in insertions.most_common(30):
            (r, h) = ins
            f.write(r + ' -> ' + h)
            f.write('\t')
            f.write(str(count))
            f.write('\n')
        f.write('deletions (ref -> hyp)\n')
        for dels, count in deletions.most_common(30):
            (r, h) = dels
            f.write(r + ' -> ' + h)
            f.write('\t')
            f.write(str(count))
            f.write('\n')


for level in ['word', 'subword']:
    for corpus in ['coraal', 'nsp']:
        corpus_substitutions, corpus_insertions, corpus_deletions = Counter(), Counter(), Counter()
        for method in ['hubert', 'wav2vec2', 'wavlm', 'xlsr', 'fbank']:
            file_suffix = '_tokens' if level == 'subword' else ''
            preds = pd.read_csv(f'preds/{corpus}/{method + file_suffix}.csv')
        
            labels = list(preds['reference'])
            predictions = list(preds['prediction'])
            assert len(labels) == len(predictions)

            # sometimes, there are empty hypotheses
            new_labels, new_preds = [], []
            for label, pred in zip(labels, predictions):
                if not pd.isna(label) and not pd.isna(pred) and len(label) > 0 and len(pred) > 0:
                    new_labels.append(label)
                    new_preds.append(pred)

            out = jiwer.process_words(new_labels, new_preds)
            Path(f"analysis/{corpus}/{method}").mkdir(parents=True, exist_ok=True)
            metric = 'wer' if level == 'word' else 'ter'
            with open(f'analysis/{corpus}/{method}/{metric}.txt', 'w') as f:
                f.write(jiwer.visualize_alignment(out, show_measures=False))

            if level == 'word':
                print(method, corpus, 'wer', jiwer.wer(new_labels, new_preds))
                print(method, corpus, 'cer', jiwer.cer(new_labels, new_preds))

                out = jiwer.process_characters(new_labels, new_preds)
                Path(f"analysis/{corpus}/{method}").mkdir(parents=True, exist_ok=True)
                with open(f'analysis/{corpus}/{method}/cer.txt', 'w') as f:
                    f.write(jiwer.visualize_alignment(out, show_measures=False))
            else:
                print(method, corpus, 'ter', jiwer.wer(new_labels, new_preds))

            # find the most common word/subword edits
            substitutions, insertions, deletions = Counter(), Counter(), Counter()
            for label, pred in zip(new_labels, new_preds):
                sub, ins, dels = get_edits(label, pred)
                substitutions.update(Counter(sub))
                insertions.update(Counter(ins))
                deletions.update(Counter(dels))

            # only count SSL edits
            if method != 'fbank':
                corpus_substitutions.update(substitutions)
                corpus_insertions.update(insertions)
                corpus_deletions.update(deletions)

            Path(f"analysis/{corpus}/{method}").mkdir(parents=True, exist_ok=True)
            write_common_edits(f'analysis/{corpus}/{method}/{level}_edits', substitutions, insertions, deletions)

        # TODO: find the most common character deletions
        
        # corpus-level
        write_common_edits(f'analysis/{corpus}/{level}_edits', corpus_substitutions, corpus_insertions, corpus_deletions)
