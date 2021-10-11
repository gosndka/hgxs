#--------------------------------------------------#--------------------------------------------------#
# GSAclone -- rclone with multiple and randomized Google Service Accounts.
# https://github.com/shirooo39/GSAclone
#
# This script is PROVIDED FOR FREE, AS IS, WITHOUT ANY WARRANTY, and released under the MIT License.
# Please also keep in mind that this script is far from perfeect.
#--------------------------------------------------#--------------------------------------------------#

import sys, pathlib, subprocess, configparser, glob, time, random, argparse

def clear_output():
    os_name = check_os()

    if os_name == 'windows':
        subprocess.run('cls', shell=True)
    else:
        subprocess.run('clear', shell=True)
    
    return None

def check_os():
    if sys.platform.startswith('win32'):
        os_name = 'windows'
    elif sys.platform.startswith('linux'):
        os_name = 'linux'
    else:
        sys.exit('Sorry! Unsupported OS!')

    return os_name

def check_python():
    clear_output()

    version = ".".join(map(str, sys.version_info[:3]))

    if sys.version_info < (3, 7):
        print(f'You are running Python version: {version}')
        sys.exit('Python 3.7 or newer is required to run this script!')
    else:
        pass

    return None

def check_cfg():
    clear_output()

    cfg_file = pathlib.Path(__file__).parent.resolve().joinpath('GSAclone.conf')
    parser = configparser.ConfigParser()

    if cfg_file.exists() and cfg_file.is_file():
        try:
            parser.read(cfg_file)

            if (parser.has_section('GSAclone') and parser.has_section('PATHS') and parser.has_section('OPTIONS')) is True:
                return True
            else:
                return False
        except:
            return False

        # return True
    elif cfg_file.exists() and cfg_file.is_dir():
        return False
    else:
        parser['GSAclone'] = {
            'task_repeat': '3',
            'task_delay': '60'
        }
        parser['PATHS'] = {
            'rclone': '/path/to/rclone',
            'service_account': '/path/to/service_accounts'
        }
        parser['OPTIONS'] = {
            'flags': '--max-transfer 740G -drive-acknowledge-abuse --drive-stop-on-upload-limit=true --drive-server-side-across-configs',
            'dry_run': 'False',
            'verbose': 'False',
            'verbose_level': 'default',
            'logging': 'False',
            'log_mode': 'default',
            'log_level': 'default',
            'show_progress': 'True',
            'check_first': 'False',
            'fast_list': 'False',
            'update_mod_time': 'True',
            'compare': 'default',
            'perform_check': 'False',
            'quick_check': 'False',
            'one_way_check': 'False',
            'check_mode': 'default'
        }

        try:
            with open((f'{cfg_file}'), 'w') as to_file:
                parser.write(to_file)
        except:
            sys.exit('Error when generating the configuration file!')

#==================================================#==================================================#
# These functions are not working properly. Inspect later...
#==================================================#==================================================#
def check_rclone(rclone_path, _ext):
    clear_output()

    if rclone_path.exists() and rclone_path.is_dir():
        cmd = f'rclone{_ext} -h'

        try:
            subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=rclone_path)
        except:
            sys.exit('Unable to locate the rclone executable!')
    else:
        sys.exit('The specified rclone path does not exist!')
    
    return None

def check_service_account(service_account_path):
    clear_output()

    if service_account_path.exists() and service_account_path.is_dir():
        sa_none = not bool(sorted(service_account_path.rglob('*.json')))

        if sa_none:
            sys.exit('The specified service account path does not seem to contain any service account file!')
        else:
            pass
    else:
        sys.exit('The specified service account path does not exist!')
    
    return None
#==================================================#==================================================#

def perform_remote_check(rclone_path, _ext, source, destination, show_progress, fast_list, quick_check, one_way_check, check_mode):
    clear_output()

    cmd = f'rclone{_ext} check "{source}" "{destination}" {show_progress} {fast_list} {quick_check} {one_way_check} {check_mode} "{rclone_path}/GSAclone_check.txt"'

    print('Performing check...\n')

    try:
        subprocess.run(cmd, shell=True, cwd=rclone_path)

        try:
            log_file = open(f'{rclone_path}/GSAclone_check.txt', 'a')

            try:
                log_file.write('\n' + ('=' * 80) + '\n' + 'GSAclone' + '\n' + ('=' * 80) + '\n\n')
            except:
                print('Something went wrong when writing to the file!')
            finally:
                log_file.close()
        except:
            pass

        print(f'\nCheck reports are printed into: {rclone_path}/GSAclone_check.txt')
        print('=' * 80)
    except:
        pass

    return None

def main():
    clear_output()

    check_os()
    check_python()
    check_cfg()

    parser = argparse.ArgumentParser(description='rclone with multiple and randomized Google Service Accounts.')
    parser.add_argument('-m', '--mode', help='copy, sync or check', required=True)
    parser.add_argument('-s', '--source', help='Example: --source remote_1:', required=True)
    parser.add_argument('-d', '--destination', help='Example: --destination remote_2:', required=True)
    cmd_args = vars(parser.parse_args())

    #==================================================#==================================================#
    #
    # Declare Variables -- DO NOT CHANGE ANY OF THESE VARIABLES! CHANGE THE .conf FILE INSTEAD!
    #
    if check_cfg() is True:
        cfg_file = pathlib.Path(__file__).parent.resolve().joinpath('GSAclone.conf')
        parser = configparser.ConfigParser()
        parser.read(cfg_file)

        #--------------------------------------------------
        task_repeat = parser.getint('GSAclone', 'task_repeat')
        task_delay = parser.getint('GSAclone', 'task_delay')
        #--------------------------------------------------
        rclone_path = pathlib.Path(parser.get('PATHS', r'rclone'))
        service_account_path = pathlib.Path(parser.get('PATHS', r'service_account'))
        service_account_list = []
        log_path = rclone_path
        #--------------------------------------------------
        flags = parser.get('OPTIONS', 'flags')
        dry_run = parser.getboolean('OPTIONS', 'dry_run')
        verbose = parser.getboolean('OPTIONS', 'verbose')
        verbose_level = parser.get('OPTIONS', 'verbose_level')
        logging = parser.getboolean('OPTIONS', 'logging')
        log_name = 'GSAclone_log'
        log_mode = parser.get('OPTIONS', 'log_mode')
        log_level = parser.get('OPTIONS', 'log_level')
        show_progress = parser.getboolean('OPTIONS', 'show_progress')
        check_first = parser.getboolean('OPTIONS', 'check_first')
        fast_list = parser.getboolean('OPTIONS', 'fast_list')
        update_mod_time = parser.getboolean('OPTIONS', 'update_mod_time')
        compare = parser.get('OPTIONS', 'compare')
        perform_check = parser.getboolean('OPTIONS', 'perform_check')
        quick_check = parser.getboolean('OPTIONS', 'quick_check')
        one_way_check = parser.getboolean('OPTIONS', 'one_way_check')
        check_mode = parser.get('OPTIONS', 'check_mode')
        #--------------------------------------------------
    else:
        sys.exit('Error when reading the configuration file!')
    #==================================================#==================================================#

    #==================================================#==================================================#
    os_name = check_os()

    if os_name == 'windows':
        _ext = '.exe'

        # if rclone_path == 'default':
        #     sys.exit(f'The path value {rclone_path} is not accepted in Windows, as rclone does not need to be installed on Windows.')
        # else:
        #     if service_account_path == 'default':
        #         service_account_path = f'{rclone_path}/service_accounts'
        #     else:
        #         pass
    else:
        _ext = ''

        # if rclone_path == 'default':
        #     rclone_path = pathlib.Path('/usr/bin').as_posix()
        # else:
        #     pass

        # if service_account_path == 'default':
        #     service_account_path = f'{rclone_path}/service_accounts'
        # else:
        #     pass
    #==================================================#==================================================#

    #==================================================#==================================================#
    # This bock is not working properly. Inspect later...
    #==================================================#==================================================#
    check_rclone(rclone_path, _ext)
    check_service_account(service_account_path)
    #==================================================#==================================================#

    #==================================================#==================================================#
    if (cmd_args['mode'] == "copy") or (cmd_args['mode'] == "sync") or (cmd_args['mode'] == "check"):
        mode = cmd_args['mode']
    else:
        sys.exit('The operation mode could only be: copy, sync or check!')

    if cmd_args['source'] is None:
        sys.exit("The remote source cannot be empty!")
    else:
        source = cmd_args['source']

    if cmd_args['destination'] is None:
        sys.exit("The remote destination cannot be empty!")
    else:
        destination = cmd_args['destination']

    if dry_run is True:
        dry_run = '--dry-run'
        test_message = True
    else:
        dry_run = ''
        test_message = False

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
        log_message = True
    else:
        logging = ''
        log_path = ''
        log_name = ''
        log_ext = ''
        log_mode = ''
        log_level = ''
        log_message = False

    if quick_check is True:
        quick_check = '--size-only'
    else:
        quick_check = ''

    if one_way_check is True:
        one_way_check = '--one-way'
    else:
        one_way_check = ''

    if check_mode == 'missing-on-source':
        check_mode = '--missing-on-src'
    elif check_mode == 'missing-on-desination':
        check_mode = '--missing-on-dst'
    elif check_mode == 'match':
        check_mode = '--match'
    elif check_mode == 'error':
        check_mode = '--error'
    elif check_mode == 'combined':
        check_mode = '--combined'
    else:
        check_mode = '--differ'
    #==================================================#==================================================#

    # Get all the service account names under the specified path (service_account_path).
    # Splits out the path and leaving only the file name.
    # Store the file names into a list
    for file in glob.glob(f'{service_account_path}/*.json'):
        tmp_var = file.split('/')[-1].split('\\')[-1].split(',')[0]
        service_account_list.append(tmp_var)

    # Call randomly from the service account list
    service_account = random.choice(service_account_list)

    if cmd_args['mode'] == 'check':
        clear_output()

        print(('=' * 80))
        perform_remote_check(rclone_path, _ext, source, destination, show_progress, fast_list, quick_check, one_way_check, check_mode)
    else:
        for x in range(task_repeat):
            clear_output()

            print(('=' * 80))
            print(f'Source: {source}')
            print(f'Destination: {destination}')
            print(f'Using service account: {service_account}\n')

            if test_message is True:
                print('rclone is currently running in simulated mode!')
            else:
                pass

            if log_message is True:
                print(f'Logging is enabled! ({log_path}/{log_name}{log_ext})')
            else:
                pass
            print('')

            cmd = f'rclone{_ext} {mode} "{source}" "{destination}" {dry_run} {verbose} {show_progress} {compare} {check_first} {fast_list} {update_mod_time} {flags} --drive-service-account-file="{service_account_path}/{service_account}" {logging}'
            subprocess.run(cmd, shell=True, cwd=rclone_path)

            # Adds some line break to the log file.
            # If the log is a json file, ignore it, as json does NOT support comment.
            # If the log file is just a normal standard .txt file, then write line breaks.
            if log_message is True:
                if log_mode == 'json':
                    pass
                else:
                    try:
                        log_file = open(f'{log_path}/{log_name}{log_ext}', 'a')

                        try:
                            log_file.write('\n' + ('=' * 80) + '\n' + 'GSAclone' + '\n' + ('=' * 80) + '\n\n')
                        except:
                            pass
                        finally:
                            log_file.close()
                    except:
                        pass
            else:
                pass

            print('\n' + ('=' * 80) + '\n')
            time.sleep(task_delay)

        if perform_check is True:
            perform_remote_check(rclone_path, _ext, source, destination, show_progress, fast_list, quick_check, one_way_check, check_mode)
        else:
            pass

    sys.exit()

if __name__ == '__main__':
    main()
