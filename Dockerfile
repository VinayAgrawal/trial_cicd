#FROM python:3.8-stretch
FROM alpine:3.16
#ARG BASE_IMAGE=python:3.9-slim
#FROM $BASE_IMAGE as runtime-environment

USER root

#https://github.com/nextcloud/docker/issues/380
RUN mkdir -p /usr/share/man/man1
RUN apt-get update && apt-get install -y apt-transport-https
RUN apt-get install curl pandoc openjdk-8-jdk-headless -y && \
    apt-get clean && update-alternatives --set java /usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java
RUN apt-get install -y python3-pip

COPY src/requirements.txt /tmp/requirements.txt
#COPY src/test_requirements.txt /tmp/test_requirements.txt
#COPY packages/ /tmp/packages/

#ARG ARTIFACTORY_USER
#ARG ARTIFACTORY_PASSWORD

RUN pip3 install -U pip setuptools wheel
RUN #pip3 install /tmp/packages/*
RUN pip3 install -r /tmp/requirements.txt
RUN #pip3 install -r /tmp/test_requirements.txt

