from textgrid import TextGrid
from scipy.io import wavfile
from unicodedata import normalize
import argparse
import os
import glob
import re
import pandas as pd


# source: https://github.com/ThiagoCF05/PraatSegmentation/blob/master/main.py
MIN_CLIP_SEC, MAX_CLIP_SEC = 3, 49
clip_durations = []


def segment_wavfile(spk_id, start, end, duration, write_dir, freq, audio, transcription, transcript_csv, demographics):
	spk_demographics = demographics[demographics["Subject Number"] == spk_id.upper()].iloc[0]
	age, gender = spk_demographics["Age at Test"], spk_demographics["Gender"]
	gender = gender.replace("m", "Male").replace("f", "Female")
	# remove brackets then replace double spaces left behind
		# removes [laugh]
	transcription = re.sub(r"\[[^]]*\]", "", transcription).replace("  ", " ")
	# remove the timestamps from the transcripts
	transcription = re.sub(r" [0-9] [0-9][0-9]$", "", transcription).strip()

	fname = f'{spk_id}_{str(round(start))}_{str(round(end))}.wav'
	wavfile.write(os.path.join(write_dir, fname), freq, audio[1][int(start):int(end)])
	with open(transcript_csv, 'a') as f:
		f.write(f'{spk_id},{spk_id[:2]},{fname},{transcription},{duration},{age},{gender}\n')


def segment_tier(write_dir, grid, audio, speaker_id, transcript_csv, demographics):
	# find the tier with the words
	word_tier = list(filter(lambda x: x.nameid == 'words', grid.tiers))[0].simple_transcript

	# frequency, length and duration of the audio
	freq = int(audio[0])
	length = len(audio[1])
	duration = float(length)/freq # in seconds

	# speaker_id is the interviewee
	speaker = ""
	utterance, utterance_start, utterance_end = [], 0, 0
	for i, interval in enumerate(word_tier):
		(word_start, word_end, word) = interval
		word_start = (float(word_start) * length) / duration
		word_end = (float(word_end) * length) / duration

		if word == "/[interviewer]/":
			# previous utterance was speaker
			# end previous utterance
			utterance = ' '.join(utterance)
			# skip if < 3s or contains overlapping speech (/)
			if utterance_end - utterance_start > (MIN_CLIP_SEC * length) / duration and \
				"/" not in utterance:
				utt_duration = (utterance_end - utterance_start) * duration / length
				clip_durations.append(utt_duration)
				segment_wavfile(speaker_id, utterance_start, utterance_end, utt_duration, write_dir, freq, audio, utterance, transcript_csv, demographics)
			# start new utterance
			speaker = "interviewer"
			utterance_start = word_start
			utterance = []
		elif word == f"/[{speaker_id}]/":
			# previous utterance was interviewer
			# do not include the speaker utterance
			# start new utterance
			utterance_start = word_start
			utterance = []
			speaker = speaker_id
		else:
			utterance_end = word_end
			if word.strip():
				utterance.append(word.strip())
			elif word == "" and speaker == speaker_id and utterance_end - utterance_start > (MAX_CLIP_SEC * length) / duration:
				utt = ' '.join(utterance)
				if "/" not in utt:
					utt_duration = (utterance_end - utterance_start) * duration / length
					clip_durations.append(utt_duration)
					segment_wavfile(speaker_id, utterance_start, utterance_end, utt_duration, write_dir, freq, audio, utt, transcript_csv, demographics)
					# start new utterance
					utterance_start = word_start
					utterance = []

	# final utterance in the recording
	if speaker == speaker_id:
		# end previous utterance
		utterance = ' '.join(utterance)
		# skip if < 3s or contains overlapping speech (/)
		if utterance_end - utterance_start > (MIN_CLIP_SEC * length) / duration and \
			"/" not in utterance:
			utt_duration = (utterance_end - utterance_start) * duration / length
			clip_durations.append(utt_duration)
			segment_wavfile(speaker_id, utterance_start, utterance_end, utt_duration, write_dir, freq, audio, utterance, transcript_csv, demographics)


def main(wav_dir, textgrid_dir, write_dir, transcript_csv, demographics_file):
	with open(transcript_csv, 'w') as f:
		f.write('speaker,region,wav,transcript,duration,age,gender\n')

	demographics = pd.read_csv(demographics_file, sep="\t")

	for filepath in glob.iglob(wav_dir + '/**/*.wav'):
		speaker_id, audio_file = filepath.split('/')[1], filepath.split('/')[2]
		audio_file = audio_file.split('.wav')[0]
		
		try:
			audio = wavfile.read(filepath)
			textgrid = os.path.join(textgrid_dir, speaker_id, audio_file + '.TextGrid')
			grid = normalize('NFKD', open(textgrid).read()).encode('ascii', 'ignore')
			if grid[0] == 'y':
				grid = TextGrid(grid[1:])
			else:
				grid = TextGrid(open(textgrid).read())

			if not os.path.exists(os.path.join(write_dir, filepath)):
				os.makedirs(os.path.join(write_dir, filepath))
			segment_tier(os.path.join(write_dir, filepath), grid, audio, speaker_id, transcript_csv, demographics)
		except Exception as e:
			print('Error in file ', filepath, e)

	print(len(clip_durations), "utterances extracted")
	print(sum(clip_durations) / len(clip_durations), " avg clip length (s)")
	print(sum(clip_durations) / 3600, " total hours extracted")

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Segmentation of a .wav file based on its .TextGrid annotation.')
	parser.add_argument("--wav_dir", help="directory with the wav files", default='spont', type=str)
	parser.add_argument("--textgrid_dir", help="directory with the textgrid files (output of MFA)", default='spont_aligned', type=str)
	parser.add_argument("--dest", help="directory where the chunks should be written", default='segmented', type=str)
	parser.add_argument("--transcript_csv", help="CSV storing the ASR transcription", default='transcript.csv', type=str)
	parser.add_argument("--demographics", help="txt file storing the speaker demographics", default='demographics.txt', type=str)
	args = parser.parse_args()

	main(args.wav_dir, args.textgrid_dir, args.dest, args.transcript_csv, args.demographics)
