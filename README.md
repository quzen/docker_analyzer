# Contents and requirements
This app contains scripted inputs for Docker stats, top, logs, events collection.
And few dashboards enabling deep analysis of Docker data in a simple yet powerful manner.




# Installation
In order to collect Docker data scripted inputs make use of docker cli.
For this to work splunk user has to be added to docker group (https://docs.docker.com/engine/reference/commandline/cli/)

This app has to be installed in forwarders, indexers and search heads.
Scripted inputs configured to send data to docker index.
