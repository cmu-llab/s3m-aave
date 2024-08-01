############################################
## May Pik Yu Chan ## pikyu@sas.upenn.edu ##
## Formant Extraction ######################
## Spring 2022 #############################
############################################
## Extracts formants for all vowels in a TextGrid

# Form to ask user to enter the name of the file (passed as CLI args)
form Give me information:
	comment Please indicate the word tier
	natural word 3
	comment Please indicate the segment tier
	natural seg 4
	comment Please enter your wavfile directory
	sentence WavDirectory .\
	comment Please enter your TextGrid directory
	sentence GridDirectory .\
	comment Please enter the CSV containing all the files in the corpus
	sentence CsvPath .\
	comment Corpus name
	sentence Corpus coraal
	comment Current working directory (relative to Praat script)
	sentence Cwd "../../"
endform


metadata = Read Table from comma-separated file: cwd$ + csvPath$
number_files = Get number of rows

for j from 1 to number_files

selectObject: metadata
filename$ = Get value: j, "Filename"

# one file per speaker since these files get large!
output_file$ = cwd$ + "analysis/vowels/" + corpus$ + "/" + filename$ + "_formants.csv"
writeFile: output_file$
appendFile: output_file$, "recording", ",", "vwl_index", ",", "vowel", ",", "word_intvl", ",", "word", ",", "f1_50", ",", "f2_50", ",", "f3_50", ",", "f1_F1max", ",", "f2_F1max", ",", "f3_F1max", ",", "f1_F2max", ",", "f2_F2max", ",", "f3_F2max", ",", "vowelDur", ",", "PrecC", ",", "FolC" 
appendFile: output_file$, newline$
appendInfoLine: "Creating " + output_file$

# This is to open the file
wavfile = Read from file: cwd$ + wavDirectory$ + filename$ + ".wav"
tgfile = Read from file: cwd$ + gridDirectory$ + filename$ + ".TextGrid"

# This tells us that the files are opened
appendInfoLine: "The files " + filename$ + ".wav" + " and " + filename$ + ".TextGrid" + " are opened."

selectObject: tgfile
totalTiers = Get number of tiers
# for CORAAL
if totalTiers > 2
	filenameLen = length (filename$)
	basefile$ = left$ (filename$, filenameLen - 2)
	wordTierName$ = basefile$ + " - words"
	phoneTierName$ = basefile$ + " - phones"

	i = 1
	repeat
		currentLabel$ = Get tier name... i
		i = i + 1
	until currentLabel$ == wordTierName$ or i > totalTiers
	word = i - 1

	i = 1
	repeat
		currentLabel$ = Get tier name... i
		i = i + 1
	until currentLabel$ == phoneTierName$ or i > totalTiers
	seg = i - 1

	name$ = Get tier name... word
endif

# This is to create a formant object
selectObject: wavfile
formant = To Formant (burg): 0, 5, 5500, 0.025, 50

# Now we are getting the number of intervals on tier segment
selectObject: tgfile
nInt = do ("Get number of intervals...", seg)

# This is the start of 'for loop'
for i to nInt

	#Here we are getting the word label out
	selectObject: tgfile
	seg$ = do$ ("Get label of interval...", seg, i)
	unstressed_target = index_regex (seg$, "0")
	pristressed_target = index_regex (seg$, "1")
	secstressed_target = index_regex (seg$, "2")

	#Here we are saying, if the word interval is not empty, then we need to get into another loop.
	if unstressed_target > 0 or pristressed_target > 0 or secstressed_target > 0

		#This is to make variables to correspond to different time points in relation to the vowel.
		vowel$ = do$ ("Get label of interval...", seg, i)
		precC$ = Get label of interval: seg, i-1
		# not all TextGrids will have an empty string at the end
		if i+1 > nInt
			folC$ = ""
		else
			folC$ = Get label of interval: seg, i+1
		endif

		vowelStart = do ("Get start point...", seg, i)
		vowelEnd = do ("Get end point...", seg, i)
		vowelDur = vowelEnd - vowelStart
		vowelMid = (vowelEnd + vowelStart) / 2
		vowel25 = vowelStart + (vowelDur)*0.25
		vowel75 = vowelStart + (vowelDur)*0.75
	
		wrd_int = Get interval at time: word, vowelMid
		word$ = Get label of interval: word, wrd_int		

		#And now it's time to measure some formants using the formant object
		selectObject: formant

		# f1_25 = do ("Get value at time...", 1, vowel25, "Hertz", "Linear")
		# f2_25 = do ("Get value at time...", 2, vowel25, "Hertz", "Linear")
		# f3_25 = do ("Get value at time...", 3, vowel25, "Hertz", "Linear")

		f1_50 = do ("Get value at time...", 1, vowelMid, "Hertz", "Linear")
		f2_50 = do ("Get value at time...", 2, vowelMid, "Hertz", "Linear")
		f3_50 = do ("Get value at time...", 3, vowelMid, "Hertz", "Linear")

		# f1_75 = do ("Get value at time...", 1, vowel75, "Hertz", "Linear")
		# f2_75 = do ("Get value at time...", 2, vowel75, "Hertz", "Linear")
		# f3_75 = do ("Get value at time...", 3, vowel75, "Hertz", "Linear")

		#measure at F2 max
		f2max = Get time of maximum: 2, vowelStart, vowelEnd, "Hertz", "Parabolic"
		f1_f2max = Get value at time: 1, f2max, "Hertz", "Linear"
		f2_f2max = Get value at time: 2, f2max, "Hertz", "Linear"
		f3_f2max = Get value at time: 3, f2max, "Hertz", "Linear"
		
		#measure at F1 max
		f1max = Get time of maximum: 1, vowelStart, vowelEnd, "Hertz", "Parabolic"
		f1_f1max = Get value at time: 1, f1max, "Hertz", "Linear"
		f2_f1max = Get value at time: 2, f1max, "Hertz", "Linear"
		f3_f1max = Get value at time: 3, f1max, "Hertz", "Linear"

		#This is to add the points to the point tier - deal with this later
		#selectObject: tgfile
		#Insert point: point, f2max, "F2Max"
		#Insert point: point, f1max, "F1Max"

		#And we then need to print out the data nicely
		appendFile: output_file$, filename$, ",", i, ",", vowel$, ",", wrd_int, ",", word$, ",", f1_50, ",", f2_50, ",", f3_50, ",", f1_f1max, ",", f2_f1max, ",", f3_f1max, ",", f1_f2max, ",", f2_f2max, ",", f3_f2max, ",", vowelDur, ",", precC$, ",", folC$
		appendFile: output_file$, newline$
	endif
endfor

removeObject: wavfile
removeObject: tgfile
removeObject: formant

endfor