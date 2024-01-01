import boto3
import os


def lambda_handler(event, context):
    if 'arn' in event:
        arn = event['arn']
    else:
        arn = str(os.environ.get('arn_permission'))
    print(arn)
    try:
        client = boto3.client('lakeformation')

        glue_client = boto3.client('glue')
        databases = glue_client.get_databases()

        for database in databases['DatabaseList']:
            database_name = database['Name']
            client.grant_permissions(
                Principal={
                    'DataLakePrincipalIdentifier': arn
                },
                Resource={
                    'Database': {
                        'Name': database_name
                    }
                },
                Permissions=[
                    'ALL'
                ]
            )
            print('ok database', database_name)

            tables = glue_client.get_tables(DatabaseName=database_name)

            for table in tables['TableList']:
                table_name = table['Name']
                client.grant_permissions(
                    Principal={
                        'DataLakePrincipalIdentifier': arn
                    },
                    Resource={
                        'Table': {
                            'DatabaseName': database_name,
                            'Name': table_name
                        }
                    },
                    Permissions=[
                        'ALL'
                    ]
                )
                print('ok table', table_name)
    except Exception as e:
        print(e)
        raise e
