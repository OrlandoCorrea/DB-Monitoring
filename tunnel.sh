#!/bin/bash
portNAT=$2
ip=$3
portIP=$4
user=$5
host=$6
SSHPASS=$1 sshpass -e $pass ssh -f -o ExitOnForwardFailure=yes -L $portNAT:$ip:$portIP $user@$host sleep 4800
