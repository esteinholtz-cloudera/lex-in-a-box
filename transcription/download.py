import boto3


def download(_object):
    target_dir = "./downloads/"
    target_filename = target_dir + _object.key.split("/")[1]
    # with open(target_filename, 'wb') as data:
    s3.download_file(_object.bucket_name, object.key, target_filename)


# main
sandbox_session = boto3.session.Session(profile_name='sandbox')
s3 = sandbox_session.client("s3")

my_bucket = s3.bucket('esteinholtz-audio')
prefix='lex-transcripts'
objects = list(my_bucket.objects.filter(Prefix=prefix))

for obj in objects:
    if (obj.key != prefix + "/"):
        download(obj)

