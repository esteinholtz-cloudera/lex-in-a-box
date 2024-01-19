
cd out/Sam_Harris/

# to get the original text before transformation
cat ../../transcription/transcriptions/lex_ai_sam_harris_2_A.json|jq '.results.transcripts.[].transcript' > orig_input

#to get all the text in chunks from transformation for reference and comparison
for f in *;do cat $f|jq '.Text';done > ref_output