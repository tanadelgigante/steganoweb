#!/bin/sh

# Add custom hosts if config file exists
if [ -f /etc/hosts.extra ]; then
    cat /etc/hosts.extra >> /etc/hosts
fi

# Execute the main command
exec "$@"
