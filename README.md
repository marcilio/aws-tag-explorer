# AWS Tag Explorer

Extract all AWS tags within an account. Use SQL to query them.

Python3 scripts are provided to:

1. Extract Tag information for all resources within an AWS account (into a CSV file which is then uploaded to an Amazon S3 bucket)
2. Query Tag information from the CSV file using ```SQL``` queries

## Requirements

This project was built on a MacOS environment with Python3 installed.

## Extract Tagged Resources

Here is how the extract process can be triggered for a given QA account (assuming that there is a QA_AWS_ACCOUNT AWS profile defined under your ```~/.aws/credentials``` file).

```bash
export AWS_PROFILE=QA_AWS_ACCOUNT
python aws-tagged-resources-extractor.py --output /tmp/qa-tagged-resources.csv
```

This will extract all tags (Tagged resource ARN, Tag Name, Tag Value) in your QA account into a CSV file.

## Query Tagged Resources

First, upload generated file ```/tmp/qa-tagged-resources.csv``` to an S3 bucket of your choice like this: 

```bash
aws s3 cp /tmp/qa-tagged-resources.csv s3://[REPLACE-WITH-YOUR-S3-BUCKET]
```

The CSV file contains the following columns: ```ResourceArn```, ```TagKey```, ```TagValue```. Run, SQL queries against the CSV file in S3 like this:

Query: __Return the resource ARNs of all route tables containing a tag named 'aws:cloudformation:stack-name' in the ```QA``` AWS account__

```bash
export AWS_PROFILE= CENTRAL_AWS_ACCOUNT
python aws-tagged-resources-querier \
     --bucket [REPLACE-WITH-YOUR-S3-BUCKET] \
     --key qa-tagged-resources.csv \
     --query "select ResourceArn from s3object s \
              where s.ResourceArn like 'arn:aws:ec2%route-table%' \
                and s.TagKey='aws:cloudformation:stack-name'"
```

Happy Tagging!