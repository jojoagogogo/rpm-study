#
# Cookbook Name:: rpmbuild
# Recipe:: default
#
# Copyright 2013, YOUR_COMPANY_NAME
#
# All rights reserved - Do Not Redistribute
#
[
"rpm-build",
"make",
"gcc",
"autoconf",
"automake"
].each do |name|
  package name do 
    #action :install
    action [:install,:upgrade]
    #version "2.2.20"
  end
end

script "install_rpm-study" do
  interpreter "bash"
  user "root"
  cwd "/tmp"
  code <<-EOH
  rm -Rf /tmp/rpm-study
  git clone https://github.com/jojoagogogo/rpm-study.git
  mv /tmp/rpm-study/source ~/
  mv /tmp/rpm-study/rpmbuild ~/
  EOH
end
