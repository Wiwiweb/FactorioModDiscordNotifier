import os
import boto3
from common import ModSavedInfo

AWS_REGION = os.environ.get('AWS_REGION')
DDB_TABLE_NAME = os.environ.get('DDB_TABLE')

ddb = boto3.client('dynamodb', region_name=AWS_REGION)


def get_known_mods():
    response = ddb.scan(TableName=DDB_TABLE_NAME)
    mods = {}
    for item in response['Items']:
        mod_id = item['ModName']['S']
        last_known_version = item['LastKnownVersion']['S']
        last_posted_changelog = item['LastPostedChangelog']['S']
        mods[mod_id] = ModSavedInfo(last_known_version, last_posted_changelog)
    return mods


def set_version_and_changelog(mod_id, last_version, last_posted_changelog):
    ddb.update_item(
        TableName=DDB_TABLE_NAME,
        Key={'ModName': {'S': mod_id}},
        UpdateExpression='SET LastKnownVersion = :a, LastPostedChangelog = :b',
        ExpressionAttributeValues={':a': {'S': last_version},
                                   ':b': {'S': last_posted_changelog}}
    )
    print("Updated {} in DDB: LastKnownVersion: {} - LastPostedChangelog: {}"
          .format(mod_id, last_version, last_posted_changelog))


def set_last_known_version(mod_id, last_known_version):
    ddb.update_item(
        TableName=DDB_TABLE_NAME,
        Key={'ModName': {'S': mod_id}},
        UpdateExpression='SET LastKnownVersion = :a',
        ExpressionAttributeValues={':a': {'S': last_known_version}}
    )
    print("Updated {} in DDB: LastKnownVersion: {}".format(mod_id, last_known_version))
