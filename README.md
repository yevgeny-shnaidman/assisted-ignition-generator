### This is a image for generating ignition manifests & kubeconfig

after updating the installer-config.yaml file template run this image with the directory containing the installer-config.yaml file mounted
for example:

```
docker run -v $(pwd)/installer_dir:/installer_dir -it quay.io/oscohen/ignition-manifests-and-kubeconfig-generate:latest
```
in the mounted dir the ignition files and the kubeconfig will be generated.

Usage: 
```
usage: process-ignition-manifests-and-kubeconfig.py [-h]
                                                       [--file_name FILE_NAME]
                                                       [--s3_endpoint_url S3_ENDPOINT_URL]
                                                       [--s3_bucket S3_BUCKET]
   
   Generate ignition manifest & kubeconfig
   
   optional arguments:
     -h, --help            show this help message and exit
     --file_name FILE_NAME
                           output directory name
     --s3_endpoint_url S3_ENDPOINT_URL
                           s3 endpoint url
     --s3_bucket S3_BUCKET
                           s3 bucket
```