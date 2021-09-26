#--------------------------------------------------#--------------------------------------------------#
# GSAclone -- rclone but with (somewhat) "randomized" Google Service Accounts.
# https://github.com/shirooo39/GSAclone
#
# This script is provided "AS IS" and is licensed under the MIT License.
# Useful short information about the MIT License allows you: https://tldrlegal.com/license/mit-license
#--------------------------------------------------#--------------------------------------------------#
#
# This is a simple python script that loops through an rclone command for an X number of times
# while also "randomizing" the service account it should use on each command.
#
# I know I said that the service accounts are randomized, but rather, the script will generate a random
# number from X to Y (which you can change by yourself) and then "attach" the generated random
# number onto the service account name.
#
# Your service accounts should first be renamed into "service_account_X.json" before using this script.
# Example: service_account_39.json, service_account_40.json.
#
#--------------------------------------------------#--------------------------------------------------#
#
# This script is NOT flawless! The current biggest issue with the script is that it can NOT ---
# handle input with spaces. (I know, I know. I'm sorry, but... I don't know how to fix that.)
#
# Example: Source: remote_1:/path/to whatever/test
#          rclone_path = "D:/path/to where/rclone/is/rclone"
#
#--------------------------------------------------#--------------------------------------------------#

import subprocess, time, random, argparse

subprocess.call("cls", shell=True)

parser = argparse.ArgumentParser(description='rclone but with multiple Google Service Accounts.')
parser.add_argument('-m', '--mode', help='copy or sync', required=True)
parser.add_argument('-s', '--source', help='Example: --source remote_1:', required=True)
parser.add_argument('-d', '--destination', help='Example: --destination remote_2:', required=True)
cmd_args = vars(parser.parse_args())

if not (cmd_args['mode'] == "copy" or cmd_args['mode'] == "sync") :
    exit('The operation mode could only be "copy" or "sync"!')
else:
    rclone_mode = cmd_args['mode']

if cmd_args['source'] is None:
    exit("The input source cannot be empty!")
else:
    remote_source = cmd_args['source']

if cmd_args['destination'] is None:
    exit("The input destination cannot be empty!")
else:
    remote_destination = cmd_args['destination']

##### [Parameters] #################################################################################
var_loop = 3                              # Tells the script how many times it should be looping for.
var_sleep = 60                            # Tells the script how long it should delay the next routine.

rclone_path = "D:/path/to/rclone"        # Path to where you store rclone. You do NOT need to type in "/rclone.exe"!
rclone_sa_path = "default"                # Set this to "default" to use the same path as your rclone path, or set your own path.


rclone_dry_run = "disabled"               # Tells rclone to run in simulated mode (--dry-run). (Default is "disabled")
rclone_verbose = "disabled"               # Print useful information onto the console (or a log file). (Default is "disabled")
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
rclone_modtime = "update"                 # Tells rclone to update the modified time of a file. (Set to "update" or "noupdate". Default is "update")

# For the sake of keeping the script from having any issue nor conflict, please do NOT add more flags! You could, however, edit the value.
# Unless you know what you're doing and you know EXACTLY the flow of this script, you are absolutely free to do whatever you want.
rclone_args = "--progress \
                --retries 5 \
                --tpslimit 10 \
                --checkers 10 \
                --transfers 10 \
                --max-transfer 740G \
                --low-level-retries 10 \
                --create-empty-src-dirs \
                --drive-acknowledge-abuse \
                --drive-stop-on-upload-limit=true \
                --drive-server-side-across-configs"

rclone_compare = "default"                # rclone compare mode:
                                          # default            : rclone will look at modification time and size.
                                          # checksum           : rclone will look at checksum and size.
                                          # only-mod-time      : rclone will look at checksum and modification time.
                                          # only-size          : rclone will look at file size only.
                                          # only-checksum      : rclone will look at checksum only.
####################################################################################################

####################################################################################################

## TO DO LATER: add isfile or isfolder to check whether these paths do exist or not.

if rclone_path == "":
    exit("Variable rclone_path cannot be empty!")
else:
    pass

if rclone_sa_path == "":
    exit("Variable rclone_sa_path cannot be empty!")
elif rclone_sa_path == "default":
    rclone_sa_path = "--drive-service-account-file=" + rclone_path + "/service_accounts/"
else:
    rclone_sa_path = "--drive-service-account-file=" + rclone_sa_path + "/"

if rclone_verbose == "enabled":
    if rclone_verbose_level == "super":
        rclone_verbose = "-vv"
        rclone_logging = "disabled"
    else:
        rclone_verbose = "-v"
        rclone_logging = "disabled"
else:
    rclone_verbose = ""

if rclone_logging == "enabled":
    if rclone_log_mode == "json":
        rclone_log_mode = "--use-json-log"
        rclone_log_name = "/SAclone_log.json"
    else:
        rclone_log_mode = ""
        rclone_log_name = "/SAclone_log.txt"

    if rclone_log_path == "":
        exit("Variable rclone_log_path cannot be empty!")
    elif rclone_log_path != "default":
        rclone_log_path = rclone_log_path + rclone_log_name
    else:
        rclone_log_path = rclone_path + rclone_log_name

    if rclone_log_level == "debug" or rclone_log_level == "DEBUG":
        rclone_log_level = "--log-level DEBUG"
    elif rclone_log_level == "info" or rclone_log_level == "INFO":
        rclone_log_level = "--log-level INFO"
    elif rclone_log_level == "error" or rclone_log_level == "ERROR":
        rclone_log_level = "--log-level DEBUG"
    else:
        rclone_log_level = "--log-level NOTICE"

    rclone_logging = rclone_log_mode + " " + rclone_log_level + " --log-file=" + rclone_log_path
    rclone_logging_message = "enabled"
else:
    rclone_logging = ""
    rclone_log_mode = ""
    rclone_log_path = ""
    rclone_log_name = ""
    rclone_logging_message = "disabled"

if rclone_dry_run == "enabled":
    rclone_dry_run = "--dry-run"
    rclone_dry_run_message = "enabled"
else:
    rclone_dry_run = ""
    rclone_dry_run_message = "disabled"

if rclone_check_first == "disabled":
    rclone_check_first = ""
else:
    rclone_check_first = "--check-first"

if rclone_fast_list == "disabled":
    rclone_fast_list = ""
else:
    rclone_fast_list = "--fast-list"

if rclone_modtime == "noupdate":
    rclone_modtime = "--no-update-modtime"
else:
    rclone_modtime = ""

if rclone_compare == "checksum":
    rclone_compare = "--checksum"
elif rclone_compare == "only-mod-time":
    rclone_compare = "--ignore-size"
elif rclone_compare == "only-size":
    rclone_compare = "--size-only"
elif rclone_compare == "only-checksum":
    rclone_compare = "--checksum --ignore-size"
else:
    rclone_compare = ""
####################################################################################################

####################################################################################################
for x in range(var_loop):
    subprocess.call("cls", shell=True)

    var_rand = random.randint(0, 100)   # The range of the generated random number. (0, 100) means it will generate a random number from 0 - 100.
    service_account = "service_account_" + str(var_rand) + ".json"

    print("----- Performing task for", str(var_loop), "time(s)")
    print("----- Each task will be delayed for", str(var_sleep), "second(s)\n")
    print("=" * 70)
    print("Source:", remote_source)
    print("Destination:", remote_destination)
    print("Using service account:", service_account)
    print("")
    if rclone_dry_run_message == "enabled":
        print("Running in simulated mode!")
    else:
        pass

    if rclone_logging_message == "enabled":
        print("Logging is enabled! (" + rclone_log_path + ")")
    else:
        pass
    print("")

    subprocess.call(rclone_path + "/rclone.exe" + " " + rclone_mode + " " + remote_source + " " + remote_destination + " " + rclone_dry_run + " " + rclone_verbose + " " + rclone_fast_list + " " + rclone_check_first + " " + rclone_compare + " " + rclone_args + " " + rclone_modtime + " " + rclone_sa_path + service_account + " " + rclone_logging, shell=True)

    print("\n" + ("=" * 70) + "\n")
    time.sleep(var_sleep)
####################################################################################################

exit()