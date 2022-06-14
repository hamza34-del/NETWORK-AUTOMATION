import grpc
import get_config_pb2
import get_config_pb2_grpc

def run():
    # Instantiate stub on the client.
    connect = grpc.insecure_channel('localhost:8080')
    stub = get_config_pb2_grpc.get_configStub(channel=connect)
    # Invoke the Login_info method of the server through stub.
    response = stub.Login_info(get_config_pb2.Request(host='192.168.56.100',username='python',password='Huawei12#$'))
    print (response.message)

if __name__ == "__main__":
    run()
