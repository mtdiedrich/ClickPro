import os
import google.auth
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import boto3
import json

# Environment variables
VIDEO_ID = os.getenv('VIDEO_ID')
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
S3_OBJECT_KEY = os.getenv('S3_OBJECT_KEY')


def get_credentials():
    s3 = boto3.client('s3')
    response = s3.get_object(Bucket=S3_BUCKET_NAME, Key=S3_OBJECT_KEY)
    credentials_data = response['Body'].read().decode('utf-8')
    return Credentials.from_authorized_user_info(json.loads(credentials_data),
                                                 scopes=['https://www.googleapis.com/auth/youtube.force-ssl'])


def update_thumbnail(youtube, video_id, thumbnail_url):
    request = youtube.thumbnails().set(
        videoId=video_id,
        media_body=thumbnail_url
    )
    response = request.execute()
    print(response)


def lambda_handler(event, context):
    body = json.loads(event['body'])
    video_id = body.get('video_id', VIDEO_ID)
    thumbnail_url = body['thumbnail_url']

    youtube = build('youtube', 'v3', credentials=get_credentials())
    update_thumbnail(youtube, video_id, thumbnail_url)

    return {
        'statusCode': 200,
        'body': json.dumps('Thumbnail updated successfully!')
    }
