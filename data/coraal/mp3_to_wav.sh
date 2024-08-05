# ffmpeg -i /ocean/projects/cis210027p/ychou1/aal-ssl/coraal/CORAAL_audio/dcb/DCB_se1_ag2_f_01_1_179711_185563.mp3 -f wav -ar 16000 -ab 16 -ac 1 /ocean/projects/cis210027p/ychou1/aal-ssl/coraal/CORAAL_audio_wav/dcb/DCB_se1_ag2_f_01_1_179711_185563.wav
root="CORAAL_audio"
outdir="CORAAL_audio_wav"


mkdir $outdir

# dcb/ prv/ roc/ 
mkdir -p $outdir/dcb
mkdir -p $outdir/prv
mkdir -p $outdir/roc

for dir in $root/*; do
    subset=$(basename "$dir")
    for fn in $dir/*; do
        fn_base=$(basename "$fn" .mp3)
        outfn=$outdir/$subset/$fn_base.wav
        if [ ! -f $outfn ]
        then
            ffmpeg -i $fn -f wav -ar 16000 -ab 16 -ac 1 $outfn
        fi
    done
done
