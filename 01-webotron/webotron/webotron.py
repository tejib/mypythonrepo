#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Deploy websites to AWS."""
import boto3
import click
from bucket import BucketManager

session = boto3.Session(profile_name='admin')
bucket_manager = BucketManager(session)
# s3 = session.resource('s3')
# print("s3 session profile is setup")


@click.group()
def cli():
    """Use click group to drive the commands."""
    pass


@cli.command('list-buckets')
def list_buckets():
    """List all S3 buckets."""
    for bucket in bucket_manager.all_buckets():
        print(bucket)


@cli.command('list-objects')
@click.argument('bucket')
def list_objects(bucket):
    """List of objects in an S3 bucket."""
    for obj in bucket_manager.all_bucket_objects(bucket):
        print(obj)


@cli.command('setup-bucket')
@click.argument('bucket')
def setup_bucket(bucket):
    """Set up the S3 bucket."""
    s3_bucket = bucket_manager.init_bucket(bucket)
    # print(s3_bucket)
    bucket_manager.apply_policy(s3_bucket)
    bucket_manager.configure_website(s3_bucket)


@cli.command('sync')
@click.argument('pathname', type=click.Path(exists=True))
@click.argument('bucket')
def sync(pathname, bucket):
    """Sync contents of a path to S3 bucket."""
    bucket_manager.sync(pathname, bucket)


if __name__ == '__main__':
    cli()
