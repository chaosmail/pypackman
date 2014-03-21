from subprocess import call, check_output

import os.path
import getopt
import sys


class Packman:

        setup_file_name = 'setup.py'
        requirements_file_name = 'requirements.txt'

        cmd_python = 'python3'
        cmd_virtualenv = 'virtualenv'

        ve_python = 'python3'
        ve_cmd_python = 'python3'
        ve_cmd_pip = 'pip3'

        app_name = ''
        app_version = ''

        version = '0.0.1'
        requirements = False
        verbose = False
        output = 'build'

        @staticmethod
        def is_valid():

            if not os.path.isfile(Packman.setup_file_name):
                print("No setup.py file found. Aborting Packman.")
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

            options, remainder = getopt.getopt(sys.argv[1:], 'o:rav',
                                               ['output=', 'requirements', 'activate', 'verbose', 'version'])

            for opt, arg in options:
                if opt in ('-o', '--output'):
                    Packman.output = arg
                elif opt in ('-r', '--requirements'):
                    Packman.requirements = True
                elif opt in ('-v', '--verbose'):
                    Packman.verbose = True
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
        def parse_output(string):

            return str(string).replace("\\r", "").replace("\\n", "").replace("b'", "").replace("'", "")

        @staticmethod
        def run():

            # Check if I can run PyPackman here
            Packman.is_valid()

            Packman.app_name = Packman.parse_output(check_output([Packman.cmd_python, Packman.setup_file_name, '--name']))
            Packman.app_version = Packman.parse_output(check_output([Packman.cmd_python, Packman.setup_file_name, '--version']))

            # Parse commandline arguments
            Packman.parse_cl_args()

            cmd_python = Packman.get_dir() + '/bin/' + Packman.ve_cmd_python
            cmd_pip = Packman.get_dir() + '/bin/' + Packman.ve_cmd_pip

            # Install Virtual Environment
            print("** PACKMAN **")
            print("Running CMD:", Packman.cmd_virtualenv,
                  '--distribute', '--no-site-packages',
                  '--python', Packman.ve_python, Packman.get_dir())
            call([Packman.cmd_virtualenv, '--distribute', '--no-site-packages', '--python', Packman.ve_python, Packman.get_dir()])

            if Packman.has_requirements():
                print("** PACKMAN **")
                print("Running CMD:", cmd_pip, 'install', '-r', Packman.requirements_file_name)
                call([cmd_pip, 'install', '-r', Packman.requirements_file_name])

            # Install the application
            print("** PACKMAN **")
            print("Running CMD:", cmd_pip, 'install', '.', '--upgrade')
            call([cmd_pip, 'install', '.', '--upgrade'])
