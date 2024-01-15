import boto3
import settings
import botocore.exceptions
from botocore.exceptions import ClientError

from os import listdir
from os.path import isfile, join

def upload_file (input_file_path):
    s3.meta.client.upload_file(Filename=input_file_path, Bucket=settings.BUCKET_NAME, Key=key_from_localFN(input_file_path))

def check(client, bucket, key):
    try:
        client.get_object_acl(Bucket=bucket, Key=key)
    except client.exceptions.NoSuchKey:
        return True
    return False

def key_from_localFN(localname):
    return settings.BUCKET_PREFIX_AUDIO + "/" + localname.split("/")[-1]

# main --
# initialize

session = boto3.session.Session(profile_name=settings.PROFILE_NAME)

s3 = session.resource('s3') # Redundant -- remove & replace with s3_service
s3_service = boto3.resource(service_name='s3')
s3_client = session.client('s3')

# get directory listing and loop through it

mypath = settings.PODCAST_AUDIO_LOCAL_PATH
podcast_files = [join(mypath, f) for f in listdir(mypath) if isfile(join(mypath, f))]

for f in podcast_files:
    AWS_key = key_from_localFN(f)
    free  = check(s3_client, settings.BUCKET_NAME, AWS_key)
    if free:
        print ("Uploading:        " + f + " to " + AWS_key)
        upload_file(f)
    else:
        print ("already uploaded: " +f)
