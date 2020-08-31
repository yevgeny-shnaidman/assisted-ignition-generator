GENERATOR := $(or ${GENERATOR},quay.io/ocpmetal/assisted-ignition-generator:latest)


all: pep8 pylint build

build:
	skipper build assisted-ignition-generator 

build-image:
	docker build --network=host  -f Dockerfile.assisted-ignition-generator . -t $(GENERATOR)

update: build
	GIT_REVISION=${GIT_REVISION} docker build --pull --build-arg GIT_REVISION -t $(GENERATOR) -f Dockerfile.assisted-ignition-generator .
	docker push $(GENERATOR)

.DEFAULT:
	skipper -v $(MAKE) $@
