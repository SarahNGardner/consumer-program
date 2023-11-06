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
    s3 = boto3.client('s3')
    response = s3.list_objects(Bucket=BUCKET_2_NAME, MaxKeys=1)

    if 'Contents' in response:
        request = response['Contents'][0]['Key']
        return request
    else:
        return None

def main():
    parser = argparse.ArgumentParser(description="Widget Request Consumer")
    parser.add_argument("--storage", choices=["s3", "dynamodb"], default="s3", help="Storage strategy (s3 or dynamodb)")
    args = parser.parse_args()

    while True:
        widget_request = read_widget_request()
        if widget_request:
            process_widget_request(widget_request)
        else:
            time.sleep(POLL_INTERVAL_SECONDS)


main()
