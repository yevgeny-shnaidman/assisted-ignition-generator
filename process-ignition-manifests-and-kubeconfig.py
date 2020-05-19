import subprocess
import random
import os
import boto3
from botocore.exceptions import NoCredentialsError
import logging
import argparse
import sys
import json

def get_s3_client():

        aws_access_key_id = os.environ.get("aws_access_key_id", "accessKey1")
        aws_secret_access_key = os.environ.get("aws_secret_access_key", "verySecretKey1")

        s3 = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            endpoint_url=args.s3_endpoint_url
        )
        return s3

def upload_to_aws(s3, local_file, bucket, s3_file):

    try:
        s3.upload_file(local_file, bucket, s3_file, ExtraArgs={'ACL': 'public-read'})
        print("Upload Successful")
        return True
    except NoCredentialsError:
        print("Credentials not available")
        return False

def remove_bmo_provisioning(ignition_file):
    found = False
    with open(ignition_file, "r") as f:
        data = json.load(f)
        storageFiles = data['storage']['files']
        for index, fileData in enumerate(storageFiles[:]):
            if 'baremetal-provisioning-config' in fileData['path']:
                del storageFiles[index]
                found = True
    if found:
        with open(ignition_file,"w") as f:
            json.dump(data, f)


parser = argparse.ArgumentParser(description='Generate ignition manifest & kubeconfig')
parser.add_argument('--file_name', help='output directory name', default="output_dir")
parser.add_argument('--s3_endpoint_url', help='s3 endpoint url', default=None)
parser.add_argument('--s3_bucket', help='s3 bucket', default='test')
parser.add_argument('--files_prefix', help='file suffix', default='')
args = parser.parse_args()


install_config = os.environ.get("INSTALLER_CONFIG", None)

if install_config:
    subprocess.check_output("mkdir -p /installer_dir", shell=True)
    args.file_name = "installer_dir"
    with open('/installer_dir/install-config.yaml', 'w+') as f:
            f.write(install_config)

else:
    if not os.path.isdir('/installer_dir'):
        raise Exception('installer directory is not mounted')

    if not os.path.isfile('/installer_dir/install-config.yaml'):
        raise Exception("install config file not located in installer dir")


sysstdout = sys.stdout
command = "./openshift-install create ignition-configs --dir /installer_dir"
try:
    subprocess.check_output(command, shell=True, stderr = sysstdout)
except Exception as ex:
    raise Exception('Failed to generate files, exception: {}'.format(ex))


try:
    remove_bmo_provisioning("/installer_dir/bootstrap.ign")
except Exception as ex:
    raise Exception('Failed to remove BMO prosioning configuration from bootstrap ignition, exception: {}'.format(ex))

args.s3_endpoint_url = os.environ.get("S3_ENDPOINT_URL", args.s3_endpoint_url)
if args.s3_endpoint_url:
    bucket = os.environ.get('S3_BUCKET', args.s3_bucket)
    s3 = get_s3_client()

#     s3.create_bucket(Bucket=bucket)
    bucket = "test"
    prefix = os.environ.get("CLUSTER_ID", args.files_prefix)

    for root, _, files in os.walk(args.file_name):
         for r_file in files:
            logging.info("Uplading file: {}".format(r_file))
            file = os.path.join(root, r_file)
            s3_file_name = "{}/{}".format(prefix, r_file)
            print(s3_file_name)
            uploaded = upload_to_aws(s3, file, bucket, s3_file_name)
