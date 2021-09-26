# About GSAclone
GSAclone is a simple python script for rclone, written with the purpose of using multiple Google service accounts on Google Drive and "randomize" them.
Though they are not really randomized, at least they are cycled through, and you won't have to manually specify which service account you use on each command.

The other solution such as AutoRclone and gclone doesn't work on me, when I tried it a few months ago.  
So I decided to write my own rclone script.

# How to use (Windows only)
1). Setting up the environment:  
Your service accounts should be first renamed into "service_account_X.json" where X is the number from 0 to (let's say) 100.

Here's how I set up mine:

>rclone is in "D:/Utility/rclone"  
>Service accounts are stored in the same folder as rclone, inside the service_account folder: "D:/Utility/rclone/service_accounts"  
>Inside the folder, I have a hunder of service accounts named from "service_account_0.json" to "service_account_100.json"
>
>To perform a sync from GDrive 1 to GDrive 2, I run: "python GSAclone -m sync -s GDrive_Shiro39: -d GDrive_Backup:

2). You must have python already installed on your system first.  
As I'm using Windows and I wrote this script on Windows, the example usage below is for Windows.

Open the script in either CMD (Command Prompt) or Windows Terminal
```
python GSAclone.py -h

usage: GSAclone.py [-h] -m MODE -s SOURCE -d DESTINATION

rclone but with multiple Google Service Accounts.

optional arguments:
  -h, --help            show this help message and exit
  -m MODE, --mode MODE                        copy or sync
  -s SOURCE, --source SOURCE                  Example: --source remote_1:
  -d DESTINATION, --destination DESTINATION   Example: --destination remote_2:
```

To copy/sync GDrive 1 to GDrive 2:
```
python GSAclone.py --mode copy/sync --source remote_name_src: --destination remote_name_dest:
```

# Configurations
Below are the configurations that you can modify to your needs.
```
var_loop = 3                              # Tells the script how many times it should be looping for.
var_sleep = 60                            # Tells the script how long it should delay the next routine.

rclone_path = "D:/Utility/_rclone"        # Path to where you store rclone. You do NOT need to type in "/rclone.exe"!
rclone_sa_path = "default"                # Set this to "default" to use the same path as your rclone path, or set your own path.


rclone_dry_run = "disabled"               # Tells rclone to run in simulated mode (--dry-run). (Default is "disabled")
rclone_verbose = "enabled"               # Print useful information onto the console (or a log file). (Default is "disabled")
rclone_verbose_level = "default"          # Set the verbose level ("default" or "super"). (Default is "default")

rclone_log_path = "default"             # Set this to "default" to use the same path as your rclone path, or set your own path.
rclone_log_mode = "default"             # Set this to "default" or "json" if you want the log to be in json format.

rclone_log_level = "debug"              # Set the debugging level. (Default is "debug". This is NOT the default from rclone! but rather, from this script.)
                                        # Debugging levels:
                                        # DEBUG is equivalent to -vv. It outputs lots of debug info - useful for bug reports and really finding out what rclone is doing.
                                        # INFO is equivalent to -v. It outputs information about each transfer and prints stats once a minute by default.
                                        # NOTICE is the default log level if no logging flags are supplied. It outputs very little when things are working normally. It outputs warnings and significant events.
                                        # ERROR is equivalent to -q. It only outputs error messages.

rclone_logging = "disabled"               # Set to "enabled" if you wish rclone to output its logs into a file. (Default is "disabled")
                                          # If verbose is enabled, logging will be disabled. You cannot have verbose and logging at the same time.
                                          # Since this script is going to loop for a certain amount of time (based on "var_loop") you could end up with a huge log file size!

rclone_check_first = "enabled"            # Tells rclone to perform check first before transfer. (Default is "enabled")
rclone_fast_list = "enabled"              # Enable --fast-list, useful to reduce the API call but uses more memory. (Default is "enabled")
rclone_modtime = "noupdate"               # Tells rclone to update the modified time of a file. (Set to "update" or "noupdate". Default is "update")

rclone_compare = "checksum"                # rclone compare mode:
                                          # default            : rclone will look at modification time and size.
                                          # checksum           : rclone will look at checksum and size.
                                          # only-mod-time      : rclone will look at checksum and modification time.
                                          # only-size          : rclone will look at file size only.
                                          # only-checksum      : rclone will look at checksum only.
```
You could modify the ```rclone_args = ""```, but for the sake of keeping the script having any issue, I recommend you not to add more rclone flags.
If you know exactly what you are doing and you know how to read the flow of the script, feel free to modify it, of course!

# Disclaimer
This script is NOT flawless and in fact, far from perfect! The current biggest issue is that it cannot accept any input containing spaces.  
For example:
```rclone_path = "path/to wherever/your/rclone/is"``` or ```"remote1:/hellow world/test"```

As long as you are backing up from the root folder, it should work just fine.

# License
This script is provided "AS IS" and is licensed under the MIT License.
