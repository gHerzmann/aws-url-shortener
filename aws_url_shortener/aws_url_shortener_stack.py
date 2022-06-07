from aws_cdk import (  # aws_certificatemanager,; aws_route53,; aws_route53_targets,
    Duration,
    RemovalPolicy,
    Stack,
    aws_apigateway,
    aws_dynamodb,
    aws_lambda,
)
from constructs import Construct


class UrlShortenerStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Defines the Dynamodb table
        table = aws_dynamodb.Table(
            self,
            "urls-table",
            partition_key=aws_dynamodb.Attribute(
                name="id", type=aws_dynamodb.AttributeType.STRING
            ),
            billing_mode=aws_dynamodb.BillingMode.PAY_PER_REQUEST,
            time_to_live_attribute="expdate",
            removal_policy=RemovalPolicy.DESTROY,
        )

        # Defines de Lambda function
        handler = aws_lambda.Function(
            self,
            "UrlShortenerFunction",
            code=aws_lambda.Code.from_asset("./aws_url_shortener/lambda"),
            handler="handler.main",
            timeout=Duration.minutes(1),
            runtime=aws_lambda.Runtime.PYTHON_3_9,
        )

        # Add an environment variable and allow the function to modify the table
        handler.add_environment("TABLE_NAME", table.table_name)
        table.grant_read_write_data(handler)

        # Defines API Gateway
        api = aws_apigateway.LambdaRestApi(
            self, "UrlShortenerAPI", handler=handler, proxy=False
        )

        create = api.root.add_resource("create")
        create.add_method("POST")  # POST /create

        shorten = api.root.add_resource("s").add_resource("{short_id}")
        shorten.add_method("GET")  # GET /s/{short_id}
