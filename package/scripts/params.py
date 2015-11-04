#!/usr/bin/config python
from resource_management import *
from resource_management.libraries.functions.default import default
from resource_management.libraries.functions.version import compare_versions, format_hdp_stack_version
from resource_management.libraries.functions.format import format

import commands
import os.path

# config object that holds the configurations declared in the -config.xml file
config = Script.get_config()
tmp_dir = Script.get_tmp_dir()

# identify archive file
tachyon_archive_file = config['configurations']['tachyon-config']['tachyon.archive.file']

# tachyon master address
tachyon_master = config['configurations']['tachyon-config']['tachyon.master.address']

# tachyon underfs address
underfs_addr = config['configurations']['tachyon-config']['tachyon.underfs.address']

# tachyon worker memory alotment 
worker_mem = config['configurations']['tachyon-config']['tachyon.worker.memory']

# Find current stack and version to push agent files to
stack_name = default("/hostLevelParams/stack_name", None)
stack_version = format_hdp_stack_version(default("/commandParams/version", None))


# ODP install dir
# *Temporary* for now as nobigtop build for tachyon RPM
if os.path.exists("/usr/bin/iop-select"):
  cmd = "/usr/bin/iop-select versions"
  usr_base = "/usr/iop/"
  base_dir = usr_base + commands.getoutput(cmd) + "/tachyon/"
  tachyon_package_dir = "/var/lib/ambari-agent/cache/stacks/" + stack_name + "/" + stack_version[:3] + "/services/TACHYON/package/"
elif os.path.exists("/usr/bin/hdp-select"):
  cmd = "/usr/bin/hdp-select versions"
  usr_base = "/usr/hdp/"
  base_dir = usr_base + commands.getoutput(cmd) + "/tachyon/"
  tachyon_package_dir = "/var/lib/ambari-agent/cache/stacks/" + stack_name + "/" + stack_version + "/services/TACHYON/package/"
else:
  base_dir = "/usr/odp/tachyon/"
  tachyon_package_dir = "/var/lib/ambari-agent/cache/stacks/" + stack_name + "/" + stack_version + "/services/tachyon-service/package/"
  

# tachyon log dir
log_dir = config['configurations']['tachyon-env']['tachyon.log.dir']

# tachyon log dir
pid_dir = config['configurations']['tachyon-env']['tachyon.pid.dir']

