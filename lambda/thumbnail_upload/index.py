import os
import json
import boto3
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
YOUTUBE_CREDENTIALS_KEY = os.getenv('YOUTUBE_CREDENTIALS_KEY')


def get_youtube_credentials():
    s3 = boto3.client('s3')
    response = s3.get_object(Bucket=S3_BUCKET_NAME, Key=YOUTUBE_CREDENTIALS_KEY)
    credentials_data = response['Body'].read().decode('utf-8')
    return Credentials.from_authorized_user_info(json.loads(credentials_data))


def update_youtube_thumbnail(video_id, file_path):
    credentials = get_youtube_credentials()
    youtube = build('youtube', 'v3', credentials=credentials)

    request = youtube.thumbnails().set(
        videoId=video_id,
        media_body=file_path
    )
    response = request.execute()
    return response


def lambda_handler(event, context):
    try:
        video_id = event['queryStringParameters']['video-id']
        file_content = event['body']
        file_name = f"/tmp/{video_id}.jpg"

        with open(file_name, 'wb') as file:
            file.write(file_content)

        response = update_youtube_thumbnail(video_id, file_name)

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Thumbnail updated successfully!', 'response': response})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
