#Extract base python image
#FROM python:3.8.15-alpine
FROM python:3.10-slim

#Set to 1 because we want python emit logs directly to stdout without keeping them in buffer
ENV PYTHONUNBUFFERED 1

# Install base utilities
RUN  apt-get -yq update

#Upgrade pip
RUN pip install --upgrade pip

#Create folder for code and set it as the working directory
RUN mkdir /fampay
WORKDIR /fampay

#Copy project requirements to the code folder
COPY ./requirements.txt /fampay

#Install all requirements
RUN  pip install -r requirements.txt --use-deprecated=legacy-resolver


#Copy project code
COPY . /fampay
