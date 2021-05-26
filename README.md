# ubiops_demoscraper
demo scraper using the UbiOps dev environment



Process flow;
Periodically

Task 1; Deployment 1; Scraper
1. Call rws data; windspeed / waveheight
2. create an output Dict containing the content

Task 2; Deployment 2; export to Sharepoint / azure fileshare / SQL
1. Input from Scraper
2. Access endpoints w/ secrets
3. create appropriate filename and export data

Task 3; create deployment pipeline
task 4; create test routine
Task 4; Create CI/CD of the deployment pipeline
