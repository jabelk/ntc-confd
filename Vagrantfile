# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  # General Vagrant VM configuration.
  config.vm.box = "bento/ubuntu-18.04"
  #config.ssh.insert_key = false
  config.vm.synced_folder ".", "/vagrant", disabled: true
  config.vm.synced_folder "~/ntc-data", "/ntc-data", create: true
  config.vm.network "forwarded_port", guest: 80, host: 8086, auto_correct: true
  config.vm.network "forwarded_port", guest: 443, host: 8446, auto_correct: true
  config.vm.network "forwarded_port", guest: 4000, host: 4006, auto_correct: true
  config.vm.network "forwarded_port", guest: 5000, host: 5006, auto_correct: true
  config.vm.network "forwarded_port", guest: 8000, host: 8006, auto_correct: true
  config.vm.provider :virtualbox do |v|
    v.memory = 2096
    # will use same base image to copy to others
    v.linked_clone = true
  end

  # confd server 1.
  config.vm.define "confd" do |confd|
    confd.vm.hostname = "confd.test"
    confd.vm.network :private_network, ip: "192.168.60.4"
  end

  # ansible server 2.
  config.vm.define "configengine" do |configengine|
    configengine.vm.hostname = "configengine.test"
    configengine.vm.network :private_network, ip: "192.168.60.5"
  end


    # Ansible provisioner.
  config.vm.provision :ansible do |ansible|
    ansible.playbook = "playbook.yml"
    ansible.become = true
  end
end
