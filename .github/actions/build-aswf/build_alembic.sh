#!/bin/bash

# Debugging options
set -e -x

# Build Alembic
cd /github/workspace/  # Default location of packages in docker action
python setup.py bdist_wheel

# Bundle external shared libraries into the wheels
find . -type f -iname "*-linux*.whl" -execdir sh -c "auditwheel repair '{}' -w ./ --plat '${PLAT}' || { echo 'Repairing wheels failed.'; auditwheel show '{}'; exit 1; }" \;

echo "Succesfully build wheels:"
find . -type f -iname "*-manylinux*.whl"
