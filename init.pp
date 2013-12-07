class virtualbox {
  exec { 'Kill Virtual Box Processes':
    command     => 'pkill "VBoxXPCOMIPCD" || true && pkill "VBoxSVC" || true && pkill "VBoxHeadless" || true',
    path        => '/usr/bin:/usr/sbin:/bin:/usr/local/bin',
    refreshonly => true,
  }

  package { 'VirtualBox-4.3.4-91027-OSX.dmg':
    ensure   => installed,
    provider => 'pkgdmg',
    source   => 'http://download.virtualbox.org/virtualbox/4.3.4/VirtualBox-4.3.4-91027-OSX.dmg',
    require  => Exec['Kill Virtual Box Processes'],
  }
}

class vagrant {
  package { 'Vagrant.1.3.5.dmg':
    ensure   => installed,
    source   => 'http://files.vagrantup.com/packages/a40522f5fabccb9ddabad03d836e120ff5d14093/Vagrant-1.3.5.dmg',
    provider => 'pkgdmg'
  }
}

include virtualbox
include vagrant
