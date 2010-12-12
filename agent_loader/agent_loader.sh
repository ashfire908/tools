#!/bin/sh
# SSH agent loader
#
# Copyright © 2010 Andrew Hampe
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


# Config
KEYS_FILE="$HOME/.ssh/agent_keys"
AUTH_SOCK="$HOME/.ssh/agent_auth_sock"

# Find the PID for the SSH agent
find_agent () {
  if [ "$OS" = "Windows_NT" ]; then
    # We appear to be in cygwin, use workaround
    ps -u $UID -s | AGENT_PATH=`which ssh-agent` awk '{if ($4 == ENVIRON["AGENT_PATH"]) {print $1}}'
  else
    ps -C ssh-agent -o pid,uid | CUID=$UID awk '{if ($2 == ENVIRON["CUID"]) {print $1}}'
  fi
}

# Start SSH agent
start_agent () {
  echo -n "Starting ssh-agent..."
  eval `ssh-agent` > /dev/null
  echo " Done."
  echo "$SSH_AUTH_SOCK" > "$AUTH_SOCK"
  while IFS="" read -r key; do
    if [ "$key" != "" ]; then
      ssh-add "$key"
    fi
  done < "$KEYS_FILE"
}

# Configure shell to use SSH agent
config_agent () {
  read SSH_AUTH_SOCK < "$AUTH_SOCK"
  export SSH_AUTH_SOCK
  export SSH_AGENT_PID=$1
}

# Look for a running SSH agent
AGENT_PID=$(find_agent)
if [ "$AGENT_PID" = "" ]; then
  # No SSH agent running, start one
  start_agent
else
  # Configure shell to use SSH agent
  config_agent $AGENT_PID
fi
