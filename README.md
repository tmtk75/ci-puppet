# README

*NOTE*: Currently this mqy not work well because docker's I/F for ssh port was changed a little. I'll take case of it if I have a time to fix.

This repository provides how to set up CI server with Docker + Jenkins on ububntu 12.04 LTS.

See <http://tmtk75.github.io/2013/09/28/docker-jenkins-serverspec-puppet.ja.html> (ja)


## Set up on MacOS with puppet
To install VirtualBox and Vagrant

    $ bundle install --binstubs --path vendor
    $ sudo ./bin/puppet apply init.pp
