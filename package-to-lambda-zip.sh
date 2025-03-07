#!/bin/bash

rm lambda-deployment-package.zip
rm -rf lambda-dependencies

set -e

pip3 install --target ./lambda-dependencies -r requirements-lambda.txt
cd lambda-dependencies
7z a -r ../lambda-deployment-package.zip .

cd ..
for i in *.py; do
    7z a lambda-deployment-package.zip $i
done
