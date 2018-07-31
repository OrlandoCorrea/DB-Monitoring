#!/usr/bin/expect
set ip [lindex $argv 0]
set port [lindex $argv 1]
set user [lindex $argv 2]
set pass [lindex $argv 3]

log_user 0                   ;# turn off the usual output
spawn telnet $ip $port
sleep 20
expect -re "Username"
send "$user\t"
sleep 15
expect -re "Contrase"
send "$pass\r\n"
sleep 15
expect -re ">"
send "DSPSYSSTS\r"
log_user 1
sleep 10
expect -re ">"
expect eof
