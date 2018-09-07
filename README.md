# azure-mount-ftp-webapps-as-curlftpfs
This code will use the Azure API to mount all your webapps as mounts in /mnt/ 

## What it does?

For Example, if you have 3 webapps on Azure. 

`www-web1-com
www-web2-com
www-web3-com`

running this python script, with the correct credentials will mount automaticly for you. 

`/mnt/www-web1-com
/mnt/www-web2-com
/mnt/www-web3-com`

We wrote this script alongside our Wordpress WP-CLI Python script so you can use a single server to run WP-CLI against multiple instances of wordpress running on webapps. 


## Using it

### 1)
Use the following repos to install the Python SDK for Azure

https://github.com/Azure-Samples/app-service-web-python-manage
https://github.com/Azure/azure-sdk-for-python

### 2)
Clone this repo to somewhere

`sudo git clone https://github.com/landscapeinstitute-bot/azure-mount-ftp-webapps-as-curlftpfs.git`

### 3)

Install curlftpfs `sudo apt-get install curlftpfs`

### 3)

Create a new app in Azure Directory 
Use the following for details https://docs.microsoft.com/en-us/azure/azure-resource-manager/resource-group-create-service-principal-portal

### 4)

now edit the `azure-mount-all-webapps.py` file and enter the following information

resource_group_name = *Your Resource Group Name*
subscription_id = *Your Subscription ID, found under azure portal / subscriptions*
client_id = *In Azure Portal, enter your client/app id*
secret = *Your App Secret*
tenant = *Your Tenant ID* (https://docs.microsoft.com/en-us/onedrive/find-your-office-365-tenant-id)
ftp_username = *Your master FTP username set in webapps for ALL your webapps* (this comes before the individual username for each app)
ftp_password = *Your password for your FTP*

### 6) Run `sudo python azure-mount-all-webapps.py`

## Finishing up + Protection

You should now have all your sites mounted in /mnt/ only accessable by root. 
to protect this script, make it readable only by root 

This script contains clear text copies of important details. You should protect it. 

`
sudo chown root:root /path/to/script
sudo chmod 700 /path/to/script
`

Do not recomend running anything like this as non-root. Use this to then run scripts against your sites. 

If correct, non-root users should have no access to the scripts, or the sites. 




