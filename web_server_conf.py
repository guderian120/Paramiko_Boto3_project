import paramiko
import time
import logging, os
# from email_server import send_email_to_admin
logging.getLogger("botocore").setLevel(logging.WARNING)
logging.getLogger("boto3").setLevel(logging.WARNING)
logging.getLogger().setLevel(logging.WARNING)

admin_email = "andy.amponsah@amalitechtraining.org"
log_path = os.path.join(os.path.dirname(__file__), "instance_creation.log")

"""
This script ssh into an EC2 instance and installs a web server (Apache) on it.
"""

class WebServerSetup:
    def __init__(self, key_file_path='./keys/my-ec2-key'): #a constructor that takes our key path
        self.key_file_path = key_file_path
        self.ssh = paramiko.SSHClient() #instantiate the ssh client
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) #handle unknown host keys automatically

    def print_to_log(self, message):
            print(message)
            with open("instance_creation.log", "a") as log_file:
                log_file.write(message + "\n")


    #------------------------------------------provisioning the web server-----------------------------------------------------------
    
    # method to provision the webserver
    def provision(self, ip_address, custom_message):   

        self.print_to_log(f"Connecting to instance at {ip_address}...")
        key = paramiko.RSAKey.from_private_key_file(self.key_file_path)


        #   loop for a a maximim of 10 * 10 seconds if connection fails
        for attempt in range(10): 
            try:
                # attempt to connect
                self.ssh.connect(hostname=ip_address, username='ec2-user', pkey=key) 
                self.print_to_log("SSH connection established.")
                break
            except Exception as e:
                logging.error(f"SSH not ready, retrying in 10s... ({attempt+1}/10)")
                time.sleep(10)
        else:
            raise Exception("SSH connection failed after 10 attempts.")
        

        #commands to run on the ec2 instance

        commands = [        
            "sudo yum update -y",
            "sudo yum install -y httpd",
            "sudo systemctl start httpd",
            "sudo systemctl enable httpd",
            f'echo "{custom_message}" | sudo tee /var/www/html/index.html'  
        ]


        # write to the root html of the server
        for cmd in commands:
            self.print_to_log(f"Running: {cmd}")
            stdin, stdout, stderr = self.ssh.exec_command(cmd)
            stdout.channel.recv_exit_status()

        self.print_to_log("Sending Log files to admin.")
        self.print_to_log(f"✅ Web server installed and index.html updated. http://{ip_address}/")
        # self.print_to_log(f"sending log file to {admin_email}")
        # send_email_to_admin(log_file_path=log_path, to_email=admin_email)
        self.ssh.close()



        
    #------------------------------------------provisioning the web server-----------------------------------------------------------


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        self.print_to_log("Usage: python script.py <IP_ADDRESS> <CUSTOM_MESSAGE>")
        sys.exit(1)

    ip = sys.argv[1]
    message = sys.argv[2]

    setup = WebServerSetup(key_file_path="./keys/my-ec2-key")
    setup.provision(ip_address=ip, custom_message=message)
