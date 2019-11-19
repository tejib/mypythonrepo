#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Deploy websites to AWS."""

from pathlib import Path
import mimetypes

import boto3
from botocore.exceptions import ClientError
import click

session = boto3.Session(profile_name='admin')
s3 = session.resource('s3')
# print("s3 session profile is setup")


@click.group()
def cli():
    """Use click group to drive the commands."""
    pass


@cli.command('list-buckets')
def list_buckets():
    """List all S3 buckets."""
    for bucket in s3.buckets.all():
        print(bucket)


@cli.command('list-bucket-objects')
@click.argument('bucket')
def list_bucket_objects(bucket):
    """List of objects in an S3 bucket."""
    for obj in s3.Bucket(bucket).objects.all():
        print(obj)


@cli.command('setup-bucket')
@click.argument('bucket')
def setup_bucket(bucket):
    """Set up the S3 bucket."""
    try:
        s3.meta.client.head_bucket(Bucket=bucket)
        print("Bucket exists")
    except ClientError as error:
        # error_code=e.response
        error_code = error.response['Error']['Code']
        if error_code == '404':
            create_bucket(bucket)
        else:
            raise error

    apply_policy(bucket)

    # return


def create_bucket(bucket):
    """Create S3 bucket."""
    if session.region_name == 'us-east-1':
        s3.create_bucket(Bucket=bucket)
        print("bucket_created in us-east-1")
    else:
        s3.create_bucket(Bucket=bucket, CreateBucketConfiguration={
            'LocationConstraint': session.region_name})
        print("bucket_created in region " + session.region_name)


def apply_policy(s3_bucket_name):
    """Apply Policy to S3 bucket.Set up bucket for static website."""
    policy = """
    {
      "Version":"2012-10-17",
      "Statement":[{
        "Sid":"PublicReadGetObject",
            "Effect":"Allow",
          "Principal": "*",
          "Action":["s3:GetObject"],
          "Resource":["arn:aws:s3:::%s/*"
          ]
        }
      ]
    }
    """ % s3_bucket_name

    policy = policy.strip()

    s3_bucket = s3.Bucket(s3_bucket_name)

    bucket_policy = s3_bucket.Policy()
    bucket_policy.put(Policy=policy)

    bucket_website = s3_bucket.Website()
    bucket_website.put(WebsiteConfiguration={
        'ErrorDocument': {
            'Key': 'error.html'
        },
        'IndexDocument': {
            'Suffix': 'index.html'
        }
        })

    print("S3 bucket " + s3_bucket_name + " set up for static website hosting")


def s3_upload(s3_bucket, path, key):
    """Upload objects to S3."""
    content_type = mimetypes.guess_type(key)[0] or 'text/plain'
    s3_bucket.upload_file(
        path,
        key,
        ExtraArgs={
            'ContentType': content_type
        })


@cli.command('sync')
@click.argument('pathname', type=click.Path(exists=True))
@click.argument('bucket')
def sync(pathname, bucket):
    """Sync contents of a path to S3 bucket."""
    s3_bucket = s3.Bucket(bucket)

    root = Path(pathname).expanduser().resolve()

    def handle_directory(target):
        for p in target.iterdir():
            if p.is_dir():
                handle_directory(p)
            if p.is_file():
                # print("Path: {} \n Key: {}".
                # format(p,str(p.relative_to(root).as_posix())))
                # as_posix() converts the path with forward /
                s3_upload(s3_bucket, str(p),
                          str(p.relative_to(root).as_posix()))

    handle_directory(root)


if __name__ == '__main__':
    cli()
