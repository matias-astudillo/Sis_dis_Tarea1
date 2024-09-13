from flask import Flask, request, jsonify
import redis
import grpc
import grpc_client

app = Flask(__name__)
cache = redis.Redis(host='redis_container', port=6379)

@app.route('/resolve', methods=['POST'])
def resolve_domain():
    domain = request.json['domain']
    
    # Buscar en Redis
    ip = cache.get(domain)
    if ip:
        return jsonify({"domain": domain, "ip": ip.decode('utf-8'), "source": "cache"})

    # No está en caché, hacemos resolución gRPC
    ip = grpc_client.resolve_domain_via_grpc(domain)

    # Almacenar en Redis
    cache.set(domain, ip)
    return jsonify({"domain": domain, "ip": ip, "source": "dns"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)