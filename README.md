# splat-upi-installer-dependencies

## Multi-architecture govc and PowerShell images

This repository builds Linux `amd64` and `arm64` variants of:

- `quay.io/ocp-splat/govc:v0.30.7`
- `quay.io/ocp-splat/pwsh:v7.3.12`

The image recipes download the official architecture-specific upstream releases and verify their SHA-256 checksums before assembling the image. The govc image stays `scratch`-based. The PowerShell image uses native UBI 9.4 variants, installs PowerShell 7.3.12 and Azure CLI 2.61.0.post20240516044921, and carries VMware.PowerCLI 13.2.1.22851661 plus EPS 1.0 from the pinned amd64 source-image digest in its Containerfile. The module files are architecture-independent; the final image imports them and smoke-checks PowerShell on the target architecture.

## CI build and publish

`.github/workflows/build-multiarch-images.yml` builds both images for `linux/amd64,linux/arm64` on pull requests and pushes to `main`. Those runs build but do not publish. A manual `workflow_dispatch` from `main` publishes the versioned tags to Quay and verifies that each tag's manifest index includes both architectures.

Configure repository secrets `QUAY_USERNAME` and `QUAY_PASSWORD` with credentials that can push to `quay.io/ocp-splat`. Dispatching the workflow on a branch other than `main` only builds; it never logs in or pushes.

## Local build and publish

Use Docker Buildx with a builder that supports emulation, then build and push each image:

```sh
docker buildx build --platform linux/amd64,linux/arm64 \
  -f images/govc/Containerfile \
  -t quay.io/ocp-splat/govc:v0.30.7 --push .

docker buildx build --platform linux/amd64,linux/arm64 \
  -f images/pwsh/Containerfile \
  -t quay.io/ocp-splat/pwsh:v7.3.12 --push .
```

Check the published indexes:

```sh
docker buildx imagetools inspect quay.io/ocp-splat/govc:v0.30.7
docker buildx imagetools inspect quay.io/ocp-splat/pwsh:v7.3.12
```

The Dockerfiles pin artifact checksums. When upgrading either upstream version, update its Dockerfile version and per-architecture checksums together, then update the corresponding workflow tag.

## Runtime contract

The PowerShell image preserves the UPI CI inputs: PowerCLI and EPS are available for all users, and Azure CLI is at `/go/src/github.com/openshift/installer/azure-cli/bin/az` (also linked as `/usr/local/bin/az`). Azure CLI is installed from `images/pwsh/azure-cli-requirements.lock` in a target-platform stage with native Python build dependencies, then copied into the runtime image without the compiler toolchain. The Dockerfile smoke-checks Azure CLI's version and MySQL command module, and imports both PowerShell modules for each target architecture. Update the lock from a known-good image when changing the Azure CLI version; keep the PowerCLI/EPS source-image digest in sync with consumers.
