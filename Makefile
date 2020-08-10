SERVICE := $(or ${SERVICE},quay.io/ocpmetal/assisted-ignition-generator:latest)


all: pep8 pylint build

build:
	skipper build assisted-ignition-generator

update: build
	GIT_REVISION=${GIT_REVISION} docker build --pull --build-arg GIT_REVISION -t $(SERVICE) -f Dockerfile.assisted-ignition-generator .
	docker push $(SERVICE)

.DEFAULT:
	skipper -v $(MAKE) $@
