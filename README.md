## Tachyon Service for Ambari

Service definition for Tachyon v 0.8.0 - Deploys on IOP 4.1 and HDP 2.3


Install, start/stop service functional

**Installing in IOP 4.1**
```
# Clone the service deployer
git clone https://github.com/chuyqa/tachyon-ambari-service /var/lib/ambari-server/resources/stacks/BigInsights/4.1/services/TACHYON

ambari-server restart

```

**Installing in HDP 2.3**

```
# Clone the service deployer
git clone https://github.com/chuyqa/tachyon-ambari-service /var/lib/ambari-server/resources/stacks/HDP/2.3/services/TACHYON

ambari-server restart

```



* Add service via ambari ui 

* Select a master server node and worker nodes 

* Update required tachyon-config:

    tachyon.master.address = Hostname of Tachyon master selected 
    tachyon.underfs.address = hdfs://namenode:8020

* tachyon.worker.memory = Specifiy how much memory to allocate to each tachyon worker master/worker


Once Service is started, you may access Tachyon Master on ***tachyon.master.ip*:19999**

**Future Work:**

Alerts.json

Kerberos.json

Status Check via Ambari

Parse tachyon.underfs.address from HDFS Advanced core-site: fs.defaultFS 


Inspried from outdated fork: https://github.com/seraphin/tachyon-service
