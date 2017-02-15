#### Notes

For me not you.  Unless you care then they are for you too ;-)


Simulate external registry
```
atomic install projectatomic/atomic-registry-install 10.53.252.55
systemctl enable --now atomic-registry-master.service
/var/run/setup-atomic-registry.sh 10.53.252.55
docker exec -it atomic-registry-master bash
oadm ca create-server-cert     --signer-cert=/etc/atomic-registry/master/ca.crt     --signer-key=/etc/atomic-registry/master/ca.key     --signer-serial=/etc/atomic-registry/master/ca.serial.txt     --hostnames='docker-registry.default.svc.cluster.local,172.30.117.177,10.53.252.55'     --cert=/etc/atomic-registry/registry/registry.crt     --key=/etc/atomic-registry/registry/registry.key
oc secrets new registry-secret /etc/atomic-registry/registry/registry.crt /etc/atomic-registry/registry/registry.key
oc secrets link registry registry-secret
oc secrets link default  registry-secret
oc volume dc/docker-registry --add --type=secret     --secret-name=registry-secret -m /etc/secrets
```



If you want to query the openshift api from Jenkins - really this is just for an example not sure why you want to do this.

```
keytool -importcert -v -file /run/secrets/kubernetes.io/serviceaccount/ca.crt -keystore /etc/pki/java/cacerts -alias openshift
```

restart Jenkins - this doesn't work yet, needs auth...
```
oc exec jenkins-4-9x5nq -it -- java -jar ./var/lib/jenkins/war/WEB-INF/jenkins-cli.jar -s http://jenkins restart
```


This is required for the Jenkinsfile below to function properly 
```
<?xml version='1.0' encoding='UTF-8'?>
<scriptApproval plugin="script-security@1.24">
  <approvedScriptHashes/>
  <approvedSignatures>
    <string>method java.net.URL openConnection</string>
    <string>method java.net.URLConnection getContent</string>
    <string>staticMethod org.codehaus.groovy.runtime.DefaultGroovyMethods toURL java.lang.String</string>
  </approvedSignatures>
  <aclApprovedSignatures>
    <string>staticMethod org.codehaus.groovy.runtime.DefaultGroovyMethods toURL java.lang.String</string>
  </aclApprovedSignatures>
  <approvedClasspathEntries/>
  <pendingScripts/>
  <pendingSignatures/>
  <pendingClasspathEntries/>
</scriptApproval>sh-4.2$ 


```


Jenkinsfile
(yeah I can read...don't do this but what is easier adding a plugin or allowing the methods?)
```
node('nodejs') {
  stage('build') {
    openshiftBuild(buildConfig: 'nodejs-mongodb-example', showBuildLogs: 'true')
  }
  stage('deploy') {
    openshiftDeploy(deploymentConfig: 'nodejs-mongodb-example')
  }
  stage('build-ex-reg') {
    openshiftBuild(buildConfig: 'nodejs-mongodb-example-ex-reg', showBuildLogs: 'true')
  }
  stage('rest-api') {
    def address = "https://openshift.default.svc.cluster.local/api/v1"
    def urlInfo = address.toURL()
    def connection = urlInfo.openConnection()
    println "${connection.content}"
  }
}
 ```



Old Way

```
docker login -p ZTStdkOQMiRtM1S3tFH0-gqz5cu4wP1I87NeEj_AKP8 -e unused -u unused 10.53.252.55:5000
oc secrets new container-zone ~/.docker/config.json
oc secrets link builder container-zone
oc set build-secret --push bc/nodejs-mongodb-example-ex-reg container-zone
```
