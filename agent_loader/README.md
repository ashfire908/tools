SSH agent loader
================

Script to automatically start an ssh agent (if needed), configure the shell to
use the started SSH agent, and load in the SSH keys. Useful for remote shells
or systems you don't have a built-in preconfigured SSH agent for.

Setting up the script
---------------------

1. Copy `agent_loader.sh` to your `.ssh` folder.
2. Create a text file listing the SSH keys (file name + path) you want the
   script to automatically load (one per line). __Important:__ _Leave a blank
   line at the end of the file or not all the keys will be loaded._
3. Edit your shell login script (eg. .bashrc, .bash_profile) to source the
   script, like so:

    `source ~/.ssh/agent_loader.sh`

4. The script with automatically run when you open a new shell.

_Note: Each time the SSH agent starts, you will be prompted for the passphrase
for each of your SSH keys. After that, you will not have to enter them back in
(unless the SSH agent is restarted)._

Copyright/License
-----------------

Copyright © 2010 Andrew Hampe

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as
published by the Free Software Foundation, either version 2.1 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this program. If not, see
<http://www.gnu.org/licenses/>.
