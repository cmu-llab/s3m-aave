import argparse
import pandas as pd


def get_args():
    parser = argparse.ArgumentParser(description="")
    
    parser.add_argument("--dataset", type=str, choices=["coraal", "nsp", "coraal_ddm"], required=True)
    parser.add_argument("--fbank", action="store_true", help="FBANK model")
    parser.add_argument("--region", action="store_true", help="print region breakdown")
    parser.add_argument("--sslr", action="store_true", help="print model(sslr) breakdown")
    parser.add_argument("--store_wer", action="store_true", help="save each utterance's WER to preds/CORPUS/MODEL.csv")

    args = parser.parse_args()

    return args


def read_lines(filename, get_stats=False, uppercase_region=False):
    """
    Parse correct, substitution, deletion, insertion breakdown from sclite output
    Return aggregate breakdown for each region 

    or if get_stats=True, a dict mapping utterance ID to its (correct, substitution, deletion, insertion) stats
    """
    with open(filename, "r") as f:
        lines = f.readlines()

    regions = dict()
    # {region: [c,s,d,i]}
    utt_to_edit_stats = {}
    # utt_id: (c,s,d,i)

    for i in range(len(lines)):
        line = lines[i]
        if "Scores: (#C #S #D #I)" in line:
            # CORAAL - id: (dcb_se1_ag2_f_01_1-dcb_se1_ag2_f_01_1_1597704_1603279)
            # NSP - id: (at0-at0_10872414_11447478)
            utt_id = lines[i-1]
            utt_id = utt_id[utt_id.find("-")+1:utt_id.find(")")]
            region = utt_id.split('_')[0].split('-')[0]
            region = ''.join((ch for ch in region if not ch.isdigit()))
            if uppercase_region:
                region = region.upper()
                utt_id = region + '_' +  utt_id.split('_', maxsplit=1)[1]

            # correct, substitution, deletion, insertion
            scores = line.split("Scores: (#C #S #D #I)")[1].split()
            scores = [int(s) for s in scores]
            utt_to_edit_stats[utt_id] = tuple(scores)

            if region not in regions:
                regions[region] = [0,0,0,0]
            regions[region] = [x+y for x,y in zip(regions[region], scores)]

    if get_stats:
        return utt_to_edit_stats

    return regions


def calc_wer(info):
    c, s, d, i = info
    edits = s+d+i
    len_ref = c+s+d
    return edits / len_ref 


def store_wer(dataset, model):
    # assumes the preds already exist
    filename = f"analysis/{dataset}/wer-{model}"
    utt_to_edit_stats = read_lines(filename, get_stats=True, uppercase_region=(dataset != 'nsp'))
    utt_to_wer = {}
    for utt, edit_stats in utt_to_edit_stats.items():
        utt_to_wer[utt] = calc_wer(edit_stats)
    
    filename = f"preds/{dataset}/{model}.csv"
    df = pd.read_csv(filename)
    df['wer'] = df.apply(lambda row: utt_to_wer[row['segment_filename']], axis=1)
    df.to_csv(filename, index=False)


if __name__ == '__main__':
    args = get_args()

    sslrs = dict()
    # {sslr (str): regions (dict)}
    for sslr in ["hubert", "wav2vec2", "wavlm", "xlsr"]:
        filename = f"analysis/{args.dataset}/wer-{sslr}"
        regions = read_lines(filename)
        sslrs[sslr] = regions

        if args.store_wer:
            store_wer(args.dataset, sslr)

    if args.fbank:
        filename = f"analysis/{args.dataset}/wer-fbank"
        regions = read_lines(filename)
        fbank = regions

        if args.store_wer:
            store_wer(args.dataset, "fbank")

    #print(sslrs)
    print('-'*100)

    region_agg = dict()
    for sslr in sslrs:
        sslr_agg = [0,0,0,0]
        for region in sslrs[sslr]:
            # model and region breakdown
            if args.region and args.sslr:
                wer = calc_wer(sslrs[sslr][region])
                print(f"{sslr} / {region}: {wer:.3f}")
            if region not in region_agg:
                region_agg[region] = [0,0,0,0]
            region_agg[region] = [x+y for x,y in zip(region_agg[region], sslrs[sslr][region])]
            sslr_agg = [x+y for x,y in zip(sslr_agg, sslrs[sslr][region])]

        # model breakdown
        if args.sslr:
            wer = calc_wer(sslr_agg)
            print(f"{sslr}: {wer:.3f}")
    
    if args.fbank:
        fbank_agg = [0,0,0,0]
        for region in fbank:
            # model and region breakdown
            if args.region:
                wer = calc_wer(fbank[region])
                print(f"FBANK / {region}: {wer:.3f}")
            fbank_agg = [x+y for x,y in zip(fbank_agg, fbank[region])]
        wer = calc_wer(fbank_agg)
        print(f"FBANK: {wer:.3f}")

    # region breakdown
    if args.region and not args.sslr:
        for region in region_agg:
            wer = calc_wer(region_agg[region])
            print(f"{region}: {wer:.3f} (SSLR)")
            
            if args.fbank:
                wer = calc_wer(fbank[region])
                print(f"{region}: {wer:.3f} (FBANK)")

    # aggregated
    agg = [0,0,0,0]
    for region in region_agg:
        agg = [x+y for x,y in zip(region_agg[region], agg)]
    wer = calc_wer(agg)
    print(f"\naggregated: {wer:.3f} (SSLR)")

    if args.fbank:
        wer = calc_wer(fbank_agg)
        print(f"\naggregated: {wer:.3f} (FBANK)")

    print('-'*100)
