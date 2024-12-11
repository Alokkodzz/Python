import boto3
from botocore.exceptions import  ClientError

def send_email_success(sender, recipient, subject1, body_text1, aws_region="us-east-1"):
    
    client = boto3.client("ses", region_name=aws_region)

    try:
        # Send the email
        response = client.send_email(
            Source=sender,
            Destination={
                "ToAddresses": [
                    recipient,
                ]
            },
            Message={
                "Subject": {
                    "Data": subject1,
                    "Charset": "UTF-8"
                },
                "Body": {
                    "Text": {
                        "Data": body_text1,
                        "Charset": "UTF-8"
                    },
                }
            }
        )
        print(f"Email sent successfully!")
    except ClientError as e:
        print(f"Failed to send email: {e.response["Error"]["Message"]}")

def send_email_failed(sender, recipient, subject2, body_text2, aws_region="us-east-1"):
    
    client = boto3.client("ses", region_name=aws_region)

    try:
        # Send the email
        response = client.send_email(
            Source=sender,
            Destination={
                "ToAddresses": [
                    recipient,
                ]
            },
            Message={
                "Subject": {
                    "Data": subject2,
                    "Charset": "UTF-8"
                },
                "Body": {
                    "Text": {
                        "Data": body_text2,
                        "Charset": "UTF-8"
                    },
                }
            }
        )
        print(f"Email sent successfully!")
    except ClientError as e:
        print(f"Failed to send email: {e.response["Error"]["Message"]}")

