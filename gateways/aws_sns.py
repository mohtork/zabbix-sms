import boto3
import config


# Create an SNS client
client = boto3.client(
    "sns",
    aws_access_key_id=config.aws_access_key,
    aws_secret_access_key=config.aws_secret_key,
    region_name=config.aws_region
)

topic_arn = config.sns_topicArn  # get its Amazon Resource Name
contacts = ["type phone numbers"] # Type phone numbers as a list

#SMS Subscribers
for number in contacts:
    client.subscribe(
        TopicArn=topic_arn,
        Protocol=config.sns_protocol,
        Endpoint=number  
    )

# Publish a message.
def AWS_SNS(alert):
	client.publish(Message=alert, TopicArn=topic_arn)


