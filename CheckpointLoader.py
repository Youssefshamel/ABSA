from boto3.session import Session
from botocore.config import Config
import os
from zipfile import ZipFile

def download_model():
    file = "ABSA_checkpoints/checkpoint_1.0.tar.gz"
    file_name = "checkpoint_1.0.tar.gz"
    # Check if model file exists locally, if not, download it
    if not os.path.exists(file):
        print("Downloading...")
        # fetch S3 Keys
        ACCESS_KEY_CA=os.environ["ACCESS_KEY_CA"]
        SECRET_KEY_CA=os.environ["SECRET_KEY_CA"]

        session_ca = Session(aws_access_key_id=ACCESS_KEY_CA,
                          aws_secret_access_key=SECRET_KEY_CA)

        config = Config(connect_timeout=5, read_timeout=100, max_pool_connections=40)
        s3_own = session_ca.resource('s3', config=config)
        data_science_bucket = s3_own.Bucket('ds.crowdanalyzer.com')
        # download model
        data_science_bucket.download_file(
            file,
            file_name)
    # extract file
    out_file = "checkpoint"
    if not os.path.exists(out_file):
        print("extracting...")
        # loading the temp.zip and creating a zip object
        with ZipFile(file_name, 'r') as zObject:
            zObject.extractall(
                path=out_file)
    return out_file