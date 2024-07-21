# MIT-Fishery-Cloud
Contains the web app for processing video data in AWS

### Linux install instructions

#### AWS setup
1. In terminal run `sudo apt install npm` to install npm
2. In terminal, run `sudo npm install -g aws-cdk`
3. Log into your AWS account in a browser window and type "IAM" into the search bar on the top of the home page. Select IAM (red icon of an ID card) from the dropdown choices.
4. In the IAM sidebar menu, select "Access Management" -> "Users"
5. On the Users page, click the "Create User" button. Click through the walkthrough and add the user to the admin group when prompted, then click the "Create User" button to confirm. DO NOT NAVIGATE OFF OF THE USER CREATED SCREEN UNTIL STEP 7 IS COMPLETE: YOU WILL NEED THE ACCESS KEY AND SECRET ACCESS KEY VALUES AND THEY ARE ONLY VISIBLE ONCE AT CREATION.
6. In terminal, run `aws configure` to configure your AWS credentials.
    - Input your newly created user's AWS Access Key
    - Input your newly created user's AWS Secret Access Key
    - Set default region to `us-east-1`
    - Simply hit enter when prompted for default output format to leave field blank.
7. Confirm correct credential setup by running `aws sts get-caller-identity` in terminal and verifying the ARN field is your newly created user.
    - The format of the ARN will be `"Arn": "arn:aws:iam::ACCOUNT:user/NEW_USER_NAME"`

#### Git setup
  
1. cd to the filepath you would like to install MIT-Fishery-Cloud to.
2. In terminal, run `git clone https://github.com/YOUR_GIT_USERNAME_HERE/MIT-Fishery-Cloud.git`. You may be prompted for your credentials.
3. cd inside the MIT-Fishery-Cloud directory that was created.

### To build the stack

1. WARNING: Currently the S3 bucket has a static name, so it must be deleted if it already exists prior to deploying or the deployment will fail. This is because buckets have globally unique names.
    - To delete the bucket, use the search bar on the top of the logged-in AWS home page to navigate to the S3 page.
    - Select the bucket and click Delete
    - Type the bucket name and confirm deletion
    - Continue with cdk deployment

2. cd inside the MIT-Fishery-Cloud/aws-cdk-mit-herring-cloud directory.
3. In terminal, run `cdk bootstrap` and accept the prompt by typing Y.
4. In terminal, run `cdk deploy` and verify the created resources look correct. Then accept the prompt by typing Y to deploy the resources.
5. Verify resource creation was successful in the terminal stack trace. If unsuccessful, the stack update will be rolled back to its prior state automatically and a stack trace will be printed to terminal.
