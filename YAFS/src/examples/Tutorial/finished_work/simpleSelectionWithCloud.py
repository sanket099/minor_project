from yafs.selection import Selection
import networkx as nx
import math


class FIFOCloud(Selection):

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
            print("HELLO DES" + str(des))
            print("HELLO NODE " + str(alloc_DES[des]))
            if message.getIns() > 3000:  # message.msgType == 3:
                # find des of cloud
                if message.name == "M.A" or message.name == "M.B" or message.name == "M.C" or message.name == "M.D" :
                    des_cloud = 8
                    dst_node_cloud = alloc_DES[des_cloud]

                    print("\t\t Looking the path to id_node CLOUD: %i" % dst_node_cloud )
                    print(" INSTRUCTION : %i" % message.getIns())

                    path = list(nx.shortest_path(sim.topology.G, source=node_src, target=dst_node_cloud))
                    print(path)

                    nodeIPT = sim.topology.get_node(dst_node_cloud)["IPT"]
                    print("IPT OF CLOUD " + str(nodeIPT))
                    bestPath = [path]
                    bestDES = [des_cloud]
                    break
                else :
                    des_cloud = 4
                    dst_node_cloud = alloc_DES[des_cloud]

                    print("\t\t Looking the path to id_node CLOUD: %i" % dst_node_cloud)
                    print(" INSTRUCTION : %i" % message.getIns())

                    path = list(nx.shortest_path(sim.topology.G, source=node_src, target=dst_node_cloud))
                    print(path)

                    nodeIPT = sim.topology.get_node(dst_node_cloud)["IPT"]
                    print("IPT OF CLOUD " + str(nodeIPT))
                    bestPath = [path]
                    bestDES = [des_cloud]
                    break
            else:
                dst_node = alloc_DES[des]
                print("\t\t Looking the path to id_node: %i" % dst_node)
                print(" INSTRUCTION : %i" % message.getIns())

                path = list(nx.shortest_path(sim.topology.G, source=node_src, target=dst_node))

                bestPath = [path]
                bestDES = [des]
                break


        return bestPath, bestDES


class FIFOCloudScaled(Selection):

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
            print("HELLO DES" + str(des))
            print("HELLO NODE " + str(alloc_DES[des]))
            if(des == 27): continue
            if message.getIns() > 5000:  # message.msgType == 3:

                if message.name == "M.A" or message.name == "M.B" or message.name == "M.C" or message.name == "M.D" \
                        or message.name == "M.E" or message.name == "M.F" or message.name == "M.G" \
                        or message.name == "M.H" or message.name == "M.I" or message.name == "M.J" \
                        or message.name == "M.K" or message.name == "M.L" or message.name == "M.M" \
                        or message.name == "M.N" or message.name == "M.O" or message.name == "M.P" \
                        or message.name == "M.Q" or message.name == "M.R" or message.name == "M.S" \
                        or message.name == "M.T" or message.name == "M.U" or message.name == "M.V" \
                        or message.name == "M.W" or message.name == "M.X" or message.name == "M.Y" \
                        or message.name == "M.Z":
                    des_cloud = 78
                    dst_node_cloud = alloc_DES[des_cloud]

                    print("\t\t Looking the path to id_node CLOUD: %i" % dst_node_cloud )
                    print(" INSTRUCTION : %i" % message.getIns())

                    path = list(nx.shortest_path(sim.topology.G, source=node_src, target=dst_node_cloud))
                    print(path)

                    nodeIPT = sim.topology.get_node(dst_node_cloud)["IPT"]
                    print("IPT OF CLOUD " + str(nodeIPT))
                    bestPath = [path]
                    bestDES = [des_cloud]
                    break
                else :
                    des_cloud = 26
                    dst_node_cloud = 2

                    print("\t\t Looking the path to id_node CLOUD: %i" % dst_node_cloud)
                    print(" INSTRUCTION : %i" % message.getIns())

                    path = list(nx.shortest_path(sim.topology.G, source=node_src, target=dst_node_cloud))
                    print(path)

                    nodeIPT = sim.topology.get_node(dst_node_cloud)["IPT"]
                    print("IPT OF CLOUD " + str(nodeIPT))
                    bestPath = [path]
                    bestDES = [des_cloud]
                    break
            else:


                dst_node = alloc_DES[des]
                print("\t\t Looking the path to id_node: %i" % dst_node)

                path = list(nx.shortest_path(sim.topology.G, source=node_src, target=dst_node))

                bestPath = [path]
                bestDES = [des]
                break

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
            print("POP" + str(DES_dst.remove(8)))
            print("POP" + str(len(DES_dst)))

        if message.getIns() > 3000:  # message.msgType == 3:
            # find des of cloud
            if message.name == "M.A" or message.name == "M.B" or message.name == "M.C" or message.name == "M.D":
                des = 8
            else:
                des = 4
            dst_node = alloc_DES[des]

            print("\t\t Looking the path to id_node: %i" % dst_node)

            path = list(nx.shortest_path(sim.topology.G, source=node_src, target=dst_node))
            print(path)
            bestPath = [path]
            bestDES = [des]
            return bestPath, bestDES


        for des in DES_dst:
            print("DES")

            if message.name == "M.A" or message.name == "M.B" or message.name == "M.C" or message.name == "M.D" :

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

class CacheBasedSolutionWithCloudScaled(Selection):

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

        if (27 in DES_dst):
            print("POP" + str(DES_dst.remove(27)))  # removing random node, idk why it is there


        if (DES_dst[0] == 78): # removing cloud because have to add manually
            print("POP" + str(DES_dst.remove(78)))
            print("POP" + str(len(DES_dst)))

        if message.getIns() > 5000:  # message.msgType == 3:
            # find des of cloud
            if message.name == "M.A" or message.name == "M.B" or message.name == "M.C" or message.name == "M.D" \
                    or message.name == "M.E" or message.name == "M.F" or message.name == "M.G" \
                    or message.name == "M.H" or message.name == "M.I" or message.name == "M.J" \
                    or message.name == "M.K" or message.name == "M.L" or message.name == "M.M" \
                    or message.name == "M.N" or message.name == "M.O" or message.name == "M.P" \
                    or message.name == "M.Q" or message.name == "M.R" or message.name == "M.S" \
                    or message.name == "M.T" or message.name == "M.U" or message.name == "M.V" \
                    or message.name == "M.W" or message.name == "M.X" or message.name == "M.Y" \
                    or message.name == "M.Z":

                    des_cloud = 78
            else:
                    des_cloud = 26

            dst_node = alloc_DES[des_cloud]

            print("\t\t Looking the path to id_node: %i" % dst_node)

            path = list(nx.shortest_path(sim.topology.G, source=node_src, target=dst_node))
            print(path)

            nodeIPT = sim.topology.get_node(dst_node)["IPT"]
            print("IPT OF CLOUD " + str(nodeIPT))
            bestPath = [path]
            bestDES = [des_cloud]
            return bestPath, bestDES

        for des in DES_dst:


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
                    or message.name == "M.E2" or message.name == "M.F2" or message.name == "M.G2"\
                    or message.name == "M.H2" or message.name == "M.I2" or message.name == "M.J2"\
                    or message.name == "M.K2" or message.name == "M.L2" or message.name == "M.M2"\
                    or message.name == "M.N2" or message.name == "M.O2" or message.name == "M.P2"\
                    or message.name == "M.Q2" or message.name == "M.R2" or message.name == "M.S2"\
                    or message.name == "M.T2" or message.name == "M.U2" or message.name == "M.V2"\
                    or message.name == "M.W2" or message.name == "M.X2" or message.name == "M.Y2"\
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
        print("best des" + message.name + str(message.getIns()))
        print(bestDES.__len__())
        self.hm[message.name] = bestDES[0]

        if bestDES[0] in self.tr.keys():
            if self.tr[bestDES[0]] == 1:
                self.busy += 1


        return bestPath, bestDES


class RoundRobinCloud(Selection):

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

        if(8 in DES_dst):
            print("POP" + str(DES_dst.remove(8))) #removing cloud process as that is done manually

        if message.getIns() > 3000:
            # find des of cloud
            if message.name == "M.A" or message.name == "M.B" or message.name == "M.C" or message.name == "M.D":
                des = 8
            else:
                des = 4
            dst_node = alloc_DES[des]

            print("\t\t Looking the path to id_node: %i" % dst_node)

            path = list(nx.shortest_path(sim.topology.G, source=node_src, target=dst_node))
            print(path)
            bestPath = [path]
            bestDES = [des]
            return bestPath, bestDES


        for ix, des in enumerate(DES_dst):
            print("HELLO DES" + str(des))
            print("HELLO NODE " + str(alloc_DES[des]))

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

                    self.rr[message.dst] = (self.rr[message.dst] + 1) % len(DES_dst)
                    break

            else:  # message.name == "M.B or M.D"

                # if message.getIns() > 5000:
                #     # find des of cloud
                #     des = 8
                #     dst_node = 5
                #
                #     print("\t\t Looking the path to id_node: %i" % dst_node)
                #
                #     path = list(nx.shortest_path(sim.topology.G, source=node_src, target=dst_node))
                #     print(path)
                #     bestPath = [path]
                #     bestDES = [des]
                #     return bestPath, bestDES

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
                    #break

        return bestPath, bestDES


class RoundRobinCloudScaled(Selection):

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

        if (78 in DES_dst):
            print("POP" + str(DES_dst.remove(78)))  # removing cloud process as that is done manually

        if message.getIns() > 5000:
            # find des of cloud
            if message.name == "M.A" or message.name == "M.B" or message.name == "M.C" or message.name == "M.D" \
                    or message.name == "M.E" or message.name == "M.F" or message.name == "M.G" \
                    or message.name == "M.H" or message.name == "M.I" or message.name == "M.J" \
                    or message.name == "M.K" or message.name == "M.L" or message.name == "M.M" \
                    or message.name == "M.N" or message.name == "M.O" or message.name == "M.P" \
                    or message.name == "M.Q" or message.name == "M.R" or message.name == "M.S" \
                    or message.name == "M.T" or message.name == "M.U" or message.name == "M.V" \
                    or message.name == "M.W" or message.name == "M.X" or message.name == "M.Y" \
                    or message.name == "M.Z":
                des = 78
            else:
                des = 26
            dst_node = alloc_DES[des]

            print("\t\t Looking the path to id_node: %i" % dst_node)

            path = list(nx.shortest_path(sim.topology.G, source=node_src, target=dst_node))
            print(path)
            bestPath = [path]
            bestDES = [des]
            return bestPath, bestDES

        if (27 in DES_dst):
            print("POP" + str(DES_dst.remove(27)))  # removing random node, idk why it is there

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

            else:  # message.name == "M.B or M.D"

                # if message.getIns() > 5000:
                #     # find des of cloud
                #     des = 8
                #     dst_node = 5
                #
                #     print("\t\t Looking the path to id_node: %i" % dst_node)
                #
                #     path = list(nx.shortest_path(sim.topology.G, source=node_src, target=dst_node))
                #     print(path)
                #     bestPath = [path]
                #     bestDES = [des]
                #     return bestPath, bestDES

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
                break

        return bestPath, bestDES
