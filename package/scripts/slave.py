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
    
    #mount ramfs
    cmd = params.base_dir + '/bin/tachyon-start.sh ' + 'worker' + ' Mount'
      
    Execute('echo "Running cmd: ' + cmd + '"')    
    Execute(cmd)

  #Called to stop the service using the pidfile
  def stop(self, env):
    import params
    
    #execure the startup script
    cmd = params.base_dir + '/bin/tachyon-stop.sh'
      
    Execute('echo "Running cmd: ' + cmd + '"')    
    Execute(cmd)
      	
  #Called to get status of the service using the pidfile
  def status(self, env):
    import params
  
    #call status
    cmd = params.base_dir + '/bin/tachyon status slave'

    try:
      Execute(cmd)
    except Fail:
      raise ComponentIsNotRunning()


if __name__ == "__main__":
  Slave().execute()
