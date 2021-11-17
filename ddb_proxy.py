import os
import boto3

AWS_REGION = os.environ.get('AWS_REGION')
DDB_TABLE_NAME = os.environ.get('DDB_TABLE')

ddb = boto3.client('dynamodb', region_name=AWS_REGION)

def get_known_mods():
    response = ddb.scan(TableName=DDB_TABLE_NAME)
    mods = {}
    for item in response['Items']:
        mod_id = item['ModName']['S']
        latest_known_version = item['LatestVersion']['S']
        mods[mod_id] = latest_known_version
    return mods

def set_latest_version(mod_id, latestVersion):
    ddb.update_item(
        TableName=DDB_TABLE_NAME, 
        Key={'ModName': {'S': mod_id}},
        UpdateExpression='SET LatestVersion = :v',
        ExpressionAttributeValues={':v': {'S': latestVersion}}
    )
    print("Updated {} to version {} in DDB".format(mod_id, latestVersion))
