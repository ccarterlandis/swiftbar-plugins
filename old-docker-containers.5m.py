#!/usr/bin/python3

# <bitbar.title>Long-running Docker containers</bitbar.title>
# <bitbar.version>v1.0</bitbar.version>
# <bitbar.author>Carter Landis</bitbar.author>
# <bitbar.author.github>ccarterlandis</bitbar.author.github>
# <bitbar.desc>Notifies you when you have any Docker containers that have been running for more than 8 hours.</bitbar.desc>
# <bitbar.image>http://www.hosted-somewhere/pluginimage</bitbar.image>
# <bitbar.dependencies>python3,docker</bitbar.dependencies>

have_long_running_containers = False

import subprocess

running_containers = [container for container in subprocess.run("docker container ls -a --filter status=running --format '{{.Names}} -- {{.RunningFor}}'", capture_output=True, text=True, shell=True).stdout.split('\n') if container != '']

for container in running_containers:
    if container.split(' -- ')[1] == 'About an hour ago':
        # I can't believe this is necessary. Is it really so hard to just put "1 hour ago" and be consistent?
        running_for = '1 hour'
    else:
        running_for = container.split(' -- ')[1].replace('ago', '').split(' ')

    # anything that's not seconds or minutes (only options are hours, days, weeks, months, and years), so any value of those over 8 is too long
        if running_for[1] not in ['seconds', 'minutes'] and int(running_for[0]) >= 8:
            have_long_running_containers = True
            break

if have_long_running_containers:
    print("🐋❗️")
elif not have_long_running_containers and running_containers != []:
    print("🐋")
else:
    print("🐋🚫")

print("---------------")
if running_containers != []:
    for container in running_containers:
        print(container)

