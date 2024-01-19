import settings
import boto3
import os

sandbox_session = boto3.session.Session(AWS_PROFILE=settings.AWS_PROFILE)
s3 = sandbox_session.client("s3")


sandbox_session = boto3.session.Session(AWS_PROFILE=settings.AWS_PROFILE)
s3_resource = sandbox_session.resource("s3")

my_bucket = s3_resource.Bucket(settings.AWS_BUCKET_NAME)
objects = list(my_bucket.objects.filter(Prefix=settings.AWS_PREFIX_TRANSCRIPTS))

for obj in objects:
    print('downloading ' + obj.key + ' to ' + settings.RAW_TRANSCRIPTS)
    if obj.key[-1]!="/":
        if len(obj.key.split("/")) >1:
            filename = obj.key.split("/")[1]
        else:
            filename = obj.key
        fsplit = filename.split(".")
        if len(fsplit) > 0:
            if fsplit[-1] == "json":
                local_file = settings.RAW_TRANSCRIPTS + "/" + filename
                if os.path.isfile(local_file):
                    print ("skipping existing file: " + local_file)
                    continue
                print("downloading: " + local_file)
                with open(local_file, 'wb') as f:
                    s3.download_fileobj(settings.AWS_BUCKET_NAME, obj.key, f)
                    