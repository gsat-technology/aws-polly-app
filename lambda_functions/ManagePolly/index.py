import os
import json
import uuid
import xml.dom.minidom
import re
import requests
import urllib

import boto3


#environment variables
polly_bucket = os.environ['polly_bucket']
pwd = os.environ['password']
yandex_key = os.environ['yandex_key']
yandex_translate_endpoint = os.environ['yandex_translate_endpoint']

polly_client = boto3.client('polly')
s3_client = boto3.client('s3')


def caseInsensitiveReplace(text, orig, new):
    pattern = re.compile(orig, re.IGNORECASE)
    return pattern.sub(new, text)


def textToS3Location(text, voice):
    print('textToS3Location()')

    key = '{}.mp3'.format(str(uuid.uuid4())[:6])

    #if it kinda looks like SSML, let's assume that's what
    #the use is trying to do
    if '<speak>' in text:
        print('textType is SSML')
        text_type = 'ssml'
    else:
        print('textType is text')
        text_type = 'text'


    response = polly_client.synthesize_speech(
         OutputFormat='mp3',
         SampleRate='8000',
         Text=text,
         TextType=text_type,
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


def translate(text, lang):

    #yandex requires text to be urlencoded
    url_enc_text = urllib.quote_plus(text)

    query = '{}?key={}&text={}&lang={}'.format(yandex_translate_endpoint, yandex_key, url_enc_text, lang)
    r = requests.get(query)

    if r.status_code == 200:
        return r.json()['text'][0]
    else:
        print('there was some error trying to translate')
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

                text = body['text']

                if 'translation' in body:
                     text = translate(text, body['translation'])

                #if translation doesn't work, just continue with orig text
                if not text:
                    text = body['text']

                result = textToS3Location(text, body['voice'])

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
