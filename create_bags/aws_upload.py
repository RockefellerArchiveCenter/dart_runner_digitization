import boto3
from botocore.exceptions import ClientError


class S3Uploader(object):
    def __init__(self, region_name, access_key, secret_key, bucket):
        s3 = boto3.resource(service_name="s3", region_name=region_name,
                            aws_access_key_id=access_key, aws_secret_access_key=secret_key)
        self.bucket = s3.Bucket(bucket)

    def upload_pdf_to_s3(self, filepath, object_name):
        """Uploads a PDF file to a 'pdf' directory

        Args:
            filepath (Path obj): full filepath to the PDF to upload
            object_name (str): object name (including directories) to be added to bucket
        """
        try:
            self.bucket.upload_file(str(filepath), object_name, ExtraArgs={
                                    'ContentType': "application/pdf"})
            return True
        except ClientError as e:
            raise Exception(f"AWS upload error: {e}")
