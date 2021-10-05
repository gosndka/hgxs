#--------------------------------------------------#--------------------------------------------------#
# GSAclone -- rclone with multiple and randomized Google Service Accounts.
# https://github.com/shirooo39/GSAclone
#
# This script is PROVIDED FOR FREE, AS IS, WITHOUT ANY WARRANTY, and released under the MIT License.
# Please also keep in mind that this script is far from perfeect.
#--------------------------------------------------#--------------------------------------------------#

import sys, pathlib, subprocess

subprocess.run('title GSAclone', shell=True)

def clear_output():
    subprocess.run('cls', shell=True)

def get_os():
    clear_output()

    if sys.platform.startswith('win32'):
        pass
    else:
        sys.exit('Sorry! This script only support the Microsoft Windows operating system!')

def python_version():
    clear_output()

    version = ".".join(map(str, sys.version_info[:3]))

    if sys.version_info < (3, 8):
        print(f'You are running Python version ({version}).')
        sys.exit('Python 3.8 or newer is required to run this script!')
    else:
        pass

def rclone_check(rclone_path):
    clear_output()

    if rclone_path.exists() and rclone_path.is_dir():
        try:
            subprocess.run((f'"{rclone_path}/rclone.exe" -h'), shell=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except FileNotFoundError:
            sys.exit('Unable to locate rclone.exe!')
    else:
        sys.exit('The specified rclone path does not exist!')

def sa_check(service_account_path):
    clear_output()

    if service_account_path.exists() and service_account_path.is_dir():
        sa_path_empty = not bool(sorted(service_account_path.rglob('*.json')))

        if sa_path_empty:
            sys.exit('The specified service account path does not seem to contain any service account file!')
        else:
            pass
    else:
        sys.exit('The specified service account path does not exist!')

def GSAclone():
    get_os()
    python_version()
    clear_output()

    import glob, time, random, argparse

    parser = argparse.ArgumentParser(description='rclone but with multiple Google Service Accounts.')
    parser.add_argument('-m', '--mode', help='copy or sync', required=False)
    parser.add_argument('-s', '--source', help='Example: --source remote_1:', required=True)
    parser.add_argument('-d', '--destination', help='Example: --destination remote_2:', required=True)
    cmd_args = vars(parser.parse_args())

    #==================================================#==================================================#
    #
    # Configurations
    #
    var_loop = 3 # (Default is: "3")
    # Tells the script how many times it should be looping for.
    # Looping it 3 times should be enough, as 740 x 3 is more than 2TB,
    # more than the limit of copy activity (including server-side) you can do on Google Drive.

    var_sleep = 60 # (Default is: "60")
    # Tells the script how long it should delay the next routine.
    # Set it to "0" to disable the delay.
    # This isn't really necessary, but oh well, whatever...

    rclone_path = pathlib.Path(r'D:/path/to/rclone')
    # Path to where you store your rclone.
    # Only change the text inside the single quotation ('') marks!
    # You also do NOT need to type in "/rclone.exe" nor "rclone.exe" at the end of the path!

    log_path = rclone_path # (Default is the same as "rclone_path")
    # Set this to "default" to use the same path as your rclone path, or set your own path.

    service_account_path = pathlib.Path(r'D:/path/to/service_account')
    # Path to where you store your service account files.
    # Only change the text inside the single quotation ('') marks!
    
    service_account_list = []
    # Do NOT modify this!

    dry_run = False # (Default is: "False")
    # Set this to "True" to run rclone in simulated mode and make no changes.

    verbose = False # (Default is: "False")
    # Set this to "True" and you will see magic.
    # Oh, by the way, you can't have verbose and logging enabled at the same time.
    # This script will prioritize verbose over logging.

    verbose_level = 'default' # (Default is: "default")
    # Set the level of verbose. ("default" or "super")

    logging = False # (Default is: "False")
    # Throws whatever rclone prints on your screen into a file.
    # Please keep in mind that if you enable logging, you could ends up with a huge log file size
    # as the script is going to repeat itself for an X amount of time (as specified by the variable "var_loop" above).

    log_name = 'GSAclone' # (Default is "GSAclone")
    # The name of the log file.
    # Feel free to change it to whatever you want.

    log_mode = 'default' # (Default is: "default")
    # Set it to "json" if you want rclone to output the log into a json file, or set it to "default".

    log_level = 'default' # (Default is: "default" or "notice")
    # The level of information that you want rclone to print into the log file.
    # Debugging levels:
    # DEBUG is equivalent to -vv. It outputs lots of debug info - useful for bug reports and really finding out what rclone is doing.
    # INFO is equivalent to -v. It outputs information about each transfer and prints stats once a minute by default.
    # NOTICE is the default log level if no logging flags are supplied. It outputs very little when things are working normally. It outputs warnings and significant events.
    # ERROR is equivalent to -q. It only outputs error messages.

    show_progress = True # (Default is: "True")
    check_first = False # (Default is: "False")
    fast_list = False # (Default is: "False")
    update_mod_time = True # (Default is: "True")

    compare = 'default' # (Default is: "default")
    # rclone compare mode:
    # default            : rclone will look at modification time and size.
    # checksum           : rclone will look at checksum and size.
    # only-mod-time      : rclone will look at checksum and modification time.
    # only-size          : rclone will look at file size only.
    # only-checksum      : rclone will look at checksum only.

    flags = '--tpslimit 10\
            --checkers 10\
            --transfers 10\
            --max-transfer 740G\
            --drive-stop-on-upload-limit=true\
            --drive-server-side-across-configs'
    #
    # I'm thinking of using a config file instead, but as I still don't know how to use configparser yet, that's for another day lol
    # For now, if you want to change something, edit the script directly.
    #
    #==================================================#==================================================#

    #==================================================#==================================================#
    #
    # To do later: add checking whether the paths specified above do exist or not.
    #
    if (cmd_args['mode'] == "copy") or (cmd_args['mode'] == "sync"):
        mode = cmd_args['mode']
    else:
        mode = 'copy'

    if cmd_args['source'] is None:
        sys.exit("The input source cannot be empty!")
    else:
        source = cmd_args['source']

    if cmd_args['destination'] is None:
        sys.exit("The input destination cannot be empty!")
    else:
        destination = cmd_args['destination']
    
    rclone_check(rclone_path)
    sa_check(service_account_path)
    
    if dry_run is True:
        dry_run = '--dry-run'
        test_switch = True
    else:
        dry_run = ''
        test_switch = False
    
    if verbose is True:
        if logging is True:
            logging = False
        else:
            pass

        if verbose_level == 'super':
            verbose = '-vv'
        else:
            verbose = '-v'
    else:
        verbose = ''
    
    if show_progress is True:
        show_progress = '-P'
    else:
        show_progress = ''
    
    if check_first is True:
        check_first = '--check-first'
    else:
        check_first = ''
    
    if fast_list is True:
        fast_list = '--fast-list'
    else:
        fast_list = ''
    
    if update_mod_time is True:
        update_mod_time = ''
    else:
        update_mod_time = '--no-update-modtime'
    
    if compare == 'checksum':
        compare = '--checksum'
    elif compare == 'only-mod-time':
        compare = '--ignore-size'
    elif compare == 'only-size':
        compare = '--size-only'
    elif compare == 'only-checksum':
        compare = '--checksum --ignore-size'
    else:
        compare = ''
    
    if logging is True:
        if verbose is True:
            logging = False
        else:
            pass

        if log_path == '':
            sys.exit('The log path cannot be empty!')
        else:
            pass
        
        if log_mode == 'json':
            log_mode = "--use-json-log"
            log_ext = '.json'
        else:
            log_mode = ''
            log_ext = '.txt'
        
        if log_level == "debug" or log_level == "DEBUG":
            log_level = "DEBUG"
        elif log_level == "info" or log_level == "INFO":
            log_level = "INFO"
        elif log_level == "error" or log_level == "ERROR":
            log_level = "DEBUG"
        else:
            log_level = "NOTICE"
        
        logging = f'--log-file="{log_path}/{log_name}{log_ext}" {log_mode} --log-level {log_level}'
        log_switch = True
    else:
        logging = ''
        log_path = ''
        log_name = ''
        log_ext = ''
        log_mode = ''
        log_level = ''
        log_switch = False
    #==================================================#==================================================#

    # Get all the service account names under the specified path (service_account_path).
    # Splits out the path and leaving only the file name.
    # Store the file names into a list
    for file in glob.glob(f'{service_account_path}/*.json'):
        tmp_var = file.split('\\')[-1].split(',')[0]
        service_account_list.append(tmp_var)

    # Call randomly from the service account list
    service_account = random.choice(service_account_list)

    for x in range(var_loop):
        clear_output()

        # print(f'Performing task for {var_loop} time(s).\n')
        print(('=' * 80))
        print(f'Source: {source}')
        print(f'Destination: {destination}')
        print(f'Using service account: {service_account}\n')
        if test_switch is True:
            print('rclone is currently running in simulated mode!')
        else:
            pass
        if log_switch is True:
            print(f'Logging is enabled! ({log_path}/{log_name}{log_ext})')
        else:
            pass
        print('')

        cmd = f'"{rclone_path}/rclone.exe" {mode} "{source}" "{destination}" {dry_run} {verbose} {show_progress} {compare} {check_first} {fast_list} {update_mod_time} {flags} --drive-service-account-file="{service_account_path}/{service_account}" {logging}'
        subprocess.run(cmd, shell=False)

        # Adds some line break to the log file.
        # If the log is a json file, ignore it, as json does NOT support comment.
        # If the log file is just a normal standard .txt file, then write line breaks.
        if log_switch is True:
            if log_mode == 'json':
                pass
            else:
                try:
                    log_file = open(f'{log_path}/{log_name}{log_ext}', 'a')
                    log_file.write('\n' + ('=' * 80) + '\n' + 'GSAclone' + '\n' + ('=' * 80) + '\n\n')
                    log_file.close()
                except:
                    pass
        else:
            pass

        print('\n' + ('=' * 80))
        # print(f'Delaying the next task for {var_sleep} second(s).')
        time.sleep(var_sleep)

    sys.exit()

if __name__ == '__main__':
    GSAclone()
