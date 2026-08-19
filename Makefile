IMAGE     ?= harbor.winniewinnie.com/ecowitt2mqtt/ecowitt2mqtt
TAG       ?= latest
# The cluster nodes are amd64; a native build on Apple Silicon produces an
# arm64-only manifest the nodes cannot pull ("no match for platform").
PLATFORM  ?= linux/amd64
# Namespace the deployment runs in; push rolls it to pull the new image.
NAMESPACE ?= home-automation

.PHONY: docker push

docker:
	docker build -t $(IMAGE):$(TAG) .

# Build for the cluster's architecture, load the (cross-built) image into the
# local docker store, then push. --load keeps this working with the default
# "docker" buildx driver, which cannot push to a registry directly. Finally roll
# the deployment so the node pulls the new :latest image.
push:
	docker buildx build --platform $(PLATFORM) -t $(IMAGE):$(TAG) --load .
	docker push $(IMAGE):$(TAG)
	kubectl rollout restart deployment/ecowitt2mqtt -n $(NAMESPACE)
