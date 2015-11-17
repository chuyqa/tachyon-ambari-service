## Tachyon Service for Ambari

Service definition for Tachyon v 0.8.0 - Deploys on IOP 4.1 and HDP 2.3


Install, start/stop, status, service check functional


**1. Clone the service into the dir for the Stack you are running in Ambari**

**- Adding tachyon to IOP 4.1 stack**
```
# Clone the service deployer
git clone https://github.com/chuyqa/tachyon-ambari-service /var/lib/ambari-server/resources/stacks/BigInsights/4.1/services/TACHYON

ambari-server restart

```

**- Adding tachyon to HDP 2.3 stack**

```
# Clone the service deployer
git clone https://github.com/chuyqa/tachyon-ambari-service /var/lib/ambari-server/resources/stacks/HDP/2.3/services/TACHYON

ambari-server restart

```


**2. Add service via ambari ui**

**3. Assign a Tachyon Master And Worker nodes.**
By default the master will also run a worker 


Once Service is started, you may access Tachyon Master Web UI on ***tachyon.master.hostname*:19999**

**Future Work:**

Alerts.json

Kerberos.json

Parse tachyon.underfs.address from HDFS Advanced core-site: fs.defaultFS 

Inspried from outdated fork: https://github.com/seraphin/tachyon-service
