# Docker assignment

## Release notes
* tested with ansible 2.1.2.0.
* There is one (https://github.com/ansible/ansible/issues/17495|bug) in Ansible 2.1 that prevents docker build module from working. Workaround included in the playbook.
* There is no module for docker networking in ansible <2.2. Workaround included.

# 2. Separately from 1. create EC2 instance with Docker environment with:

More info on how to get ansible up and running can be found in ansible-library README (the most important task here is to make SSH key being forwarded)

* `ansible-playbook create-docker.yml -u ubuntu`

The Docker role is not mine, it's googled and taken from Github page (link in the role)

## a) Apache Kafka with 2 brokers (running in 2 different containers) and persistent storage

### Run

Kafka containers are build from `spotify/kafka`, a functional single-container Kafka broker. I just added support for multiple zookeepers and unique `broker.id`s.

I used 3 containers, because Zookeeper refuses to work in HA mode with 2 brokers (because of possible split-brain situation).

I run 3 ZKs and 3 Kafka brokers.

### What the playbook does

* Builds a new image called `misko/kafka`, derived from `spotify/kafka`, extending it to run in multiple containers
* creates a docker network kafkanet
* start 3 instances of kafka (accessible via container IPs only)

## b) Monitoring system with metrics for host, containers and Kafka brokers.

TBD
~
