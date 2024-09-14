from flask import Flask, request, jsonify
import redis
import grpc
import grpc_client

app = Flask(__name__)
#cache = redis.Redis(host='redis_container', port=6379)

redis_clients = [
    redis.Redis(host='redis_container1', port=6379),
    redis.Redis(host='redis_container2', port=6380),
    redis.Redis(host='redis_container3', port=6381),
    redis.Redis(host='redis_container4', port=6382),
]

def get_redis_client(key: str):
    if key[0] < 'g':
        return redis_clients[0], 0
    elif key[0] < 'n':
        return redis_clients[1], 1
    elif key[0] < 't': 
        return redis_clients[2], 2
    else:
        return redis_clients[3], 3

@app.route('/resolve', methods=['POST'])
def resolve_domain():
    domain = request.json['domain']
    cache, partition = get_redis_client(domain)
    
    # Buscar en Redis
    ip = cache.get(domain)
    if ip:
        return jsonify({"domain": domain, "ip": ip.decode('utf-8'), "source": "cache", "partition": partition})

    # No está en caché, hacemos resolución gRPC
    ip = grpc_client.resolve_domain_via_grpc(domain)

    # Almacenar en Redis
    cache.set(domain, ip)
    return jsonify({"domain": domain, "ip": ip, "source": "dns", "partition": partition})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)