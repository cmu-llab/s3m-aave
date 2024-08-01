import glob
import re
import pandas as pd
from preprocess import normalize_text


# run before forced alignment

for transcript_file in glob.glob("nsp/spont/*/*_original.txt"):
    with open(transcript_file, "r") as f:
        lines = f.readlines()

    normalized_lines = []
    
    for line in lines:
        line = line.strip()
        speaker, transcription = "", ""
        if len(line) == 0:
            normalized_lines.append(line)
            continue
        elif line in ["(end)", "[end]"]:
            # remove "(end) and [end]"
            continue
        elif re.search(r"[0-9]:[0-9][0-9]", line[:4]):
            # line starts with timestamp
            # remove the timestamp
            transcription = line[4:].strip()
        else:
            transcription = line

        # possible to have both timestamp and speaker on same line
        if "cc:" in transcription[:3]:
            speaker = "interviewer"
            transcription = transcription[3:].strip()
        elif re.search(r"[a-z][a-z][0-9]:", transcription[:4]):
            speaker = transcription[:3]
            transcription = transcription[4:].strip()
        else:
            raise Exception("malformatted line")

        
        # See NSP readme file


        # ensure all timestamps removed
        assert re.match(r"[0-9] [0-9][0-9]$", transcription) is None

        # ensure (end) removed
        assert "(end)" not in transcription
        
        # remove dash for dysfluency
            # MFA says brackets can be used for dysfluency, but it converts all brackets to [bracketed], losing the content
            # then add a space
            # TODO: listen
        transcription = re.sub(r"([A-Za-z0-9]+)\-", r"\1 ", transcription)
        

        # parentheses
        # remove (p) - pause
        transcription = transcription.replace("(p)", "")
        # remove (  ) - "indistinct words"
            # 53 instances; lots of single words and mostly from the interviewer
            # still see annotations like (laugh), (microphone noise) that should be in brackets
        transcription = transcription.replace("(laugh)", "[laugh]")
        transcription = transcription.replace("(inaudible)", "")
        transcription = transcription.replace("(click)", "")
        transcription = transcription.replace("(mic noise)", "")
        transcription = transcription.replace("(microphone noise)", "")
        transcription = transcription.replace("(mouth noise)", "")
        transcription = transcription.replace("(inhale)", "")
        transcription = transcription.replace("(sniff)", "")
        transcription = transcription.replace("(negative)", "")

        #   if not an annotation, possible dysfluency - remove parens
            # TODO: listen?
        transcription = transcription.replace("(", "").replace(")", "")

        # remove asterisk (whispered speech)
        transcription = transcription.replace("*", "")

        # brackets - "non-speech sounds"
            # remove the annotations
            # but the rest are actual words, perhaps dysfluency - keep in brackets
        for annotation in [
            "[microphone noise]",
            "[sound with mouth]",
            "[breath]",
            "[clear throat]",
            "[utterance noise]",
            "[microphone bump]",
            "[mic noise]",
            "[mic]",
            "[big microphone noise]",
            "[loud microphone noise]",
            "[loud exhale]",
            "[exhaling, laugh]",
            "[exhale]",
            "[inhale]",
            "[exhaling]",
            "[breathing]",
            "[stretching noise]",
            "[sniffle]",
            "[sniff]",
            "[mouth noise]",
            "[swallow]",
            "[click]",
            "[cough]",
            "[sigh]",
            "[click click click click]",
            "[throat clearing]",
            "[tape cuts off there.]",
            "[recording ends]",
        ]:
            transcription = transcription.replace(annotation, "")

        # remove double spaces
        transcription = transcription.replace("  ", " ")


        # keep [laugh] since Montreal Forced Aligner recognizes this

        # keep overlapping speech (in //) so we can exclude it after the alignment
            # MFA will preserve the //

        # removes punctuation and normalizes remaining numbers
        #   also normalizes 'cause -> because
        #   but preserves 'em
        transcription = normalize_text(transcription)

        # misspellings - perform after text normalization since there might be punctuation
        misspelled = [
            ('philedelphia', 'philadelphia'),
            ('philidelphia', 'philadelphia'),
            ('barbeque', 'barbecue'),
            ('individal', 'individual'),
            ('diverisity', 'diversity'),
            ('greatneck', 'great neck'),
            ('defiitely', 'definitely'),
            ('subrub', 'suburb'),
            ("soit's", "so it's"),
            ("sobut", 'so but'),
            ("sowe'll", "so we'll")
        ]
        split_words = transcription.split()
        for before, after in misspelled:
            split_words = [x if x.lower() != before else after for x in split_words]
        transcription = ' '.join(split_words)

        # need to preserve the speaker ID and "cc" since this is how we know who is talking
        # put "cc" / speaker_id in brackets So it’s an annotation
        # wrap in // to avoid being lost
            # will be treated as silence anyway
        normalized_lines.append(f"/[{speaker}]/ " + transcription)

    # save the transcripts
    with open(transcript_file.replace("_original", ""), 'w') as f:
        for line in normalized_lines:
            f.write(line)
            f.write('\n')
