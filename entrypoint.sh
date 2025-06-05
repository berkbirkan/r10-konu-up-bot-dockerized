#!/bin/bash
set -e

# Cron'u normalde arka planda (daemon)   al   ^=t  r  r
# Bu sayede komut sat  r   bloke olmaz
cron

# cron.log'u ekrana s  rekli yans  tmak i  in 'tail -f'   al   ^=t  r  yoruz.
echo "Tailing /var/log/cron.log..."
tail -f /var/log/cron.log

