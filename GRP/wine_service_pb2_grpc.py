# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from GRP import wine_service_pb2 as wine__service__pb2

GRPC_GENERATED_VERSION = '1.68.1'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in wine_service_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class WinePredictorStub(object):
    """Servicio de predicción de vinos
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.PredictWine = channel.unary_unary(
                '/wine.WinePredictor/PredictWine',
                request_serializer=wine__service__pb2.WineFeatures.SerializeToString,
                response_deserializer=wine__service__pb2.WinePrediction.FromString,
                _registered_method=True)
        self.CheckHealth = channel.unary_unary(
                '/wine.WinePredictor/CheckHealth',
                request_serializer=wine__service__pb2.HealthRequest.SerializeToString,
                response_deserializer=wine__service__pb2.HealthResponse.FromString,
                _registered_method=True)


class WinePredictorServicer(object):
    """Servicio de predicción de vinos
    """

    def PredictWine(self, request, context):
        """Método para predecir la calidad del vino
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CheckHealth(self, request, context):
        """Método para verificar el estado del servicio
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_WinePredictorServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'PredictWine': grpc.unary_unary_rpc_method_handler(
                    servicer.PredictWine,
                    request_deserializer=wine__service__pb2.WineFeatures.FromString,
                    response_serializer=wine__service__pb2.WinePrediction.SerializeToString,
            ),
            'CheckHealth': grpc.unary_unary_rpc_method_handler(
                    servicer.CheckHealth,
                    request_deserializer=wine__service__pb2.HealthRequest.FromString,
                    response_serializer=wine__service__pb2.HealthResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'wine.WinePredictor', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('wine.WinePredictor', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class WinePredictor(object):
    """Servicio de predicción de vinos
    """

    @staticmethod
    def PredictWine(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/wine.WinePredictor/PredictWine',
            wine__service__pb2.WineFeatures.SerializeToString,
            wine__service__pb2.WinePrediction.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def CheckHealth(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/wine.WinePredictor/CheckHealth',
            wine__service__pb2.HealthRequest.SerializeToString,
            wine__service__pb2.HealthResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
