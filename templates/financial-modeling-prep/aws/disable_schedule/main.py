import boto3
import os


SCHEDULER = boto3.client('scheduler')
SCHEDULE_NAME = os.environ['ScheduleName']


def handler(event, context):
    response = SCHEDULER.get_schedule(Name=SCHEDULE_NAME)
    sqs_templated = dict(RoleArn=response['Target']['RoleArn'], Arn=response['Target']['Arn'], Input=dict())
    flex_window = dict(Mode='OFF')
    SCHEDULER.update_schedule(Name=SCHEDULE_NAME,
                              ScheduleExpression=response['ScheduleExpression'],
                              Target=sqs_templated,
                              FlexibleTimeWindow=flex_window,
                              State='DISABLED'
                              )
