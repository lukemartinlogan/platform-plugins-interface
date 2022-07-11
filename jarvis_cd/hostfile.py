import os
from jarvis_cd.exception import Error, ErrorCode

class Hostfile:
    def __init__(self):
        self.all_hosts = None
        self.hosts = None
        self.path = None

    def LoadHostfile(self, path):
        if not os.path.exists(path):
            raise Error(ErrorCode.HOSTFILE_NOT_FOUND).format(path)
        a_file = open(path, "r")
        list_of_lists = []
        for line in a_file:
            stripped_line = line.strip()
            line_list = stripped_line.split(sep=":")
            if len(line_list) == 2:
                for i in range(int(line_list[1])):
                    list_of_lists.append(line_list[0])
            else:
                list_of_lists.append(line_list[0])
        a_file.close()
        self.all_hosts = list_of_lists
        self.hosts = self.all_hosts
        self.path = path
        return self

    def SetHosts(self, hosts):
        self.all_hosts = hosts
        self.hosts = hosts
        return self

    def Load(self, hosts):
        if hosts is None:
            hosts = []
        if isinstance(hosts, str):
            self.LoadHostfile(hosts)
        else:
            self.SetHosts(hosts)
        return self

    def SelectHosts(self, hostset):
        #Hosts are numbered from 1
        hostset = str(hostset)
        hosts = self.copy()
        hosts.hosts = []
        ranges = hostset.split(',')
        for range in ranges:
            range = range.split('-')
            if len(range) == 2:
                min = int(range[0])
                max = int(range[1])
                hosts.hosts += hosts.all_hosts[min-1:max]
            else:
                val = int(range[0])
                hosts.hosts += [hosts.all_hosts[val-1]]
        return hosts

    def Path(self):
        return self.path

    def list(self):
        return self.hosts

    def enumerate(self):
        return enumerate(self.hosts)

    def to_str(self, sep=','):
        return sep.join(self.hosts)

    def copy(self):
        hosts = Hostfile()
        if self.all_hosts:
            hosts.all_hosts = self.all_hosts.copy()
        if self.hosts:
            hosts.hosts = self.hosts.copy()
        return hosts

    def __len__(self):
        return len(self.hosts)

    def __getitem__(self, idx):
        return self.hosts[idx]
