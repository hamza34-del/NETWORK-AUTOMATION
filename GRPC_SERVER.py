from concurrent import futures
import time
import grpc
import get_config_pb2
import get_config_pb2_grpc
import paramiko

class Display_Config(get_config_pb2_grpc.get_configServicer):
    # Invoke paramiko to log in to the device and obtain the current configurations.
    def Login_info(self, request, context):
        ssh = paramiko.client.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=request.host, port=22, username=request.username, password=request.password)
        cli = ssh.invoke_shell()
        cli.send('N\n')
        time.sleep(0.5)
        cli.send('screen-length 0 temporary\n')
        time.sleep(0.5)
        cli.send('display cu\n')
        time.sleep(3)
        data = cli.recv(999999).decode()
        ssh.close()
        # Return the configuration information in the command output.
        return get_config_pb2.Reply(message=data)

def serve():
    # Create the gRPC service.
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # Deploy the gRPC server in the defined service.
    get_config_pb2_grpc.add_get_configServicer_to_server(Display_Config(),server)
    # Start the server.
    server.add_insecure_port('localhost:8080')
    server.start()
    _ONE_DAY_IN_SECONDS = 60 * 60 * 24
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop()

if __name__ == "__main__":
    serve()
