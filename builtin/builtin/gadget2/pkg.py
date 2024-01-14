"""
This module provides classes and methods to launch the Gadget2 application.
Gadget2 is ....
"""
from jarvis_cd.basic.pkg import Application
from jarvis_util import *


class Gadget2(Application):
    """
    This class provides methods to launch the Gadget2 application.
    """
    def _init(self):
        """
        Initialize paths
        """
        pass

    def _configure_menu(self):
        """
        Create a CLI menu for the configurator method.
        For thorough documentation of these parameters, view:
        https://github.com/scs-lab/jarvis-util/wiki/3.-Argument-Parsing

        :return: List(dict)
        """
        return [
            {
                'name': 'nprocs',
                'msg': 'Number of processes to spawn',
                'type': int,
                'default': 4,
            },
            {
                'name': 'ppn',
                'msg': 'Processes per node',
                'type': int,
                'default': None,
            },
            {
                'name': 'j',
                'msg': 'Number of threads to use for building gadget',
                'type': int,
                'default': 8,
            },
            {
                'name': 'test_case',
                'msg': 'The test case to use',
                'type': str,
                'default': 'gassphere',
            },
            {
                'name': 'out',
                'msg': 'The directory to output data to',
                'type': str,
                'default': '${HOME}/gadget_data',
            },
        ]

    def _configure(self, **kwargs):
        """
        Converts the Jarvis configuration to application-specific configuration.
        E.g., OrangeFS produces an orangefs.xml file.

        :param kwargs: Configuration parameters for this pkg.
        :return: None
        """
        test_case = self.config['test_case']
        paramfile = f'{self.config_dir}/{test_case}.param'
        self.copy_template_file(f'{self.pkg_dir}/paramfiles/{test_case}.param',
                                paramfile,
                                replacements={
                                    'REPO_DIR': self.env['GADGET_PATH'],
                                    'OUTPUT_DIR': self.config['out']
                                })
        build_dir = f'{self.shared_dir}/build'
        Cmake(self.env['GADGET2_PATH'],
              build_dir,
              opts=YamlFile('').Load(f'{self.pkg_dir}/config/{test_case}.yaml'))
        Make(build_dir, nthreads=self.config['j'])

    def start(self):
        """
        Launch an application. E.g., OrangeFS will launch the servers, clients,
        and metadata services on all necessary pkgs.

        :return: None
        """
        pass

    def stop(self):
        """
        Stop a running application. E.g., OrangeFS will terminate the servers,
        clients, and metadata services.

        :return: None
        """
        pass

    def clean(self):
        """
        Destroy all data for an application. E.g., OrangeFS will delete all
        metadata and data directories in addition to the orangefs.xml file.

        :return: None
        """
        pass
