import boto3

AWS_REGION = "us-east-2"
DDB_TABLE_NAME = "FactorioModDiscordNotifier-SE"

ddb = boto3.client('dynamodb', region_name=AWS_REGION)

def get_all_mods():
    response = ddb.scan(TableName=DDB_TABLE_NAME)
    mods = {}
    for item in response['Items']:
        mod_name = item['ModName']['S']
        latest_version = item['LatestVersion']['S']
        mods[mod_name] = latest_version
    return mods

def set_latest_version(mod_name, current_version):
    ddb.update_item(
        TableName=DDB_TABLE_NAME, 
        Key={'ModName': {'S': mod_name}},
        UpdateExpression='SET LatestVersion = :v',
        ExpressionAttributeValues={':v': {'S': current_version}}
    )
    print("Updated {} to version {} in DDB".format(mod_name, current_version))