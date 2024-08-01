import pandas as pd
from nltk import ngrams


def valid(candidate, st, end):
    xmin = candidate.split("xmin = ")[1].split('\n')[0]
    xmax = candidate.split("xmax = ")[1].split('\n')[0]
    xmin, xmax = float(xmin), float(xmax)

    if st <= xmin and xmax <= end:
        return xmin, xmax 
    return -1, -1

def extract(extracted, word, st, end):
    extracted = extracted.split("intervals [")    
    extracted = [ext for ext in extracted if word in ext]
    
    ret = []
    for ext in extracted:
        subst, subend = valid(ext, st, end)
        if subst != -1: 
            ret.append((subst-st, subend-st))
    
    return ret 

def find_aave_timestamp(row, word):
    region = row["source"]
    base = row["segment_filename"].strip('.wav')
    elems = base.split('_')
    st, end = elems[-2], elems[-1]
    st, end = int(st) / 1000, int(end) / 1000
    
    grid_base = row["basefile"] 
    coraal_grid_fn = f"textgrid/{region}_MFA_2019.06.19/{grid_base}.TextGrid"
    with open(coraal_grid_fn) as f:
        words = f.read()

    # whole textgrid
    extracted = words.split("item [3]:")[1].split("item [4]")[0]
    ret = extract(extracted, word, st, end) 
    if ret == []: 
        extracted = extracted.split("intervals [")    
        extracted = [ext for ext in extracted if word in ext]
        return None, ret 

    region = region.lower()
    fn = f"aal-ssl/data/coraal/CORAAL_audio_wav/{region}/{base}.wav"

    return fn, ret

def find_nsp_timestamp(row, word):
    spk, wav = row["speaker"], row["wav"]
    nsp_grid_fn = f"textgrid/spont_aligned_backup/{spk}/{spk}I0.TextGrid"
    with open(nsp_grid_fn) as f:
        words = f.read()

    fn = f"aal-ssl/data/nsp/segmented/16000/{spk}/{wav}"

    _, st, end = wav.strip('.wav').split('_')
    st, end = int(st) / 44100, int(end) / 44100
    str_st, str_end = f"xmin = {st}", f"xmax = {end}"

    extracted = words.split("item [1]:")[1].split("item [2]")[0]
    ret = extract(extracted, word, st, end)

    if ret == []:
        extracted = extracted.split("intervals [")    
        extracted = [ext for ext in extracted if word in ext]
        return None, ret

    return fn, ret


if __name__ == "__main__":
    coraal = "aal-ssl/matching/coraal_matched.csv"
    nsp = "aal-ssl/matching/nsp_matched.csv"

    coraal_df = pd.read_csv(coraal)
    # ,DCB_se1_ag2_f_01_1_179711_185563.wav, The people. The neighborhood, like all of that
    nsp_df = pd.read_csv(nsp)
    # ,speaker,region,wav,transcript,duration,age,gender
    # 0,we8,we,we8_243432_599319.wav,and so i spent like twelve years there moving around but it's a nice place to live i guess it's kind of busy fast paced,8.07,21,Female

    n = 1
    cnt = 0
    with open("common_word.txt", 'w') as out:
        out.write("index,word,NSP filename,NSP start,NSP end,CORAAL filename,CORAAL start,CORAAL end\n")

        for (i1, row1), (i2, row2) in zip(coraal_df.iterrows(), nsp_df.iterrows()):
            aa_words = row1["clean_content"].lower().split()
            sa_words = row2["clean_content"].lower().split()

            aa_grams = set(ngrams(aa_words, n))
            sa_grams = set(ngrams(sa_words, n))
            commons = aa_grams & sa_grams
            if len(commons) == 0:
                continue

            for ngram in commons:
                word = ' '.join(ngram)
                # TODO: skip filler word (uh, the)?
                if len(word) == 1 or word in {"um", "uh", "yeah", "like"}:      # i, a
                    continue

                # find timestamp
                aave_fn, aave_ret = find_aave_timestamp(row1, f"\"{word}\"")
                nsp_fn, nsp_ret = find_nsp_timestamp(row2, f"\"{word}\"")
                if aave_fn is None or nsp_fn is None:
                    continue
                #print(aave_ret)
                #print(nsp_ret)
                print(word)
                for aave_timestamp in aave_ret:
                    aave_st, aave_end = aave_timestamp
                    for nsp_timestamp in nsp_ret:
                        nsp_st, nsp_end = nsp_timestamp
                        out.write(f"{i1},{word},{nsp_fn},{nsp_st},{nsp_end},{aave_fn},{aave_st},{aave_end}\n")


            cnt += 1
            #if cnt > 10:
            #    exit(1)
