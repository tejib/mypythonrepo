import boto3
s3 = boto3.resource('s3')
my_bucket = s3.Bucket('sample-bucket')

for my_bucket_object in my_bucket.objects.all():  # Iterate thru all the objects
    print(my_bucket_object.key)

for my_bucket_filter in my_bucket.objects.filter(Prefix='Code Refer/bmw'):  #Iterate thru a specific folder in S3
    print(my_bucket_filter.key)
