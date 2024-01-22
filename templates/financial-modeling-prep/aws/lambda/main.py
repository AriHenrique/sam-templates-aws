import boto3
import os


CODE_BUILD_NAME = os.environ.get('CODE_BUILD_NAME')
SNS = os.environ.get('SNS_TOPIC')
CODEBUILD_CLIENT = boto3.client('codebuild')
DYNAMODB = boto3.resource('dynamodb')
TABLE = DYNAMODB.Table('table_name')
RUN_CODEBUILD = False


def get_endpoint(endpoint_name):
    """
    Get config endpoint.

    :param endpoint_name:
    :return: dict -> config endpoint or None if not exists.
    """
    response = TABLE.get_item(
        Key={'endpoint': endpoint_name})
    return response.get('Item', None)


def start_codebuild(code_build_name: str = CODE_BUILD_NAME):
    """
    Start CodeBuild project.

    :param code_build_name:
    :return: response or dict -> error if not exists.
    """
    try:
        response = CODEBUILD_CLIENT.start_build(
            projectName=code_build_name
        )
        return response
    except Exception as e:
        return {'error': str(e)}


def lambda_handler(event, context):
    try:
        #
        #
        #  PROCESS ETL...
        #
        #
        if RUN_CODEBUILD:
            start_codebuild()
    except Exception as err:
        client = boto3.client('sns')
        client.publish(
            TopicArn=SNS,
            Message=str(err),
            Subject='Lambda ETL function failure',
        )
        raise err
