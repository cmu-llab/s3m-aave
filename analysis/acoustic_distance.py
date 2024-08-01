from typing import Optional
from dtw import dtw 
from transformers.models.wav2vec2 import Wav2Vec2Model
import soundfile as sf
from scipy import signal
import torch
import numpy as np

KNOWN_MODELS = { 
    # Pre-trained
    "wav2vec2-base": "facebook/wav2vec2-base",
    "wav2vec2-large": "facebook/wav2vec2-large",
    "wav2vec2-large-lv60": "facebook/wav2vec2-large-lv60",
    "wav2vec2-large-xlsr-53": "facebook/wav2vec2-large-xlsr-53",
    # Fine-tuned
    "wav2vec2-base-960h": "facebook/wav2vec2-base-960h",
    "wav2vec2-large-960h": "facebook/wav2vec2-large-960h",
    "wav2vec2-large-960h-lv60": "facebook/wav2vec2-large-960h-lv60",
    "wav2vec2-large-960h-lv60-self": "facebook/wav2vec2-large-960h-lv60-self",
    "wav2vec2-large-xlsr-53-english": "jonatasgrosman/wav2vec2-large-xlsr-53-english",
    # Voxpopuli
    "wav2vec2-base-10k-voxpopuli": "facebook/wav2vec2-base-10k-voxpopuli",
    "wav2vec2-base-100k-voxpopuli": "facebook/wav2vec2-base-100k-voxpopuli",
    "wav2vec2-large-100k-voxpopuli": "facebook/wav2vec2-large-100k-voxpopuli",
    "wav2vec2-base-10k-voxpopuli-ft-en": "facebook/wav2vec2-base-10k-voxpopuli-ft-en",
    # Dutch
    "wav2vec2-large-xlsr-53-dutch": "facebook/wav2vec2-large-xlsr-53-dutch",
    "wav2vec2-large-xlsr-53-dutch-wietsedv": "wietsedv/wav2vec2-large-xlsr-53-dutch",
    "wav2vec2-large-nl-voxpopuli": "facebook/wav2vec2-large-nl-voxpopuli",
    "wav2vec2-base-10k-voxpopuli-ft-nl": "facebook/wav2vec2-base-10k-voxpopuli-ft-nl",
}

def load_wav2vec2_featurizer(model: str, layer: Optional[int] = None):
    """ 
    Loads Wav2Vec2 featurization pipeline and returns it as a function.

    Featurizer returns a list with all hidden layer representations if "layer" argument is None.
    Otherwise, only returns the specified layer representations.
    """

    model_name_or_path = KNOWN_MODELS.get(model, model)
    model_kwargs = {}
    if layer is not None:
        model_kwargs["num_hidden_layers"] = layer if layer > 0 else 0
    model = Wav2Vec2Model.from_pretrained(model_name_or_path, **model_kwargs)
    model.eval()
    if torch.cuda.is_available():
        model.cuda()

    @torch.no_grad()
    def _featurize(path, sr, start=0, end=None):
        start = int(start*sr)
        if end:
            end = int(end*sr)
        input_values, rate = sf.read(path, dtype=np.float32, start=start, stop=end)
        assert rate == sr, f"sample rate: {rate}" 
        if len(input_values.shape) == 2:
            input_values = input_values.mean(1)
        if rate != 16_000:
            new_length = int(input_values.shape[0] / rate * 16_000)
            input_values = signal.resample(input_values, new_length)

        input_values = torch.from_numpy(input_values).unsqueeze(0)
        if torch.cuda.is_available():
            input_values = input_values.cuda()

        if layer is None:
            hidden_states = model(input_values, output_hidden_states=True).hidden_states
            hidden_states = [s.squeeze(0).cpu().numpy() for s in hidden_states]
            return hidden_states

        if layer >= 0:
            hidden_state = model(input_values).last_hidden_state.squeeze(0).cpu().numpy()
        else:
            hidden_state = model.feature_extractor(input_values)
            hidden_state = hidden_state.transpose(1, 2)
            if layer == -1:
                hidden_state = model.feature_projection(hidden_state)
            hidden_state = hidden_state.squeeze(0).cpu().numpy()

        return hidden_state

    return _featurize


def dtw_distance(a_feats, b_feats):
    if a_feats.shape[0] < 2 or b_feats.shape[0] < 2:
        return np.nan

    return dtw(
        a_feats,
        b_feats,
        distance_only=True,
    ).normalizedDistance




if __name__ == "__main__":
    model, layer = "wav2vec2-base", 9
    featurizer = load_wav2vec2_featurizer(model, layer)

    with open("common_word.txt") as f:
        lines = f.readlines()

    distances = []
    # index,word,NSP filename,NSP start,NSP end,CORAAL filename,CORAAL start,CORAAL end

    for i in range(1, 10):  #len(lines)):
        info = lines[i].split(',')
        assert len(info) == 8
        nsp_fn, nsp_st, nsp_end = info[2], info[3], info[4]
        coraal_fn, coraal_st, coraal_end = info[5], info[6], info[7]

        f1 = featurizer(coraal_fn, 16000, float(coraal_st), float(coraal_end))
        f2 = featurizer(nsp_fn, 16000, float(nsp_st), float(nsp_end))

        dist = dtw_distance(f1, f2)
        distances.append(dist)

    #print(distances)
    distances = np.array(distances)
    print("mean:", np.mean(distances), "std:", np.std(distances))
