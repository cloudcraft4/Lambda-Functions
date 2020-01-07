from __future__ import print_function

import json
import boto3
import time
import urllib

print(“loading function”)

s3 = boto3.client(‘s3’)

def lambda_handler(event,context):
	source_bucket = event[‘Records’][0][‘s3’][‘bucket’][‘name’]
	key = urllib.unquote_plus(event[‘Records’][0][‘s3’][‘object’][‘key’])
	target_bucket = ‘aws-lambda-s3bucket’ #your s3 bucket name
	copy_source = {‘Bucket’:source_bucket ,’Key’:key}

	try:
		print(“waiting for the file persist in the source bucket”)
		waiter = s3.get_waiter(‘object_exists’)
		waiter.wait(Bucket=source_bucket, key=key)
		print(“copying the object from the source s3 bucket to destination s3 bucket”)
		s3.copy_object(Bucket=target_bucket, Key=key,CopySource= copy_source)
	except Exception as e:
		print(e)
		print(“Error getting object {} from bucket {}. Make sure tehy exists in the bucket”)
		raise e