Download Docker Desktop ----> Run it in background

------------------------------------------------ SETUP JENKINS CONTAINER ---------------------------------------------

Create a custom_jenkins folder ---> Create a Dockerfile inside it ---> Paste Below Code in it



# Use the Jenkins image as the base image
FROM jenkins/jenkins:lts

# Switch to root user to install dependencies
USER root

# Install prerequisites and Docker
RUN apt-get update -y && \
    apt-get install -y apt-transport-https ca-certificates curl gnupg software-properties-common && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add - && \
    echo "deb [arch=amd64] https://download.docker.com/linux/debian bullseye stable" > /etc/apt/sources.list.d/docker.list && \
    apt-get update -y && \
    apt-get install -y docker-ce docker-ce-cli containerd.io && \
    apt-get clean

# Add Jenkins user to the Docker group (create if it doesn't exist)
RUN groupadd -f docker && \
    usermod -aG docker jenkins

# Create the Docker directory and volume for DinD
RUN mkdir -p /var/lib/docker
VOLUME /var/lib/docker

# Switch back to the Jenkins user
USER jenkins


After Creating Dockerfile ----> Open VS Code Terminal in CMD ----> cd custom_jenkins 


After this use following commands one by one:

docker build -t jenkins-dind . 
docker images

docker run -d --name jenkins-dind ^
--privileged ^
-p 8080:8080 -p 50000:50000 ^
-v //var/run/docker.sock:/var/run/docker.sock ^
-v jenkins_home:/var/jenkins_home ^
jenkins-dind


------ You will get some alphanumeric if code run is sucessfull....

docker ps
docker logs jenkins-dind

------- This will give you a password for Jenkins Installation ---> Copy that password


GO to browser--> localhost:8080 --> Paste that password --> Install suggested plugins and create your user...


AGAIN COME TO TERMINAL ( custom_jenkins terminal ) : Write following commands -->

docker exec -u root -it jenkins-dind bash
apt update -y
apt install -y python3
python3 --version
ln -s /usr/bin/python3 /usr/bin/python
python --version
apt install -y python3-pip
apt install -y python3-venv
exit

docker restart jenkins-dind

GO TO JENKINS DASHBOIARD AND SIGN IN AGAIN----->

--------------------------------------------------------- PROJECT DOCKERFILE --------------------------------------------------

# Use a lightweight Python image
FROM python:slim

# Set environment variables to prevent Python from writing .pyc files & Ensure Python output is not buffered
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install system dependencies required by LightGBM
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the application code
COPY . .

# Install the package in editable mode
RUN pip install --no-cache-dir -e .

# Train the model before running the application
RUN python pipeline/training_pipeline.py

# Expose the port that Flask will run on
EXPOSE 5000

# Command to run the app
CMD ["python", "application.py"]



----------------------------------------------------- INSTALL GOOGLE CLOUD CLI ON JENKINS CONTAINER ------------------------------------------------


---- Come to Terminal( custom_jenkins terminal )

docker exec -u root -it jenkins-dind bash
apt-get update
apt-get install -y curl apt-transport-https ca-certificates gnupg
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
echo "deb https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list

apt-get update && apt-get install -y google-cloud-sdk
gcloud --version
exit


--------------------------------------------------------- Give Docker PERMISSIONS -------------------------------------------

----------GRANT DOCKER PERMSIION TO JENKINS USER :

docker exec -u root -it jenkins-dind bash
groupadd docker
usermod -aG docker jenkins
usermod -aG root jenkins
exit
docker restart jenkins-dind


YOU CAN COPY CODE FROM HEREE ..............................

