"""
This module provides classes and methods to launch the LabstorIpcTest application.
LabstorIpcTest is ....
"""
from jarvis_cd.basic.pkg import Application
from jarvis_util import *


class HermesUnitTests(Application):
    """
    This class provides methods to launch the LabstorIpcTest application.
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
                'name': 'TEST_CASE',
                'msg': 'Destroy previous configuration and rebuild',
                'type': str,
                'default': 'TestIpc'
            },
            {
                'name': 'nprocs',
                'msg': 'The number of processes to spawn',
                'type': int,
                'default': None,
            },
            {
                'name': 'ppn',
                'msg': 'The number of processes per node',
                'type': int,
                'default': 1,
            },
        ]

    def _configure(self, **kwargs):
        """
        Converts the Jarvis configuration to application-specific configuration.
        E.g., OrangeFS produces an orangefs.xml file.

        :param kwargs: Configuration parameters for this pkg.
        :return: None
        """
        pass

    def start(self):
        """
        Launch an application. E.g., OrangeFS will launch the servers, clients,
        and metadata services on all necessary pkgs.

        :return: None
        """
        nprocs = self.config['nprocs']
        if self.config['nprocs'] is None:
            nprocs = len(self.hostfile)
        test_ipc_execs = ['TestIpc', 'TestAsyncIpc', 'TestIO', 'TestIpcMultithread4', 'TestIpcMultithread8']
        test_config_execs = [
            'TestHermesPaths'
        ]
        test_hermes_execs = [
            'TestHermesPut1n', 'TestHermesPut', 'TestHermesSerializedPutGet',
            'TestHermesAsyncPut', 'TestHermesAsyncPutLocalFlush', 'TestHermesPutGet',
            'TestHermesPartialPutGet', 'TestHermesBlobDestroy',
            'TestHermesBucketDestroy', 'TestHermesReorganizeBlob',
            'TestHermesBucketAppend', 'TestHermesBucketAppend1n',
            'TestHermesConnect', 'TestHermesGetContainedBlobIds',
            'TestHermesMultiGetBucket', 'TestHermesDataStager',
            'TestHermesDataOp', 'TestHermesCollectMetadata', 'TestHermesDataPlacement',
            'TestHermesDataPlacementFancy', 'TestHermesCompress', 'hermes'
        ]
        test_latency_execs = ['TestRoundTripLatency',
                              'TestHshmQueueAllocateEmplacePop',
                              'TestWorkerLatency']
        test_ping_pong = ['TestPingPong']
        print(self.config['TEST_CASE'])
        if self.config['TEST_CASE'] in test_config_execs:
            Exec(f'test_config_exec {self.config["TEST_CASE"]}',
                 LocalExecInfo(hostfile=self.hostfile,
                             nprocs=nprocs,
                             ppn=self.config['ppn'],
                             env=self.env,
                             do_dbg=self.config['do_dbg'],
                             dbg_port=self.config['dbg_port']))
        elif self.config['TEST_CASE'] in test_ipc_execs:
            Exec(f'test_ipc_exec {self.config["TEST_CASE"]}',
                 MpiExecInfo(hostfile=self.hostfile,
                             nprocs=nprocs,
                             ppn=self.config['ppn'],
                             env=self.env,
                             do_dbg=self.config['do_dbg'],
                             dbg_port=self.config['dbg_port']))
        elif self.config['TEST_CASE'] in test_hermes_execs:
            case = self.config['TEST_CASE']
            if self.config['TEST_CASE'] == 'hermes':
                case = ''
            Exec(f'test_hermes_exec {case}',
                 MpiExecInfo(hostfile=self.hostfile,
                             nprocs=nprocs,
                             ppn=self.config['ppn'],
                             env=self.env,
                             do_dbg=self.config['do_dbg'],
                             dbg_port=self.config['dbg_port']))
        elif self.config['TEST_CASE'] in test_latency_execs:
            Exec(f'test_performance_exec {self.config["TEST_CASE"]}',
                 LocalExecInfo(env=self.env,
                             do_dbg=self.config['do_dbg'],
                             dbg_port=self.config['dbg_port']))
        elif self.config['TEST_CASE'] in test_ping_pong:
            Exec(f'test_ping_pong_exec',
                MpiExecInfo(nprocs=2,
                            ppn=2,
                            env=self.env,
                             do_dbg=self.config['do_dbg'],
                             dbg_port=self.config['dbg_port']))

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
