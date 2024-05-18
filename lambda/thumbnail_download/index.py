import os
import boto3
import json
import requests

# Environment variables
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')


def download_thumbnail(video_id):
    # Get number of items in bucket
    s3 = boto3.client('s3')
    response = s3.list_objects_v2(Bucket=S3_BUCKET_NAME)
    number_of_items = len(response['Contents'])
    # Download thumbnail
    thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
    response = requests.get(thumbnail_url)
    if response.status_code == 200:
        s3 = boto3.client('s3')
        s3.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=f"{video_id}/{number_of_items}.jpg",
            Body=response.content,
            ContentType='image/jpeg'
        )
        return f"Thumbnail for video ID {video_id} downloaded successfully."
    else:
        return f"Failed to download thumbnail for video ID {video_id}. Status code: {response.status_code}"


def lambda_handler(event, context):
    body = json.loads(event['body'])
    video_id = body['video_id']

    result = download_thumbnail(video_id)

    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
