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

Scripted inputs configured to send data to a default index.
No HTTP Event Collector needed. Uses default forwarder to indexer tcp stream.

Create a new index for docker data, example config is in indexes.conf.example.
Configure inputs to send data to the created docker index (index=docker is commented out in inputs.conf)

docker_stats.py script supports --label argument to specify the exact label name to be extracted (ex. --label=maintainer)

# Links
Github repository: https://github.com/quzen/docker_analyzer