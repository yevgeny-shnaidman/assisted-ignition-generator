import subprocess
import random
import os
import boto3
from botocore.exceptions import NoCredentialsError
import logging
import argparse

FILES_TO_COPY = ["master.ign", "worker.ign", "bootstrap.ign", "metadata.json", "auth"]

def upload_to_aws(local_file, bucket, s3_file):
    aws_access_key_id = os.environ.get("aws_access_key_id", "accessKey1")
    aws_secret_access_key = os.environ.get("aws_secret_access_key", "verySecretKey1")
    endpoint_url = args.s3_endpoint_url

    s3 = boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        endpoint_url=endpoint_url
    )
    try:
        s3.upload_file(local_file, bucket, s3_file, ExtraArgs={'ACL': 'public-read'})
        print("Upload Successful")
        return True
    except NoCredentialsError:
        print("Credentials not available")
        return False


parser = argparse.ArgumentParser(description='Generate ignition manifest & kubeconfig')
# TODO support pass yaml as string
# parser.add_argument('--install_config_string', help='install config string', default=None)
parser.add_argument('--file_name', help='output directory name', default="output_dir")
parser.add_argument('--s3_endpoint_url', help='s3 endpoint url', default=None)
parser.add_argument('--s3_bucket', help='s3 bucket', default='test')
args = parser.parse_args()

# TODO support pass yaml as string
# if not (args.install_config_string or os.path.isfile('install-config.yaml')):
#     raise Exception("Must pass install_config file or string")
#
# if args.install_config_string:
#     with open('install-config.yaml', 'w') as f:
#         f.write(args.install_config_string)

if not os.path.isdir('/installer_dir'):
    raise Exception('installer directory is not mounted')

if not os.path.isfile('/installer_dir/install-config.yaml'):
    raise Exception("install config file not located in installer dir")

command = "./openshift-install create ignition-configs --dir /installer_dir"
try:
    subprocess.check_output(command, shell=True)
except Exception as ex:
    raise Exception('Failed to generate files, exception: {}'.format(ex))

if args.s3_endpoint_url:
    subprocess.check_output("zip {file_name}.zip {file_name} ".format(file_name=args.file_name), shell=True)
    uploaded = upload_to_aws(args.file_name+'.zip', args.s3_bucket, args.file_name+'.zip')
