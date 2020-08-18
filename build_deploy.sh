#!/bin/bash

TAG=$(git rev-parse --short=7 HEAD)
ASSISTED_IGNITION_GENERATOR="quay.io/app-sre/assisted-ignition-generator"

docker build -t "${ASSISTED_IGNITION_GENERATOR}:latest" -f Dockerfile.assisted-ignition-generator .
docker tag "${ASSISTED_IGNITION_GENERATOR}:latest" "${ASSISTED_IGNITION_GENERATOR}:${TAG}"

DOCKER_CONF="${PWD}/.docker"
mkdir -p "${DOCKER_CONF}"
docker --config="${DOCKER_CONF}" login -u="${QUAY_USER}" -p="${QUAY_TOKEN}" quay.io

docker --config="${DOCKER_CONF}" push "${ASSISTED_IGNITION_GENERATOR}:latest"
docker --config="${DOCKER_CONF}" push "${ASSISTED_IGNITION_GENERATOR}:${TAG}"

