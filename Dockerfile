FROM registry.access.redhat.com/rhel7

ENV HOME=/home/skopeo

RUN INSTALL_PKGS="skopeo atomic-openshift-clients" && \
    yum install -y --disablerepo "*" \
                   --enablerepo rhel-7-server-rpms,rhel-7-server-optional-rpms,rhel-7-server-extras-rpms,rhel-7-server-ose-3.4-rpms \
                   --setopt=tsflags=nodocs $INSTALL_PKGS && \
    rpm -V $INSTALL_PKGS && \
    yum clean all -y

RUN mkdir $HOME && \
    chown -R 1001:0 $HOME && \
    chmod -R g+rw $HOME

USER 1001

CMD tail -f /dev/null 
