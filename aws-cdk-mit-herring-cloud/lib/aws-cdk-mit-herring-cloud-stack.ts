import * as cdk from 'aws-cdk-lib';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as apigateway from 'aws-cdk-lib/aws-apigateway';
import { Construct } from 'constructs';

export class AwsCdkMitHerringCloudStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const herringBucket = new s3.Bucket(this, "mit-herring-cloud-bucket", {
        bucketName: "mit-herring-cloud-bucket",
    });

    const herringLambda = new lambda.Function(this, "MitHerringLambda", {
      runtime: lambda.Runtime.PYTHON_3_10,
      handler: "index.handler",
      timeout: cdk.Duration.seconds(30),
      code: lambda.Code.fromAsset("lambda/"),
      environment: {
        BUCKET_NAME: herringBucket.bucketName
      },
    });

    new apigateway.LambdaRestApi(this, 'MitHerringApi', {
      handler: herringLambda
    });

    herringBucket.grantPut(herringLambda);
  }
}
