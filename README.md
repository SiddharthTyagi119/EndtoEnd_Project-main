Problem Statement
The purpose of this data is to look into the different features to observe their relationship. Features such as age,location,family condition against their existing medical expense to be used for predicting future medical expense of individuals that help medical insurance to make decision on charging the premium.This can assist a person in concentrating on the health side of an insurance policy rather han the ineffective part.

# Run from terminal:
docker login insurancepremium.azurecr.io

docker build -t insurancepremium.azurecr.io/insurance1 .

docker push insurancepremium.azurecr.io/insurance1

# Deployment Steps to deploy on azure ci/cd pipeline:
Build the Docker image of the Source Code

Push the Docker image to Container Registry

Launch the Web App Server in Azure

Pull the Docker image from the container registry to Web App server and run

# Project Pipeline

![training_pipeline](https://github.com/SiddharthTyagi119/EndtoEnd_Project-main/assets/52122171/f01d8373-b7fd-41b5-9cb4-f0967a2ad1e2)

# Flowchart of deployment of application on azure web app
![azure](https://github.com/SiddharthTyagi119/EndtoEnd_Project-main/assets/52122171/05ac9fd7-f75e-4b3e-962a-1666e14d9b66)
