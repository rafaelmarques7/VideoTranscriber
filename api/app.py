from aws_cdk import (
  core,
  aws_lambda as _lambda,
  aws_apigateway as _apigw
)

APP_NAME = "VideoTranscriberApi"
STACK_NAME = f'{APP_NAME}Stack'


class ApiCorsLambdaStack(core.Stack):

  def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
    super().__init__(scope, id, **kwargs)

    requests_layer = _lambda.LayerVersion(
      self, "requests",
      code=_lambda.AssetCode('layers/requests.zip')
    )

    pytube_layer = _lambda.LayerVersion(
      self, "pytube",
      code=_lambda.AssetCode('layers/pytube.zip')
    )

    base_lambda = _lambda.Function(self, APP_NAME,
                                   handler='main.handler',
                                   runtime=_lambda.Runtime.PYTHON_3_8,
                                   code=_lambda.Code.asset('src'),
                                   timeout=core.Duration.seconds(30),
                                   layers=[requests_layer, pytube_layer],
                                   )

    base_api = _apigw.RestApi(self, 'ApiGatewayWithCors',
                              rest_api_name=APP_NAME)

    route_transcribe = base_api.root.add_resource('transcribe')
    route_transcribe_lambda_integration = _apigw.LambdaIntegration(base_lambda, proxy=True, integration_responses=[{
      'statusCode': '200',
      'responseParameters': {
        'method.response.header.Access-Control-Allow-Origin': "'*'",
      }}]
                                                                 )
    route_transcribe.add_method('GET', route_transcribe_lambda_integration,
                              method_responses=[{
                                'statusCode': '200',
                                'responseParameters': {
                                  'method.response.header.Access-Control-Allow-Origin': True,
                                }}]
                              )

    self.add_cors_options(route_transcribe)

  def add_cors_options(self, apigw_resource):
    apigw_resource.add_method('OPTIONS', _apigw.MockIntegration(
      integration_responses=[{
        'statusCode': '200',
        'responseParameters': {
          'method.response.header.Access-Control-Allow-Headers': "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'",
          'method.response.header.Access-Control-Allow-Origin': "'*'",
          'method.response.header.Access-Control-Allow-Methods': "'GET,OPTIONS'"
        }
      }
      ],
      passthrough_behavior=_apigw.PassthroughBehavior.WHEN_NO_MATCH,
      request_templates={"application/json": "{\"statusCode\":200}"}
    ),
                              method_responses=[{
                                'statusCode': '200',
                                'responseParameters': {
                                  'method.response.header.Access-Control-Allow-Headers': True,
                                  'method.response.header.Access-Control-Allow-Methods': True,
                                  'method.response.header.Access-Control-Allow-Origin': True,
                                }
                              }],
                              )


app = core.App()
ApiCorsLambdaStack(app, STACK_NAME)
app.synth()
