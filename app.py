#!/usr/bin/env python3

import aws_cdk as cdk

from aws_url_shortener.aws_url_shortener_stack import UrlShortenerStack

app = cdk.App()
UrlShortenerStack(app, "aws-url-shortener")

app.synth()
