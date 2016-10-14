#!/usr/bin/env python

import re
import os
import sys
import subprocess
import json
import pprint

hosts = {}
groups = {}

regions = ["ap-southeast-2"]

def add_instances(region):
    output = subprocess.check_output("aws --region={} ec2 describe-instances".format(region), shell=True)
    reservations = json.loads(output)

    for reservation in reservations ['Reservations']:
        for instance in reservation['Instances']:
            tags = set()
            hostname = ""
            if instance['State']['Name'] != 'running':
                continue
#            pprint.pprint(instance)
            for x in instance['Tags']:
                if x['Key'] == 'hostname':
                    hostname = x['Value']
                    continue
                if x['Key'] in ('tags','tags2'):
                    tags.update(x['Value'].split(','))
                    continue
            if 'InstanceLifecycle' in instance and instance['InstanceLifecycle'] == 'spot':
                tags.update(["spotinstances"])

            if not hostname:
                print "You forgot to name instance {}, fix this!".format(reservation['ReservationId'])
                sys.exit(1)
            if not tags:
                print "You forgot to tag instance {}, fix this!".format(hostname)
                sys.exit(1)

            if 'no-ansible' in tags:
                continue

            hosts[hostname] = {'private_ip': instance['PrivateIpAddress'],'ansible_ssh_host': instance['PublicIpAddress']}

            for metadata in instance.get('Tags', []):
                if metadata['Key'].startswith('ansible_'):
                    key = metadata['Key'][len('ansible_'):]
                    hosts[hostname][key] = metadata['Value']

            for tag in tags:
                groups.setdefault(tag, []).append(hostname)

for region in regions:
    add_instances(region)

output = open(os.path.join(os.path.dirname(__file__), '../inventory/hosts_aws'), 'w')

print >>output, "[aws]"
for host, vars in sorted(hosts.items()):
    vars_str = " ".join("{}={}".format(*item) for item in sorted(vars.items()))
    print >>output, "{host} {vars}".format(host=host, vars=vars_str)

for group, hosts in sorted(groups.items()):
    print >>output
    print >>output, "[{group}]".format(group=group)
    for host in sorted(hosts):
        print >>output, host
