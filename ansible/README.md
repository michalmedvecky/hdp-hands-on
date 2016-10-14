# Ansible - HDP

This library of ansible playbooks and roles makes setup of HortonWorks HDP on RHEL 7.2 less painful.

It yet supports only setup of HDFS with HA namenode (journal quorum, zkfc) and Zookeeper.

## What does it not do
* Playbooks don't care about the storage for HDFS. If you want to create HDFS storage space, you should run datanode instances on d2 instances (with local drives). Don't forget to place (at least datanode) instances in the same placement group. Depending on your load, you should use machines with better networking
* Playbooks do not test your installation, you should do this by yourselfA
* No support for other distributions, no check for the distro - you have to be sure where are you installing (or rely on `create.yml` playbook)

## What will you need

### Client side

- Some recent Ubuntu machine (or anything else to run Ansible)
- `apt-get install awscli`
- setup awscli (`awscli configure`)
- install ansible >2.1 `pip install ansible` (do not pick the ubuntu package, it's outdated)

### Server (or Cloud?) side
* Credentials for AWS
* pre-generate ssh key for deployment in AWS console or CLI

## Deployment

    export AWS_ACCESS_KEY_ID=<Your aws credentials>
    export AWS_SECRET_ACCESS_KEY=<Your aws credentials>
OR
    awscli configure

Provision instances:
    ansible-playbook create.yml

Update ansible inventory file:
    scripts/update_inventory.py

Run ssh-agent and add your private key
    eval `ssh-agent`
    ssh-add /path/to/your/private-key.pem

Deploy the cluster
    ansible-playbook -i inventory/hosts_aws hdp.yml -u ec2-user -e hdfs_force_format=yes

## How to test

### hdfs

This command returns df -h for hdfs:

    `hdfs dfs -df -h`

If you see zeroes or questionmarks, something is wrong.

## Logs

Logs of your installations can be found in:
* `/var/log/hdfs/`
* `/var/log/zookeeper`

## Problems
* `hdfs zkfc -format` in combination with Ansible eats all memory and playbook fails, but not always.
* systemd unit files are too lame, if the service fails when starting, Ansible does not know about this
* Playbooks use shell command `yum install -y hadoop-*` instead of the Yum module (commented out), because when using Yum module, it complains that packages do not exist (even if they do..)

## Things that can be improved but I can't
* I have no idea how to merge the two tasks in create.yml into one, because of different tags (zookeeper id)

