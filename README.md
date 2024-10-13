```markdown
# Weather App Project on Ubuntu Server (Azure)

This project demonstrates how to set up an Ubuntu server on Microsoft Azure, configure SSH login with private/public keys, install Nginx, deploy a simple Python weather app, and secure the server with a firewall.

## Table of Contents
1. [Setting Up the Local Environment](#1-setting-up-the-local-environment)
2. [Generating SSH Keys](#2-generating-ssh-keys)
3. [Connecting to the Ubuntu Server on Azure](#3-connecting-to-the-ubuntu-server-on-azure)
4. [Setting Up the Server](#4-setting-up-the-server)
   - [Creating a New User](#a-creating-a-new-user)
   - [Setting Up SSH for the New User](#b-set-up-ssh-for-the-new-user)
5. [Disabling Password Authentication](#5-disabling-password-authentication-securing-ssh)
6. [Installing and Configuring Nginx](#6-installing-and-configuring-nginx)
7. [Installing Python and Setting Up the Weather Project](#7-installing-python-and-setting-up-the-weather-project)
8. [Running the Python Project](#8-running-the-python-project)
9. [Configuring Nginx to Serve the Python App](#9-configuring-nginx-to-serve-the-python-app-optional)
10. [Opening Firewall Ports](#10-opening-firewall-ports-for-web-traffic)
11. [Testing Everything](#11-testing-everything)

---

## 1. Setting Up the Local Environment

```bash
# Install virtualenv if you don't have it
pip install virtualenv

# Create a virtual environment
virtualenv weather_env

# Activate the virtual environment (Windows)
weather_env\Scripts\activate

# Activate the virtual environment (Linux/macOS)
source weather_env/bin/activate

# Install the requests library to make HTTP calls
pip install requests
```

---

## 2. Generating SSH Keys

```bash
# Generate SSH keys (public and private) on your local machine
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"

# View the public key
cat ~/.ssh/id_rsa.pub
```

---

## 3. Connecting to the Ubuntu Server on Azure

1. **Create the Ubuntu VM in Azure** and during the setup, paste the public key generated in the previous step.

2. **Get the public IP address of the VM from the Azure portal**.

```bash
# Connect to your Ubuntu server using SSH
ssh -i ~/.ssh/id_rsa username@your_server_ip
```

---

## 4. Setting Up the Server

### a. Creating a New User

```bash
# Add a new user (replace 'newuser' with the actual username)
sudo adduser newuser

# Add the new user to the sudo group for administrative privileges
sudo usermod -aG sudo newuser

# Switch to the new user
su - newuser
```

### b. Set Up SSH for the New User

```bash
# On the server, create an .ssh directory for the new user
mkdir ~/.ssh

# Set proper permissions for the .ssh directory
chmod 700 ~/.ssh

# Add the public key to the authorized_keys file
nano ~/.ssh/authorized_keys

# (Paste your public key here and save the file)

# Set the correct permissions for the authorized_keys file
chmod 600 ~/.ssh/authorized_keys
```

---

## 5. Disabling Password Authentication (Securing SSH)

```bash
# Open the SSH configuration file
sudo nano /etc/ssh/sshd_config

# Disable password-based login and root login
# Ensure these lines are set as follows:
PasswordAuthentication no
PermitRootLogin no

# Restart the SSH service
sudo systemctl restart sshd
```

---

## 6. Installing and Configuring Nginx

```bash
# Update package lists
sudo apt update

# Install Nginx
sudo apt install nginx

# Allow Nginx through the firewall
sudo ufw allow 'Nginx Full'

# Verify Nginx is running
sudo systemctl status nginx

# Visit your server's public IP in a browser to check Nginx's default page
```

---

## 7. Installing Python and Setting Up the Weather Project

```bash
# Install Python on the Ubuntu server
sudo apt install python3-pip python3-venv

# Create a project directory and navigate into it
mkdir ~/weather_project && cd ~/weather_project

# Create a virtual environment for Python
python3 -m venv weather_env

# Activate the virtual environment
source weather_env/bin/activate

# Install the required libraries
pip install requests

# Create the Python script for fetching weather data
nano weather_app.py

# (Paste the Python weather script here, save, and exit)
```

---

## 8. Running the Python Project

```bash
# Run the Python weather script
python weather_app.py
```

---

## 9. Configuring Nginx to Serve the Python App (Optional)

If you're deploying a web application using Python, you would configure Nginx to serve the Python app (e.g., Flask or Django).

```bash
# Install Gunicorn (a Python WSGI HTTP Server)
pip install gunicorn

# Create a Gunicorn systemd service file (optional if using Flask/Django)
sudo nano /etc/systemd/system/gunicorn.service

# Configure Nginx to reverse proxy to Gunicorn
sudo nano /etc/nginx/sites-available/weather_project

# (Set up Nginx for reverse proxy and save the configuration)
```

---

## 10. Opening Firewall Ports for Web Traffic

```bash
# Allow HTTP and HTTPS through the firewall
sudo ufw allow 'Nginx Full'

# Check the firewall status to confirm the rules are in place
sudo ufw status
```

---

## 11. Testing Everything

- Visit your server’s IP address in the browser to test the Nginx setup.
- Run your Python app to test the weather data retrieval.

---


sudo ufw allow 5000/tcp
gunicorn --bind 0.0.0.0:5000 app:app
curl "http://your-server-ip:5000/weather?city=London"


### Step 1: Install Gunicorn and Nginx
```bash
pip install gunicorn
sudo apt update
sudo apt install nginx
```

### Step 2: Set Up Gunicorn

1. **Create a Gunicorn service file**:
   ```bash
   sudo nano /etc/systemd/system/gunicorn.service
   ```

2. **Add this content to the service file**:
   *(Replace paths as necessary)*
   ```ini
   [Unit]
   Description=Gunicorn instance to serve Flask app
   After=network.target

   [Service]
   User=your_user_name
   Group=www-data
   WorkingDirectory=/path/to/your/project
   ExecStart=/path/to/your/virtualenv/bin/gunicorn --workers 3 --bind 127.0.0.1:5000 weather_app:app

   [Install]
   WantedBy=multi-user.target
   ```

3. **Start and enable Gunicorn service**:
   ```bash
   sudo systemctl start gunicorn
   sudo systemctl enable gunicorn
   ```

4. **Check Gunicorn status**:
   ```bash
   sudo systemctl status gunicorn
   ```

### Step 3: Configure Nginx

1. **Create an Nginx configuration file**:
   ```bash
   sudo nano /etc/nginx/sites-available/your_flask_app
   ```

2. **Add the following content**:
   ```nginx
   server {
       listen 80;
       server_name your_domain_or_IP;

       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }

       location /static {
           alias /path/to/your/project/static;
       }
   }
   ```

3. **Enable the Nginx site**:
   ```bash
   sudo ln -s /etc/nginx/sites-available/your_flask_app /etc/nginx/sites-enabled
   ```

4. **Test the Nginx configuration**:
   ```bash
   sudo nginx -t
   ```

5. **Restart Nginx**:
   ```bash
   sudo systemctl restart nginx
   ```

### Step 4: Open Port 80
```bash
sudo ufw allow 'Nginx Full'
```

### Step 5: Check the status of the firewall
```bash
sudo ufw status
```

