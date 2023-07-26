import boto3

def toS3(file_path):
    s3 = boto3.client('s3')
    s3.upload_file(file_path, 'rekognition-video-console-demo-fra-107915466383-1685211164', file_path)
    print("Upload successful")
