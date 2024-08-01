import pandas as pd
import re
from preprocess import normalize_text


def remove_markers(line, markers):
    # Remove any text within markers, e.g. 'We(BR) went' -> 'We went'
    # markers = list of pairs, e.g. ['()', '[]'] denoting breath or noise in transcripts
    for s, e in markers:
        line = re.sub(" ?\\" + s + "[^" + e + "]+\\" + e, "", line)
    return line

def remove_annotations(transcript):
    # Replace original unmatched CORAAL transcript square brackets with squiggly bracket
    transcript = transcript.replace('\[','\{')
    transcript = transcript.replace('\]','\}')

    # remove CORAAL unintelligible flags
    transcript = re.sub("\/(?i)unintelligible\/",'',''.join(transcript))
    transcript = re.sub("\/(?i)inaudible\/",'',''.join(transcript))
    transcript = re.sub('\/RD(.*?)\/', '',''.join(transcript))
    transcript = re.sub('\/(\?)\1*\/', '',''.join(transcript))
    transcript = transcript.replace('/', '')

    # remove nonlinguistic markers
    transcript = remove_markers(transcript, ['<>', '()', '{}'])

    # remove remaining floating non-linguistic words (CORAAL)
    single_paren = ['<','>']
    for paren in single_paren:
        linguistic_words  = [word for word in transcript.split() if paren not in word]
        transcript = ' '.join(linguistic_words)

    return transcript


coraal = pd.read_csv('coraal/CORAAL_transcripts.csv')
coraal = coraal.drop(["google_transcription","ibm_transcription","amazon_transcription","msft_transcription","apple_transcription"], axis=1)

coraal["clean_content"] = coraal["content"].apply(remove_annotations)
coraal["clean_content"] = coraal["clean_content"].apply(normalize_text)

coraal = coraal.drop(["content"], axis=1)
coraal.to_csv('coraal/CORAAL_transcripts_clean.csv', index=None)
