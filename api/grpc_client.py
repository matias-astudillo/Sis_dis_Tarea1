import grpc
import dns_pb2
import dns_pb2_grpc

def resolve_domain_via_grpc(domain):
    channel = grpc.insecure_channel('grpc_container:50051')
    stub = dns_pb2_grpc.DnsResolverStub(channel)
    response = stub.Resolve(dns_pb2.DomainRequest(domain=domain))
    return response.ip
