# Louis Varley, 05-Sep-2018
# This script uses Azure CLI to find all Webapps and get their publishing profiles
# Create folders in mount and then use curlftpfs to mount them
# Before mount, it unmounts them so they are refreshed

# https://github.com/Azure-Samples/app-service-web-python-manage
# https://github.com/Azure/azure-sdk-for-python

import os
import json
from xml.dom.minidom import parse, parseString
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.web import WebSiteManagementClient
from azure.mgmt.web.models import Site, Deployment
from subprocess import call

# Extract FTP Details from a PublishProfile
def getProfileFTPDetails(publishProfile,ftp_username,ftp_password):

	publishMethod = publishProfile.getAttribute('publishMethod')
		
	if(publishMethod == "FTP"):
		PublishURL = str(publishProfile.getAttribute('publishUrl'))
		PublishUser = str(publishProfile.getAttribute('userName'))
		PublishPass = str(publishProfile.getAttribute('userPWD'))
		ProfileName = str(publishProfile.getAttribute('profileName')).replace(" - FTP","")
		
		ftp = {}
		ftp['username'] = str(PublishUser.split("\\")[0].replace("$","") + "\\" + ftp_username)
		ftp['password'] = str(ftp_password)
		ftp['host'] = str(PublishURL.replace("ftp://",""))
		ftp['mount'] = str("/mnt/"+ProfileName)	
	
		return ftp
		

def getProfileMethod(publishProfile):

	publishMethod = publishProfile.getAttribute('publishMethod')
	return publishMethod
		
# Get All Sites and Publish Profiles
def getSites(group_name,web_client):

	sites = []

	for site in web_client.web_apps.list_by_resource_group(group_name):
		name = format(site.name)
		publishXML = parseString(list(web_client.web_apps.list_publishing_profile_xml_with_secrets(group_name,site.name))[0])
		sites.append({'publishProfiles':publishXML.getElementsByTagName('publishProfile'),'name':site.name})

	return sites

#Map a given FTP on OS
def mapFTPfs(ftp):

	os.system("mkdir " + ftp['mount'] + " > /dev/null 2>&1")
	os.system("umount " + ftp['mount'] + " > /dev/null 2>&1")
	os.system("curlftpfs " + "'" + ftp['username'] + "':" + ftp['password'] + "@" + ftp['host'] + " " + ftp['mount'] + " > /dev/null 2>&1")
	
	if os.listdir(ftp['mount']) == []:
		return False
	else:
		return True
	
	

def ftpfsMapWebApps(self):

	web_client = WebSiteManagementClient(credentials, subscription_id)

	for site in web_client.web_apps.list_by_resource_group(group_name):
		name = format(site.name)
		publishXML = parseString(list(web_client.web_apps.list_publishing_profile_xml_with_secrets(group_name,site.name))[0])
		publishProfiles = publishXML.getElementsByTagName('publishProfile')
		for publishProfile in publishProfiles:
			publishMethod = publishProfile.getAttribute('publishMethod')
			if(publishMethod == "FTP"):
				PublishURL = str(publishProfile.getAttribute('publishUrl'))
				PublishUser = str(publishProfile.getAttribute('userName'))
				PublishPass = str(publishProfile.getAttribute('userPWD'))
				ProfileName = str(publishProfile.getAttribute('profileName')).replace(" - FTP","")

				ftpUsername = PublishUser.split("\\")[0].replace("$","") + "\\" + subscription_ftp_username
				ftpPassword = subscription_ftp_password
				ftpHost = PublishURL.replace("ftp://","")
				ftpMount = "/mnt/"+ProfileName

				print "\033[92m" + "Mounting " + ProfileName + "\033[0m" 
				os.system("mkdir " + ftpMount + " > /dev/null 2>&1")
				os.system("umount " + ftpMount + " > /dev/null 2>&1")
				os.system("curlftpfs " + "'" + ftpUsername + "':" + ftpPassword + "@" + ftpHost + " " + ftpMount + " > /dev/null 2>&1")

				if len(os.listdir(ftpMount))==0:
					print "\033[91m" + "Mounting Failed" + "\033[0m"
				else:
					print "\033[92m" + "Mounted Successfully" + "\033[0m"
