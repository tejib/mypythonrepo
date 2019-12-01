#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Deploy websites to AWS."""
import boto3
import click
from bucket import BucketManager

# s3 = session.resource('s3')
# print("s3 session profile is setup")
session = None
bucket_manager = None


@click.group()
@click.option('--profile', default=None, help="Use a given AWS profile")
def cli(profile):
    """Use click group to drive the commands."""
    global session, bucket_manager

    session_cfg = {}
    if profile:
        session_cfg['profile_name'] = profile

    session = boto3.Session(**session_cfg)
    bucket_manager = BucketManager(session)


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
    print(bucket_manager.get_bucket_url(bucket))


if __name__ == '__main__':
    cli()
