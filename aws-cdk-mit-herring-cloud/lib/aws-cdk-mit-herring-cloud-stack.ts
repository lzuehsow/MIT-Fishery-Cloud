import * as apigateway from 'aws-cdk-lib/aws-apigateway';
import * as cdk from 'aws-cdk-lib';
import * as iam from 'aws-cdk-lib/aws-iam'
import * as actions from 'aws-cdk-lib/aws-ses-actions';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import { Construct } from 'constructs';
import {v4 as uuidv4} from 'uuid';


export class AwsCdkMitHerringCloudStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    var bucket_name = `mit-herring-cloud-bucket-${uuidv4()}`;

    const herringBucket = new s3.Bucket(this, bucket_name, {
        bucketName: bucket_name,
    });

    const herringRole = new iam.Role(this, 'MitHerringLambdaRole', {
        assumedBy: new iam.ServicePrincipal('lambda.amazonaws.com'),
    });

    herringRole.addManagedPolicy(iam.ManagedPolicy.fromAwsManagedPolicyName("service-role/AWSLambdaBasicExecutionRole"));
    herringRole.addManagedPolicy(iam.ManagedPolicy.fromAwsManagedPolicyName("CloudWatchLogsFullAccess"));

    const herringLambda = new lambda.Function(this, "MitHerringLambda", {
      runtime: lambda.Runtime.PYTHON_3_10,
      handler: "handler.handler",
      timeout: cdk.Duration.seconds(30),
      code: lambda.Code.fromAsset("lambda/"),
      role: herringRole,
      environment: {
        BUCKET_NAME: herringBucket.bucketName
      },
    });

    new apigateway.LambdaRestApi(this, 'MitHerringApi', {
      handler: herringLambda
    });

    //herringBucket.grantPut(herringLambda);
    herringBucket.grantPut(herringRole);
  }
}
