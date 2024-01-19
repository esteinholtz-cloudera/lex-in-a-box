import boto3

sandbox_session = boto3.session.Session(AWS_PROFILE='sandbox')
s3_resource = sandbox_session.resource("s3")

my_bucket = s3_resource.Bucket('esteinholtz-audio')
objects = list(my_bucket.objects.filter(Prefix='lex-audio'))


for file in objects:
    print(file.key)


