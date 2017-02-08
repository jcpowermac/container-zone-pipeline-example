# container-zone-pipeline-example


```
docker login -p ZTStdkOQMiRtM1S3tFH0-gqz5cu4wP1I87NeEj_AKP8 -e unused -u unused 10.53.252.55:5000
oc secrets new container-zone ~/.docker/config.json
oc secrets link builder container-zone
oc set build-secret --push bc/nodejs-mongodb-example-ex-reg container-zone
```
