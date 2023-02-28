
# CSE546 IaaS - Cloud-Based Image Recognition Service
Our project is to develop a cloud-based image recognition service that leverages deep learning to classify and identify images provided by users. The service will be accessible to users via a web interface, and it will utilize cloud resources to perform the deep learning computations needed for image recognition.

This is an elastic application that can automatically scale out and in on-demand by leveraging the Infrastructure-as-a-Service (IaaS) resources from Amazon Web Services (AWS). 

## Installation

Install Unzip (If you do not have it installed)

```bash
sudo apt install unzip
```

Install AWS CLI

```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

Set Up the AWS (Add access key, secret, region and format)

```bash
aws configure
```

Install Dependencies

```bash
pip install -r requirements.txt
```

## Run 

Start Web-Tier

```bash
python3 server.py
```

Start App-Tier

```bash
python3 app/app.py
```

Now web server will be listening on http://127.0.0.1:3000/. It will take Image file as payload. Image will be stored on S3 Bucket and key of image will be sent to request-queue(SQS). App-Tier will continously processing images and sending output on response-queue(SQS). Web-Tier will fetch responses and return it to the client.

    
## Auto-Start Services Of App-Tier Instances

Create .service file

```bash
sudo touch /etc/systemd/system/myservice.service
```

Edit .service file

```bash
sudo nano /etc/systemd/system/myservice.service
```

Copy this service file into the .service created and save the .service file (change the path according to your system)

```bash
[Unit]
Description=Run AppTier Service Each Time Server Starts Up
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/
ExecStart=/usr/bin/python3 /home/ubuntu/app.py
Restart=always

[Install]
WantedBy=multi-user.target

```

Reload the systemd daemon to read the new service file

```bash
sudo systemctl daemon-reload
```

Enable the service to start at boot time

```bash
sudo systemctl enable myservice.service
```

Start the service

```bash
sudo systemctl start myservice.service
```
## AWS Resources

- SQS Request Queue: request-queue

- SQS Response Queue: response-queue

- S3 Input Bucket: cse546-cc-autoscale-input-bucket

- S3 Output Bucket: cse546-image-processing-op

- EC2 Web-Tier: CC-ImageProcessing-Web

- EC2 App-Tier: cc-image-processing-app-tier

## Help

**Web-Tier contains** `server.py, resources/s3.py, resources/sqs.py, resources/__init__.py`


**App-Tier contains** `app/app.py, app/image_classification.py, app/imagenet-labels.json, app/__init__.py, resources/s3.py, resources/sqs.py, resources/__init__.py`

**resouces** folder is shared by Web-Tier and App-Tier. It contains basic operations related to `S3 and SQS`

`requirements.txt` is common for Web-Tier and App-Tier.

`workload_generator.py` and `multithread_workload_generator.py` are used to test the services.



