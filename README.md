## Dev Environment for NTC ConfD

To ensure we're working with a common development environment

### Step 1

Install Vagrant and VirtualBox (Windows or MAC)
(Ensure that Vagrant version is 1.9.1 or greater)

### Step 2

Clone this repo and navigate into the repo

### Step 3

Use the command `vagrant up` in the directory where `Vagrantfile` is.

The first time, it'll download the vagrant "box" (VM).

The provisioning steps will complete and you should be able to login to the box using

``` shell
vagrant status
vagrant ssh DEVICENAME
```
from within the ntc-confd directory.

### Step 4


```
ssh-copy-id vagrant@localhost -p PORTNUMBER
```


Then you can `ssh vagrant@localhost -p 2222` without a password.


### Common Commands

* vagrant up
* vagrant ssh
* vagrant halt
* vagrant reload
* vagrant destroy
* vagrant provision - if just the playbook changes, use this as an option
* vagrant status - give list of VM's 
* vagrant port confd - to see which ports to login for the localhost
* vagrant port configengine 
`hint`: use -f for destroy to destroy VM's without asking for each VM

Whenever you **destroy** and then `vagrant up` again, you'll have a fresh clean install (in a few minutes).  Can do multiple using different directories and same Vagrantfile.


### Sharing Data

* `.` (on your host, where the Vagrantfile is) automatically synch'd with `/vagrant` in the vagrant box so you can easily use client applications such as text editors and run scripts seamlessly in the VM.
* `~/ntc-data` (on your host) automatically synch'd with `/ntc-data` in the vagrant box so you can easily use client applications such as text editors and run scripts seamlessly in the VM.

## Setting up ConfD NTC


Start ConfD

```
vagrant ssh confd
cd ntc_confd_sot/
make all
make start
```

Open a new terminal (keeping the other one open with daemon running)

```
vagrant ssh confd
kickoffconfd

or if you prefer the non-alias

confd_cli -C -u admin
```

```
vagrant@confd:~$ kickoffconfd

admin connected from 10.0.2.2 using ssh on confd
confd# conf
Entering configuration mode terminal
confd(config)# 
```

Now copy and paste all the values from `files/confd_cdb.cfg` and enter `commit`


## Testing the ConfD API from Ansible

you can test the ConfD API from Ansible 

```
vagrant ssh configengine
```

copy the ansible directory from ntc-confd/ansible repo onto the configengine server into `configengine` directory


```
cd ansible
ansible-playbook -i inventory gather_vars.yml
```

response should be something like this

```yaml
vagrant@configengine:ansible$ ansible-playbook -i inventory gather_vars.yml

PLAY [PLAY 1 - ISSUE API CALL TO ConfD] *********************************************************

TASK [GET Dummy ALL Vars Info] ******************************************************************
ok: [confd]

TASK [set_fact] *********************************************************************************
ok: [confd]

TASK [GET Dummy HOST Vars Info] *****************************************************************
ok: [confd]

TASK [set_fact] *********************************************************************************
ok: [confd]

TASK [COPY CONFD CSR1 VARS to ANSIBLE LOCATION] *************************************************
changed: [confd]

TASK [COPY CONFD CSR1 VARS to ANSIBLE LOCATION] *************************************************
changed: [confd]

TASK [COPY CONFD CSR1 VARS to ANSIBLE LOCATION] *************************************************
changed: [confd]

TASK [COPY CONFD CSR1 VARS to ANSIBLE LOCATION] *************************************************
changed: [confd]

PLAY RECAP **************************************************************************************
confd                      : ok=8    changed=4    unreachable=0    failed=0

```

It has gathered all the data from ConfD CDB and put them into group_vars and host_vars for use to build the config. 

Run the playbook `build_config.yml`

```
vagrant ssh configengine
cd ansible
ansible-playbook -i inventory build_config.yml

``` 


sample output
```

PLAY [PLAY 1 - ISSUE API CALL TO ConfD] *********************************************************

TASK [BUILD CONFIGS FROM NEW YAML] **************************************************************
changed: [csr2]
changed: [csr3]
changed: [csr1]

PLAY RECAP **************************************************************************************
csr1                       : ok=1    changed=1    unreachable=0    failed=0
csr2                       : ok=1    changed=1    unreachable=0    failed=0
csr3                       : ok=1    changed=1    unreachable=0    failed=0

```

check the `configs` dir for new configs `cat configs/csr1.cfg`, also verify the created YAML files `group_vars` and `host_vars`




## FYI Using Cookiecutter

Update the ./files/cookiecutterrc to change default values for the vagrant created confd directory

by default the values are

```yaml
default_context:
    author_name: "Jason Belk"
    author_email: "jason.belk@networktocode.com"
    github_username: "jabelk"
    project_name: "ntc_confd_sot"
    project_description: "NTC Source of Truth Project using ConfD"
    yang_module: "ntc_sot"
cookiecutters_dir: "/home/vagrant/cookiecutter-confd/"
abbreviations:
    cc: https://github.com/jabelk/cookiecutter-confd.git
```

When the provisioning playbook runs it calls the `install-ntc-confd.yml` playbook, issuing the following commands:

```yaml
  - name: Create ConfD SoT from cookiecutter
    shell: "cookiecutter --config-file /home/{{ user }}/.cookiecutterrc /home/{{ user }}/cookiecutter-confd --no-input"
    ignore_errors: yes
    become_user: "{{ user }}"
    register: cookiecutteroutput
```

Which uses the config file of the .cookiecuterrc as default values overriding the default JSON in the git repo.
You can provide another YAML file or change the rc file, which will be auto checked be cookiecutter, but explicitly called
since Ansible does not pick it up