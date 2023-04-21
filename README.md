# Puzzle Multi-Agents

This is a project developped during the Module of **Opening** from the Engineer Path of CY TECH, France. 
</br>

## Project Description
</br>


## Available Deployment

The interface is hosted through Streamlit. It is available at the following [Link](https://dorian-roux-ing3-ouverture-ia-app-oq0zfc.streamlit.app/).

Due to the lack of time, we could not make the most suitable interface regarding the project, however, we tried to make it as user-friendly as possible while being able to display answers to the multi-agents problematic.

</br>

## Local Deployment
### Prerequisite

The local deployment is based on Docker. Thus, to correctly launch our interface, the following software must be installed.
- [Docker](https://www.docker.com/)


### Launch the Interface

The local deployment using Docker is really fast and simple since it consists of the three steps described below.

#### 1° - Clone the Repository
Firstly, you must clone this reposity. To do so, you can use the following command.
```bash
git clone https://github.com/dorian-roux/ing3-ouverture-ia
```

#### 2° - Build the Docker Image
Secondly, you need to build the Docker Image based on this repository Dockerfile. To do so, you can use the following command.
```bash
docker build -t {TAG} .
```
<u>Note:</u> &nbsp; `{TAG}` is the name you want to give to your Docker Image. It is used to identify it later.


#### 3° - Run the Docker Container
Finally, you need to run the Docker Container based on the Docker Image you just built. To do so, you can use the following command.
```bash
docker run -p 8501:8501 {TAG}
```
<u>Note:</u> &nbsp; We defined the port `8501` as the port used by the Streamlit Interface. Thus, you can access it by typing `localhost:8501` in your browser.



