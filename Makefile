# ==== Config (override via env or make VAR=...) ====
REGISTRY 	?= registry.rednet.lan
IMAGE    	?= $(REGISTRY)/pxe-api
VERSION  	?= 1.0.0
TAGS     	?= dev
FORMAT   	?= docker
DOCKERFILE 	?= Dockerfile
CONTEXT    	?= .

# Build metadata
VCS_REF    	:= $(shell git rev-parse --short HEAD 2>/dev/null || echo unknown)
BUILD_DATE 	:= $(shell date -u +%Y-%m-%dT%H:%M:%SZ)

# Derived
ALL_TAGS   	:= $(VERSION) $(TAGS)
TAG_ARGS   	:= $(foreach t,$(ALL_TAGS),-t $(IMAGE):$(t))

# ==== Requirements ====
REQS_IN		?= pyproject.toml
REQS_OUT	?= requirements.txt
REQS_ARGS	?= --generate-hashes --no-annotate --strip-extras
# ==== Phony targets ====
.PHONY: help build rebuild clean requirements

help:
	@echo "Targets:"
	@echo "  make build         Build image (format=$(FORMAT)) with tags: $(ALL_TAGS)"
	@echo "  make rebuild       Build without cache"
	@echo "  make clean         Remove image tags locally"
	@echo ""
	@echo "Vars: REGISTRY, IMAGE, VERSION, TAGS, FORMAT, DOCKERFILE, CONTEXT"
	@echo "Examples:"d
	@echo "  make build FORMAT=docker TAGS=\"latest stable\""

$(REQS_OUT): $(REQS_IN)
	@echo ">> Compiling $(REQS_IN) -> $(REQS_OUT)"
	pip-compile $(REQS_ARGS) --output-file $(REQS_OUT) $(REQS_IN)

upgrade: $(REQS_IN)
	@echo ">> Upgrading $(REQS_OUT)"
	pip-compile --upgrade $(REQS_ARGS) --output-file $(REQS_OUT) $(REQS_IN)

requirements: $(REQS_OUT)


build: $(REQS_OUT)
	@echo ">> Building $(IMAGE) as $(ALL_TAGS) (format=$(FORMAT))"
	podman build \
	  --format $(FORMAT) \
	  --layers \
	  --build-arg VCS_REF=$(VCS_REF) \
	  --build-arg BUILD_DATE=$(BUILD_DATE) \
	  $(TAG_ARGS) \
	  -f $(DOCKERFILE) $(CONTEXT)

rebuild: $(REQS_OUT)
	@echo ">> Rebuilding (no cache) $(IMAGE) as $(ALL_TAGS) (format=$(FORMAT))"
	podman build \
	  --format $(FORMAT) \
	  --no-cache \
	  --build-arg VCS_REF=$(VCS_REF) \
	  --build-arg BUILD_DATE=$(BUILD_DATE) \
	  $(TAG_ARGS) \
	  -f $(DOCKERFILE) $(CONTEXT)

clean:
	@set -e; \
	for t in $(ALL_TAGS); do \
	  if podman image exists $(IMAGE):$$t; then \
	    echo ">> Removing $(IMAGE):$$t"; \
	    podman rmi -f $(IMAGE):$$t; \
	  fi; \
	done && rm $(REQS_OUT)
