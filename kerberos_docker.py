"""ShutIt module. See http://shutit.tk
"""

from shutit_module import ShutItModule


class kerberos_docker(ShutItModule):


	def build(self, shutit):
		shutit.send('rm -rf /tmp/kerberos_docker')
		shutit.send('mkdir -p /tmp/kerberos_docker')
		shutit.send('cd /tmp/kerberos_docker')
		shutit.send('vagrant init williamyeh/centos7-docker')
		shutit.send('vagrant up --provider virtualbox')
		shutit.login(command='vagrant ssh')
		shutit.login(command='sudo su -',password='vagrant',note='Become root (there is a problem logging in as admin with the vagrant user')
		shutit.send('yum install -y git')
		shutit.send('git clone https://github.com:tillt/docker-kdc.git')
		shutit.send('cd docker-kdc')
		shutit.send('./kdc config',note='Check the configuration is sane')
		shutit.send('./kdc build',note='Build the container')
		shutit.send('./kdc start',note='Start up the kerberos server')
		shutit.send('./kdc test',note='Test the server is up ok')
#krb5-user
#kinit tillt/osboxes.localdomain@LOCALDOMAIN
#Password for tillt/osboxes.localdomain@LOCALDOMAIN: 
#klist
#cat krb5.conf
#file krb5.keytab
#
#imiell@osboxes:/space/git/docker-kdc$ ktutil --keytab=./krb5.keytab list
#ktutil:  list
#slot KVNO Principal
#---- ---- ---------------------------------------------------------------------
#ktutil:  keytab
#ktutil: Unknown request "keytab".  Type "?" for a request list.
#ktutil:  ?
#Available ktutil requests:
#
#clear_list, clear        Clear the current keylist.
#read_kt, rkt             Read a krb5 keytab into the current keylist.
#read_st, rst             Read a krb4 srvtab into the current keylist.
#write_kt, wkt            Write the current keylist to a krb5 keytab.
#write_st, wst            Write the current keylist to a krb4 srvtab.
#add_entry, addent        Add an entry to the current keylist.
#delete_entry, delent     Delete an entry from the current keylist.
#list, l                  List the current keylist.
#list_requests, lr, ?     List available requests.
#quit, exit, q            Exit program.
#ktutil:  read_kt krb5.keytab
#ktutil:  l
#slot KVNO Principal
#---- ---- ---------------------------------------------------------------------
#   1    1    tillt/osboxes.localdomain@LOCALDOMAIN
#   2    1    tillt/osboxes.localdomain@LOCALDOMAIN
#   3    1    tillt/osboxes.localdomain@LOCALDOMAIN
#
#kinit -kt krb5.keytab tillt/hostname.example.com@EXAMPLE.COM
#klist
		shutit.send('ktdestroy')
		shutit.send('./kdc stop',note='cleanup')
		shutit.logout()
		shutit.logout()
		return True

	def get_config(self, shutit):
		# CONFIGURATION
		# shutit.get_config(module_id,option,default=None,boolean=False)
		#                                    - Get configuration value, boolean indicates whether the item is
		#                                      a boolean type, eg get the config with:
		# shutit.get_config(self.module_id, 'myconfig', default='a value')
		#                                      and reference in your code with:
		# shutit.cfg[self.module_id]['myconfig']
		return True

	def test(self, shutit):
		# For test cycle part of the ShutIt build.
		return True

	def finalize(self, shutit):
		# Any cleanup required at the end.
		return True
	
	def is_installed(self, shutit):
		return False


def module():
	return kerberos_docker(
		'shutit.kerberos_docker.kerberos_docker.kerberos_docker', 416177174.0001,
		description='',
		maintainer='',
		delivery_methods=['bash'],
		depends=['shutit.tk.setup']
	)

