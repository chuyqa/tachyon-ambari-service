#import status properties defined in -env.xml file from status_params class
import sys, os, pwd, signal, time
from resource_management import *
from resource_management.core.base import Fail
from resource_management.core.exceptions import ComponentIsNotRunning
from subprocess import call
import cPickle as pickle

class Master(Script):

  #Call setup.sh to install the service
  def install(self, env):
  
    import params
    # Install packages listed in metainfo.xml
    self.install_packages(env)

    # Create the base_dir/tachyon dir
    cmd = '/bin/mkdir' + ' -p ' + params.base_dir 
    Execute('echo "Running ' + cmd + '"')
    Execute(cmd)

    #extract archive and symlink dirs
    cmd = '/bin/tar' + ' -zxf ' + params.tachyon_package_dir + 'files/' +  params.tachyon_archive_file + ' --strip 1 -C ' + params.base_dir
    Execute('echo "Running ' + cmd + '"')
    Execute(cmd)

    cmd = '/bin/ln' + ' -s ' + params.base_dir + ' ' + params.usr_base + 'current/tachyon'
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
	  mode=0700,
          content=Template('tachyon-env.sh.j2', conf_dir=tachyon_config_dir)
    )

    File(format("{tachyon_libexec_dir}/tachyon-config.sh"),
          owner='root',
          group='root',
	  mode=0700,
          content=Template('tachyon-config.sh.j2', conf_dir=tachyon_libexec_dir)
    )


  #Call start.sh to start the service
  def start(self, env):
    import params
    
    #call format
    cmd = params.base_dir + '/bin/tachyon ' + 'format'
      
    Execute('echo "Running cmd: ' + cmd + '"')    
    Execute(cmd)
    
    #execute the startup script
    cmd = params.base_dir + '/bin/tachyon-start.sh ' + 'master'
      
    Execute('echo "Running cmd: ' + cmd + '"')    
    Execute(cmd)
    
    #mount ramfs local to master service
    cmd = params.base_dir + '/bin/tachyon-start.sh ' + 'worker' + ' Mount'
      
    Execute('echo "Running cmd: ' + cmd + '"')    
    Execute(cmd)

    # Create pid file - note check_process_status expects a SINGLE int in the file
    cmd = "mkdir -p " + params.pid_dir
    cmd = "echo `ps -A -o pid,command | grep -i \"[j]ava\" | grep TachyonMaster | awk '{print $1}'`> " + params.pid_dir + "/tachyon.pid"
    Execute(cmd)
    pid_file = format("{params.pid_dir}/tachyon.pid")

  #Called to stop the service using tachyon provided stop
  def stop(self, env):
    import params
    
    #execure the startup script
    cmd = params.base_dir + '/bin/tachyon-stop.sh'
      
    Execute('echo "Running cmd: ' + cmd + '"')    
    Execute(cmd)
      	
  #Called to get status of the service using the pidfile
  def status(self, env):
    import params
    
    pid_file = format("{params.pid_dir}/tachyon.pid")
    check_process_status(pid_file)    

if __name__ == "__main__":
  Master().execute()
