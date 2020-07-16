FROM python:3

WORKDIR /usr/src/app

RUN pip install PyYAML && pip install paramiko

ADD ressources/hosts /etc/ansible/

COPY . .

CMD [ "python", "./ansible-playbook.py", "playbook.yml" ]