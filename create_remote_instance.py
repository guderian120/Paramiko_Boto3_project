import boto3
from web_server_conf import WebServerSetup
import logging

# Suppress boto3 and botocore debug logs
logging.getLogger("botocore").setLevel(logging.WARNING)
logging.getLogger("boto3").setLevel(logging.WARNING)
logging.getLogger().setLevel(logging.WARNING)


"""
This script launches an EC2 instance on AWS using Boto3.
It uses the default Amazon Linux 2 AMI and a t2.micro instance type. Passes the public IP address of the instance to a WebServerSetup class to provision a web server.
using paramiko for SSH connection.
But you can also specify custom values for the AMI ID, instance type, key name, and security group ID.
"""

class EC2Launcher:
    def __init__(
        self,
        ami_id='ami-04e7764922e1e3a57',
        instance_type='t2.micro',
        key_name='my-presentation-key',
        security_group_id='sg-001e5942116deda06'
    ):
        self.ami_id = ami_id
        self.instance_type = instance_type
        self.key_name = key_name
        self.security_group_id = security_group_id
        self.ec2 = boto3.resource('ec2')



        #--------------------------------------Creating Instance with this method-----------------------------------------------------------



    def create_instance(self):
         # a boto3 method to create new ec2 instances
        print("Launching EC2 instance...")
        instance = self.ec2.create_instances(  
            ImageId=self.ami_id,
            MinCount=1,
            MaxCount=1,
            InstanceType=self.instance_type,
            KeyName=self.key_name,
            SecurityGroupIds=[self.security_group_id],
        )[0]

        instance.wait_until_running() # This script waits until the instance is running before proceeding
        instance.reload()

        print(f"Instance launched with ID: {instance.id}")
        print(f"Public IP: {instance.public_ip_address}")

        return instance.public_ip_address   #return the ip address of the instance
    


    

    #--------------------------------------Creating Instance with this method-----------------------------------------------------------


if __name__ == "__main__":
    launcher = EC2Launcher()    #instantiate the instance class
    ip = launcher.create_instance() #call the method to create instances
    web_serevr_setup = WebServerSetup() #instantiate the web server creating class
    web_serevr_setup.provision(ip_address=ip, custom_message="Hello from EC2!, This is the First Time I am running this webserver") #pass the Ip addres and your custom message to it
