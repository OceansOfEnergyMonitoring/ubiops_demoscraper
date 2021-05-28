"""
This file simulates the platform back-end that initialises the deployment and makes a request. It should not be included
in a deployment package.
"""

import os
import sys
import pandas as pd

fn_input = "short_rws_windspeed_example.csv"

# Deployment_directory points to base folder of the deployment, which should therefore be called 'deployment_package'.
deployment_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'deployment_package')

# Update $PATH with the deployment base directory and libraries before importing the deployment package.
sys.path = [deployment_directory, os.path.join(deployment_directory, 'libraries')] + sys.path

# Import the deployment package
import deployment_package.deployment

def main():
    print("Starting deployment request example")

    # Initialise the deployment. The platform calls this method in exactly the same way.
    # Here, we leave the context argument as an empty dictionary since it is normally filled in by the platform
    # when loading the deployment.
    deployment = deployment_package.deployment.Deployment(
        base_directory=deployment_directory, context=dict()
    )

    # Mock input data. When a request is made, this dictionary is initialized.
    # In case of deployments with structured data, it will contain the keys defined by the user upon deployment
    # creation via the platform. In case of a deployment that receives a plain input, it will be a string.

    # load in a dataFrame to push to the deployment, to simulate serialized pandas dataframe 
    df_input = pd.read_csv(fn_input,sep=';',header='infer')
    inputdata = df_input.to_json(orient='split')

    """
    INPUT EXAMPLE:
'{"columns":["Datum","Tijd","Parameter","Locatie","Waarde","Verwachting","Eenheid","Windrichting","Windrichting eenheid","Bemonsteringshoogte","Referentievlak","Unnamed: 11"],"index":[0,1,2,3],"data":[["28-4-2021","13:30:00","Windsnelheid Lucht t.o.v. Mean Sea Level in m\\/s","Europlatform",8.65,null,"m\\/s",19.7,"graden",2910,"NVT",null],["28-4-2021","13:40:00","Windsnelheid Lucht t.o.v. Mean Sea Level in m\\/s","Europlatform",8.86,null,"m\\/s",18.3,"graden",2910,"NVT",null],["28-4-2021","13:50:00","Windsnelheid Lucht t.o.v. Mean Sea Level in m\\/s","Europlatform",8.89,null,"m\\/s",15.4,"graden",2910,"NVT",null],["28-4-2021","14:00:00","Windsnelheid Lucht t.o.v. Mean Sea Level in m\\/s","Europlatform",8.72,null,"m\\/s",13.2,"graden",2910,"NVT",null]]}'
    """
    # Adjust this example to test deployment input and request processing
    input_data = {
        "input" : inputdata,
        "spfolderpath": '07 OMM/47 Data Logging/UbiOpsdata/',
        "spfilename" : "rws_windspeed_example.csv"  
    }

    # Make the prediction. The platform calls this method in exactly the same way
    request_result = deployment.request(input_data)

    print("Deployment request result: %s" % request_result)


if __name__ == '__main__':
    main()
