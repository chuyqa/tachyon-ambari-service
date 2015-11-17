#import status properties defined in -env.xml file from status_params class

import sys, os, pwd, signal, time
from resource_management import *
from resource_management.core.base import Fail
from resource_management.core.exceptions import ComponentIsNotRunning
from subprocess import call
import cPickle as pickle

class Slave(Script):

  #Call setup.sh to install the service
  def install(self, env):
    import params
  
    # Install packages listed in metainfo.xml
    self.install_packages(env)

    # Create the base_dir/tachyon dir
    cmd = '/bin/mkdir' + ' -p ' + params.base_dir
    Execute('echo "Running ' + cmd + '"')
    Execute(cmd)

    cmd = '/bin/tar' + ' -zxf ' + params.tachyon_package_dir + 'files/' +  params.tachyon_archive_file + ' --strip 1 -C ' + params.base_dir
    Execute('echo "Running ' + cmd + '"')
    Execute(cmd)
   
    #hackyy for now, should be resolved via conf-select/iop-select/hdp-select if rpm is avail     
    cmd = '/bin/ln' + ' -s ' + params.base_dir  + ' ' + params.usr_base + 'current/'
    Execute('echo "Running ' + cmd + '"')
   
    try:
      Execute(cmd)
    except:
      pass

    self.configure(env)

  def configure(self, env):
    import params
    env.set_params(params)

    tachyon_config_dir = params.base_dir + '/conf/'
    tachyon_libexec_dir = params.base_dir + '/libexec/'

    File(format("{tachyon_config_dir}/tachyon-env.sh"),
          owner='root',
          group='root',
          content=Template('tachyon-env.sh.j2', conf_dir=tachyon_config_dir)
    )

    File(format("{tachyon_libexec_dir}/tachyon-config.sh"),
          owner='root',
          group='root',
          content=Template('tachyon-config.sh.j2', conf_dir=tachyon_libexec_dir)
    )
  #Call start.sh to start the service
  def start(self, env):
    import params
    
    #Mount ramfs
    cmd = params.base_dir + '/bin/tachyon-start.sh ' + 'worker' + ' Mount'
    
    Execute('echo "Running cmd: ' + cmd + '"')    
    Execute(cmd)

    # Create pid file - note check_process_status expects a SINGLE int in the file
    cmd = "mkdir -p " + params.pid_dir
    cmd = "echo `ps -A -o pid,command | grep -i \"[j]ava\" | grep TachyonWorker | awk '{print $1}'`> " + params.pid_dir + "/TachyonWorker.pid"
    Execute(cmd)
    pid_file = format("{params.pid_dir}/TachyonWorker.pid")


  #Called to stop the service using the pidfile
  def stop(self, env):
    import params
    
    #execure the startup script
    cmd = params.base_dir + '/bin/tachyon-stop.sh'
      
    Execute('echo "Running cmd: ' + cmd + '"')    
    Execute(cmd)
      	
  #Check pid file using Ambari check_process_status
  def status(self, env):
    import params
    
    pid_file = format("{params.pid_dir}/TachyonWorker.pid")
    check_process_status(pid_file)   


if __name__ == "__main__":
  Slave().execute()
