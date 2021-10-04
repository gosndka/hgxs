#--------------------------------------------------#--------------------------------------------------#
# GSAclone -- rclone with multiple and randomized Google Service Accounts.
# https://github.com/shirooo39/GSAclone
#
# This script is PROVIDED FOR FREE, AS IS, WITHOUT ANY WARRANTY, and released under the MIT License.
# Please also keep in mind that this script is far from perfeect.
#--------------------------------------------------#--------------------------------------------------#

import subprocess, sys

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

    version = (3, 5)

    if sys.version_info < version:
        print(f'Your Python version is: {sys.version}')
        sys.exit('Python 3.5 or newer is required to run this script.')
    else:
        pass

def GSAclone():
    get_os()
    python_version()
    clear_output()

    import pathlib, glob, time, random, argparse

    parser = argparse.ArgumentParser(description='rclone but with multiple Google Service Accounts.')
    parser.add_argument('-m', '--mode', help='copy or sync', required=False)
    parser.add_argument('-s', '--source', help='Example: --source remote_1:', required=True)
    parser.add_argument('-d', '--destination', help='Example: --destination remote_2:', required=True)
    cmd_args = vars(parser.parse_args())

    #==================================================#==================================================#
    var_loop = 3
    var_sleep = 60

    rclone_path = pathlib.Path(r'D:\path\to\rclone') # Only change the text inside the single quotation ('') maarks!
    service_account_path = pathlib.Path(r'D:\path\to\service_account') # Only change the text inside the single quotation ('') maarks!
    service_account_list = []

    dry_run = False
    verbose = False
    verbose_level = 'default' # Set this to either "default" or "super".
    # logging = False
    # log_path = ''
    # log_mode = 'default'
    # log_level = 'default'
    show_progress = True
    check_first = False
    fast_list = False
    update_mod_time = True
    compare = 'default'   # rclone compare mode:
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
    #==================================================#==================================================#

    #==================================================#==================================================#
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
    
    if dry_run is True:
        dry_run = '--dry-run'
    else:
        dry_run = ''
    
    if verbose is True:
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

        print(f'Performing task for {var_loop} time(s).')
        print('\n' + ('=' * 70))
        print(f'Source: {source}')
        print(f'Destination: {destination}')
        print(f'Using service account: {service_account}')
        print('')

        cmd = f'"{rclone_path}/rclone.exe" {mode} "{source}" "{destination}" {dry_run} {verbose} {show_progress} {compare} {check_first} {fast_list} {update_mod_time} {flags} --drive-service-account-file={service_account_path}/{service_account}'
        subprocess.run(cmd, shell=True)

        print('')
        print(('=' * 70) + '\n')

        print(f'Delaying the next task for {var_sleep} second(s).')
        time.sleep(var_sleep)

if __name__ == '__main__':
    GSAclone()
