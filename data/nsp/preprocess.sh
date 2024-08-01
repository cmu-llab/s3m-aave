# all files will be in spont
# organize by speaker
for region in at mi ne no so we
do
    for i in $(seq 0 9)
    do
        mkdir spont/$region$i
        mv spont/$region$i* spont/$region$i
    done
done

mv spont/no8/no8l0.txt spont/no8/no8I0.txt
mv spont/ne6/ne6l0.txt spont/ne6/ne6I0.txt
mv spont/ne5/ne5l0.txt spont/ne5/ne5I0.txt

mkdir preprocess
cp -r spont spont_copy
mv spont spont_old
mv spont_copy spont

# convert aiff to wav
for f in spont/**/*.aiff
do
    ffmpeg -i "$f" "${f%.aiff}.wav"
done

for f in spont/*/*.txt
do
    cp $f "${f%.txt}_original.txt"
done

python preprocess_nsp_prealign.py
