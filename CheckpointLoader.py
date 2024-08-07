from boto3.session import Session
from botocore.config import Config
import os
from zipfile import ZipFile


# Check if model file exists locally, if not, download it
if not os.path.exists("ABSA_checkpoints/ABSA_checkpoint_1.0.zip"):
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
        'ABSA_checkpoints/ABSA_checkpoint_1.0.zip',
        'ABSA_checkpoint_1.0.zip')
# extract file
if not os.path.exists("fast_lcf_atepc_my_dataset_cdw_apcacc_83.5_apcf1_78.89_atef1_64.24"):
    # loading the temp.zip and creating a zip object
    with ZipFile("ABSA_checkpoint_1.0.zip", 'r') as zObject:
        zObject.extractall(
            path="")