cd full/DCB
wget http://lingtools.uoregon.edu/coraal/dcb/2018.10.06/DCB_audio_part01_2018.10.06.tar.gz
wget http://lingtools.uoregon.edu/coraal/dcb/2018.10.06/DCB_audio_part02_2018.10.06.tar.gz
wget http://lingtools.uoregon.edu/coraal/dcb/2018.10.06/DCB_audio_part03_2018.10.06.tar.gz
wget http://lingtools.uoregon.edu/coraal/dcb/2018.10.06/DCB_audio_part04_2018.10.06.tar.gz
wget http://lingtools.uoregon.edu/coraal/dcb/2018.10.06/DCB_audio_part05_2018.10.06.tar.gz
wget http://lingtools.uoregon.edu/coraal/dcb/2018.10.06/DCB_audio_part06_2018.10.06.tar.gz
wget http://lingtools.uoregon.edu/coraal/dcb/2018.10.06/DCB_audio_part07_2018.10.06.tar.gz
wget http://lingtools.uoregon.edu/coraal/dcb/2018.10.06/DCB_audio_part08_2018.10.06.tar.gz
wget http://lingtools.uoregon.edu/coraal/dcb/2018.10.06/DCB_audio_part09_2018.10.06.tar.gz
wget http://lingtools.uoregon.edu/coraal/dcb/2018.10.06/DCB_audio_part10_2018.10.06.tar.gz
wget http://lingtools.uoregon.edu/coraal/dcb/2018.10.06/DCB_audio_part11_2018.10.06.tar.gz
wget http://lingtools.uoregon.edu/coraal/dcb/2018.10.06/DCB_audio_part12_2018.10.06.tar.gz
wget http://lingtools.uoregon.edu/coraal/dcb/2018.10.06/DCB_audio_part13_2018.10.06.tar.gz
wget http://lingtools.uoregon.edu/coraal/dcb/2018.10.06/DCB_audio_part14_2018.10.06.tar.gz
for f in *.tar.gz; do tar xvf "$f"; done

cd ../../full/PRV
wget http://lingtools.uoregon.edu/coraal/prv/2018.10.06/PRV_audio_part01_2018.10.06.tar.gz
wget http://lingtools.uoregon.edu/coraal/prv/2018.10.06/PRV_audio_part02_2018.10.06.tar.gz
wget http://lingtools.uoregon.edu/coraal/prv/2018.10.06/PRV_audio_part03_2018.10.06.tar.gz
wget http://lingtools.uoregon.edu/coraal/prv/2018.10.06/PRV_audio_part04_2018.10.06.tar.gz
for f in *.tar.gz; do tar xvf "$f"; done
# removes the weird files starting with a dot
rm -rf .[!.] .??*

cd ../../full/ROC
wget http://lingtools.uoregon.edu/coraal/roc/2020.05/ROC_audio_part01_2020.05.tar.gz
wget http://lingtools.uoregon.edu/coraal/roc/2020.05/ROC_audio_part02_2020.05.tar.gz
wget http://lingtools.uoregon.edu/coraal/roc/2020.05/ROC_audio_part03_2020.05.tar.gz
wget http://lingtools.uoregon.edu/coraal/roc/2020.05/ROC_audio_part04_2020.05.tar.gz
wget http://lingtools.uoregon.edu/coraal/roc/2020.05/ROC_audio_part05_2020.05.tar.gz
for f in *.tar.gz; do tar xvf "$f"; done

mv **/*.wav .
