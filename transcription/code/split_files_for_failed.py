# Purpose: gets a list of failed transcription jobs
# The only error cause I've seen is that files are too large - so error type is not checked. Room for improvement
# With the list of failed jobs, split the corresponding local files in 235 minute chunks. That's 3h55min, and the 
# upper limit is 4h.
# splitting is performed using mp3splt, so it must be installed

# TODO:
# check that the AWS transcription is indeed "file too large"
# fine-tune the split call using -a, so that is will split on silence

import boto3, subprocess
import settings


# get failed transcr jobs
sandbox_session = boto3.session.Session(AWS_PROFILE=settings.AWS_PROFILE)

transcribe = sandbox_session.client('transcribe', region_name=settings.AWS_REGION)

response = transcribe.list_transcription_jobs(
    Status='FAILED',
#    JobNameContains='string',
 #   NextToken='string',
    MaxResults=100
)
for item in list(response.values())[1]:
    jobname = item['TranscriptionJobName']
    command = ["mp3splt",
               "-o",
               jobname.split(".")[0] + "_@A@u",
               "-t",
               "235.00",
               settings.PODCAST_AUDIO_LOCAL_PATH + "/" + jobname
               ]
    print(command)
    subprocess.run(command)
