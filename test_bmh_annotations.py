#!/usr/bin/env python

import argparse
import logging
import subprocess
import sys
import os
import re
import base64
import glob
import json
import yaml
import boto3
from botocore.exceptions import NoCredentialsError
import bmh_utils

# BMH_CR_FILE_PATTERN = 'openshift-cluster-api_hosts'


#def is_bmh_cr_file(path):
#    if BMH_CR_FILE_PATTERN in path:
#        return True
#    return False


#def get_bmh_dict_from_file(file_data):
#    source_string = file_data['contents']['source']
#    base64_string = re.split("base64,", source_string)[1]
#    decoded_string = base64.b64decode(base64_string).decode()
#    return yaml.safe_load(decoded_string)


def main():
    expected_annotations = []
    test_result_files = glob.glob("tests/test_annotation_host*")
    for file in test_result_files:
        with open(file) as json_file:
            data = json.load(json_file)
            expected_annotations.append(data)

    with open("installer_dir/bootstrap.ign", "r") as file_obj:
        data = json.load(file_obj)
        storage_files = data['storage']['files']
        for file_data in storage_files:
            if bmh_utils.is_bmh_cr_file(file_data['path']):
                bmh_dict = bmh_utils.get_bmh_dict_from_file(file_data)
                annotations = bmh_dict['metadata']['annotations']
                res_annotation = json.loads(annotations['baremetalhost.metal3.io/status'])
                found = False
                for annot in expected_annotations[:]:
                    if annot == res_annotation:
                        expected_annotations.remove(annot)
                        found = True
                if not found:
                    raise Exception("no matching expected annotation for: ", json.dumps(res_annotation))
        if len(expected_annotations) != 0:
            raise Exception("some expected annotations were not found")
    print("BMH Test finished successfully")

if __name__ == "__main__":
    main()
