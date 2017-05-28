import os
import json
import uuid

import boto3

#environment variables
polly_bucket = os.environ['polly_bucket']
pwd = os.environ['password']

polly_client = boto3.client('polly')
s3_client = boto3.client('s3')


def textToS3Location(text, voice):
    print('textToS3Location()')

    key = '{}.mp3'.format(str(uuid.uuid4())[:6])

    response = polly_client.synthesize_speech(
         OutputFormat='mp3',
         SampleRate='8000',
         Text=text,
         TextType='text',
         VoiceId=voice
     )

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        #create object in S3
        s3_client.put_object(Bucket=polly_bucket, Key=key, Body=response['AudioStream'].read())
        presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params = {
                'Bucket': polly_bucket,
                'Key': key
            },
            ExpiresIn = 300
        )

        print(presigned_url)
        return presigned_url
    else:
        return None



def handler(event, context):

    print(event)


    response = {
        'statusCode': None,
        'headers': { 'Content-Type': 'application/json' },
        'body': None
    }

    try:
        body = json.loads(event['body'])
    except:
        body = None

    if not body:
        response['statusCode'] = 400
        response['body'] = json.dumps({'error': 'no post data'})
    else:
        if 'text' in body and 'password' in body and 'voice' in body:
            #valid request
            print('valid request')

            if pwd == body['password']:
                print('correct password')

                result = textToS3Location(body['text'], body['voice'])

                if result:
                    response['statusCode'] = 200
                    response['body'] = json.dumps({'location': result})
                else:
                    response['statusCode'] = 400
                    response['body'] = json.dumps({'error': 'an unknown error occurred'})

            else:
                #wrong password
                print('incorrect password')
                response['statusCode'] = 401
                response['body'] = json.dumps({'error': 'incorrect password'})

        else:
            #it's a bad request
            print('bad request')
            response['statusCode'] = 400
            response['body'] = json.dumps({'error': 'bad request - expected values for password, text, voice'})


    return response
