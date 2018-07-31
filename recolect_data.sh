#!/usr/bin/expect

set ip [lindex $argv 0]
set user [lindex $argv 1]
set pass [lindex $argv 2]

log_user 0                   ;# turn off the usual output
spawn tn5250 $ip
expect -re "Username"
send "$user\t"
sleep 5
expect -re "Contrase"
send "$pass\r\n"
sleep 5
expect -re ">"
send "DSPSYSSTS\r"
log_user 1
sleep 10
expect -re ">"
expect eof
