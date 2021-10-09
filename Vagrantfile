Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/bionic64"
  config.disksize.size = '15GB'
  config.vm.network "private_network", ip: "192.168.33.107"
  config.vm.provider "virtualbox" do |vb|
	  vb.memory=4096
  end
  config.vm.provision :docker
  config.vm.provision :docker_compose, yml: "/vagrant/docker-compose.yml", run: "always" 
end