#!/usr/bin/python3

import sys
import paramiko
import yaml


class Ansible:
    """
    A class used to represent a simple version of Ansible Playbook

    ...

    Attributes
    ----------
    defaultHostsFilePath : str
        the path of the hosts file
    playbookFile : str
        the name of the playbook file
    hostsListName : str
        the list name of hosts
    hosts : list
        a list of all the hosts
    tasks : list
        a list of tasks to executed for each hosts

    """

    def __init__(self, playbookFile):
        """
        Parameters
        ----------
        playbookFile : str
            path to the yaml playbook file
        """
        self.playbookFile = playbookFile
        self.defaultHostsFilePath = self.getHostsFilePath()
        self.hostsListName = self.getHostsListName()
        self.hosts = self.getHosts()
        self.tasks = self.getTask()

    def getHostsFilePath(self):
        """Return the hosts file path

        Returns
        -------
        the hosts file path
        """
        return "/etc/ansible/hosts"

    def getHostsListName(self):
        """Parse the playbook file and return the list name of hosts

        Raises
        ------
        YAMLError
         If the program isn't able to parse the file

        Returns
        -------
        list name of hosts
        """
        with open(self.playbookFile, 'r') as f:
            try:
                document = yaml.safe_load(f)
                return '[' + document[0]['hosts'] + ']'
            except yaml.YAMLError as exc:
                print(exc)

    def getHosts(self):
        """Parse the hosts file and return the hosts list

        Raises
        ------
        FileExistsError
         If the hosts file doesn't exist

        Returns
        -------
        the hosts list
        """
        hostsList = []
        try:
            with open(self.defaultHostsFilePath, 'r') as f:
                lines = f.read().splitlines()
                hostListIndex = lines.index(self.hostsListName) + 1
                line = lines[hostListIndex]

                while (not line[:1]) or line[:1] != '[':
                    if line != '':
                        hostsList.append(line)
                    hostListIndex += 1
                    if hostListIndex >= len(lines):  # python needs do-while loop
                        break
                    line = lines[hostListIndex]

            return hostsList

        except FileExistsError:
            print("File doesn't exist", str(self.defaultHostsFilePath))

    def getTask(self):
        """Parse the playbook file and return the list of tasks

        Raises
        ------
        YAMLError
         If the program isn't able to parse the file

        Returns
        -------
        list of tasks
        """
        with open(self.playbookFile, 'r') as stream:
            try:
                document = yaml.safe_load(stream)
                tasks = document[0]['tasks']
                return tasks
            except yaml.YAMLError as exc:
                print(exc)

    def execPlaybook(self):
        """Connect to each hosts with the rsa key and execute tasks

        """
        for host in self.hosts:
            self.print_info("PLAY [" + host + "] ************************\n")
            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(host, key_filename="/root/.ssh/id_rsa", look_for_keys=True, )

            for task in self.tasks:
                self.print_info("\nTASK [" + task['name'] + "] ************************")
                stdin, stdout, stderr = client.exec_command(task['bash'])
                stdout.channel.recv_exit_status()
                lines = stdout.readlines()
                for line in lines:
                    print(line)

            client.close()

    @staticmethod
    def print_info(message, end='\n'):
        """Display message in blue

        """
        sys.stdout.write('\x1b[1;34m' + message.strip() + '\x1b[0m' + end)


myAnsible = Ansible(sys.argv[1])
myAnsible.execPlaybook()
