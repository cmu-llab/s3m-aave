# Self-supervised Speech Representations Still Struggle with African American Vernacular English

This is the code for the Interspeech 2024 paper "Self-supervised Speech Representations Still Struggle with African American Vernacular English."

arXiv: https://www.arxiv.org/abs/2408.14262

> Underperformance of ASR systems for speakers of African American Vernacular English (AAVE) and other marginalized language varieties is a well-documented phenomenon, and one that reinforces the stigmatization of these varieties. We investigate whether or not the recent wave of Self-Supervised Learning (SSL) speech models can close the gap in ASR performance between AAVE and Mainstream American English (MAE). We evaluate four SSL models (wav2vec 2.0, HuBERT, WavLM, and XLS-R) on zero-shot Automatic Speech Recognition (ASR) for these two varieties and find that these models perpetuate the bias in performance against AAVE. Additionally, the models have higher word error rates on utterances with more phonological and morphosyntactic features of AAVE. Despite the success of SSL speech models in improving ASR for low resource varieties, SSL pre-training alone may not bridge the gap between AAVE and MAE.


# Models
* FBANK https://huggingface.co/sophia14/s3m-aave-fbank-asr
* XLS-R https://huggingface.co/sophia14/s3m-aave-xlsr-asr
* wav2vec 2.0 https://huggingface.co/sophia14/s3m-aave-wav2vec2-large-asr
* WavLM https://huggingface.co/sophia14/s3m-aave-wavlm-asr
* HuBERT https://huggingface.co/sophia14/s3m-aave-hubert-large-asr


# Poster

![Interspeech_2024_Poster](https://github.com/user-attachments/assets/d823fc5d-12b6-45a2-b81f-feae495fc97e)


# Citation

Please cite our paper as follows:

Kalvin Chang*, Yi-Hui Chou*, Jiatong Shi, Hsuan-Ming Chen, Nicole Holliday, Odette Scharenborg,
David R. Mortensen. 2024. Self-supervised Speech Representations Still Struggle with African American 
Vernacular English. In *Proceedings of the 25th Interspeech Conference*, Kos Island, Greece.

```
@inproceedings{chang-chou-etal-2024-s3m-aave,
    title = "Self-supervised Speech Representations Still Struggle with African American Vernacular English",
    author = "Chang, Kalvin and
      Chou, Yi-Hui and
      Shi, Jiatong and
      Chen, Hsuan-Ming and
      Holliday, Nicole and
      Scharenborg, Odette and
      Mortensen, David R.",
    booktitle={Proc. INTERSPEECH 2024},
    month = September,
    year = "2024",
    address = "Greece",
    publisher = "ISCA",
}
```
