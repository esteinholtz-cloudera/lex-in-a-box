import settings
import boto3

sandbox_session = boto3.session.Session(profile_name=settings.PROFILE_NAME)
s3 = sandbox_session.client("s3")


sandbox_session = boto3.session.Session(profile_name=settings.PROFILE_NAME)
s3_resource = sandbox_session.resource("s3")

my_bucket = s3_resource.Bucket(settings.BUCKET_NAME)
objects = list(my_bucket.objects.filter(Prefix=settings.BUCKET_PREFIX_TRANSCRIPTS))

for obj in objects:
    print('downloading ' + obj.key + ' to ' + settings.TARGET_DIR)
    if obj.key[-1]!="/":
        if len(obj.key.split("/")) >1:
            filename = obj.key.split("/")[1]
        else:
            filename = obj.key
        fsplit = filename.split(".")
        if len(fsplit) > 0:
            if fsplit[-1] == "json":
                with open(settings.TARGET_DIR + "/" + filename, 'wb') as f:
                    s3.download_fileobj(settings.BUCKET_NAME, obj.key, f)
                    