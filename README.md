## workflow to transcribe the Lex podcast

1. start by uploading mp3's found at lexfridman.com
   1. to the AWS bucket BUCKET_NAME that is pointed out by settings.py, and put it in the dir BUCKET_PREFIX_AUDIO
2. Run transcribe.py
3. Run download.py. The files will be downloaded to TARGET_DIR
4. Finally, run the transform_output.py as below:


```
for f in downloads/*.json
  do /usr/bin/python3 transcription/code/transform_output.py $f
done
```

5. The resulting files will be found in /out