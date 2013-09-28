require 'serverspec'
require 'pathname'
require 'net/ssh'
require 'json'

include Serverspec::Helper::DetectOS


def vagrant_ssh_config(site)
  opts = {}
  config = `vagrant ssh-config #{site}`
  config.each_line do |line|
    if match = /IdentityFile (.*)/.match(line)
      opts[:keys] =  [match[1].gsub(/"/,'')]
    elsif match = /Port (.*)/.match(line)
      opts[:port] = match[1]
    end
  end
  opts
end

case ENV['TEST_TARGET']
when 'local'
  include Serverspec::Helper::Exec
  # Nothing to configure

when 'docker'
  include Serverspec::Helper::Ssh
  require "json"
  require "net/http"
  require "uri"
  RSpec.configure do |c|
    c.before :all do
      host = "localhost"
      user = "core"
      opts = {}
      opts[:keys] = ["#{ENV['HOME']}/.ssh/id_rsa"]
      if ENV['CONTAINER_ID']
        uri = URI.parse "http://localhost:4243/v1.4/containers/#{ENV['CONTAINER_ID']}/json"
        opts[:port] = (JSON.parse Net::HTTP.get uri)["NetworkSettings"]["PortMapping"]["Tcp"]["22"]
      else
        opts[:port] = ENV['SSH_PORT']
      end
      raise "SSH_PORT is empty. e.g) export SSH_PORT=49153 or CONTAINER_ID=ed9c8138da13" if opts[:port] == nil or opts[:port] == ""
      c.ssh.close if c.ssh
      c.ssh = Net::SSH.start(host, user, opts)
    end
  end
end 
