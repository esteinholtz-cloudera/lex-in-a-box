import boto3, settings

# functions
def amazon_transcribe(input_object, max_speakers = -1):
  
  if max_speakers > 10:
    raise ValueError("Maximum detected speakers is 10.")
 
  job_name = input_object.key.split("/")[1]
  if job_name == "": return # noop on empty file name
  file_name = job_name

  uri_base = "s3://" + settings.AWS_BUCKET_NAME +  "/" + settings.AWS_BUCKET_PREFIX_AUDIO + "/"
  job_uri = uri_base + file_name

  transcribe = sandbox_session.client('transcribe', region_name=settings.AWS_REGION)
  print("job Name: " + job_name)

  # check if name is taken or not
  try:
    response = transcribe.get_transcription_job(TranscriptionJobName=job_name)
  except:
    print("Jobname did not exist: ", job_name + ". creating...")
    mediaformat=file_name.split('.')[1]
    outputkey=settings.AWS_PREFIX_TRANSCRIPTS + "/" + file_name.split(".")[0] + ".json"

    transcribe.start_transcription_job(
        OutputBucketName=settings.AWS_BUCKET_NAME,
        OutputKey=outputkey,
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        MediaFormat=mediaformat,
        LanguageCode='en-US',
        Settings = {'ShowSpeakerLabels': True,
                    'MaxSpeakerLabels': max_speakers}
                    )
    return 0
  else:
    print ("job name already taken")
    return 1

# -- main --
  
# initialize, get the files
sandbox_session = boto3.session.Session(AWS_PROFILE=settings.AWS_PROFILE)
s3_resource = sandbox_session.resource("s3")

my_bucket = s3_resource.Bucket(settings.AWS_BUCKET_NAME)
objects = list(my_bucket.objects.filter(Prefix=settings.AWS_BUCKET_PREFIX_AUDIO)) 

print("ready to process....:")
for file in objects:
    print(file.key)

# transcribe with 3 speakers
for object in objects:
   amazon_transcribe(object, 3)
