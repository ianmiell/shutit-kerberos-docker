#!/bin/bash
VBoxManage list runningvms | grep '^"kerberos_docker_default' | awk '{print $1}' | xargs --no-run-if-empty -IXXX VBoxManage controlvm 'XXX' poweroff && VBoxManage list vms | awk '{print $1}'  | xargs --no-run-if-empty -IXXX VBoxManage unregistervm 'XXX' --delete

[[ -z "$SHUTIT" ]] && SHUTIT="$1/shutit"
[[ ! -a "$SHUTIT" ]] || [[ -z "$SHUTIT" ]] && SHUTIT="$(which shutit)"
if [[ ! -a "$SHUTIT" ]]
then
	echo "Must have shutit on path, eg export PATH=$PATH:/path/to/shutit_dir"
	exit 1
fi
$SHUTIT build -d bash -m shutit-library/virtualbox -m shutit-library/vagrant "$@"
if [[ $? != 0 ]]
then
	exit 1
fi
