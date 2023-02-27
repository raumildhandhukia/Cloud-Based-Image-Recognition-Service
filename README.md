
# CSE546 IaaS - Cloud-Based Image Recognition Service
Our project is to develop a cloud-based image recognition service that leverages deep learning to classify and identify images provided by users. The service will be accessible to users via a web interface, and it will utilize cloud resources to perform the deep learning computations needed for image recognition.

This is an elastic application that can automatically scale out and in on-demand by leveraging the Infrastructure-as-a-Service (IaaS) resources from Amazon Web Services (AWS). 

# Authors

## Raumil Bharatbhai Dhandhukia

- Developed Web-Tier source code which enables clients to upload the file to the web server. Created functionality that sends the messeges to request-queue and fetches appropriate image recognition results from response-queue.

- Set up the Web-Tier EC2 Instance and configured Web-Tier instance with nginx to forwarded the traffic. Wrote a script on App-Tier to automatically start the image recognition service as soon as server is started or restarted.

## Parv Jetalkumar Dave

- Developed S3 resources to utilize the boto3 library easily. Developed App-Tier source code to retrieve the messeges from request-queue and perform the image recognition. 

- Set up the AWS. Created users and roles with appropriate securities. Created AMI and launch templates. Created Alarms for cloudwatch and integrated it with request-queue.

## Chaitya Dharmeshkumar Dave

- Developed SQS resources to utilize boto3 and co-operated in developing algorithm of the App-Tier. Handled different test cases for the web-tier, app-tier & resources, and managed the exceptions.

- Created Auto Scaling Group to Scale In/Out the App-Tier based upon cloudwatch's metrix.





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

- AMI ID: ami-02962ef374eadec5a


