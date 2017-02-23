## Container Zone Example


This project provides a simple example how to use Red Hat's ISV Container Zone with OpenShift.


### Quick Start

Create a secret for the container zone.
```
oc secrets new-dockercfg container-zone --docker-email='' --docker-password='[registry key here]' --docker-username='[rh user account' --docker-server='[registry]'
```

#### Existing project
The `create-buildconfig.py` script will take an existing BuildConfig and output two new BuildConfigs - one for Jenkins Pipeline and the other for outputting to a external registry.
```
oc export buildconfig demo | ./create-buildconfig.py -f - --buildconfig demo-ex-reg --pushsecret container-zone --docker 10.53.252.55:5000/jcallen/demo | oc create -f -
```

#### New project
Use the example template.yaml to configure a BuildConfig appropriate for your configuration.
