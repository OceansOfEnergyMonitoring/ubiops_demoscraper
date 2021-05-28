"""
The file containing the deployment code is required to be called 'deployment.py' and should contain the 'Deployment'
class and 'request' method.
"""

# Always use absolute imports when importing modules from the deployment package directory. For example
# `import my_module` instead of `import .my_module`
import os
import pandas as pd
from dotenv import load_dotenv
import pysharepoint as ps

class Deployment:
    def __init__(self, base_directory, context):
        """
        Initialisation method for the deployment. It can for example be used for loading modules that have to be kept in
        memory or setting up connections. Load your external deployment files (such as pickles or .h5 files) here.

        :param str base_directory: absolute path to the directory where the deployment.py file is located
        :param dict context: a dictionary containing details of the deployment that might be useful in your code.
            It contains the following keys:
                - deployment (str): name of the deployment
                - version (str): name of the version
                - input_type (str): deployment input type, either 'structured' or 'plain'
                - output_type (str): deployment output type, either 'structured' or 'plain'
                - language (str): programming language the deployment is running
                - environment_variables (str): the custom environment variables configured for the deployment.
                    You can also access those as normal environment variables via os.environ
        """
        #get environmental variables
        load_dotenv('.env')  # if your env file is stored in /app directory
        self.sharepoint_base_url = os.environ['SHAREPOINT_BASEURL']
        self.sharepoint_site = os.environ['SHAREPOINT_BASESITE']

        #create a sharepoint connector
        self.site = ps.SPInterface(self.sharepoint_base_url,os.environ['AZURE_UID'],os.environ['AZURE_PASS'])

        #make base directory path available in this class
        self.base_directory = base_directory
        print("Initialising My Deployment")

    def download_sp(self,sp_baseurl,sp_site,sp_folderpath,sp_filename, sink):
        sharepoint_site = sp_baseurl + '/sites/' + sp_site + '/'
        source_path = 'Shared Documents/' + sp_folderpath
        return self.site.download_file_sharepoint(source_path, sink,sp_filename,sharepoint_site) 

    def upload_sp(self,source_path,sp_baseurl,sp_site,sp_folderpath, sp_filename):
        sharepoint_site = sp_baseurl + '/sites/' + sp_site + '/'
        sink_path = 'Shared Documents/' + sp_folderpath
        return self.site.upload_file_sharepoint(source_path, sink_path,sp_filename,sharepoint_site)

    def request(self, data):
        """
        Method for deployment requests, called separately for each individual request.

        :param dict/str data: request input data. In case of deployments with structured data, a Python dictionary
            with as keys the input fields as defined upon deployment creation via the platform. In case of a deployment
            with plain input, it is a string.
        :return dict/str: request output. In case of deployments with structured output data, a Python dictionary
            with as keys the output fields as defined upon deployment creation via the platform. In case of a deployment
            with plain output, it is a string. In this example, a dictionary with the key: output.
        """
        # expected input variables;
        # payload
        # SpFlderpath; full folder path from site onwards, ex: '07 OMM/47 Data Logging/UbiOpsdata/'
        # spFilename; target filename including extensions, ex: 'rws_windspeed_example.csv'

        #determine destination path on Sharepoint
        spFolderpath = data['spFolderpath']
        spFilename = data['spFilename']

        print("Exporting; ", spFilename, "to: ", spFolderpath)

        #DEBUG:prepare a local mockup csv and load as pandas dataframe, overwrite spFilename key to the mockup file
        spFilename = "rws_windspeed_example.csv"
        
        path = self.base_directory + "\\" + spFilename
        
        #check if filepath is valid
        self.mockup_payload = pd.read_csv(os.path.join(self.base_directory,spFilename),sep=';',header='infer')
        print("mockup csv loaded: " + str(self.mockup_payload.head(1)))

        #upload csv file to sharepoint, # a directories will be created if they do not exist yet
        out = self.upload_sp(self.base_directory, self.sharepoint_base_url, self.sharepoint_site, spFolderpath, spFilename)
        
        #output_df = self.mockup_payload.head(1).to_json(orient='split')
        #print("out dict: ")
        #print(output_df)

        # You can run any code to handle the request here.

        # For a structured deployment, we return a Python dict with output. In this example, we are assuming this
        # deployment receives one input field called 'input' and outputs one field called 'output'
        return {
            "output": out
        }