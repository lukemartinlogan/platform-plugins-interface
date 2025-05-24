from jarvis_cd.basic.pkg import Service
from jarvis_util import *
import os


class OrangefsFuse:
    def fuse_start(self):
        # start pfs servers
        for host in self.server_hosts:
            # pvfs2_server = os.path.join(self.orangefs_root,"sbin","pvfs2-server")
            server_start_cmds = [
                f"pvfs2-server {self.pfs_conf} -f -a {host}",
                f"pvfs2-server {self.pfs_conf} -a {host}"
            ]
            Exec(server_start_cmds, hosts=host)
        
        self.Status()

        # start pfs client
        # pvfs2_fuse = os.path.join(self.orangefs_root, "bin", "pvfs2fuse")
        for i,client in self.client_hosts.enumerate():
            mdm_ip = self.md_hosts.hostname_list()[i % len(self.md_hosts)]
            start_client_cmds = [
                "pvfs2fuse -o fs_spec={protocol}://{ip}:{port}/pfs {mount_point}".format(
                    pvfs2_fuse=pvfs2_fuse,
                    protocol=self.config['protocol'],
                    port=self.config['port'],
                    ip=mdm_ip,
                    mount_point=self.config['mount'])
            ]
            Exec(start_client_cmds, hosts=client)

    def fuse_stop(self):
        cmds = [
            f"umount -l {self.config['mount']}",
            f"umount -f {self.config['mount']}",
            f"umount {self.config['mount']}"
        ]
        Exec(cmds, hosts=self.client_hosts)

        Kill('.*pvfs2-client.*', PsshExecInfo(hosts=self.client_hosts,
                                        env=self.env))
        Kill('pvfs2-server',
             PsshExecInfo(hosts=self.server_hosts,
                          env=self.env))
        Exec("pgrep -la pvfs2-server", hosts=self.client_hosts)
