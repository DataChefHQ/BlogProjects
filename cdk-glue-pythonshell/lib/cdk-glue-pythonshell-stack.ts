import * as cdk from '@aws-cdk/core';
import * as iam from '@aws-cdk/aws-iam';
import * as glue from '@aws-cdk/aws-glue';
import * as s3 from '@aws-cdk/aws-s3';
import * as s3deploy from '@aws-cdk/aws-s3-deployment';

export class CdkGluePythonshellStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Define IAM Role
    const role = new iam.Role(this, 'my-glue-job-role', {
      assumedBy: new iam.ServicePrincipal('glue.amazonaws.com'),
    });
    const gluePolicy = iam.ManagedPolicy.fromAwsManagedPolicyName("service-role/AWSGlueServiceRole");
    role.addManagedPolicy(gluePolicy);

    // Define S3 Bucket
    const myBucket = new s3.Bucket(this, 'MyCdkGlueJobBucket', {
      versioned: true,
      bucketName: '<id>-my-cdk-glue-job-bucket',
      removalPolicy: cdk.RemovalPolicy.RETAIN,
      blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL
    });
    myBucket.grantRead(role);

    // Define Glue Job
    new glue.CfnJob(this, 'my-glue-job', {
      role: role.roleArn,
      command: {
        name: 'pythonshell',
        pythonVersion: '3',
        scriptLocation: 's3://<id>-my-cdk-glue-job-bucket/glue-python-scripts/hi.py'
      }
    });

    // Define S3 Deployment
    new s3deploy.BucketDeployment(this, 'DeployGlueJobFiles', {
      sources: [s3deploy.Source.asset('./resources/glue-scripts')], 
      destinationBucket: myBucket,
      destinationKeyPrefix: 'glue-python-scripts'
    });

  }
}
