import paramiko
import time
import logging

logging.basicConfig(level=logging.DEBUG)


class WebServerSetup:
    def __init__(self, key_file_path='./keys/my-ec2-key'): #a constructor that takes our key path
        self.key_file_path = key_file_path
        self.ssh = paramiko.SSHClient() #instantiate the ssh client
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) #handle unknown host keys automatically

    def provision(self, ip_address, custom_message):    # method to provision the webserver
        logging.debug(f"Connecting to instance at {ip_address}...")
        key = paramiko.RSAKey.from_private_key_file(self.key_file_path)

        for attempt in range(10): #loop for a a maximim of 10 * 10 seconds if connection fails
            try:
                self.ssh.connect(hostname=ip_address, username='ec2-user', pkey=key) # attempt to connect
                logging.info("SSH connection established.")
                break
            except Exception as e:
                logging.error(f"SSH not ready, retrying in 10s... ({attempt+1}/10)")
                time.sleep(10)
        else:
            raise Exception("SSH connection failed after 10 attempts.")

        commands = [        #commands to run on the ec2 instance
            "sudo yum update -y",
            "sudo yum install -y httpd",
            "sudo systemctl start httpd",
            "sudo systemctl enable httpd",
            f'echo "{custom_message}" | sudo tee /var/www/html/index.html'  # write to the root html of the server
        ]

        for cmd in commands:
            logging.debug(f"Running: {cmd}")
            stdin, stdout, stderr = self.ssh.exec_command(cmd)
            stdout.channel.recv_exit_status()

        logging.info("✅ Web server installed and index.html updated.")
        self.ssh.close()


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        logging.info("Usage: python script.py <IP_ADDRESS> <CUSTOM_MESSAGE>")
        sys.exit(1)

    ip = sys.argv[1]
    message = sys.argv[2]

    setup = WebServerSetup(key_file_path="./keys/my-ec2-key")
    setup.provision(ip_address=ip, custom_message=message)
