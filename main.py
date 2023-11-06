import time
import argparse
import boto3

# Constants
POLL_INTERVAL_SECONDS = 0.1  # 100 ms
BUCKET_2_NAME = "usu-cs5260-red-requests"
BUCKET_3_NAME = "usu-cs5260-red-web"
DYNAMODB_TABLE_NAME = "your-dynamodb-table-name"

def process_widget_request(request):
    s3_client = boto3.client('s3')
    s3_client.upload_file(request, BUCKET_3_NAME, request)

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(DYNAMODB_TABLE_NAME)

    s3_client.delete_object(Bucket=BUCKET_2_NAME, Key=request)

def read_widget_request():


def main():


main()
