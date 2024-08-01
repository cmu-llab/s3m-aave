import pandas as pd
 
nsp_file = "matching/util/nsp_matched.csv"
coraal_file = "matching/util/coraal_matched.csv"

def get_word_count(filename:str, column:str):
    """
    Get word counts
    Return dictionary, each key (str) appears >= 2 in utts in filename
    """
    df = pd.read_csv(filename)
    count = dict()
    seen = set()
    for _, row in df.iterrows():
        utt = row[column]
        words = utt.split()
        for word in words:
            if word not in seen:
                seen.add(word)
            else:
                count[word] = count.get(word,1) + 1

    print(filename, ':', len(count))

    return count

nsp_cnt = get_word_count(nsp_file, "transcript")
coraal_cnt = get_word_count(coraal_file, "content")

common_words = set(nsp_cnt.keys()).intersection(set(coraal_cnt.keys()))
print("common words:", len(common_words))
print(list(common_words)[:10])
