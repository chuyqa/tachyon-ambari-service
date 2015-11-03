#!/usr/bin/config python
from resource_management import *
import commands
import os.path

# config object that holds the configurations declared in the -config.xml file
config = Script.get_config()

# identify archive file
tachyon_archive_file = config['configurations']['tachyon-config']['tachyon.archive.file']

# tachyon master address
tachyon_master = config['configurations']['tachyon-config']['tachyon.master.address']

# tachyon underfs address
underfs_addr = config['configurations']['tachyon-config']['tachyon.underfs.address']

# tachyon worker memory alotment 
worker_mem = config['configurations']['tachyon-config']['tachyon.worker.memory']

# ODP install dir
if os.path.exists("/usr/bin/iop-select"):
  cmd = "/usr/bin/iop-select versions"
  base_dir = "/usr/iop/" + commands.getoutput(cmd) + "/tachyon/"
elif os.path.exists("/usr/bin/hdp-select"):
  cmd = "/usr/bin/hdp-select versions"
  base_dir = "/usr/hdp/" + commands.getoutput(cmd) + "/tachyon/"
else:
  base_dir = "/usr/odp/tachyon/"

# ambari-agent package
tachyon_package_dir = "/var/lib/ambari-agent/cache/stacks/*/*/services/tachyon-service/package/" 

# tachyon log dir
log_dir = config['configurations']['tachyon-env']['tachyon.log.dir']

# tachyon log dir
pid_dir = config['configurations']['tachyon-env']['tachyon.pid.dir']

