import argparse
import boto3

# Examples:
#
# 1) Return the resource ARNs of all route tables containing a tag named 'aws:cloudformation:stack-name'
# python aws-tagged-resources-querier.py \
#      --bucket mybucket \
#      --key mytaggedresources-files.csv \
#      --query "select ResourceArn from s3object s \
#               where s.ResourceArn like 'arn:aws:ec2%route-table%' \
#                 and s.TagKey='aws:cloudformation:stack-name'"
#
# 2) Return the resource ARNs of all resources created by a stack named 'my-stack'
# python aws-tagged-resources-querier.py \
#      --bucket mybucket \
#      --key mytaggedresources-files.csv \
#      --query "select ResourceArn from s3object s \
#               where s.TagKey='aws:cloudformation:stack-name'"
#                 and s.TagValue='my-stack'"

def input_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bucket", required=True, help="SQL query to filter tagged resources output")
    parser.add_argument("--key", required=True, help="SQL query to filter tagged resources output")
    parser.add_argument("--query", default="select * from s3object", help="SQL query to filter tagged resources output")
    return parser.parse_args()

def main():

    args = input_args()

    s3 = boto3.client('s3')
    response = s3.select_object_content(
        Bucket=args.bucket,
        Key=args.key,
        ExpressionType='SQL',
        Expression=args.query,
        InputSerialization = {'CSV': {"FileHeaderInfo": "Use"}},
        OutputSerialization = {'CSV': {}},
    )

    for event in response['Payload']:
        if 'Records' in event:
            records = event['Records']['Payload'].decode('utf-8')
            print(records)
            
if __name__ == '__main__':
    main()
