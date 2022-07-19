#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import { CdkGluePythonshellStack } from '../lib/cdk-glue-pythonshell-stack';

const app = new cdk.App();
new CdkGluePythonshellStack(app, 'CdkGluePythonshellStack');
