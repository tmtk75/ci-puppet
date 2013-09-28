import os
import re
from fabric.api import env, run, put, sudo, runs_once, task, execute

@task
def prepare_dirs():
  ## Link to ephemeral disk
  # for docker
  sudo("mkdir -p /mnt/var/lib/docker")
  sudo("ln -sf /mnt/var/lib/docker /var/lib/docker")
  # for jenkins
  sudo("mkdir -p /mnt/var/lib/jenkins")
  sudo("ln -sf /mnt/var/lib/jenkins /var/lib/jenkins")

@task
def install_docker():
  sudo("curl http://get.docker.io | sh")
  put("etc-init-dockerd.conf", "etc-init-dockerd.conf")
  sudo("mv etc-init-dockerd.conf /etc/init/dockerd.conf")
  sudo("stop dockerd")
  sudo("start dockerd")

@task
def ssh_keygen():
  run("ssh-keygen -t rsa -q -P '' -f ~/.ssh/id_rsa")

@task
def docker_build():
  put("Dockerfile", "Dockerfile")
  put("etc-pam.d-sshd", "etc-pam.d-sshd")
  put("etc-sudoers", "etc-sudoers")
  sudo("docker build -t core/sshd .")

@task
def install_jenkins():
  # jenkins
  sudo("wget -q -O - http://pkg.jenkins-ci.org/debian/jenkins-ci.org.key | sudo apt-key add -")
  sudo("echo deb http://pkg.jenkins-ci.org/debian binary/ >> /etc/apt/sources.list")
  sudo("aptitude update")
  sudo("aptitude install -y jenkins")
  sudo("apt-get install ttf-dejavu")  # to visualize junit results.xml

@task
def packages():
  sudo("apt-get remove -y ruby1.8")
  sudo("apt-get install -y git")
  sudo("apt-get install -y ruby1.9.1")
  sudo("gem install rake serverspec builder --no-ri --no-rdoc")
  execute(install_jenkins)

@task
def ssh_config():
  put("ssh-config", ".ssh/config")
  put("%s/.ssh/id_rsa" % os.environ['HOME'], ".ssh/github.pem") # expected ~/.ssh/id_rsa is registered in github
  run("chmod 600 .ssh/github.pem")

  sudo("mkdir -p /var/lib/jenkins/.ssh")
  sudo("cp .ssh/* /var/lib/jenkins/.ssh")
  sudo("chown jenkins.nogroup /var/lib/jenkins/.ssh/*")
  sudo("echo 'jenkins ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers")

@task
def setup():
  execute("prepare_dirs")
  execute("install_docker")
  execute("ssh_keygen")
  execute("docker_build")
  execute("packages")
  execute("ssh_config")

