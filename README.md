### This is a image for generating ignition manifests & kubeconfig

1) Dockerfile (depricated) - dockerfile for building the ignition-manifests-and-kubeconfig-generate image with openshift-installer platform none
2) Dockerfile.baremetal - dockerfile for building the ignition-manifests-and-kubeconfig-generate image with openshift-installer platform baremetal
3) installer_dir/install-config.yaml - example of install-config.yaml for none platform
4) installer_dir/install-config.yaml.baremetal - example of install-config.yaml for baremetal platform. 
5) openshift-install - executable that produces ignition files. It is copied from installer repository before issuing docker build command. Should be build in accordance with the platform we are running on
    a) none platform       - should be build with command <TAGS="none" hack/build.sh>
    b) baremetal platform  - should be build with command <TAGS="baremetal" hack/build.sh>. Prior to that the following files in the installer souce code should be changed:
                             - hack/build.sh                             - CGO_ENABLED flag should be enable in case of baremetal platform also: <if (echo "${TAGS}" | grep -q 'libvirt\|baremetal')>
                             - pkg/types/baremetal/validation/libvirt.go -  build tag should be changed from baremetal to libvirt ( to avoid validations via libvirt)

Building:
----------------
1) currently we use our own openshift-install executable. We save it into the containener using Dockerfile.installer-image and pushing it to a repository ( make sure ot make it public. Currently
   we use quay.io/yshnaidm/openshift-installer. In case we recompile openshift-install, we need to update this image:
   docker build -f Dockerfile.installer-image -t <repository> .
   Example: docker build -f Dockerfile.installer-image -t quay.io/yshnaidm/openshift-installer:latest .
2) we are using the image built in step 1 to get the needed openshift-install. Once we start using openshift-install from the release, we can update Dockerfile.baremetal accordingly
   docker build -f Dockerfile.baremetal . -t quay.io/ocpmetal/ignition-manifests-and-kubeconfig-generate:stable


Testing:
---------------
You can test generation of files (not the uploading) locally on your laptop
After coping the install-config.yaml.platform to installer-config.yaml and updating installer-config.yaml file template run this image with the directory containing the installer-config.yaml file mounted
for example:

```
docker run -v $(pwd)/installer_dir:/data/installer_dir -it quay.io/oscohen/ignition-manifests-and-kubeconfig-generate:latest
```
in the mounted dir the ignition files and the kubeconfig will be generated.
you will also be able to see the list of the files that would have been uploaded to s3 in case of an actual run

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
