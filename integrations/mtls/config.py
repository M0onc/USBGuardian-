import ssl

def get_client_ssl_context():
    ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    ctx.load_cert_chain("certs/client.crt", "certs/client.key")
    ctx.load_verify_locations("certs/ca.crt")
    ctx.verify_mode = ssl.CERT_REQUIRED
    return ctx

def get_server_ssl_context():
    ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ctx.load_cert_chain("certs/server.crt", "certs/server.key")
    ctx.load_verify_locations("certs/ca.crt")
    ctx.verify_mode = ssl.CERT_REQUIRED
    return ctx