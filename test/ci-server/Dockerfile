FROM centos

RUN yum install -y passwd
RUN yum install -y openssh
RUN yum install -y openssh-server
RUN yum install -y openssh-clients
RUN yum install -y sudo
RUN yum install -y rsync

# create user
RUN useradd core
RUN passwd -f -u core
RUN mkdir -p /home/core/.ssh; chown core /home/core/.ssh; chmod 700 /home/core/.ssh
ADD ./.ssh/id_rsa.pub /home/core/.ssh/authorized_keys
RUN chown core /home/core/.ssh/authorized_keys; chmod 600 /home/core/.ssh/authorized_keys

# puppet
RUN wget -O puppetlabs-release-6-7.noarch.rpm http://yum.puppetlabs.com/el/6/products/i386/puppetlabs-release-6-7.noarch.rpm
RUN rpm -ivh puppetlabs-release-6-7.noarch.rpm
RUN yum install puppet -y

# Enable ssh login for CoreOS
ADD ./etc-pam.d-sshd /etc/pam.d/sshd

# Disable `Defaults    requiretty`
ADD ./etc-sudoers /etc/sudoers
RUN chown root.root /etc/sudoers; chmod 600 /etc/sudoers

# setup sudoers
RUN echo "core    ALL=(ALL)       ALL" >> /etc/sudoers.d/core

# setup sshd and generate ssh-keys by init script
#ADD ./sshd_config /etc/ssh/sshd_config
RUN /etc/init.d/sshd start
RUN /etc/init.d/sshd stop

# expose sshd port
EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]
