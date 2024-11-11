import boto3
import io
import json
import os
import time

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

from botocore.exceptions import ClientError

def handler(event, context):
    subsection = event['body'] # The options passed by the Google script on trigger
    payload = json.loads(subsection)
    print(type(payload))

    # Parse the json to get the sender email and gdrive link to video to upload
    arguments = payload['values']
    email = arguments[1]
    link = arguments[2]

    log_to_cloudwatch(subsection)
    log_to_cloudwatch("Email was {} and link is {}".format(email, link))
    
    get_id_success, gdrive_id = parse_file_id(link)

    status_code = 200
    message = "Successfully uploaded your data"
    if not get_id_success:
        status_code = 400
        message = "Could not find file: malformed Google Drive URL"
    else:
        download_success = download_file(gdrive_id)
        #upload_success = upload_file(gdrive_id, bucket)
        if not download_success:
            status_code = 500
            message = "Could not upload file: Encountered an error during file upload"

    return {
        'statusCode': status_code,
        'body': json.dumps(message)
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
    

def get_file_id(link):
    """ Gets the Google file ID from the Google Drive link and does some input checks.
    Example link formats: 
    - https://drive.google.com/file/d/14QHXcqEmt17yAy3D78sPN9Xj6z1vl-xK/view?usp=drive_link
    - https://drive.google.com/open?id=1G2nzSyHA6idoQRwymPIsSdee72C6xWoV

    :param link: Google Drive link of file to be uploaded
    """
    if "drive.google.com" not in link:
        log_to_cloudwatch("Not a Google Drive link")
        return False, ""
    
    if link.find("file/d/") == -1:
        log_to_cloudwatch("Unsupported Google Drive link format. Link was {}".format(str(link)))
        return False, ""
    else:
        start_index = link.find("file/d/")
        stop_index = link.find(value="/", start=start_index)
        gdrive_file_id = ""

        if stop_index == -1: # Copy from start_index to end of link str
            gdrive_file_id = link[start_index:]
        else: # Only copy the file ID (disregard view/edit/etc postscripts)
            gdrive_file_id = link[start_index:stop_index]

        log_to_cloudwatch("Valid Google Drive link. Link was {}".format(str(link)))
        return True, gdrive_file_id

def download_file(gdrive_id):
    return False
