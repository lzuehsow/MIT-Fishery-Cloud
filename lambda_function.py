import boto3
import json
import os
import time

from botocore.exceptions import ClientError

# TODO: replace this w cloudformation

def lambda_handler(event, context):
    subsection = event['body']
    
    log_to_cloudwatch(subsection)
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
    
def log_to_cloudwatch(log_message):
    client = boto3.client('logs')

    LOG_GROUP='HerringLambda'
    LOG_STREAM='{}-{}'.format(time.strftime('%Y-%m-%d'),'logstream')
    
    try:
       client.create_log_group(logGroupName=LOG_GROUP)
    except client.exceptions.ResourceAlreadyExistsException:
       pass
    
    try:
       client.create_log_stream(logGroupName=LOG_GROUP, logStreamName=LOG_STREAM)
    except client.exceptions.ResourceAlreadyExistsException:
       pass
    
    response = client.describe_log_streams(
       logGroupName=LOG_GROUP,
       logStreamNamePrefix=LOG_STREAM
    )
    
    event_log = {
       'logGroupName': LOG_GROUP,
       'logStreamName': LOG_STREAM,
       'logEvents': [
           {
               'timestamp': int(round(time.time() * 1000)),
               'message': time.strftime('%Y-%m-%d %H:%M:%S')+'\t {}'.format(log_message)
           }
       ],
    }
    
    if 'uploadSequenceToken' in response['logStreams'][0]:
       event_log.update({'sequenceToken': response['logStreams'][0] ['uploadSequenceToken']})
    
    response = client.put_log_events(**event_log)
    print(response)
    

# def upload_file(file_name, bucket, object_name=None):
#     """Upload a file to an S3 bucket

#     :param file_name: File to upload
#     :param bucket: Bucket to upload to
#     :param object_name: S3 object name. If not specified then file_name is used
#     :return: True if file was uploaded, else False
#     """

#     # If S3 object_name was not specified, use file_name
#     if object_name is None:
#         object_name = os.path.basename(file_name)

#     # Upload the file
#     s3_client = boto3.client('s3')
#     try:
#         response = s3_client.upload_file(file_name, bucket, object_name)
#     except ClientError as e:
#         logging.error(e)
#         return False
#     return True
