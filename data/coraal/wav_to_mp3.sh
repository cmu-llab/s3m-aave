for file in $(find coraal/ -name "*.wav"); do
    FILEPATH=${file%.*}
    NEW_FILE=$FILEPATH.mp3
    ffmpeg -i $file $NEW_FILE
    rm $file
done
