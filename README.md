Ashfire's Tools
===============

This is a collection of old tools and scripts I made while learning programming.
They are all probably pretty horrible now, but are collected here ~~to shame
me~~ for posterity. Below is a list of the scripts currently contained in this
collection.

Scripts and Tools
-----------------

* GitHub Repo Updater - A post-receive hook that updates local git repos on
  commit. Keeps a log of updates and errors. (github_repo_updater.php)
* Remote Wireshark - Connects to another machine via SSH, starts tshark
  remotely, and returns the sniffed traffic to Wireshark running locally on
  your machine. (remote_wireshark.py)
* Image gallery - A client-side JavaScript image gallery that reads the gallery
  configuration from an XML file (jsxml_gallery/)
* SSH agent loader - Script to automatically start an ssh agent (if needed),
  configure the shell to use the started SSH agent, and load in the SSH keys.
  Useful for remote shells or systems you don't have a built-in preconfigured
  SSH agent for. (agent_loader/)
* Fallout Terminal Hacker - Script that assists with the terminal hacking
  minigame in Fallout 3 (and later games). One of the first (if not the first)
  programs I ever wrote. Designed for Linux terminals; term color codes probably
  won't work on Windows. Last modified in 2009 before having a styling/typo pass
  and being committed. (fallout3/)
