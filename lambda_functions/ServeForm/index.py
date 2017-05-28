import form

import boto3

body = form.content

def handler(event, context):

    return {
        'statusCode': "200",
        'body': body,
        'headers': {
            'Content-Type': 'text/html',
        },
    }
