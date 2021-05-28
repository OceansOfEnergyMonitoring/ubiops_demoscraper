import pysharepoint as ps
from dotenv import load_dotenv
import os


load_dotenv('.env')

sharepoint_base_url = os.environ['SHAREPOINT_BASEURL']
sharepoint_site = os.environ['SHAREPOINT_BASESITE']
username = os.environ['AZURE_UID']
password = os.environ['AZURE_PASS']

folderpath= '07 OMM/47 Data Logging/'
filename = 'UbiOpsdataexport.txt'


site = ps.SPInterface(sharepoint_base_url,username,password)

def download_sp(sp_baseurl,sp_site,sp_folderpath,sp_filename, sink):
    sharepoint_site = sp_baseurl + '/sites/' + sp_site + '/'
    source_path = 'Shared Documents/' + sp_folderpath
    return site.download_file_sharepoint(source_path, sink,sp_filename,sharepoint_site)
    
def upload_sp(source_path,sp_baseurl,sp_site,sp_folderpath, sp_filename):
    sharepoint_site = sp_baseurl + '/sites/' + sp_site + '/'
    sink_path = 'Shared Documents/' + sp_folderpath
    return site.upload_file_sharepoint(source_path, sink_path,sp_filename,sharepoint_site)

sink = os.getcwd()
out = download_sp(sharepoint_base_url,sharepoint_site, folderpath, filename, sink)

source_path = os.getcwd()
out = upload_sp(source_path, sharepoint_base_url, sharepoint_site, folderpath,filename)




