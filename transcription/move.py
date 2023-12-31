import boto3
def amazon_transcribe_remove(input_object, max_speakers = -1):
  
  if max_speakers > 10:
    raise ValueError("Maximum detected speakers is 10.")
 
  job_name = input_object.key.split("/")[1]
  file_name = job_name

  uri_base = "s3://esteinholtz-audio/lex-audio/" # constant
  job_uri = uri_base + file_name

  transcribe = sandbox_session.client('transcribe', region_name='eu-central-1')
  print("job Name: " + job_name)

  # check if name is taken or not
  try:
    response = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    transcribe.delete_transcription_job(
      TranscriptionJobName=job_name)
    return 0
  except:
    print("Jobname did not exist: ", job_name)
    return 1

# --main --
#initialize, get the files

sandbox_session = boto3.session.Session(profile_name='sandbox')
s3_resource = sandbox_session.resource("s3")

my_bucket = s3_resource.Bucket('esteinholtz-audio')
objects = list(my_bucket.objects.filter(Prefix='lex-audio'))

print("ready to process....:")
for file in objects:
    print(file.key)

# transcribe with 3 speakers
for object in objects:
   amazon_transcribe_remove(object, 3)
