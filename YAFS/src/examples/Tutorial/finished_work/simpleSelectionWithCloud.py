from yafs.selection import Selection
import networkx as nx
import math


class FIFO(Selection):

    # def __init__(self, hm):
    #     self.hm = hm

    def get_path(self, sim, app_name, message, topology_src, alloc_DES, alloc_module, traffic, from_des):
        """
        Computes the minimun path among the source elemento of the topology and the localizations of the module

        Return the path and the identifier of the module deployed in the last element of that path
        """
        node_src = topology_src
        DES_dst = alloc_module[app_name][message.dst]

        print("GET PATH")
        print("\tNode _ src (id_topology): %i" % node_src)
        print("\tRequest service: %s " % message.dst)
        print("\tProcess serving that service: %s " % DES_dst)

        bestPath = []
        bestDES = []

        for des in DES_dst:  ## In this case, there are only one deployment
            dst_node = alloc_DES[des]
            print("\t\t Looking the path to id_node: %i" % dst_node)

            path = list(nx.shortest_path(sim.topology.G, source=node_src, target=dst_node))

            bestPath = [path]
            bestDES = [des]

        return bestPath, bestDES


class RoundRobin(Selection):

    def __init__(self):
        self.rr = {}  # for a each type of service, we have a mod-counter

    def get_path(self, sim, app_name, message, topology_src, alloc_DES, alloc_module, traffic, from_des):
        """
        Computes the minimun path among the source elemento of the topology and the localizations of the module
        Return the path and the identifier of the module deployed in the last element of that path
        """
        node_src = topology_src
        DES_dst = alloc_module[app_name][message.dst]  # returns an array with all DES process serving

        print("alloc module " + str(alloc_module[app_name]))

        if message.dst not in self.rr.keys():
            self.rr[message.dst] = 0

        print("GET PATH")
        print("\tNode _ src (id_topology): %i" % node_src)
        print("\tRequest service: %s " % (message.dst))
        print("\tProcess serving that service: %s (pos ID: %i)" % (DES_dst, self.rr[message.dst]))

        bestPath = []
        bestDES = []
        print("Round Robin * ***************************")

        for ix, des in enumerate(DES_dst):
            print("DES " + str(DES_dst))
            print("ix %i" % ix)
            print("des %i" % des)

            print(message.dst)

            if message.name == "M.A" or message.name == "M.B" or message.name == "M.C" or message.name == "M.D":
                print("rr dict " + str(self.rr))

                if self.rr[message.dst] == ix:
                    dst_node = alloc_DES[des]

                    print("DST NOde" + str(dst_node))
                    path = list(nx.shortest_path(sim.topology.G, source=node_src, target=dst_node))
                    print("path " + str(path))

                    bestPath = [path]
                    bestDES = [des]

                    self.rr[message.dst] = (self.rr[message.dst] + 2) % len(DES_dst)
                    break
            else:  # message.name == "M.B or M.D"

                dst_node = alloc_DES[des]

                print("ix %i" % ix)
                print("des %i" % des)

                path = list(nx.shortest_path(sim.topology.G, source=node_src, target=dst_node))
                if message.broadcasting:
                    bestPath.append(path)
                    bestDES.append(des)
                else:
                    bestPath = [path]
                    bestDES = [des]

        return bestPath, bestDES


class MinPathTraffic(Selection):

    def get_path(self, sim, app_name, message, topology_src, alloc_DES, alloc_module, traffic, from_des):
        """
        Computes the minimun path among the source elemento of the topology and the localizations of the module
        Return the path and the identifier of the module deployed in the last element of that path
        """
        print("Traffic " + str(traffic))
        node_src = topology_src
        DES_dst = alloc_module[app_name][message.dst]  # returns an array with all DES process serving

        print("alloc module " + str(alloc_module[app_name]))

        msgType = message.getMsgType()

        print("MSG TYPE" + str(msgType))

        # if msgType not in self.hm.keys():
        #     self.hm[msgType] = -1

        print("GET PATH")
        print("\tNode _ src (id_topology): %i" % node_src)
        print("\tRequest service: %s " % message.dst)
        #        print("\tProcess serving that service: %s (pos ID: %i)" % (DES_dst, self.rr[message.dst]))

        bestPath = []
        bestDES = []
        print("Round Robin * ***************************")
        maxDiff = -math.inf

        # if self.hm[msgType] != -1:
        #
        #     des = self.hm[msgType]
        #     dst_node = alloc_DES[des]
        #     print("DST NOde" + str(dst_node))
        #     path = list(nx.shortest_path(sim.topology.G, source=node_src, target=dst_node))
        #     print("path " + str(path))
        #
        #     bestPath = [path]
        #     bestDES = [des]
        #     return bestPath, bestDES
        # else :
        min = math.inf
        restup = ()
        for ix, tup in enumerate(traffic):
            if traffic[tup] % 100 < min:
                min = traffic[tup] % 100
                restup = tup
        print("restup" + str(restup))
        finalDes = 0
        for ix, des in enumerate(DES_dst):
            print("DES " + str(DES_dst))
            print("ix %i" % ix)
            print("des %i" % des)

            print(message.dst)

            # if message.name == "M.A" or message.name == "M.B" or message.name == "M.C" or message.name == "M.D":
            # print("rr dict " + str(self.rr))

            dst_node = alloc_DES[des]
            path = list(nx.shortest_path(sim.topology.G, source=node_src, target=dst_node))

            # traffic consider
            path = tuple(path)
            if len(traffic) != 0 and path not in traffic.keys():
                bestPath = [path]
                bestDES = [des]
                # self.hm[msgType] = des
                break

            elif path != restup and len(restup) != 0:
                bestPath = [path]
                bestDES = [des]
                continue
            else:
                bestPath = [path]
                bestDES = [des]
                # nodeIPT = sim.topology.get_node(dst_node)["IPT"]
                # print(str(message.getIns()))
                # msgIns = message.getIns()
                #
                # diff = nodeIPT / msgIns  # should be max
                #
                # if maxDiff < diff:
                #     maxDiff = diff
                #     bestPath = [path]
                #     bestDES = [des]

            # self.hm[msgType] = des

            if message.name == "M.A" or message.name == "M.B" or message.name == "M.C" or message.name == "M.D":

                pass
                # self.hm[msgType] = des

                # print("Get Node" + str(sim.topology.get_node(dst_node)["IPT"]))
                # nodeIPT = sim.topology.get_node(dst_node)["IPT"]
                # print(str(message.getIns()))
                # msgIns = message.getIns()
                #
                # diff = nodeIPT / msgIns  # should be max
                #
                # if maxDiff < diff:
                #     maxDiff = diff
                #     bestPath = [path]
                #     bestDES = [des]
                #
                #     print("if condition")
            else:  # message.name == "M.B or M.D"

                # dst_node = alloc_DES[des]
                # path = list(nx.shortest_path(sim.topology.G, source=node_src, target=dst_node))
                # path = tuple(path)
                # if len(traffic) != 0 and path not in traffic.keys():
                #     bestPath = [path]
                #     bestDES = [des]
                #     self.hm[msgType] = des
                #     break
                # # elif path != restup and len(restup) != 0:
                # #     bestPath = [path]
                # #     bestDES = [des]
                # #     continue
                # else:
                #     bestPath = [path]
                #     bestDES = [des]

                # self.hm[msgType] = des

                # print("Get Node" + str(sim.topology.get_node(dst_node)["IPT"]))
                # nodeIPT = sim.topology.get_node(dst_node)["IPT"]
                # print(str(message.getIns()))
                # msgIns = message.getIns()
                #
                # diff = nodeIPT / msgIns  # should be max
                #
                # if maxDiff < diff:
                #     maxDiff = diff
                #     bestPath = [path]
                #     bestDES = [des]
                #     self.hm[msgType] = des
                #     print("if condition")

                if message.broadcasting:
                    bestPath.append(path)
                    bestDES.append(des)

            # else:  #
            #
            #     dst_node = alloc_DES[des]
            #
            #     print("ix %i" % ix)
            #     print("des %i" % des)
            #
            #     path = list(nx.shortest_path(sim.topology.G, source=node_src, target=dst_node))
            #     if message.broadcasting:
            #         bestPath.append(path)
            #         bestDES.append(des)
            #     else:
            #         bestPath = [path]
            #         bestDES = [des]
            finalDes = des

        print(bestDES)
        return bestPath, bestDES


class MinPath_Cache(Selection):

    def __init__(self):
        self.rr = {}  # for a each type of service, we have a mod-counter
        self.hm = {}

    def get_path(self, sim, app_name, message, topology_src, alloc_DES, alloc_module, traffic, from_des):

        node_src = topology_src
        DES_dst = alloc_module[app_name][message.dst]  # returns an array with all DES process serving
        print(sim.last_busy_time)
        print("alloc module " + str(alloc_module[app_name]))

        msgType = message.getMsgType()
        if message.dst not in self.rr.keys():
            self.rr[message.dst] = 0

        if msgType not in self.hm.keys():
            self.hm[msgType] = -1

        print("GET PATH")
        print("\tNode _ src (id_topology): %i" % node_src)
        print("\tRequest service: %s " % (message.dst))
        print("\tProcess serving that service: %s (pos ID: %i)" % (DES_dst, self.rr[message.dst]))

        bestPath = []
        bestDES = []

        print("Round Robin * ***************************")

        print("Alloc Des" + str(DES_dst))

        n = len(DES_dst)
        if self.hm[msgType] != -1:

            des = self.hm[msgType]
            print("if condition des" + str(des))
            dst_node = alloc_DES[des]
            print("DST NOde" + str(dst_node))
            path = list(nx.shortest_path(sim.topology.G, source=node_src, target=dst_node))
            print("path " + str(path))

            bestPath = [path]
            bestDES = [des]
            return bestPath, bestDES
        else:
            for i in range(n - 1):
                for j in range(0, n - i - 1):

                    dst_node1 = alloc_DES[DES_dst[j]]
                    dst_node2 = alloc_DES[DES_dst[j + 1]]

                    nodeIPT_j = sim.topology.get_node(dst_node1)["IPT"]
                    nodeIPT_j1 = sim.topology.get_node(dst_node2)["IPT"]
                    if nodeIPT_j < nodeIPT_j1:
                        DES_dst[j], DES_dst[j + 1] = DES_dst[j + 1], DES_dst[j]

            for ix, desNode in enumerate(DES_dst):
                print("desNode" + str(desNode))
                if message.name == "M.A" or message.name == "M.B" or message.name == "M.C" or message.name == "M.D":
                    if self.rr[message.dst] == ix:
                        dst_node = alloc_DES[desNode]

                        print("DST NOde" + str(dst_node))
                        path = list(nx.shortest_path(sim.topology.G, source=node_src, target=dst_node))
                        print("path " + str(path))

                        bestPath = [path]
                        bestDES = [desNode]

                        self.rr[message.dst] = (self.rr[message.dst] + 1) % len(DES_dst)
                        break

                else:
                    dst_node = alloc_DES[desNode]

                    path = list(nx.shortest_path(sim.topology.G, source=node_src, target=dst_node))
                    if message.broadcasting:
                        bestPath.append(path)
                        bestDES.append(desNode)
                    else:
                        bestPath = [path]
                        bestDES = [desNode]

        self.hm[msgType] = bestDES[0]
        return bestPath, bestDES


class MinPathTraffic2(Selection):

    def __init__(self):
        self.tr = {}
        self.times = {}

    def get_path(self, sim, app_name, message, topology_src, alloc_DES, alloc_module, traffic, from_des):

        node_src = topology_src
        DES_dst = alloc_module[app_name][message.dst]

        if len(self.tr) == 0:
            print("TR IS 0")
            for des in DES_dst:
                self.tr[des] = 0
        if len(self.times) == 0:
            print("times IS 0")
            for des in DES_dst:
                self.times[des] = 101

        # print("Message time in" + str(sim.timeIn))

        print("traffic")
        print("GET PATH")
        print("\tNode _ src (id_topology): %i" % node_src)
        print("\tRequest service: %s " % message.dst)
        print("\tProcess serving that service: %s " % DES_dst)

        print("Time Emit " + str(sim.env.now))

        bestPath = []
        bestDES = []

        n = len(DES_dst)
        for i in range(n - 1):
            for j in range(0, n - i - 1):

                dst_node1 = alloc_DES[DES_dst[j]]
                dst_node2 = alloc_DES[DES_dst[j + 1]]

                nodeIPT_j = sim.topology.get_node(dst_node1)["IPT"]
                nodeIPT_j1 = sim.topology.get_node(dst_node2)["IPT"]
                if nodeIPT_j < nodeIPT_j1:
                    DES_dst[j], DES_dst[j + 1] = DES_dst[j + 1], DES_dst[j]

        # time_emit = sim.env.now
        # latency = float(message.timestamp_rec) - float(message.timestamp)

        for des in DES_dst:
            print("DES")
            if message.name == "M.A" or message.name == "M.B" or message.name == "M.C" or message.name == "M.D":
                time_emit_present = sim.env.now
                print("time_emit_pres" + str(time_emit_present) + "times" + str(self.times[des]))

                if self.tr[des] == 1 and (time_emit_present - self.times[des] < 99):
                    continue
                elif self.tr[des] == 1 and (time_emit_present - self.times[des] >= 99):
                    self.tr[des] = 0

                    dst_node = alloc_DES[des]

                    print("\t\t Looking the path to id_node: %i" % dst_node)

                    path = list(nx.shortest_path(sim.topology.G, source=node_src, target=dst_node))

                    bestPath = [path]
                    bestDES = [des]

                    nodeIPT = sim.topology.get_node(dst_node)["IPT"]
                    print(str(message.getIns()))
                    msgIns = message.getIns()

                    div = msgIns / nodeIPT
                    time_out = sim.time_out
                    print("time_out" + str(time_out))
                    time_emit = sim.time_emit

                    if div > 1:
                        print("div is more than 1")
                        self.tr[des] = 1

                        self.times[des] = time_emit_present
                    break
                else:

                    dst_node = alloc_DES[des]

                    print("\t\t Looking the path to id_node: %i" % dst_node)

                    path = list(nx.shortest_path(sim.topology.G, source=node_src, target=dst_node))

                    bestPath = [path]
                    bestDES = [des]

                    nodeIPT = sim.topology.get_node(dst_node)["IPT"]
                    print(str(message.getIns()))
                    msgIns = message.getIns()

                    div = msgIns / nodeIPT
                    time_out = sim.time_out
                    print("time_out" + str(time_out))
                    time_emit = sim.time_emit

                    if div > 1:
                        print("div is more than 1")
                        self.tr[des] = 1

                        self.times[des] = time_emit_present
                    break
            else:
                dst_node = alloc_DES[des]

                path = list(nx.shortest_path(sim.topology.G, source=node_src, target=dst_node))
                if message.broadcasting:
                    bestPath.append(path)
                    bestDES.append(des)
                else:
                    bestPath = [path]
                    bestDES = [des]

        return bestPath, bestDES


class CacheBasedSolution(Selection):

    def __init__(self):
        self.tr = {}
        self.times = {}
        self.hm = {}
        self.busy = 0

    def get_path(self, sim, app_name, message, topology_src, alloc_DES, alloc_module, traffic, from_des):

        node_src = topology_src
        DES_dst = alloc_module[app_name][message.dst]

        if len(self.tr) == 0:
            print("TR IS 0")
            for des in DES_dst:
                self.tr[des] = 0

        if len(self.times) == 0:
            print("times IS 0")
            for des in DES_dst:
                self.times[des] = 101
        if message.name not in self.hm.keys():
            self.hm[message.name] = -1

        # print("Message time in" + str(sim.timeIn))

        print("traffic")
        print("GET PATH")
        print("\tNode _ src (id_topology): %i" % node_src)
        print("\tRequest service: %s " % message.dst)
        print("\tProcess serving that service: %s " % DES_dst)

        print("Time Emit " + str(sim.env.now))

        bestPath = []
        bestDES = []
        buffer = 99
        if self.hm[message.name] != -1:
            print("Message Name" + str(message.name))
            des = self.hm[message.name]
            dst_node = alloc_DES[des]

            print("\t\t Looking the path to id_node: %i" % dst_node)

            path = list(nx.shortest_path(sim.topology.G, source=node_src, target=dst_node))

            bestPath = [path]
            bestDES = [des]
            return bestPath, bestDES

        # if message.name == "M.A" or message.name == "M.B" or message.name == "M.C" or message.name == "M.D":
        n = len(DES_dst)
        for i in range(n - 1):
            for j in range(0, n - i - 1):

                dst_node1 = alloc_DES[DES_dst[j]]
                dst_node2 = alloc_DES[DES_dst[j + 1]]

                nodeIPT_j = sim.topology.get_node(dst_node1)["IPT"]
                nodeIPT_j1 = sim.topology.get_node(dst_node2)["IPT"]
                if nodeIPT_j < nodeIPT_j1:
                    DES_dst[j], DES_dst[j + 1] = DES_dst[j + 1], DES_dst[j]

        # time_emit = sim.env.now
        # latency = float(message.timestamp_rec) - float(message.timestamp)

        for des in DES_dst:
            print("DES")
            if message.name == "M.A" or message.name == "M.B" or message.name == "M.C" or message.name == "M.D":
                time_emit_present = sim.env.now
                print("time_emit_pres" + str(time_emit_present) + "times" + str(self.times[des]))

                if self.tr[des] == 1 and (time_emit_present - self.times[des] < buffer):
                    continue
                elif self.tr[des] == 1 and (time_emit_present - self.times[des] >= buffer) or self.busy == len(DES_dst):
                    self.tr[des] = 0
                    self.busy -= 1

                dst_node = alloc_DES[des]

                print("\t\t Looking the path to id_node: %i" % dst_node)

                path = list(nx.shortest_path(sim.topology.G, source=node_src, target=dst_node))

                bestPath = [path]

                bestDES = [des]

                nodeIPT = sim.topology.get_node(dst_node)["IPT"]

                print(str(message.getIns()))

                msgIns = message.getIns()

                div = msgIns / nodeIPT

                time_out = sim.time_out

                print("time_out" + str(time_out))

                time_emit = sim.time_emit

                if div > 1:
                    print("div is more than 1")

                    self.tr[des] = 1

                    self.times[des] = time_emit_present + div

                break
            else:
                dst_node = alloc_DES[des]

                print("Message2 " + str(node_src))

                print("\t\t Looking the path to id_node: %i" % dst_node)

                path = list(nx.shortest_path(sim.topology.G, source=node_src, target=dst_node))
                bestPath = [path]

                bestDES = [des]
                if message.broadcasting:
                    bestPath.append(path)
                    bestDES.append(des)
                else:
                    bestPath = [path]
                    bestDES = [des]
        self.hm[message.name] = bestDES[0]

        if bestDES[0] in self.tr.keys():
            if self.tr[bestDES[0]] == 1:
                self.busy += 1

        return bestPath, bestDES


class MinMax(Selection):

    def __init__(self):
        self.tr = {}
        self.times = {}
        self.hm = {}
        self.busy = 0

    def get_path(self, sim, app_name, message, topology_src, alloc_DES, alloc_module, traffic, from_des):

        node_src = topology_src
        DES_dst = alloc_module[app_name][message.dst]

        if len(self.tr) == 0:
            print("TR IS 0")
            for des in DES_dst:
                self.tr[des] = 0

        if len(self.times) == 0:
            print("times IS 0")
            for des in DES_dst:
                self.times[des] = 101
        if message.name not in self.hm.keys():
            self.hm[message.name] = -1

        # print("Message time in" + str(sim.timeIn))

        print("traffic")
        print("GET PATH")
        print("\tNode _ src (id_topology): %i" % node_src)
        print("\tRequest service: %s " % message.dst)
        print("\tProcess serving that service: %s " % DES_dst)

        print("Time Emit " + str(sim.env.now))

        bestPath = []
        bestDES = []
        buffer = 99
        if self.hm[message.name] != -1:
            print("Message Name" + str(message.name))
            des = self.hm[message.name]
            dst_node = alloc_DES[des]

            print("\t\t Looking the path to id_node: %i" % dst_node)

            path = list(nx.shortest_path(sim.topology.G, source=node_src, target=dst_node))

            bestPath = [path]
            bestDES = [des]
            return bestPath, bestDES

        # if message.name == "M.A" or message.name == "M.B" or message.name == "M.C" or message.name == "M.D":
        n = len(DES_dst)
        for i in range(n - 1):
            for j in range(0, n - i - 1):

                dst_node1 = alloc_DES[DES_dst[j]]
                dst_node2 = alloc_DES[DES_dst[j + 1]]

                nodeIPT_j = sim.topology.get_node(dst_node1)["IPT"]
                nodeIPT_j1 = sim.topology.get_node(dst_node2)["IPT"]
                if nodeIPT_j < nodeIPT_j1:
                    DES_dst[j], DES_dst[j + 1] = DES_dst[j + 1], DES_dst[j]

        # time_emit = sim.env.now
        # latency = float(message.timestamp_rec) - float(message.timestamp)

        for des in DES_dst:
            print("DES")
            if message.name == "M.A" or message.name == "M.B" or message.name == "M.C" or message.name == "M.D":
                time_emit_present = sim.env.now
                print("time_emit_pres" + str(time_emit_present) + "times" + str(self.times[des]))

                if self.tr[des] == 1 and (time_emit_present - self.times[des] < buffer):
                    continue
                elif self.tr[des] == 1 and (time_emit_present - self.times[des] >= buffer) or self.busy == len(DES_dst):
                    self.tr[des] = 0
                    self.busy -= 1

                dst_node = alloc_DES[des]

                print("\t\t Looking the path to id_node: %i" % dst_node)

                path = list(nx.shortest_path(sim.topology.G, source=node_src, target=dst_node))

                bestPath = [path]

                bestDES = [des]

                nodeIPT = sim.topology.get_node(dst_node)["IPT"]

                print(str(message.getIns()))

                msgIns = message.getIns()

                div = msgIns / nodeIPT

                time_out = sim.time_out

                print("time_out" + str(time_out))

                time_emit = sim.time_emit

                if div < 1:
                    print("div is more than 1")

                    self.tr[des] = 1

                    self.times[des] = time_emit_present + div

                break
            else:
                dst_node = alloc_DES[des]

                print("Message2 " + str(node_src))

                print("\t\t Looking the path to id_node: %i" % dst_node)

                path = list(nx.shortest_path(sim.topology.G, source=node_src, target=dst_node))
                bestPath = [path]

                bestDES = [des]
                if message.broadcasting:
                    bestPath.append(path)
                    bestDES.append(des)
                else:
                    bestPath = [path]
                    bestDES = [des]
        self.hm[message.name] = bestDES[0]

        if bestDES[0] in self.tr.keys():
            if self.tr[bestDES[0]] == 1:
                self.busy += 1

        return bestPath, bestDES


class CacheBasedSolution_scaled(Selection):

    def __init__(self):
        self.tr = {}
        self.times = {}
        self.hm = {}
        self.busy = 0

    def get_path(self, sim, app_name, message, topology_src, alloc_DES, alloc_module, traffic, from_des):

        node_src = topology_src
        DES_dst = alloc_module[app_name][message.dst]

        if len(self.tr) == 0:
            print("TR IS 0")
            for des in DES_dst:
                self.tr[des] = 0

        if len(self.times) == 0:
            print("times IS 0")
            for des in DES_dst:
                self.times[des] = 101
        if message.name not in self.hm.keys():
            self.hm[message.name] = -1

        # print("Message time in" + str(sim.timeIn))

        print("traffic")
        print("GET PATH")
        print("\tNode _ src (id_topology): %i" % node_src)
        print("\tRequest service: %s " % message.dst)
        print("\tProcess serving that service: %s " % DES_dst)

        print("Time Emit " + str(sim.env.now))

        bestPath = []
        bestDES = []
        buffer = 99
        if self.hm[message.name] != -1:
            print("Message Name" + str(message.name))
            des = self.hm[message.name]
            dst_node = alloc_DES[des]

            print("\t\t Looking the path to id_node: %i" % dst_node)

            path = list(nx.shortest_path(sim.topology.G, source=node_src, target=dst_node))

            bestPath = [path]
            bestDES = [des]
            return bestPath, bestDES

        # if message.name == "M.A" or message.name == "M.B" or message.name == "M.C" or message.name == "M.D":
        n = len(DES_dst)
        for i in range(n - 1):
            for j in range(0, n - i - 1):

                dst_node1 = alloc_DES[DES_dst[j]]
                dst_node2 = alloc_DES[DES_dst[j + 1]]

                nodeIPT_j = sim.topology.get_node(dst_node1)["IPT"]
                nodeIPT_j1 = sim.topology.get_node(dst_node2)["IPT"]
                if nodeIPT_j < nodeIPT_j1:
                    DES_dst[j], DES_dst[j + 1] = DES_dst[j + 1], DES_dst[j]

        # time_emit = sim.env.now
        # latency = float(message.timestamp_rec) - float(message.timestamp)

        for des in DES_dst:
            print("DES")
            if message.name == "M.A" or message.name == "M.B" or message.name == "M.C" or message.name == "M.D" \
                    or message.name == "M.E" or message.name == "M.F" or message.name == "M.G" \
                    or message.name == "M.H" or message.name == "M.I" or message.name == "M.J" \
                    or message.name == "M.K" or message.name == "M.L" or message.name == "M.M" \
                    or message.name == "M.N" or message.name == "M.O" or message.name == "M.P" \
                    or message.name == "M.Q" or message.name == "M.R" or message.name == "M.S" \
                    or message.name == "M.T" or message.name == "M.U" or message.name == "M.V" \
                    or message.name == "M.W" or message.name == "M.X" or message.name == "M.Y" \
                    or message.name == "M.Z":
                time_emit_present = sim.env.now
                print("time_emit_pres" + str(time_emit_present) + "times" + str(self.times[des]))

                if self.tr[des] == 1 and (time_emit_present - self.times[des] < buffer):
                    continue
                elif self.tr[des] == 1 and (time_emit_present - self.times[des] >= buffer) or self.busy == len(DES_dst):
                    self.tr[des] = 0
                    self.busy -= 1

                dst_node = alloc_DES[des]

                print("\t\t Looking the path to id_node: %i" % dst_node)

                path = list(nx.shortest_path(sim.topology.G, source=node_src, target=dst_node))

                bestPath = [path]

                bestDES = [des]

                nodeIPT = sim.topology.get_node(dst_node)["IPT"]

                print(str(message.getIns()))

                msgIns = message.getIns()

                div = msgIns / nodeIPT

                time_out = sim.time_out

                print("time_out" + str(time_out))

                time_emit = sim.time_emit

                if div > 1:
                    print("div is more than 1")

                    self.tr[des] = 1

                    self.times[des] = time_emit_present + div

                break

            elif message.name == "M.A2" or message.name == "M.B2" or message.name == "M.C2" or message.name == "M.D2" \
                    or message.name == "M.E2" or message.name == "M.F2" or message.name == "M.G2" \
                    or message.name == "M.H2" or message.name == "M.I2" or message.name == "M.J2" \
                    or message.name == "M.K2" or message.name == "M.L2" or message.name == "M.M2" \
                    or message.name == "M.N2" or message.name == "M.O2" or message.name == "M.P2" \
                    or message.name == "M.Q2" or message.name == "M.R2" or message.name == "M.S2" \
                    or message.name == "M.T2" or message.name == "M.U2" or message.name == "M.V2" \
                    or message.name == "M.W2" or message.name == "M.X2" or message.name == "M.Y2" \
                    or message.name == "M.Z2":
                dst_node = alloc_DES[des]

                print("des %i" % des)

                path = list(nx.shortest_path(sim.topology.G, source=node_src, target=dst_node))
                if message.broadcasting:
                    bestPath.append(path)
                    bestDES.append(des)
                else:
                    bestPath = [path]
                    bestDES = [des]
                break

        self.hm[message.name] = bestDES[0]

        if bestDES[0] in self.tr.keys():
            if self.tr[bestDES[0]] == 1:
                self.busy += 1

        return bestPath, bestDES


class RoundRobin_scaled(Selection):

    def __init__(self):
        self.rr = {}  # for a each type of service, we have a mod-counter

    def get_path(self, sim, app_name, message, topology_src, alloc_DES, alloc_module, traffic, from_des):
        """
        Computes the minimun path among the source elemento of the topology and the localizations of the module
        Return the path and the identifier of the module deployed in the last element of that path
        """
        node_src = topology_src
        DES_dst = alloc_module[app_name][message.dst]  # returns an array with all DES process serving

        print("alloc module " + str(alloc_module[app_name]))

        if message.dst not in self.rr.keys():
            self.rr[message.dst] = 0

        print("GET PATH")
        print("\tNode _ src (id_topology): %i" % node_src)
        print("\tRequest service: %s " % (message.dst))
        print("\tProcess serving that service: %s (pos ID: %i)" % (DES_dst, self.rr[message.dst]))

        bestPath = []
        bestDES = []
        print("Round Robin * ***************************")

        for ix, des in enumerate(DES_dst):
            print("DES " + str(DES_dst))
            print("ix %i" % ix)
            print("des %i" % des)

            print(message.dst)

            if message.name == "M.A" or message.name == "M.B" or message.name == "M.C" or message.name == "M.D" \
                    or message.name == "M.E" or message.name == "M.F" or message.name == "M.G" \
                    or message.name == "M.H" or message.name == "M.I" or message.name == "M.J" \
                    or message.name == "M.K" or message.name == "M.L" or message.name == "M.M" \
                    or message.name == "M.N" or message.name == "M.O" or message.name == "M.P" \
                    or message.name == "M.Q" or message.name == "M.R" or message.name == "M.S" \
                    or message.name == "M.T" or message.name == "M.U" or message.name == "M.V" \
                    or message.name == "M.W" or message.name == "M.X" or message.name == "M.Y" \
                    or message.name == "M.Z":
                print("rr dict " + str(self.rr))

                if self.rr[message.dst] == ix:
                    dst_node = alloc_DES[des]

                    print("DST NOde" + str(dst_node))
                    path = list(nx.shortest_path(sim.topology.G, source=node_src, target=dst_node))
                    print("path " + str(path))

                    bestPath = [path]
                    bestDES = [des]

                    self.rr[message.dst] = (self.rr[message.dst] + 1) % len(DES_dst)
                    break
            else:

                dst_node = alloc_DES[des]

                print("ix %i" % ix)
                print("des %i" % des)

                path = list(nx.shortest_path(sim.topology.G, source=node_src, target=dst_node))
                if message.broadcasting:
                    bestPath.append(path)
                    bestDES.append(des)
                else:
                    bestPath = [path]
                    bestDES = [des]

        return bestPath, bestDES


class CacheBasedSolutionWithCloud(Selection):

    def __init__(self):
        self.tr = {}
        self.times = {}
        self.hm = {}
        self.busy = 0

    def get_path(self, sim, app_name, message, topology_src, alloc_DES, alloc_module, traffic, from_des):

        ins = message.getIns()
        node_src = topology_src
        DES_dst = alloc_module[app_name][message.dst]

        if len(self.tr) == 0:
            print("TR IS 0")
            for des in DES_dst:
                self.tr[des] = 0

        if len(self.times) == 0:
            print("times IS 0")
            for des in DES_dst:
                self.times[des] = 101
        if message.name not in self.hm.keys():
            self.hm[message.name] = -1

        # print("Message time in" + str(sim.timeIn))

        print("traffic")
        print("GET PATH")
        print("\tNode _ src (id_topology): %i" % node_src)
        print("\tRequest service: %s " % message.dst)
        print("\tProcess serving that service: %s " % DES_dst)

        print("Time Emit " + str(sim.env.now))

        bestPath = []
        bestDES = []
        buffer = 99

        if self.hm[message.name] != -1:
            # print("Message Name" + str(message.name))
            des = self.hm[message.name]
            dst_node = alloc_DES[des]

            print("\t\t Looking the path to id_node: %i" % dst_node)

            path = list(nx.shortest_path(sim.topology.G, source=node_src, target=dst_node))
            print(path)
            bestPath = [path]
            bestDES = [des]
            return bestPath, bestDES

        # if message.name == "M.A" or message.name == "M.B" or message.name == "M.C" or message.name == "M.D":
        n = len(DES_dst)
        for i in range(n - 1):
            for j in range(0, n - i - 1):

                dst_node1 = alloc_DES[DES_dst[j]]
                dst_node2 = alloc_DES[DES_dst[j + 1]]

                nodeIPT_j = sim.topology.get_node(dst_node1)["IPT"]
                nodeIPT_j1 = sim.topology.get_node(dst_node2)["IPT"]
                if nodeIPT_j < nodeIPT_j1:
                    DES_dst[j], DES_dst[j + 1] = DES_dst[j + 1], DES_dst[j]

        # time_emit = sim.env.now
        # latency = float(message.timestamp_rec) - float(message.timestamp)
        if(DES_dst[0] == 8):
            print("POP" + str(DES_dst.pop(0)))
            print("POP" + str(len(DES_dst)))
        for des in DES_dst:
            print("DES")



            if message.name == "M.A" or message.name == "M.B" or message.name == "M.C" or message.name == "M.D" \
                    or message.name == "M.E" or message.name == "M.F" or message.name == "M.G" \
                    or message.name == "M.H" or message.name == "M.I" or message.name == "M.J" \
                    or message.name == "M.K" or message.name == "M.L" or message.name == "M.M" \
                    or message.name == "M.N" or message.name == "M.O" or message.name == "M.P" \
                    or message.name == "M.Q" or message.name == "M.R" or message.name == "M.S" \
                    or message.name == "M.T" or message.name == "M.U" or message.name == "M.V" \
                    or message.name == "M.W" or message.name == "M.X" or message.name == "M.Y" \
                    or message.name == "M.Z" or \
                    message.name == "M.AA" or message.name == "M.BB" \
                    or message.name == "M.CC" or message.name == "M.DD" \
                    or message.name == "M.EE" or message.name == "M.FF" or message.name == "M.GG" \
                    or message.name == "M.HH" or message.name == "M.II" or message.name == "M.JJ" \
                    or message.name == "M.KK" or message.name == "M.LL" or message.name == "M.MM" \
                    or message.name == "M.NN" or message.name == "M.OO" or message.name == "M.PP" \
                    or message.name == "M.QQ" or message.name == "M.RR" or message.name == "M.SS" \
                    or message.name == "M.TT" or message.name == "M.UU" or message.name == "M.VV" \
                    or message.name == "M.WW" or message.name == "M.XX" or message.name == "M.YY" \
                    or message.name == "M.ZZ" or \
                    message.name == "M.AAA" or message.name == "M.BBB" \
                    or message.name == "M.CCC" or message.name == "M.DDD" \
                    or message.name == "M.EEE" or message.name == "M.FFF" or message.name == "M.GGG" \
                    or message.name == "M.HHH" or message.name == "M.III" or message.name == "M.JJJ" \
                    or message.name == "M.KKK" or message.name == "M.LLL" or message.name == "M.MMM" \
                    or message.name == "M.NNN" or message.name == "M.OOO" or message.name == "M.PPP" \
                    or message.name == "M.QQQ" or message.name == "M.RRR" or message.name == "M.SSS" \
                    or message.name == "M.TTT" or message.name == "M.UUU" or message.name == "M.VVV" \
                    or message.name == "M.WWW" or message.name == "M.XXX" or message.name == "M.YYY" \
                    or message.name == "M.ZZZ" or \
                    message.name == "M.AAAA" or message.name == "M.BBBB" \
                    or message.name == "M.CCCC" or message.name == "M.DDDD" \
                    or message.name == "M.EEEE" or message.name == "M.FFFF" or message.name == "M.GGGG" \
                    or message.name == "M.HHHH" or message.name == "M.IIII" or message.name == "M.JJJJ" \
                    or message.name == "M.KKKK" or message.name == "M.LLLL" or message.name == "M.MMMM" \
                    or message.name == "M.NNNN" or message.name == "M.OOOO" or message.name == "M.PPPP" \
                    or message.name == "M.QQQQ" or message.name == "M.RRRR" or message.name == "M.SSSS" \
                    or message.name == "M.TTTT" or message.name == "M.UUUU" or message.name == "M.VVVV" \
                    or message.name == "M.WWWW" or message.name == "M.XXXX" or message.name == "M.YYYY" \
                    or message.name == "M.ZZZZ" or \
                    message.name == "M.AAAAA" or message.name == "M.BBBBB" \
                    or message.name == "M.CCCCC" or message.name == "M.DDDDD" \
                    or message.name == "M.EEEEE" or message.name == "M.FFFFF" or message.name == "M.GGGGG" \
                    or message.name == "M.HHHHH" or message.name == "M.IIIII" or message.name == "M.JJJJJ" \
                    or message.name == "M.KKKKK" or message.name == "M.LLLLL" or message.name == "M.MMMMM" \
                    or message.name == "M.NNNNN" or message.name == "M.OOOOO" or message.name == "M.PPPPP" \
                    or message.name == "M.QQQQQ" or message.name == "M.RRRRR" or message.name == "M.SSSSS" \
                    or message.name == "M.TTTTT" or message.name == "M.UUUUU" or message.name == "M.VVVVV" \
                    or message.name == "M.WWWWW" or message.name == "M.XXXXX" or message.name == "M.YYYYY" \
                    or message.name == "M.ZZZZZ":

                if ins > 5000:
                    # find des of cloud
                    des = 8
                    dst_node = 5

                    print("\t\t Looking the path to id_node: %i" % dst_node)

                    path = list(nx.shortest_path(sim.topology.G, source=node_src, target=dst_node))
                    print(path)
                    bestPath = [path]
                    bestDES = [des]
                    return bestPath, bestDES

                time_emit_present = sim.env.now
                print("time_emit_pres" + str(time_emit_present) + "times" + str(self.times[des]))

                if self.tr[des] == 1 and (time_emit_present - self.times[des] < buffer):
                    continue
                elif self.tr[des] == 1 and (time_emit_present - self.times[des] >= buffer) or self.busy == len(DES_dst):
                    self.tr[des] = 0
                    self.busy -= 1

                dst_node = alloc_DES[des]

                print("\t\t Looking the path to id_node: %i" % dst_node)

                path = list(nx.shortest_path(sim.topology.G, source=node_src, target=dst_node))

                bestPath = [path]

                bestDES = [des]

                nodeIPT = sim.topology.get_node(dst_node)["IPT"]

                print(str(message.getIns()))

                msgIns = message.getIns()

                div = msgIns / nodeIPT

                time_out = sim.time_out

                print("time_out" + str(time_out))

                time_emit = sim.time_emit

                if div > 1:
                    print("div is more than 1")

                    self.tr[des] = 1

                    self.times[des] = time_emit_present + div

                break
            else:
                if ins > 50000:
                    # find des of cloud
                    des = 4
                    dst_node = alloc_DES[des]

                    print("\t\t Looking the path to id_node: %i" % dst_node)

                    path = list(nx.shortest_path(sim.topology.G, source=node_src, target=dst_node))
                    print(path)
                    bestPath = [path]
                    bestDES = [des]
                    return bestPath, bestDES

                dst_node = alloc_DES[des]
                print("des %i" % des)

                path = list(nx.shortest_path(sim.topology.G, source=node_src, target=dst_node))
                if message.broadcasting:
                    bestPath.append(path)
                    bestDES.append(des)
                else:
                    bestPath = [path]
                    bestDES = [des]
                break
        self.hm[message.name] = bestDES[0]

        if bestDES[0] in self.tr.keys():
            if self.tr[bestDES[0]] == 1:
                self.busy += 1

        return bestPath, bestDES

class RoundRobin_cloud(Selection):

    def __init__(self):
        self.rr = {}  # for a each type of service, we have a mod-counter

    def get_path(self, sim, app_name, message, topology_src, alloc_DES, alloc_module, traffic, from_des):
        """
        Computes the minimun path among the source elemento of the topology and the localizations of the module
        Return the path and the identifier of the module deployed in the last element of that path
        """
        node_src = topology_src
        DES_dst = alloc_module[app_name][message.dst]  # returns an array with all DES process serving

        print("alloc module " + str(alloc_module[app_name]))

        if message.dst not in self.rr.keys():
            self.rr[message.dst] = 0

        print("GET PATH")
        print("\tNode _ src (id_topology): %i" % node_src)
        print("\tRequest service: %s " % (message.dst))
        print("\tProcess serving that service: %s (pos ID: %i)" % (DES_dst, self.rr[message.dst]))

        bestPath = []
        bestDES = []
        print("Round Robin * ***************************")
        if (DES_dst[0] == 8):
            print("POP" + str(DES_dst.pop(0)))
            print("POP" + str(len(DES_dst)))

        for ix, des in enumerate(DES_dst):
            print("DES " + str(DES_dst))
            print("ix %i" % ix)
            print("des %i" % des)

            print(message.dst)
            if message.name == "M.A" or message.name == "M.B" or message.name == "M.C" or message.name == "M.D":
                print("rr dict " + str(self.rr))

                if message.getIns() > 5000:
                    # find des of cloud
                    des = 8
                    dst_node = 5

                    print("\t\t Looking the path to id_node: %i" % dst_node)

                    path = list(nx.shortest_path(sim.topology.G, source=node_src, target=dst_node))
                    print(path)
                    bestPath = [path]
                    bestDES = [des]
                    return bestPath, bestDES

                if self.rr[message.dst] == ix:
                    dst_node = alloc_DES[des]

                    print("DST NOde" + str(dst_node))
                    path = list(nx.shortest_path(sim.topology.G, source=node_src, target=dst_node))
                    print("path " + str(path))

                    bestPath = [path]
                    bestDES = [des]

                    self.rr[message.dst] = (self.rr[message.dst] + 2) % len(DES_dst)

            else:  # message.name == "M.B or M.D"

                if message.getIns() > 5000:
                    # find des of cloud
                    des = 8
                    dst_node = 5

                    print("\t\t Looking the path to id_node: %i" % dst_node)

                    path = list(nx.shortest_path(sim.topology.G, source=node_src, target=dst_node))
                    print(path)
                    bestPath = [path]
                    bestDES = [des]
                    return bestPath, bestDES

                dst_node = alloc_DES[des]

                print("ix %i" % ix)
                print("des %i" % des)

                path = list(nx.shortest_path(sim.topology.G, source=node_src, target=dst_node))
                if message.broadcasting:
                    bestPath.append(path)
                    bestDES.append(des)
                else:
                    bestPath = [path]
                    bestDES = [des]

        return bestPath, bestDES
