import boto3
import deleteDuplicates

def detect_text(photo, bucket):
    session = boto3.Session(profile_name='default',region_name='eu-central-1')
    client = session.client('rekognition')
    response = client.detect_text(Image={'S3Object': {'Bucket': bucket, 'Name': photo}})
    textDetections = response['TextDetections']
     
    s='' 
    for text in textDetections:
        s+= text['DetectedText']+"\n"
        #print(text['DetectedText'])

    with open('output.txt', 'w', encoding='utf-8') as file1:
        if s != '':
            file1.write(s)
        else:
            file1.write("no text was detected")
    


def main(photo_path):
    print('hi')
    bucket = 'rekognition-video-console-demo-fra-107915466383-1685211164'
    photo = photo_path
    detect_text(photo, bucket)
    deleteDuplicates.deleteDup('output.txt')

if __name__ == "__main__":
    main('nonEnglish.jpg')
