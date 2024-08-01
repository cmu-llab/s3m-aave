print('WER')
print('dataset', 'method', 'substitutions (%)', 'deletions (%)', 'insertions (%)')

for dataset in ['coraal', 'sbcsae']:
    for method in ['hubert', 'wav2vec2', 'wavlm', 'xlsr']:
        with open(f'analysis/{dataset}/wer-{method}', 'r') as f:
            lines = f.readlines()
            # example of a line:
                # Scores: (#C #S #D #I) 29 8 1 2
            lines = [line.strip() for line in lines if "Scores: (#C #S #D #I)" in line]
            lines = [line.split("Scores: (#C #S #D #I) ")[1] for line in lines]
            lines = [tuple(line.split()) for line in lines]
        substitutions, deletions, insertions = 0, 0, 0
        for (_, s, d, i) in lines:
            substitutions += int(s)
            deletions += int(d)
            insertions += int(i)
        edits = substitutions + deletions + insertions
        print(dataset, method, "%.2f" % (substitutions / edits), "%.2f" % (deletions / edits), "%.2f" % (insertions / edits))

# coraal hubert 0.67 0.25 0.07
# coraal wav2vec2 0.74 0.18 0.08
# coraal wavlm 0.70 0.22 0.09
# coraal xlsr 0.71 0.22 0.06
# sbcsae hubert 0.48 0.45 0.07
# sbcsae wav2vec2 0.64 0.27 0.09
# sbcsae wavlm 0.45 0.45 0.10
# sbcsae xlsr 0.59 0.34 0.07


print('CER')
print('dataset', 'method', 'substitutions (%)', 'deletions (%)', 'insertions (%)')
for dataset in ['coraal', 'sbcsae']:
    for method in ['hubert', 'wav2vec2', 'wavlm', 'xlsr']:
        with open(f'analysis/{dataset}/cer-{method}', 'r') as f:
            lines = f.readlines()
            # example of a line:
                # Scores: (#C #S #D #I) 29 8 1 2
            lines = [line.strip() for line in lines if "Scores: (#C #S #D #I)" in line]
            lines = [line.split("Scores: (#C #S #D #I) ")[1] for line in lines]
            lines = [tuple(line.split()) for line in lines]
        substitutions, deletions, insertions = 0, 0, 0
        for (_, s, d, i) in lines:
            substitutions += int(s)
            deletions += int(d)
            insertions += int(i)
        edits = substitutions + deletions + insertions
        print(dataset, method, "%.2f" % (substitutions / edits), "%.2f" % (deletions / edits), "%.2f" % (insertions / edits))

print('TER')
print('dataset', 'method', 'substitutions (%)', 'deletions (%)', 'insertions (%)')
for dataset in ['coraal', 'sbcsae']:
    for method in ['hubert', 'wav2vec2', 'wavlm', 'xlsr']:
        with open(f'analysis/{dataset}/ter-{method}', 'r') as f:
            lines = f.readlines()
            # example of a line:
                # Scores: (#C #S #D #I) 29 8 1 2
            lines = [line.strip() for line in lines if "Scores: (#C #S #D #I)" in line]
            lines = [line.split("Scores: (#C #S #D #I) ")[1] for line in lines]
            lines = [tuple(line.split()) for line in lines]
        substitutions, deletions, insertions = 0, 0, 0
        for (_, s, d, i) in lines:
            substitutions += int(s)
            deletions += int(d)
            insertions += int(i)
        edits = substitutions + deletions + insertions
        print(dataset, method, "%.2f" % (substitutions / edits), "%.2f" % (deletions / edits), "%.2f" % (insertions / edits))
