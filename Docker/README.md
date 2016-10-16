# Docker assignment

## Release notes
* tested with ansible 2.1.2.0. 
* There is one (https://github.com/ansible/ansible/issues/17495|bug) in Ansible 2.1 that prevents docker build module from working. Workaround included in the playbook.
* There is no module for docker networking in ansible <2.2. Workaround included.

# 2. Separately from 1. create EC2 instance with Docker environment with:

More info on how to get ansible up and running can be found in ansible-library README.

* `ansible-playbook create-docker.yml`
* `script/update_inventory.py`
* install python to newly created instance: `ssh ubuntu@<instance-ip> sudo apt-get install python`
* `ansible-playbook docker.yml -i inventory/hosts_aws -u ubuntu`
* ssh to the newly created instance (`ssh ubuntu@<instance-ip>`)

The playbook is not mine, it's googled and taken from Github page (link in the role)
   
## a) Apache Kafka with 2 brokers (running in 2 different containers) and persistent storage

### Run

* `git clone https://gitlab.vipdmp.com/devops/michal-hands-on-test code && cd code`
* `sh start.sh`

### What it does

* Builds a new image called `misko/kafka`, built from `spotify/kafka`, extending it to run in multiple containers
* stops all running containers named `kafka{1,2,3}`
* creates a docker network kafkanet
* start 3 instances of kafka (accessible via container IPs only)

## b) Monitoring system with metrics for host, containers and Kafka brokers.

TBD
