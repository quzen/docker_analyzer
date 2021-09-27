# Contents
This Splunk app contains scripted inputs for Docker stats, top, logs, events collection.
It enables complete Docker monitoring using all in one solution: data collection, storage and visualization.
Few Splunk dashboards allow deep analysis of Docker data in a simple yet powerful way.

# Requirements
In order to collect Docker data, scripted inputs make use of docker cli.
For this to work splunk user has to be added to docker group (https://docs.docker.com/engine/reference/commandline/cli/)

# Installation
This app has to be installed on:
* forwarders (scripted inputs)
* indexers (field extractions and docker index creation)
* search heads (dashboards)

Scripted inputs configured to send data to docker index.

# Links
Github repository: https://github.com/quzen/docker_analyzer