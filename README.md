# AWS Tag Explorer

Extract all tags from your AWS account into a S3 file. Query tags file with SQL.

This application is available on the [AWS Serverless Repository](https://aws.amazon.com/serverless/serverlessrepo/) for immediate use.

# Resources provided:

1. Lambda function to extract Tag information for all resources within an AWS account and upload the tags (via a CSV file) into an S3 bucket
2. A Python3 script to query via SQL the tag CSV file stored in S3


# Important

Due to a limitation of the AWS Serverless Repository, after you deploy this Serverless App you'll have to manually add the following policy to the Lambda role in order to allow the Lambda function to fetch resource tags.

```json
{   
    "Version" : "2012-10-17",   
    "Statement" : [{      
       "Effect" : "Allow",      
       "Action" : "tag:GetResources",      
       "Resource" : "*"      
    }] 
}
```

## Extract Tags

Navigate to the AWS Lambda Console and run provided Lambda function ```AWSTaggedResourcesExtractor``` (alternatively, add a regular trigger via CloudWatch events). The Lambda function will generate a CSV file (name provided during stack creation) under the S3 bucket (name provided during stack creation) specified to store all tags extracted from the AWS account where the Lambda resides in.

You can also invoke the extraction process locally if you have access to the code like this:

```bash
export S3TagBucket="S3-BUCKET-TO-HOLD-TAGS-FILE"
export S3TagKey="mytags.csv"  # replace with any file name you wish
python aws-tags-extractor.py 
```

## Query Tags

The CSV file containing tag information contains the following columns: ```ResourceArn```, ```TagKey```, ```TagValue```. Run, SQL queries against the CSV file using the provided ```aws-tags-querier.py ``` Python3 script.

Here's an example:

Query: __Return the resource ARNs of all route tables containing a tag named 'aws:cloudformation:stack-name' in the ```QA``` AWS account__

```bash
export AWS_PROFILE=QA_AWS_ACCOUNT
python aws-tags-querier \
     --bucket [REPLACE-WITH-YOUR-S3-BUCKET] \
     --key mytags.csv \
     --query "select ResourceArn from s3object s \
              where s.ResourceArn like 'arn:aws:ec2%route-table%' \
                and s.TagKey='aws:cloudformation:stack-name'"
```

__Happy Tagging!__
