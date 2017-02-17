FROM registry.access.redhat.com/rhel7


RUN INSTALL_PKGS="skopeo" && \
    yum install -y --disablerepo "*" \
                   --enablerepo rhel-7-server-rpms,rhel-7-server-optional-rpms,rhel-7-server-extras-rpms \
                   --setopt=tsflags=nodocs $INSTALL_PKGS && \
    rpm -V $INSTALL_PKGS && \
    yum clean all -y

RUN chown -R 1001:0 $HOME && \
    chmod -R g+rw $HOME

USER 1001

CMD ["tail -f /dev/null"] 
