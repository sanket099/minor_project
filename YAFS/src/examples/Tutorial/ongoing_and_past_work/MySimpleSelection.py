from yafs.selection import Selection
from MySelection import MySelection
import networkx as nx
from yafs.application import Message


# class FIFO(MySelection):
#
#     def get_path(self, sim, app_name, message, topology_src, alloc_DES, alloc_module, traffic, from_des):
#         """
#         Computes the minimun path among the source elemento of the topology and the localizations of the module
#         Return the path and the identifier of the module deployed in the last element of that path
#         """
#         node_src = topology_src
#         DES_dst = alloc_module[app_name][message.dst]
#
#         print("GET PATH")
#         print("\tNode _ src (id_topology): %i" % node_src)
#         print("\tRequest service: %s " % message.dst)
#         print("\tProcess serving that service: %s " % DES_dst)
#
#         bestPath = []
#         bestDES = []
#
#         for des in DES_dst:  ## In this case, there are only one deployment
#             dst_node = alloc_DES[des]
#             print("\t\t Looking the path to id_node: %i" % dst_node)
#
#             path = list(nx.shortest_path(sim.topology.G, source=node_src, target=dst_node))
#
#             bestPath = [path]
#             bestDES = [des]
#
#         return bestPath, bestDES


class MinPath_RoundRobin(MySelection):

    def __init__(self, msgList):
        self.rr = {}  # for a each type of service, we have a mod-counter
        self.msg_list = msgList

    def get_path(self, sim, app_name, message, topology_src, alloc_DES, alloc_module, traffic, from_des):
        """
        Computes the minimun path among the source elemento of the topology and the localizations of the module
        Return the path and the identifier of the module deployed in the last element of that path


        """
        # msgList = self.msg_list
        # print("MSGLIST " + str(msgList))
        #
        # if (msgList != None):
        #
        #     if (len(msgList) != 0):
        #
        #         n = len(msgList)
        #
        #         # Traverse through all array elements
        #         for i in range(n - 1):
        #             # range(n) also work but outer loop will repeat one time more than needed.
        #
        #             # Last i elements are already in place
        #             for j in range(0, n - i - 1):
        #
        #                 # traverse the array from 0 to n-i-1
        #                 # Swap if the element found is greater
        #                 # than the next element
        #
        #                 if (msgList[j]).inst > (msgList[j + 1]).inst:
        #                     msgList[j], msgList[j + 1] = msgList[j + 1], msgList[j]
        #
        #         print(msgList[0].name)
        #         message = msgList[0]
        #         del msgList[0]
        #

                #print("MSGLIST[0]" + str(msgList[0]))

        node_src = topology_src
        DES_dst = alloc_module[app_name][message.dst]  # returns an array with all DES process serving

        print("alloc module " + str(alloc_module[app_name]))

        if message.dst not in self.rr.keys():
            self.rr[message.dst] = 0

        print("Traffic " + str(traffic))
        print("GET PATH ")
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

            if message.name == "M.A" or message.name == "M.B":
                print("rr dict " + str(self.rr))

                if self.rr[message.dst] == ix:
                    dst_node = alloc_DES[des]

                    path = list(nx.shortest_path(sim.topology.G, source=node_src, target=dst_node))
                    print("path " + str(path))

                    bestPath = [path]
                    bestDES = [des]

                    self.rr[message.dst] = (self.rr[message.dst] + 1) % len(DES_dst)
                    break
            else:  # message.name == "M.B"

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
