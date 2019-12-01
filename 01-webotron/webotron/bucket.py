# -*- coding:utf-8 -*-

"""Bucket logic is encapsulapted in this file."""
from pathlib import Path
import mimetypes

from botocore.exceptions import ClientError

import util


class BucketManager:
    """Manage an S3 bucket."""

    def __init__(self, session):
        """Create Bucket manager object."""
        self.session = session
        self.s3 = self.session.resource('s3')

    def all_buckets(self):
        """Return an Iterator for S3 buckets."""
        return self.s3.buckets.all()

    def all_bucket_objects(self, bucket_name):
        """Return an Iterator for listing object in S3."""
        return self.s3.Bucket(bucket_name).objects.all()

    def init_bucket(self, bucket_name):
        """Create S3 bucket or return an existing one."""
        try:
            self.s3.meta.client.head_bucket(Bucket=bucket_name)
            print("Bucket exists")
            s3_bucket = bucket_name
        except ClientError as error:
            # error_code=e.response
            error_code = error.response['Error']['Code']
            if error_code == '404':
                region_name = self.session.region_name
                resource = self.s3
                # print(region_name)
                # print(resource)
                s3_bucket = self.create_bucket(bucket_name, region_name,
                    resource)
            else:
                raise error

        return s3_bucket

    def get_bucket_location(self, bucket_name):
        """Get the location of S3 bucket."""
        bucket_location = self.s3.meta.client.get_bucket_location(
                Bucket=bucket_name)

        return bucket_location['LocationConstraint'] or 'us-east-1'

    def get_bucket_url(self, bucket_name):
        """Get the Website URL for the bucket."""
        return "http://{}.{}".format(
            bucket_name,
            util.get_endpoint(self.get_bucket_location(bucket_name)).host
        )

    @staticmethod
    def create_bucket(bucket_name, region_name, resource):
        """Create S3 bucket."""
        if region_name == 'us-east-1':
            # self.s3.create_bucket(Bucket=bucket_name)
            resource.create_bucket(Bucket=bucket_name)
            print("bucket_created in us-east-1")
        else:
            resource.create_bucket(Bucket=bucket_name,
                                   CreateBucketConfiguration={
                                   'LocationConstraint': region_name})
            print("bucket_created in region " + region_name)

    def apply_policy(self, bucket):
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
        """ % bucket

        policy = policy.strip()

        #  s3_bucket = s3.Bucket(bucket_name)

        # bucket_policy = self.s3.Bucket(bucket).Policy()
        bucket_policy = self.s3.BucketPolicy(bucket)
        bucket_policy.put(Policy=policy)

    def configure_website(self, bucket):
        """Configure an S3 bucket to host a static website."""
        self.s3.BucketWebsite(bucket).put(WebsiteConfiguration={
            'ErrorDocument': {
                'Key': 'error.html'
            },
            'IndexDocument': {
                'Suffix': 'index.html'
            }
            })

        print("S3 bucket " + bucket + " set up for static website hosting")

    @staticmethod
    def s3_upload(s3_bucket, path, key):
        """Upload objects to S3."""
        content_type = mimetypes.guess_type(key)[0] or 'text/plain'
        s3_bucket.upload_file(
            path,
            key,
            ExtraArgs={
                'ContentType': content_type
            })

    def sync(self, pathname, bucket_name):
        """Upload contents from a path to S3 bucket."""
        s3_bucket = self.s3.Bucket(bucket_name)

        root = Path(pathname).expanduser().resolve()

        def handle_directory(target):
            for p in target.iterdir():
                if p.is_dir():
                    handle_directory(p)
                if p.is_file():
                    # print("Path: {} \n Key: {}".
                    # format(p,str(p.relative_to(root).as_posix())))
                    # as_posix() converts the path with forward /
                    # print(str(p.relative_to(root).as_posix()))
                    self.s3_upload(s3_bucket, str(p),
                                   str(p.relative_to(root).as_posix()))

        handle_directory(root)
