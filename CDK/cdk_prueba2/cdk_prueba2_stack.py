from aws_cdk import Stack

import aws_cdk.aws_lambda as lambda_ 
import aws_cdk.aws_apigateway as apigateway
import aws_cdk.aws_dynamodb as dynamodb


from constructs import Construct


class CdkPruebaStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        # Importa la tabla "auto" ya creada en la nube de AWS
        tabla_auto = dynamodb.Table.from_table_name(
            self, "tabla",
            table_name="Auto"
        )

        # Crea una funcion lambda
        lambdaPruebaCDK = lambda_.Function(
            self, "lambdaPruebaCDKGetALL",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="lambdaPruebaCDKGetALL.lambda_handler",
            code=lambda_.Code.from_asset("CodigoLambda")
        )

        # Permisos de la lambda
        tabla_auto.grant_read_data(lambdaPruebaCDK)

        # Crea una API Gateway y la vincula con la lambda "lambdaPruebaCDK"
        api = apigateway.LambdaRestApi(
            self, "apiPruebaCDK",
            handler= lambdaPruebaCDK,
            proxy=True
        )

        # Agrega un get a la API Gateway
        api.root.add_method("GET", integration = apigateway.LambdaIntegration(lambdaPruebaCDK))





