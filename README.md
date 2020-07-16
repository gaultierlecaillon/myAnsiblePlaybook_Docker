# Task 2: Simple Ansible Playbook - Docker Container

Implementation of a simple version of Ansible that allow you to run a simple ansible playbook.

This program is used to run tasks on multiple managed nodes or “hosts” in your infrastructure at the same time, using a list or group of lists know as inventory.

`This is a Docker Container` that you can run on Windows or Linux.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

* Docker running

## Configuration
The authentication works with SSH key-based

#### Allow SSH key-based authentication

Generate a SSH key pair by typing (RSA bits 1024, 2048, or 3072 are supported)
```
ssh-keygen -b 2048
```
The utility will prompt you to select a location for the keys that will be generated. By default, the keys will be stored in the `~/.ssh`

**Copying your Public Key Using SSH-Copy-ID**
```
ssh-copy-id -i ~/.ssh/id_rsa.pub username@remote_host
```

It will ask you the ssh password for the last time

#### Configure your host file
In the `./ressources/` directory, complete the host file, it should looks like this:
```
[dbservers]
192.168.1.1
192.168.1.2
192.168.1.3

[webservers]
192.168.1.4

[devservers]
192.168.1.5
```

And it's done !

## Build the Docker image
```
$ docker build -t my-python-app .
```

## Run the Docker image created
Windows command:
```
$ docker run -it --rm -v C:\Users\Gaultier\.ssh\:/root/.ssh --name my-running-app my-python-app
```
Linux Command:
```
$ docker run -it --rm -v /user/Gaultier/.ssh:/root/.ssh --name my-running-app my-python-app
```

### Authors

* **Gaultier Lecaillon** - *Proton team Task* 