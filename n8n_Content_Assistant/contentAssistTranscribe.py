import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError

def find_file_in_s3(bucket_name, filename_to_find):
    try:
        # Initialize the S3 client
        s3_client = boto3.client('s3')
        
        # Use list_objects_v2 to check if the file exists in the bucket
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=filename_to_find)
        
        # Check if 'Contents' exists in the response, indicating the file is present
        if 'Contents' in response:
            # Construct the S3 URI
            object_uri = f"s3://{bucket_name}/{filename_to_find}"
            object_uri = object_uri.strip()
            return {
                "statusCode": 200,
                "body": f"{object_uri}"
            }
        else:
            return {
                "statusCode": 404,
                "body": f"File '{filename_to_find}' not found in bucket '{bucket_name}'."
            }
    
    except NoCredentialsError:
        return {
            "statusCode": 500,
            "body": "AWS credentials not found. Please configure them using AWS CLI or environment variables."
        }
    except PartialCredentialsError:
        return {
            "statusCode": 500,
            "body": "Incomplete AWS credentials found. Please ensure both access key and secret key are set."
        }
    except ClientError as e:
        return {
            "statusCode": 500,
            "body": f"An error occurred: {e.response['Error']['Message']}"
        }

# Define the Lambda handler function
def lambda_handler(event, context):
    # Get the bucket name and filename from the event
    bucket_name = event.get('bucket_name', 'CHANGE_ME_BUCKETNAME')
    filename_to_find = event.get('fileName')
    
    # Call the function to find the file
    result = find_file_in_s3(bucket_name, filename_to_find)
    
    return result
