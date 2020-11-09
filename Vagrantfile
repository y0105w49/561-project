#!/usr/bin/env ruby


# based on https://github.com/booyaa/vagrant-bcctools
Vagrant.configure("2") do |config|
  config.vm.box = "hashicorp/bionic64"
  config.vm.box_version = "1.0.282"
  config.vm.provision :shell, :privileged => false, :inline => "sudo apt-get update && sudo apt-get install -y bpfcc-tools python3-bpfcc \"linux-headers-$(uname -r)\""
end
