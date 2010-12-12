Ashfire's Tools
===============

This is a collection of Ashfire908's (Andrew Hampe) tools and scripts that he
has made or found over time. Below is a list of the scripts currently contained
in this collection.

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
