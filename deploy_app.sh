#!/bin/bash

#======================================================================
# Deploy Lambda Function in an AWS account for testing purposes
# - Make sure AWS_PROFILE env variable is set properly
#======================================================================

set -e

function error() {
    echo "Error: $1"
    exit -1
}

[[ -n "$1" ]] || error "Missing S3 bucket to store CSV file containing tags (eg, my-tagged-resources-bucket)"
[[ -n "$2" ]] || error "Missing S3 key for CSV file containing tags (eg, my-tagged-resources.csv)"

s3_tag_bucket=$1
s3_tag_key=$2

app_name="aws-tag-explorer"
lambda_template="sam_template.yaml"
gen_lambda_template="/tmp/${app_name}-${lambda_template}"
stack_name=$app_name

aws cloudformation deploy \
    --template-file $gen_lambda_template \
    --stack-name $stack_name \
    --parameter-overrides \
        S3TagBucket="$s3_tag_bucket" \
        S3TagKey="$s3_tag_key" \
    --capabilities \
        CAPABILITY_IAM
