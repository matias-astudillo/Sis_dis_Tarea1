from concurrent import futures
import grpc
import dns_pb2
import dns_pb2_grpc
import subprocess

class DnsResolver(dns_pb2_grpc.DnsResolverServicer):
    def Resolve(self, request, context):
        domain = request.domain
        result = subprocess.run(["dig", "@8.8.8.8", "+short", domain], capture_output=True, text=True)
        ip = result.stdout.strip().split('\n')[-1]
        return dns_pb2.DomainResponse(ip=ip)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    dns_pb2_grpc.add_DnsResolverServicer_to_server(DnsResolver(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()