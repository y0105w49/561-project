#!/usr/bin/env ruby


# based on https://github.com/booyaa/vagrant-bcctools
Vagrant.configure("2") do |config|
  config.vm.box = "hashicorp/bionic64"
  config.vm.provision :shell, :privileged => false, :path => "install.sh"
end
