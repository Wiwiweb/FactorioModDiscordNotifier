# FactorioModDiscordNotifier
Posts a message in a Discord server when a Factorio mod's changelog gets updated.

Currently used in the [Space Exploration discord](https://discord.gg/yYZqu7cRxf).

The bot does not need to live on any server. It is an AWS Lambda function that runs every minute. 

The bot is light enough to live on an AWS Free tier account: On average, the function takes 1-2 seconds, but can take 5-10 seconds if an actual update is detected. That is 43,800 requests and ~100,000 seconds of compute time per month, which is way under the free tier of 1 million requests and 3.2 million seconds of compute time.

## Installing

### Locally, creating the deployment package

To create the deployment package, you will need Python 3.x and pip3 installed. The [package creation script](package-to-lambda-zip.sh) also uses 7zip, but you can replace it with your favourite command line zip library easily.

Then run the package creation script with `./package-to-lambda-zip.sh`. It should download dependencies via pip, then create a zip file named `lambda-deployment-package.zip` containing both this bot's code and its dependencies.

### In your AWS account

**In the DynamoDB console** (find AWS service consoles in the top search bar), create a new table. Give it the name you want, and a partition key of `ModName` of String type. Leave everything else default.

**In the Lambda console**, create a new Function with the Python 3.x runtime. Leave Architecture to default. Set permissions to "Create a new role with basic Lambda permissions".

**In the IAM console**, find the execution role of the Lambda function that was just created. It should be named <your-function-name>-role-<random-string>. Click "Add permissions" then "Attach policies" and give it the preset policy `AmazonDynamoDBFullAccess`.
  
**Go back to the Lambda console** and open the function. In the "Code" tab, click "Upload from" then ".zip file". Upload the zip package created earlier

In the "Configuration" tab, click "Environment variables". Add these variables:
* `DDB_TABLE`	The name of that DynamoDB table you created earlier.
* `DISCORD_CHANNEL`: Channel id that the bot will post to. It's an 18-digit number. Right click on a discord channel and "Copy ID" to find it.
* `DISCORD_TOKEN`: The "bot token" (not the client secret) of the discord Application that will post the changelog. See https://discord.com/developers/applications/
* `MOD_AUTHOR`: Your Factorio Mod Portal name. That's the name the bot will look for to find relevant mods.
  
Finally, click In the "Function overview" at the top, click "Add trigger". Choose "EventBridge (CloudWatch Events)" then "Create a new rule". Give it a name like "EveryMinute", pick the rule type "Schedule" and give it the schedule `rate(1 minute)`.

Your bot should now be running!
  
### Troubleshooting
  
In case of issue, you can find info in the "Monitor" tab of the function.  
The Invocations count should be 1 per minute. If it isn't, the function isn't running at all.  
The Error count should be 0. In case it isn't, search for the issue in the "Logs" sub-tab under "Monitor" then click the most recent log stream.  
If there's no error but the bot isn't posting anything, check the DDB table. It should contain every mod the bot is tracking, and the latest version it has seen.
