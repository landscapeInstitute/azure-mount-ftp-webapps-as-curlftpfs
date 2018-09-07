from landscape.azure import ftpmap, connection

####Credentials####
resource_group_name= ""
subscription_id = ""
client_id = ""
secret= ""
tenant= ""
ftp_username = ""
ftp_password = ""
#############

webClient = connection.createWebClient(subscription_id,client_id,secret,tenant)

sites = ftpmap.getSites(resource_group_name,webClient)

for site in sites:

	publishProfiles = site['publishProfiles']
	siteName = site['name']
	
	for publishProfile in publishProfiles:
		if(ftpmap.getProfileMethod(publishProfile) == 'FTP'):
			ftp = ftpmap.getProfileFTPDetails(publishProfile,ftp_username,ftp_password)
			map = ftpmap.mapFTPfs(ftp)
			if(map == True):
				print "\033[92m" + "Mounting " + siteName + " succeeded" + "\033[0m"
			else:
				print "\033[91m" + "Mounting " + siteName + " Failed" + "\033[0m"
