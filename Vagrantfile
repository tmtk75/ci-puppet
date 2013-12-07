$provision = <<-EOH
  sudo yum install -y http://ftp.riken.jp/Linux/fedora/epel/6/i386/epel-release-6-8.noarch.rpm
  sudo yum install -y docker-io
EOH

Vagrant.configure("2") do |conf|
  conf.vm.box     = "centos-6.4-x86_64"
  conf.vm.box_url = "http://developer.nrel.gov/downloads/vagrant-boxes/CentOS-6.4-x86_64-v20130427.box"
  conf.vm.synced_folder "manifests", "/etc/puppet/manifests", :owner => 'root', :group => 'root'
  conf.vm.synced_folder "modules",   "/etc/puppet/modules",   :owner => 'root', :group => 'root'
  conf.vm.provision :shell, :inline => $provision
end
