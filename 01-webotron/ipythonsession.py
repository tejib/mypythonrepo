# coding: utf-8
import boto3
session = boto3.Session(profile_name='admin')
s3 = session.resource('s3')
print("s3 session profile is setup")
#for bucket in s3.buckets.all():
#    print(bucket)
