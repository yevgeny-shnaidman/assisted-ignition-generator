FROM python:2.7

RUN pip install boto3
RUN pip install botocore

COPY ./openshift-install /
COPY ./process-ignition-manifests-and-kubeconfig.py /

ENTRYPOINT ["python", "process-ignition-manifests-and-kubeconfig.py"]