"""ShutIt module. See http://shutit.tk
"""

from shutit_module import ShutItModule


class kerberos_docker(ShutItModule):


	def build(self, shutit):
		shutit.send('rm -rf /tmp/kerberos_docker')
		shutit.send('mkdir -p /tmp/kerberos_docker')
		shutit.send('cd /tmp/kerberos_docker')
		shutit.send('vagrant init geerlingguy/centos7')
		shutit.send('vagrant up --provider virtualbox')
		shutit.login(command='vagrant ssh')
		shutit.login(command='sudo su -',password='vagrant')
		shutit.send('yum install -y docker git krb5-workstation telnet')
		shutit.send('systemctl enable docker')
		shutit.send('systemctl start docker')
		shutit.send('echo "127.0.0.1   localhost.localdomain localhost4 localhost4.localdomain4" > /etc/hosts')
		shutit.send('echo "::1         localhost.localdomain localhost6 localhost6.localdomain6" >> /etc/hosts')
		shutit.send('git clone https://github.com/tillt/docker-kdc.git')
		shutit.send('cd docker-kdc')
		shutit.send('./kdc config',note='Check the configuration is sane')
		shutit.send('./kdc build',note='Build the container, note the kadmin commands to set up resource')
		shutit.send('./kdc start',note='Start up the kerberos server')
		shutit.send_until('./kdc test','.*ok.*',note='Test the server is up ok')
		shutit.send('$(./kdc shellinit)',note='Set up the shell so it references this dockerized kerberos server')
		shutit.send('kinit tillt/localhost.localdomain@LOCALDOMAIN',expect='assword')
		shutit.send('matilda')
		shutit.send('cat krb5.conf',note='Two files are created; the first is thekrb5.conf file that we use. Normally this is in /etc')
		shutit.send('file krb5.keytab',note='')
		shutit.send('klist',note='List the cached kerberos tickets.')
		shutit.send('ktutil',expect='ktutil:',note='Run the keytab utility program')
		shutit.send('read_kt krb5.keytab',expect='ktutil:',note='Read in the keytab file.')
		shutit.send('list',expect='ktutil:',note='List the cached kerberos tickets.')
		shutit.send('exit',note='Quit the ktutil program')

		shutit.login(command='docker exec -ti kdc bash',note='Log into the docker container')
		shutit.send('kadmin -l add --password=teddy --use-defaults someprincipal/localhost.localdomain@LOCALDOMAIN',note='add another principal')
		shutit.send('kadmin -l ext_keytab -k /etc/docker-kdc/someprincipal.keytab someprincipal/localhost.localdomain@LOCALDOMAIN',note='Create a keytab for that principal')
		shutit.send('kadmin -l',expect='kadmin>')
		shutit.send('exit',note='quit kadmin')
		shutit.logout()

		shutit.send('docker cp kdc:/etc/docker-kdc/someprincipal.keytab someprincipal.keytab',note='Copy ')
		shutit.send('kinit someprincipal/localhost.localdomain@LOCALDOMAIN',expect='assword',note='Log into the new principal.')
		shutit.send('teddy')
		shutit.send('./kdc stop',note='Cleanup server')
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
		description='A dockerized kerberos server and ticket interactions.',
		maintainer='ian.miell@gmail.com',
		delivery_methods=['bash'],
		depends=['shutit.tk.setup']
	)

