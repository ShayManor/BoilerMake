# BoilerMake
TOMORROW: we show up 9
Elan - data compiling - schema for mongodb
Sean - Frontend - AWS schemas
Shay - Make templates - Make AI agent - sync with Elan - Sync with frontend

1 function of the website will have a repository using mongodb that holds all the different AI agents.

Each AI agent will have a name, description, and flag for which AI agent.
Users will prompt the AI and the AI will build the agent and it can be downloaded as an executable that is simple to use.
You tell the AI what you need, it asks you follow up questions, and you will answer then it will make the agent.
If the AI agent already exists, it will be on the repository and they will respond.

Frontend HTML css JS - python middle layer - mongodb backend
Make the agent - upload to mongodb - spawn an ec2 instance running the agent - website pings the ec2 instance 
There will be a template for exactly how the agent will run.
Keep as much of the formatting for the launch configuration the same so the linux commands are always the same.

sudo yum update
sudo yum install unzip -y
sudo yum install python3.12
sudo yum install nginx -y
sudo yum update
sudo yum install nginx -y
sudo systemctl start nginx
sudo systemctl enable nginx
sudo nano /etc/nginx/conf.d/flask_app.conf
paste: 
server {
    listen 80;
    server_name YOUR_EC2_PUBLIC_IP;  # Or your domain name

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
sudo nginx -t
sudo systemctl reload nginx
sudo yum install git
git clone https://github.com/ShayManor/math-practice-generator.git
cd math-practice-generator
python3.12 -m venv test
source test/bin/activate
pip3 install -r requirements.txt
python3 app.pysudo systemctl reload nginx

1) apt install
2) install git
3) clone
4) run the agent
