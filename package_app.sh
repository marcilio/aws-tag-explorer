#!/bin/bash

#======================================================================
# Package Lambda Function for AWS Serverless Repository
# - Make sure AWS_PROFILE env variable is set properly
#======================================================================

set -e

function error() {
    echo "Error: $1"
    exit -1
}

[[ -n "$1" ]] || error "Missing S3 bucket to package this SAM application"

lambda_package_s3_bucket=$1

app_name="aws-tag-explorer"
lambda_template="sam_template.yaml"
gen_lambda_template="/tmp/${app_name}-${lambda_template}"
virtual_env_location="/Users/marcilio/.virtualenv"
virtual_env_name="aws-tagging"
package_dir="/tmp/${app_name}"

rm -rf $package_dir
cp -R ./ $package_dir
cp -R "${virtual_env_location}/${virtual_env_name}/lib/python3.6/site-packages/" $package_dir

aws cloudformation package \
    --template-file $lambda_template \
    --s3-bucket $lambda_package_s3_bucket \
    --output-template-file $gen_lambda_template

