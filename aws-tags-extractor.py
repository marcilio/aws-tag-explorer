import argparse
import boto3
import csv
import os

output_s3_bucket = os.environ['S3TagBucket']
output_s3_path = os.environ['S3TagKey']
output_file_path = "/tmp/tagged-resources.csv"
field_names = ['ResourceArn', 'TagKey', 'TagValue']

def upload_to_s3():
    print("Uploading file {} to s3://{}/{}".format(output_file_path, output_s3_bucket, output_s3_path))
    s3 = boto3.resource('s3')
    s3.Bucket(output_s3_bucket).upload_file(output_file_path, output_s3_path)
    print("Done uploading file {} to s3://{}/{}".format(output_file_path, output_s3_bucket, output_s3_path))

def writeToCsv(writer, tag_list):
    for resource in tag_list:
        print("Extracting tags for resource: " +
              resource['ResourceARN'] + "...")
        for tag in resource['Tags']:
            row = dict(
                ResourceArn=resource['ResourceARN'], TagKey=tag['Key'], TagValue=tag['Value'])
            writer.writerow(row)

def extract_tags():
    restag = boto3.client('resourcegroupstaggingapi')
    with open(output_file_path, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, quoting=csv.QUOTE_ALL,
                                delimiter=',', dialect='excel', fieldnames=field_names)
        writer.writeheader()
        response = restag.get_resources(ResourcesPerPage=50)
        writeToCsv(writer, response['ResourceTagMappingList'])
        while 'PaginationToken' in response and response['PaginationToken']:
            token = response['PaginationToken']
            response = restag.get_resources(
                ResourcesPerPage=50, PaginationToken=token)
            writeToCsv(writer, response['ResourceTagMappingList'])
    print("Gerenated file: {}".format(output_file_path))

def handler(event, context):
    extract_tags()
    upload_to_s3()
    return "Done extracting tags! Use provided Python3 script 'aws-tags-querier.py' (https://github.com/marcilio/aws-tag-explorer) to run SQL queries against your tags CSV file in S3."

def main():
    handler({},{})

if __name__ == '__main__':
    main()