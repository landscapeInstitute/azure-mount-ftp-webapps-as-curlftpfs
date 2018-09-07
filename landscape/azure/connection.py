from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.web import WebSiteManagementClient

def createWebClient(this_subscription_id,this_client_id,this_secret,this_tenant):

	credentials = ServicePrincipalCredentials(
		client_id=this_client_id,
		secret=this_secret,
		tenant=this_tenant
	)
	
	web_client = WebSiteManagementClient(credentials, this_subscription_id)
	
	return web_client
	
	
