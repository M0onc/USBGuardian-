#!/bin/bash
# 批量部署边缘代理
ANSIBLE_HOSTS="hosts.ini"

ansible-playbook \
  -i $ANSIBLE_HOSTS \
  --extra-vars "central_server=api.example.com" \
  playbooks/install-agent.yml