# Ansible - HDP

This library of ansible playbooks and roles makes setup of HortonWorks HDP on RHEL 7.2 less painful.

It yet supports only setup of HDFS with HA namenode (journal quorum, zkfc) and Zookeeper.

## What does it not do
* Playbooks don't care about the storage for HDFS. If you want to create HDFS storage space, you should run datanode instances on d2 instances (with local drives). Don't forget to place (at least datanode) instances in the same placement group. Depending on your load, you should use machines with better networking
* Playbooks do not test your installation, you should do this by yourself
* No support for other distributions, no check for the distro - you have to be sure where are you installing (or rely on `create.yml` playbook)
* Machine types are just ones that "can do the install". Not modelled for any kind of load (e.g. namenodes have to be sized with HDFS in mind, kafka should have plenty of RAM, Yarn nodemanagers should provide much more memory than 2G (sooo much memory for Tez required!), storm nodes are advised to have 24GB ram ...)
* Kafka does not have any storage different than the system partition. In production, it should have it's own ext3 partition for the state storage.
* playbooks do not tune ulimits
* storm local dir is in on root partition as well
* Centralized logging (one should probably use some cloud logging service)
* Remove machines or clusters (just deployment is supported), you have to delete machines yourself 

## What will you need

### Client side

- Some recent Ubuntu machine, preferrably (or anything else to run Ansible)
- `apt-get install awscli`
- setup awscli (`awscli configure`)
- install ansible >2.1 `pip install ansible` (do not pick the ubuntu package, it's outdated)

### Server (or Cloud?) side
* Credentials for AWS
- edit `group_vars/all/aws.yml` to adjust your AWS parameters (self-explanatory)
* Credentials for AWS
* Create EC2 placement group in the desired region (EC2 dashboard -> Placement Groups -> Create Placement Group - not supported by Ansible). If you want to use placement groups, you should read those limitations: http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/placement-groups.html)
* pre-generate ssh key for deployment in AWS console or CLI, and save it to some good place

## Deployment

    export AWS_ACCESS_KEY_ID=<Your aws credentials>
    export AWS_SECRET_ACCESS_KEY=<Your aws credentials>
OR
    awscli configure

Provision instances:
    ansible-playbook create.yml

Update ansible inventory file: (not necessary for `create-docker.yml` playbook)
    scripts/update_inventory.py

Run ssh-agent and add your private key
    eval `ssh-agent`
    ssh-add /path/to/your/private-key.pem

Deploy the cluster
    ansible-playbook -i inventory/hosts_aws hdp.yml -u ec2-user -e hdfs_force_format=yes

IMPORTANT! First (successfull) run has to go with `-e hdfs_force_format=yes`, otherwise the cluster will not work AT ALL.
All other runs should be run WITHOUT this parameter.
 
## Tags

When provisioning new nodes with this playbook, tags have following meanings:
* `zookeeper` - machine will run ZK instance. You have to specify `ansible_zookeeper_server_id=<unique number 0..255>"` as well.
* `hdfs` - machine will be able to access HDFS (but not serving the datanode)
* `hdfs-namenode` - will run the namenode (only HA state is supported by the playbook). Exactly 2 machines have to be specified among the cluster.
* `hdfs-journalnode` - will run the journalnode (required for HA). At least 3 machines must be specified.
* `yarn-resourcemanager` - installs Yarn resourcemanager
* `mapred` - configures mapred
* `mapred-historyserver` - configures and starts mapred history server
* `yarn-nodemanager` - installs and configures yarn nodemanager
* `hdfs-datanode` - installs and configures hdfs datanode
* `kafka` - kafka brokers, You have to specify `ansible_kafka_broker_id=<unique number 0..255>` as well.
* `storm-nimbus` - installs storm nimbus, ui, drpc, logviewer
* `storm-supervisor` - installs storm slaves
* `tez` - installs tez (=copy to hdfs) and configures tez for any machine from where it should be used

### Example

Provision Yarn only with:
    ansible-playbook hdp.yml -u ec2-user --tags yarn -i inventory/hosts_aws

## How to test

### hdfs

This command returns df -h for hdfs:

    `hdfs dfs -df -h`

If you see zeroes or questionmarks, something is wrong.

### Tez

http://docs.hortonworks.com/HDPDocuments/HDP2/HDP-2.3.0/bk_installing_manually_book/content/ref-1a378094-a4fb-4348-bd9e-2eebf68c2e1e.1.html

### Mapred

http://docs.hortonworks.com/HDPDocuments/HDP2/HDP-2.3.0/bk_installing_manually_book/content/smoke_test_mapreduce.html

... and so on (out of scope)

## Logs

Logs of your installations can be found in:
* `/var/log/hdfs/`
* `/var/log/zookeeper`
* `/var/log/storm`
* `/var/log/yarn`
* `/var/log...`

## Problems
* `hdfs zkfc -format` in combination with Ansible eats all memory and playbook sometimes fails.
* systemd unit files are too lame, if the service fails when starting, Ansible does not know about this
* Playbooks use shell command `yum install -y hadoop-*` instead of the Yum module (commented out), because when using Yum module, it complains that packages do not exist (even if they do..)
* Ansible 2.2 will be a good improvement for this playbook, as it contains nice new modules (and fixes those bus mentioned)
* ssh fencing for namenodes is untested. I just don't have energy within the time limit.

## Things that can be improved but I can't
* I have no idea how to merge the two tasks in create.yml into one, because of different tags (zookeeper id)
* Init scripts could be better
