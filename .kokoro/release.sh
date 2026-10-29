#!/bin/bash
set -euo pipefail

# Default to dry-run for safety unless DRY_RUN=false is explicitly passed.
DRY_RUN="${DRY_RUN:-true}"
if [[ "${DRY_RUN}" != "true" && "${DRY_RUN}" != "false" ]]; then
  echo "ERROR: DRY_RUN must be 'true' or 'false' (got '${DRY_RUN}')." >&2
  exit 1
fi

# -----------------------------------------------------------------------------
# 1. Workspace & Directory Resolution
# -----------------------------------------------------------------------------
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${REPO_DIR}"

echo "=== Building and Releasing from: ${REPO_DIR} (DRY_RUN=${DRY_RUN}) ==="

# -----------------------------------------------------------------------------
# 2. Environment & Tooling Setup
# -----------------------------------------------------------------------------
PYENV_VER="3.12"

echo "=== Installing pyenv Python version (if needed): ${PYENV_VER} ==="
pyenv install -s "${PYENV_VER}"

echo "=== Activating pyenv Python version: ${PYENV_VER} ==="
pyenv global "${PYENV_VER}"

python3 -m venv .venv
source ./.venv/bin/activate

python3 -m pip install --require-hashes -r .kokoro/requirements.txt

# -----------------------------------------------------------------------------
# 3. Clean and Build Distribution Packages
# -----------------------------------------------------------------------------
echo "=== Cleaning previous build artifacts ==="
rm -rf dist/ build/ *.egg-info

echo "=== Building sdist and wheel ==="
python3 -m build

echo "=== Validating built packages with twine ==="
twine --version
twine check dist/*

# -----------------------------------------------------------------------------
# 4. Upload to Internal Exit Gate Artifact Registry
# -----------------------------------------------------------------------------
EXIT_GATE_PROJECT="oss-exit-gate-prod"
EXIT_GATE_LOCATION="us"
EXIT_GATE_REPOSITORY="google-ads-python--pypi"
PACKAGE_NAME="google-ads"

if gcloud artifacts packages describe "${PACKAGE_NAME}" \
    --project="${EXIT_GATE_PROJECT}" \
    --location="${EXIT_GATE_LOCATION}" \
    --repository="${EXIT_GATE_REPOSITORY}" &>/dev/null; then
  echo "=== Deleting existing package '${PACKAGE_NAME}' from Exit Gate staging repository ==="
  gcloud artifacts packages delete "${PACKAGE_NAME}" \
    --project="${EXIT_GATE_PROJECT}" \
    --location="${EXIT_GATE_LOCATION}" \
    --repository="${EXIT_GATE_REPOSITORY}" \
    --quiet
else
  echo "=== Skipping deletion. Package '${PACKAGE_NAME}' not found in staging repository. This is normal. ==="
fi

EXIT_GATE_REPO="https://us-python.pkg.dev/oss-exit-gate-prod/google-ads-python--pypi"

echo "=== Uploading packages to Exit Gate staging repository: ${EXIT_GATE_REPO} ==="
twine upload --repository-url "${EXIT_GATE_REPO}" dist/*

# -----------------------------------------------------------------------------
# 5. Trigger Exit Gate Release via GCS Manifest
# -----------------------------------------------------------------------------
if [[ "${DRY_RUN}" == "true" ]]; then
  echo "=== DRY_RUN is enabled. Skipping manifest upload to Exit Gate. ==="
  echo "Artifacts are staged in Artifact Registry."
  exit 0
fi

echo "=== Creating targeted release manifest for google-ads ==="
cat <<EOF > manifest.json
{
  "publish_all": false,
  "publishing_groups": [
    {
      "packages": [
        {
          "name": "google-ads"
        }
      ]
    }
  ]
}
EOF

EXIT_GATE_BUCKET="gs://oss-exit-gate-prod-projects-bucket/google-ads-python/pypi/manifests"
MANIFEST_NAME="manifest-$(date +%Y%m%d%H%M%S).json"

echo "=== Uploading manifest to ${EXIT_GATE_BUCKET}/${MANIFEST_NAME} ==="
gcloud storage cp manifest.json "${EXIT_GATE_BUCKET}/${MANIFEST_NAME}"

echo "========================================================================="
echo "Release successfully triggered! Exit Gate will now verify BCID and publish to PyPI."
echo "========================================================================="
