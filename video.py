import boto3
import json
import sys
import time
import deleteDuplicates


class VideoDetect:

    jobId = ''
    roleArn = ''
    bucket = ''
    video = ''
    startJobId = ''
    sqsQueueUrl = ''
    snsTopicArn = ''
    processType = ''


    def __init__(self, role, bucket, video, client, rek, sqs, sns):
        self.roleArn = role
        self.bucket = bucket
        self.video = video
        self.client = client
        self.rek = rek
        self.sqs = sqs
        self.sns = sns

    def GetSQSMessageSuccess(self):

        jobFound = False
        succeeded = False

        dotLine = 0
        while jobFound == False:
            sqsResponse = self.sqs.receive_message(QueueUrl=self.sqsQueueUrl, MessageAttributeNames=['ALL'],
                                                   MaxNumberOfMessages=1)

            if sqsResponse:

                if 'Messages' not in sqsResponse:
                    if dotLine < 40:
                        dotLine = dotLine + 1
                    else:
                        dotLine = 0
                    sys.stdout.flush()
                    time.sleep(5)
                    continue

                for message in sqsResponse['Messages']:
                    notification = json.loads(message['Body'])
                    rekMessage = json.loads(notification['Message'])
                    print(rekMessage['JobId'])
                    print(rekMessage['Status'])
                    if rekMessage['JobId'] == self.startJobId:
                        print('Matching Job Found:' + rekMessage['JobId'])
                        jobFound = True
                        if (rekMessage['Status'] == 'SUCCEEDED'):
                            succeeded = True

                        self.sqs.delete_message(QueueUrl=self.sqsQueueUrl,
                                                ReceiptHandle=message['ReceiptHandle'])
                    else:
                        print("Job didn't match:" +
                              str(rekMessage['JobId']) + ' : ' + self.startJobId)
                    
                    self.sqs.delete_message(QueueUrl=self.sqsQueueUrl,
                                            ReceiptHandle=message['ReceiptHandle'])

        return succeeded


    def StartTextDetection(self):
        response=self.rek.start_text_detection(Video={'S3Object': {'Bucket': self.bucket, 'Name': self.video}},
            NotificationChannel={'RoleArn': self.roleArn, 'SNSTopicArn': self.snsTopicArn})

        self.startJobId=response['JobId']

  

    def GetTextDetectionResults(self):
        maxResults = 1
        paginationToken = ''
        finished = False
        s=''

        while finished == False:
            response = self.rek.get_text_detection(JobId=self.startJobId,
                                            MaxResults=maxResults,
                                            NextToken=paginationToken)
            
            for textDetection in response['TextDetections']:
                text=textDetection['TextDetection']
                s += text['DetectedText'] + '\n'
                print(text['DetectedText'])
 
            if 'NextToken' in response:
                paginationToken = response['NextToken']
            
            else:
                finished = True
                with open('output.txt', 'w', encoding='utf-8') as file1:
                    if s != '':
                        file1.write(s)
                    else:
                        file1.write("no text was detected")
            

    def SetTopicandQueueInfo(self):

        sqsQueueName='MyQueue'
        self.sqsQueueUrl = self.sqs.get_queue_url(QueueName=sqsQueueName)['QueueUrl']
        self.snsTopicArn='arn:aws:sns:eu-central-1:107915466383:AmazonRekognitionText'

        

def main(vid_path):
    
    roleArn = 'arn:aws:iam::107915466383:role/Rekognition'
    bucket = 'rekognition-video-console-demo-fra-107915466383-1685211164'
    video = vid_path

    session = boto3.Session(profile_name='default',region_name='eu-central-1')
    client = session.client('rekognition')
    rek = boto3.client('rekognition',region_name='eu-central-1')
    sqs = boto3.client('sqs',region_name='eu-central-1')
    sns = boto3.client('sns',region_name='eu-central-1')

    analyzer = VideoDetect(roleArn, bucket, video, client, rek, sqs, sns)
    analyzer.SetTopicandQueueInfo()

    analyzer.StartTextDetection()
    if analyzer.GetSQSMessageSuccess()==True:
        analyzer.GetTextDetectionResults()
    
    else:
        with open('output.txt', 'w', encoding='utf-8') as file1:
            file1.write('failed detecting text')
    
    
    deleteDuplicates.deleteDup('output.txt')    


if __name__ == "__main__":
    main('video_230608-095401.mp4')
