#!/usr/bin/env python

import sys
import os
import subprocess

if os.environ.get('ROOT_PRJ_DIR') is None:
    print('ROOT_PRJ_DIR must be set before starting\n')
    sys.exit(1)

def run_command(command):

  process = subprocess.Popen(command, shell=True)
  process.wait()
  
  return process.returncode

def print_help():
    print('To run unittests:          python3 build/xrun.py -u')  
    print('To run curl tests:         python3 build/xrun.py -c')  
    print('To start flask server:     python3 build/xrun.py -s')      
    print('To print help:             python3 build/xrun.py -h')  
    
if __name__ == '__main__':
    if '--unittest' in sys.argv or '-u' in sys.argv:
        subprocess.call([sys.executable, '-m', 'unittest', 'discover', '-s', os.environ.get('ROOT_PRJ_DIR') + os.sep + 'components' + os.sep + 'test'])
    if '--start-server' in sys.argv or '-s' in sys.argv:
        command = '. ' + os.environ.get('ROOT_PRJ_DIR') + os.sep + 'build' + os.sep + 'activate_prj_venv.sh && FLASK_APP=' + os.environ.get('ROOT_PRJ_DIR') + os.sep + 'components' + os.sep + 'impl' + os.sep + 'server' + os.sep + 'app.py flask run'
        exit_code = run_command(command)
    if '--curl-tests' in sys.argv or '-c' in sys.argv:
        command = '. ' + os.environ.get('ROOT_PRJ_DIR') + os.sep + 'build' + os.sep + 'test.sh'
        exit_code = run_command(command)        
    if '--help' in sys.argv or '-h' in sys.argv:
        print_help()

