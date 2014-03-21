from subprocess import call, check_output

import os
import getopt
import sys
import shutil

python_latest = {}
python_latest['2'] = '2.7.6'
python_latest['2.7'] = '2.7.6'
python_latest['3'] = '3.3.5'
python_latest['3.3'] = '3.3.5'
python_latest['3.4'] = '3.4.0'

python_src = {}
python_src['2'] = 'https://www.python.org/ftp/python/'+python_latest['2']+'/Python-'+python_latest['2']+'.tgz'
python_src['2.7'] = 'https://www.python.org/ftp/python/'+python_latest['2.7']+'/Python-'+python_latest['2.7']+'.tgz'
python_src['3'] = 'https://www.python.org/ftp/python/'+python_latest['3']+'/Python-'+python_latest['3']+'.tgz'
python_src['3.3'] = 'https://www.python.org/ftp/python/'+python_latest['3.3']+'/Python-'+python_latest['3.3']+'.tgz'
python_src['3.4'] = 'https://www.python.org/ftp/python/'+python_latest['3.4']+'/Python-'+python_latest['3.4']+'.tgz'

pip_source = 'https://raw.github.com/pypa/pip/master/contrib/get-pip.py'


class Packman:

        setup_file_name = 'setup.py'
        requirements_file_name = 'requirements.txt'

        cmd_load = 'wget'
        cmd_zip = 'tar'
        cmd_python = 'python3'
        cmd_virtualenv = 'virtualenv'

        ve_python = 'python'
        ve_cmd_python = 'python'
        ve_cmd_pip = 'pip'

        app_name = ''
        app_version = ''

        version = '0.0.1'
        python_version = '3'
        clear_target = False
        requirements = False
        verbose = False
        include_python = False
        zip_output = False
        output = 'build'

        @staticmethod
        def setup_is_valid():

            if not os.path.isfile(Packman.setup_file_name):
                print("No setup.py file found. Aborting Packman.")
                exit()

        @staticmethod
        def python_is_valid():

            binaries = Packman.parse_output(check_output(['ls', '/usr/bin']))

            if not Packman.ve_cmd_python in binaries:
                print("Python version", Packman.python_version, "not found. Aborting Packman.")
                exit()

        @staticmethod
        def has_requirements():

            if not Packman.requirements:
                return False

            if os.path.isfile(Packman.requirements_file_name):
                return True

            return False

        @staticmethod
        def parse_cl_args():

            options, remainder = getopt.getopt(sys.argv[1:], 'o:rivzp:',
                    ['output=', 'requirements', 'include-python', 'verbose', 'version', 'zip', 'python', 'package'])

            for opt, arg in options:
                if opt in ('-o', '--output'):
                    Packman.output = arg
                if opt in ('-p', '--python'):
                    Packman.python_version = arg
                elif opt in ('-r', '--requirements'):
                    Packman.requirements = True
                elif opt in ('-i', '--include-python'):
                    Packman.include_python = True
                elif opt in ('-v', '--verbose'):
                    Packman.verbose = True
                elif opt in ('-z', '--zip'):
                    Packman.zip_output = True
                elif opt == '--package':
                    Packman.requirements = True
                    Packman.include_python = True
                    Packman.clear_target = True
                    Packman.zip_output = True
                elif opt == '--version':
                    Packman.return_version()

        @staticmethod
        def return_version():

            print(Packman.version)
            exit()

        @staticmethod
        def get_dir():

            return Packman.output + '/' + Packman.app_name + '-' + Packman.app_version

        @staticmethod
        def get_python_dir():

            return Packman.get_dir() + '/build/Python-' + python_latest[Packman.python_version]

        @staticmethod
        def parse_output(string):

            return str(string).replace("\\r", "").replace("\\n", "").replace("b'", "").replace("'", "")

        @staticmethod
        def virtual_python_environment():

            if os.path.isdir(Packman.get_python_dir()):
                shutil.rmtree(Packman.get_python_dir())

            print("** PACKMAN **")
            print("Running CMD:", Packman.cmd_virtualenv, '--no-site-packages', '--python', Packman.ve_cmd_python,
                  Packman.get_python_dir())
            call([Packman.cmd_virtualenv, '--no-site-packages', '--python', Packman.ve_cmd_python,
                  Packman.get_python_dir()])

        @staticmethod
        def include_python_environment():

            if os.path.isdir(Packman.get_python_dir()):
                shutil.rmtree(Packman.get_python_dir())

            current_path = os.getcwd()
            python_dir_name = 'Python-' + python_latest[Packman.python_version]

            python_dir = Packman.output + '/' + python_dir_name
            compressed_python_dir = Packman.output + '/' + python_dir_name + ".tgz"

            if os.path.isfile(compressed_python_dir):
                print("** PACKMAN **")
                print("File", compressed_python_dir, "already exists.")
            else:
                print("** PACKMAN **")
                print("Running CMD:", Packman.cmd_load, python_src[Packman.python_version], '-O', compressed_python_dir)
                call([Packman.cmd_load, python_src[Packman.python_version], '-O', compressed_python_dir])

            if not os.path.isdir(python_dir):
                print("** PACKMAN **")
                print("Running CMD:", Packman.cmd_zip, 'xfz', python_dir_name + '.tgz', '-C', Packman.output + '/')
                call([Packman.cmd_zip, 'xfz', compressed_python_dir, '-C', Packman.output + '/'])

            python_target_dir = current_path + '/' + Packman.get_dir() + '/' + python_dir

            if os.path.isdir(Packman.get_dir() + '/' + python_dir):
                os.rmdir(Packman.get_dir() + '/' + python_dir)

            os.chdir(python_dir)

            # Configure Python
            print("** PACKMAN **")
            print("Running CMD:", './configure', '--prefix', python_target_dir)
            call(['./configure', '--prefix', python_target_dir])

            # Compile Python and Install to target directory
            print("** PACKMAN **")
            print("Running CMD:", 'make && make install')
            call(['make'])
            call(['make', 'install'])

            os.chdir(current_path)

            get_pip = Packman.output + '/' + 'get-pip.py'

            if os.path.isfile(get_pip):
                print("** PACKMAN **")
                print("File", get_pip, "already exists.")
            else:
                print("** PACKMAN **")
                print("Running CMD:", Packman.cmd_load, pip_source, '-O', get_pip)
                call([Packman.cmd_load, pip_source, '-O', get_pip])

            cmd_python = Packman.get_python_dir() + '/bin/' + Packman.ve_cmd_python

            print("** PACKMAN **")
            print("Running CMD:", cmd_python, get_pip)
            call([cmd_python, get_pip])

        @staticmethod
        def run():

            # Check if I can run Packman here
            Packman.setup_is_valid()

            Packman.app_name = Packman.parse_output(check_output([Packman.cmd_python, Packman.setup_file_name, '--name']))
            Packman.app_version = Packman.parse_output(check_output([Packman.cmd_python, Packman.setup_file_name, '--version']))

            # Parse commandline arguments
            Packman.parse_cl_args()

            # Adapt the python executable with given version
            if Packman.python_version is not '2':
                Packman.ve_cmd_python += Packman.python_version.strip()
                Packman.ve_cmd_pip += Packman.python_version.strip()

            # Check if the python version exists
            Packman.python_is_valid()

            # Generate the new pip command
            cmd_pip = Packman.get_python_dir() + '/bin/' + Packman.ve_cmd_pip

            # Clear the output directory
            if Packman.clear_target and os.path.isdir(Packman.get_dir()):
                shutil.rmtree(Packman.get_dir())

            # Create output directory
            if not os.path.isdir(Packman.get_dir()):
                os.makedirs(Packman.get_dir())

            # Include complete Python environment
            if Packman.include_python:
                Packman.include_python_environment()

            # Include virtual Python environment
            if not Packman.include_python:
                Packman.virtual_python_environment()

            # Install Requirements
            if Packman.has_requirements():
                print("** PACKMAN **")
                print("Running CMD:", cmd_pip, 'install', '-r', Packman.requirements_file_name)
                call([cmd_pip, 'install', '-r', Packman.requirements_file_name])

            # Install the application
            print("** PACKMAN **")
            print("Running CMD:", cmd_pip, 'install', '.', '--upgrade')
            call([cmd_pip, 'install', '.', '--upgrade'])
