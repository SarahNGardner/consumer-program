import time
import argparse
import boto3
import os

# Constants
POLL_INTERVAL_SECONDS = 0.1  # 100 ms
BUCKET_2_NAME = "usu-cs5260-red-requests"
BUCKET_3_NAME = "usu-cs5260-red-web"
DYNAMODB_TABLE_NAME = "your-dynamodb-table-name"

aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")

boto3.setup_default_session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)

def process_widget_create_request(request, storage_strategy):
    s3_client = boto3.client('s3')
    if storage_strategy == 'dynamodb':
        dynamodb = boto3.resource('dynamodb')
        dynamodb.put_item(
            TableName=DYNAMODB_TABLE_NAME,
            Item=request
        )

    elif storage_strategy == 'bucket':
        s3_client.upload_file(request, BUCKET_3_NAME, request)

    else:
        print("Invalid storage strategy. Choose 'dynamodb' or 'bucket'.")


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

    while True:
        widget_request = read_widget_request()
        if widget_request:
            process_widget_create_request(widget_request)
        else:
            time.sleep(POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
