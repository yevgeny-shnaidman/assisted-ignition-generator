### This is a image for generating ignition manifests & kubeconfig
1) Dockerfile.assisted-ignition-generator - dockerfile for building the assisted-ignition-generator image
2) installer_dir - testing directory that includes all the files needed for local testing (on laptop)
   - install-config.yaml.baremetal -  install-config for baremetal environment
   - test_env.txt - environment variables for testing
   - test_hosts_list.yaml - simulated output of Get Host from assisted-service command.Used as an input for testing


Environment variables:
-----------------------------

Since this image will be run as a job initiated by assisted-service, all input parameters are passed as environment variables:

1) WORK_DIR - directory inside the container where we run all our code. Default: /data
2) INSTALLER_CONFIG - directory where the install-config.yaml is created/set and where the output ( ignitions) are created. Default: /data/installer_dir
3) CLUSTER_ID - input parameter for the job
4) INVENTORY_ENDPOINT - url that defines how python client connects to assisted-service.
5) S3_ENDPOINT_URL - S3 endpoint. results of the job will be uploaded to that S3
6) S3_BUCKET - the S3 bucket to upload to
7) aws_access_key_id - AWS access key id
8) aws_secret_access_key - AWS secret access key
9) OPENSHIFT_INSTALL_RELEASE_IMAGE_OVERRIDE - the OCP release image that we are working on

Building:
---------------------------------------
1) Build quay.io/ocpmetal/assisted-ignition-generator - image for running ignition generation job. Uses assisted-service container to install assisted-service python client. Install OC client by wget appropriate package 
   Note: beforebuilding make sure that you deleted all the files under installer_dir that were created during testing:
   
   cd installer_dir && sudo rm -rf auth bootstrap.ign install-config.yaml master.ign metadata.json worker.ign .openshift_install.log .openshift_install_state.json

   make build
   docker tag <image id> quay.io/ocpmetal/assisted-ignition-generator 



Testing:
-------------------------------------

Testing can be done in 2 stages:

1) Test generation of the ignition files , locally on your laptop.

   a) Copy install-config.yaml.baremetal to installer-config.yaml in installer_dir.

   b) Run assisted-ignition-generator immage that you previously created.
      Since 4.6 we use release image to extract installer.The value of release-image is set as environment value by bm-envtory. when testing we use env file installer-dir/test_env.txt
      If no error is printed, then test was successsful and the ignition files are generated in the installer_dir

      docker run -v $(pwd)/installer_dir:/data/installer_dir --env-file $(pwd)/installer_dir/test_env.txt -it assisted-ignition-generator:<hash>

2) Test specific manipulations on generated ignition. Currently only BMH annotations generations is checked. This stage must be run only after first stage
   
   a) Change permissions of the file generated in the first stage.
      From installer_dir run:
      
      sudo chmod -R 777 auth bootstrap.ign master.ign metadata.json worker.ign .openshift_install.log .openshift_install_state.json
   
   b) Test code that changes the ignitions:

      skipper run python3 test_bmh_annotations.py
