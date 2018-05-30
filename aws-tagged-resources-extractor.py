import argparse
import boto3
import csv

field_names = ['ResourceArn', 'TagKey', 'TagValue']


def writeToCsv(writer, args, tag_list):
    for resource in tag_list:
        print("Extracting tags for resource: " +
              resource['ResourceARN'] + "...")
        for tag in resource['Tags']:
            row = dict(
                ResourceArn=resource['ResourceARN'], TagKey=tag['Key'], TagValue=tag['Value'])
            writer.writerow(row)


def input_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True,
                        help="Output CSV file (eg, /tmp/tagged-resources.csv)")
    return parser.parse_args()


def main():
    args = input_args()
    restag = boto3.client('resourcegroupstaggingapi')
    with open(args.output, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, quoting=csv.QUOTE_ALL,
                                delimiter=',', dialect='excel', fieldnames=field_names)
        writer.writeheader()
        response = restag.get_resources(ResourcesPerPage=50)
        writeToCsv(writer, args, response['ResourceTagMappingList'])
        while 'PaginationToken' in response and response['PaginationToken']:
            token = response['PaginationToken']
            response = restag.get_resources(
                ResourcesPerPage=50, PaginationToken=token)
            writeToCsv(writer, args, response['ResourceTagMappingList'])


if __name__ == '__main__':
    main()
