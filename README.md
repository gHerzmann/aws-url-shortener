
# AWS URL Shortener

This is a simple AWS URL shortener created by using AWS CDK in Python. The stack
is defined inside aws_url_shortener_stack.py file and the the Lambda code is defined inside the
lambda folder. Currently it uses the folowing AWS services:

- API Gateway
- DynamoDB
- Lambd Function

This project was create mainly as a way to experiment with the AWS CDK functionalities.

## Setup

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

You will also need to install the AWS CDK:

```
$ npm install -g aws-cdk
```

Dont forget to setup your AWS credentials, CDK will use the same credentials used by AWS CLI, however you can also define it inside of the app.py.

## Deployment

Before the first deployment you'll need to bootstrap your account with the following command:

```
$ cdk bootstrap
```

Then you'll be able to deploy the stack:

```
$ cdk deploy
```

To remove and clear everything related to the stack on you account:

```
$ cdk destroy
```

*Tip: If you have multiple profiles configured on your system, you can use the --profile option during the CDK commands to define which one to use, ie.:*

```
$ cdk deploy --profile default
```
