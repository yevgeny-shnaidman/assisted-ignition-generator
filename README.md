This is a image for generating ignition manifests & kubeconfig

after updating the installer-config.yaml file template run this image with the directory containing the installer-config.yaml file mounted
for example:

docker run -v $(pwd)/installer_dir:/installer_dir -it quay.io/oscohen/ignition-manifests-and-kubeconfig-generate:latest
in the mounted dir the ignition files and the kubeconfig will be generated.
