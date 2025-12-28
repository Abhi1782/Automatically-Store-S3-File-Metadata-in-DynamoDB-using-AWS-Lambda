import json
import boto3
from urllib.parse import unquote_plus
from datetime import datetime

s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

TABLE_NAME = "S3FilesMetadata"
table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):
    try:
        for record in event['Records']:
            bucket_name = record['s3']['bucket']['name']
            object_key = unquote_plus(record['s3']['object']['key'])

            response = s3_client.head_object(
                Bucket=bucket_name,
                Key=object_key
            )

            item = {
                # MUST MATCH DynamoDB PARTITION KEY NAME
                "FileName": object_key,

                "BucketName": bucket_name,
                "FileSize": response['ContentLength'],
                "ContentType": response.get('ContentType', 'unknown'),
                "LastModified": response['LastModified'].isoformat(),
                "UploadedAt": datetime.utcnow().isoformat()
            }

            table.put_item(Item=item)
            print(f"Metadata stored successfully for {object_key}")

        return {
            "statusCode": 200,
            "body": json.dumps("Metadata stored successfully")
        }

    except Exception as e:
        print("ERROR:", str(e))
        raise
