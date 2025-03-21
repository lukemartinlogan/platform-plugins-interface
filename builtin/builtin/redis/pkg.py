"""
This module provides classes and methods to launch Redis.
Redis cluster is used if the hostfile has many hosts
"""
from jarvis_cd.basic.pkg import Application
from jarvis_util import *


class Redis(Application):
    """
    This class provides methods to launch the Ior application.
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
                'name': 'port',
                'msg': 'The port to use for the cluster',
                'type': int,
                'default': 6379,
                'choices': [],
                'args': [],
            },
        ]

    def _configure(self, **kwargs):
        """
        Converts the Jarvis configuration to application-specific configuration.
        E.g., OrangeFS produces an orangefs.xml file.

        :param kwargs: Configuration parameters for this pkg.
        :return: None
        """
        # Create the redis hostfile
        self.copy_template_file(f'{self.pkg_dir}/config/redis.conf',
                                f'{self.shared_dir}/redis.conf',
                                {
                                    'PORT': self.config['port']
                                })

    def start(self):
        """
        Launch an application. E.g., OrangeFS will launch the servers, clients,
        and metadata services on all necessary pkgs.

        :return: None
        """
        hostfile = self.hostfile
        host_str = [f'{host}:{self.config["port"]}' for host in hostfile.hosts]
        host_str = ' '.join(host_str)
        cluster_config_file = f'{self.private_dir}/nodes.conf'
        # Create redis servers
        self.log('Starting individual servers', color=Color.YELLOW)
        cmd = [
            'redis-server',
            f'{self.shared_dir}/redis.conf',
        ]
        if len(hostfile) > 1:
            cmd += [
                f'--cluster-enabled yes',
                f'--cluster-config-file {cluster_config_file}',
                f'--cluster-node-timeout 5000',
            ]

        cmd = ' '.join(cmd)
        Exec(cmd,
             PsshExecInfo(env=self.mod_env,
                          hostfile=hostfile,
                          do_dbg=self.config['do_dbg'],
                          dbg_port=self.config['dbg_port'],
                          exec_async=True))
        self.log(f'Sleeping for {self.config["sleep"]} seconds', color=Color.YELLOW)
        time.sleep(self.config['sleep'])

        # Create redis clients
        if len(hostfile) > 1:
            self.log('Flushing all data and resetting the cluster', color=Color.YELLOW)
            for host in hostfile.hosts:
                Exec(f'redis-cli -p {self.config["port"]} -h {host} flushall',
                     LocalExecInfo(env=self.mod_env,
                                   hostfile=hostfile,
                                   do_dbg=self.config['do_dbg'],
                                   dbg_port=self.config['dbg_port']))
                Exec(f'redis-cli -p {self.config["port"]} -h {host} cluster reset',
                     LocalExecInfo(env=self.mod_env,
                                   hostfile=hostfile,
                                   do_dbg=self.config['do_dbg'],
                                   dbg_port=self.config['dbg_port']))

            self.log('Creating the cluster', color=Color.YELLOW)
            cmd = [
                'redis-cli',
                f'--cluster create {host_str}',
                '--cluster-replicas 0',
                '--cluster-yes'
            ]
            cmd = ' '.join(cmd)
            print(cmd)
            Exec(cmd,
                 LocalExecInfo(env=self.mod_env,
                               hostfile=hostfile,
                               do_dbg=self.config['do_dbg'],
                               dbg_port=self.config['dbg_port']))
            self.log(f'Sleeping for {self.config["sleep"]} seconds', color=Color.YELLOW)
            time.sleep(self.config['sleep'])

    def stop(self):
        """
        Stop a running application. E.g., OrangeFS will terminate the servers,
        clients, and metadata services.

        :return: None
        """
        for i in range(3):
            Kill('redis-server',
                 PsshExecInfo(env=self.env,
                              hostfile=self.hostfile))

    def clean(self):
        """
        Destroy all data for an application. E.g., OrangeFS will delete all
        metadata and data directories in addition to the orangefs.xml file.

        :return: None
        """
        pass
