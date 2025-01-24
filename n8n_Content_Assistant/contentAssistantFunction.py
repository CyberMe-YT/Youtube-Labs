import time
import boto3

def transcribe_file(job_name, file_uri, transcribe_client):
    """Starts a transcription job and waits for its completion."""
    try:
        # Start the transcription job
        transcribe_client.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={"MediaFileUri": file_uri},
            MediaFormat="mp4",  # Update if the file format is different
            LanguageCode="en-US",
            Subtitles={
                'Formats': ['srt'],
                'OutputStartIndex': 0
            },
            OutputBucketName='CHANGE_ME_BUCKET_NAME'
        )

        # Poll for the job's status
        max_tries = 60
        while max_tries > 0:
            max_tries -= 1
            job = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
            job_status = job["TranscriptionJob"]["TranscriptionJobStatus"]

            if job_status in ["COMPLETED", "FAILED"]:
                print(f"Job {job_name} is {job_status}.")
                if job_status == "COMPLETED":
                    return {
                        "statusCode": 200,
                        "body": {
                            "message": "Transcription completed successfully.",
                            "subtitle_file_uris": job['TranscriptionJob']['Transcript']['SubtitleFileUris']
                        }
                    }
                else:
                    return {
                        "statusCode": 500,
                        "body": f"Transcription job {job_name} failed."
                    }
            else:
                print(f"Waiting for {job_name}. Current status is {job_status}.")
            time.sleep(10)

        return {
            "statusCode": 408,
            "body": f"Transcription job {job_name} timed out."
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"An error occurred: {str(e)}"
        }

def lambda_handler(event, context):
    """AWS Lambda handler for starting a transcription job."""
    # Validate input
    file_uri = event.get("file_uri")
    if not file_uri:
        return {
            "statusCode": 400,
            "body": "Missing 'file_uri' in the input."
        }
    
    job_name = event.get("job_name")
    if not job_name:
        return {
            "statusCode": 400,
            "body": "Missing 'job_name' in the input."
        }

    # Initialize the Transcribe client
    transcribe_client = boto3.client("transcribe")

    # Start the transcription process
    return transcribe_file(job_name, file_uri, transcribe_client)