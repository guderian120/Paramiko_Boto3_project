
---

# EC2 Web Server Setup with Boto3 and Paramiko

This project automates the process of launching an EC2 instance on AWS, setting up an HTTP server (Apache), and modifying the `index.html` file through SSH using **boto3** and **paramiko** libraries.

### 📝 Table of Contents

* [Requirements](#-requirements)
* [Getting Started](#-getting-started)
* [Importing SSH Key to AWS CLI](#-importing-ssh-key-to-aws-cli)
* [AWS Authentication with Boto3](#-aws-authentication-with-boto3)
* [Using the EC2 Instance Script](#-using-the-ec2-instance-script)
* [Using the Web Server Update Script](#-using-the-web-server-update-script)
* [Troubleshooting](#-troubleshooting-issues)

---

## 📋 Requirements

Before running the scripts, ensure you have the following installed:

1. **Python 3.6+**

2. **boto3** (AWS SDK for Python)

   ```bash
   pip install boto3
   ```

3. **paramiko** (for SSH connections)

   ```bash
   pip install paramiko
   ```

4. **AWS CLI** (to manage AWS services from the command line)

   ```bash
   pip install awscli
   ```

---

## 🚀 Getting Started

To use this project, follow the steps below to set up your AWS environment, import SSH keys, and configure AWS access keys.

### 🔑 Importing SSH Key to AWS CLI

Before launching your EC2 instance, you need to import an existing **public SSH key** to AWS. This key will be used for SSH access to your EC2 instances.

1. **Generate or use an existing SSH key pair**:

   * If you don't have a key pair, you can generate one with the following command:

     ```bash
     ssh-keygen -t rsa -b 2048 -f ~/.ssh/my-ec2-key
     ```

     This creates a private key file (`my-ec2-key`) and a public key file (`my-ec2-key.pub`).

2. **Import the public key to AWS**:

   * Use the AWS CLI to import the public key to your AWS account:

     ```bash
     aws ec2 import-key-pair --key-name "my-presentation-key" --public-key-material fileb://~/.ssh/my-ec2-key.pub
     ```
   * This command uploads your public key to AWS so you can use it to SSH into EC2 instances.

---

### 🧑‍💻 AWS Authentication with Boto3

To interact with AWS services using **boto3**, you need to authenticate with **AWS access keys**.

1. **Set up AWS credentials**:

   * You can configure your AWS credentials using the AWS CLI:

     ```bash
     aws configure
     ```
   * This command will prompt you to enter your:

     * **AWS Access Key ID**
     * **AWS Secret Access Key**
     * **Default region name** (e.g., `us-east-1`)
     * **Default output format** (e.g., `json`)

   If you haven't already, you can create access keys in the **IAM** section of the AWS Management Console:

   * Go to **IAM > Users > Your User > Security Credentials**.
   * Generate a new **Access Key ID** and **Secret Access Key**.

2. **Check if boto3 is properly configured**:

   * After configuring your AWS CLI, you can check if the AWS credentials are working by running:

     ```bash
     aws sts get-caller-identity
     ```
   * This command should return details about your AWS account.

---

## 🖥️ Using the EC2 Instance Script

This script creates a new EC2 instance on AWS using **boto3**. It launches the instance, outputs the instance's public IP. and pipes it to a paramiko script to spin up or upate a webserver

1. **Configure your script**:

   * In the script, specify the following details:

     * **AMI ID**: ID of the Amazon Machine Image (AMI) to launch (e.g., Amazon Linux 2).
     * **Instance Type**: Instance type (e.g., `t2.micro`).
     * **Key Name**: The name of the key pair to associate with the instance.
     * **Security Group ID**: The ID of the security group to apply to the instance(ensure port 22 and 80 is opened).

2. **Run the script**:

   * Simply run the script in your terminal:

     ```bash
     python create_ec2_instance.py
     ```
   * The script will:

     * Launch the EC2 instance
     * Return the public IP address of the new instance
     * Call the web_server_conf.py class with the ip to spin up a webserver


---

## 🔧 Using the Web Server Update Script

Once the EC2 instance is created, this script connects to the instance using **paramiko** (via SSH), installs the Apache HTTP server, and writes a custom message to the `index.html` file.

1. **Configure your script**:

   * In the script, specify the following:

     * **IP Address**: The public IP of the EC2 instance.
     * **Custom Message**: The message you want to display on the web server's `index.html`.

2. **Run the script**:

   * Run the script to connect to the EC2 instance and update the web server:

     ```bash
     python update_webserver.py <IP_ADDRESS> "<CUSTOM_MESSAGE>"
     ```

     Example:

     ```bash
     python web_server_conf.py 34.201.12.100 "Welcome to my EC2 web server!"
     ```
   * The script will:

     * Connect to the instance via SSH
     * Install Apache HTTP server
     * Write your custom message to `/var/www/html/index.html`

---

## ⚠️ Troubleshooting Issues

* **SSH connection issues**:

  * Make sure the security group allows inbound SSH traffic on port 22.
  * Ensure the key file (`my-ec2-key.pem`) has the correct permissions:

    ```bash
    chmod 400 ~/.ssh/my-ec2-key.pem
    ```

* **Instance not launching**:

  * Check your AWS quota for EC2 instances and make sure your region has enough resources.
  * Verify that your IAM user has the necessary permissions to launch EC2 instances and create key pairs.

---

## 💬 Conclusion

This project provides an easy way to automate the process of creating EC2 instances and configuring them with a basic web server setup using **boto3** and **paramiko**. By following this guide, you should be able to launch instances, install software, and modify web content dynamically.

For more details, refer to the official documentation for [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) and [paramiko](http://docs.paramikro.com/en/latest/).

---

