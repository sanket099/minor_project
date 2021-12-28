"""
    @author: isaac
"""
import random
import networkx as nx
import argparse
from pathlib import Path
import time
import numpy as np

from yafs.core import Sim
from MyApplication import Application, Message

from yafs.population import *
from yafs.topology import Topology
from simpleSelection import MinimunPath
import matplotlib.pyplot as plt
from MySimpleSelection import MinPath_RoundRobin
from simplePlacement import CloudPlacement
from yafs.stats import Stats
from yafs.distribution import deterministic_distribution
from yafs.application import fractional_selectivity

RANDOM_SEED = 1


def create_application():
    # APLICATION
    a = Application(name="SimpleCase")

    # (S) --> (ServiceA) --> (A)
    a.set_modules([{"Sensor": {"Type": Application.TYPE_SOURCE}},
                   {"ServiceA": {"RAM": 10, "Type": Application.TYPE_MODULE}},
                   # {"ServiceB": {"RAM": 10, "Type": Application.TYPE_MODULE}},
                   {"Actuator": {"Type": Application.TYPE_SINK}}
                   ])
    """
    Messages among MODULES (AppEdge in iFogSim)
    """
    m_a = Message("M.A", "Sensor", "ServiceA", instructions=900, bytes=100000, msgType=0)
    m_a2 = Message("M.A2", "ServiceA", "Actuator", instructions=900, bytes=100000, msgType=0)
    m_b = Message("M.B", "Sensor", "ServiceA", instructions=100, bytes=100, broadcasting=False, msgType=1)
    m_b2 = Message("M.B2", "ServiceA", "Actuator", instructions=100, bytes=100, broadcasting=False, msgType=1)

    m_c = Message("M.C", "Sensor", "ServiceA", instructions=500, bytes=200, broadcasting=False, msgType=2)
    m_c2 = Message("M.C2", "ServiceA", "Actuator", instructions=500, bytes=200, broadcasting=False, msgType=2)

    m_d = Message("M.D", "Sensor", "ServiceA", instructions=800, bytes=500, broadcasting=False, msgType=3)
    m_d2 = Message("M.D2", "ServiceA", "Actuator", instructions=800, bytes=500, broadcasting=False, msgType=3)

    """
    Defining which messages will be dynamically generated # the generation is controlled by Population algorithm
    """
    a.add_source_messages(m_a)
    a.add_source_messages(m_b)

    a.add_source_messages(m_c)
    a.add_source_messages(m_d)

    """
    MODULES/SERVICES: Definition of Generators and Consumers (AppEdges and TupleMappings in iFogSim)
    """
    # MODULE SERVICES
    a.add_service_module("ServiceA", m_a, m_a2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_b, m_b2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_c, m_c2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_d, m_d2, fractional_selectivity, threshold=1.0)
    # a.add_service_module("ServiceB", m_b, m_b2, fractional_selectivity, threshold=1.0)

    return a


def create_json_topology():
    """
       TOPOLOGY DEFINITION
       Some attributes of fog entities (nodes) are approximate
       """

    ## MANDATORY FIELDS
    topology_json = {}
    topology_json["entity"] = []
    topology_json["link"] = []

    cloud_dev = {"id": 0, "model": "cloud", "mytag": "cloud", "IPT": 500, "RAM": 40000, "COST": 3,
                 "WATT": 200.0}
    cloud_dev2 = {"id": 3, "model": "cloud", "mytag": "cloud", "IPT": 100, "RAM": 40000, "COST": 3,
                  "WATT": 200.0}
    cloud_dev3 = {"id": 4, "model": "cloud", "mytag": "cloud", "IPT": 800, "RAM": 40000, "COST": 3,
                  "WATT": 200.0}
    sensor_dev = {"id": 1, "model": "sensor-device", "IPT": 100 * 10 ^ 6, "RAM": 4000, "COST": 3, "WATT": 40.0}
    actuator_dev = {"id": 2, "model": "actuator-device", "IPT": 100 * 10 ^ 6, "RAM": 4000, "COST": 3, "WATT": 40.0}

    # if ipt of node is less than instructions of message, send to another node and store in hm

    link1 = {"s": 1, "d": 0, "BW": 1, "PR": 1}
    link2 = {"s": 0, "d": 2, "BW": 1, "PR": 1}
    link3 = {"s": 1, "d": 3, "BW": 1, "PR": 1}
    link4 = {"s": 3, "d": 2, "BW": 1, "PR": 1}
    link5 = {"s": 1, "d": 4, "BW": 1, "PR": 1}
    link6 = {"s": 4, "d": 2, "BW": 1, "PR": 1}

    topology_json["entity"].append(cloud_dev)
    topology_json["entity"].append(cloud_dev2)
    topology_json["entity"].append(cloud_dev3)

    topology_json["entity"].append(sensor_dev)
    topology_json["entity"].append(actuator_dev)
    topology_json["link"].append(link1)
    topology_json["link"].append(link2)
    topology_json["link"].append(link3)
    topology_json["link"].append(link4)
    topology_json["link"].append(link5)
    topology_json["link"].append(link6)

    return topology_json


# @profile
def main(simulated_time):
    random.seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)

    folder_results = Path("results/")
    folder_results.mkdir(parents=True, exist_ok=True)
    folder_results = str(folder_results) + "/"

    """
    TOPOLOGY from a json
    """
    t = Topology()
    t_json = create_json_topology()
    t.load(t_json)
    nx.write_gexf(t.G,
                  folder_results + "graph_main2")  # you can export the Graph in multiples format to view in tools like Gephi, and so on.
    nx.draw(t.G, with_labels=True)
    plt.savefig(folder_results + "graph_main2_topo.png")
    """
    APPLICATION
    """
    app = create_application()

    """
    PLACEMENT algorithm
    """
    placement = CloudPlacement("onCloud")  # it defines the deployed rules: module-device
    placement.scaleService({"ServiceA": 1})

    """
    POPULATION algorithm
    """
    # In ifogsim, during the creation of the application, the Sensors are assigned to the topology, in this case no. As mentioned,
    # YAFS differentiates the adaptive sensors and their topological assignment.
    # In their case, the use a statical assignment.
    pop = Statical("Statical")
    # For each type of sink modules we set a deployment on some type of devices
    # A control sink consists on:
    #  args:
    #     model (str): identifies the device or devices where the sink is linked
    #     number (int): quantity of sinks linked in each device
    #     module (str): identifies the module from the app who receives the messages
    pop.set_sink_control({"model": "actuator-device", "number": 2, "module": app.get_sink_modules()})

    # In addition, a source includes a distribution function:
    dDistribution = deterministic_distribution(name="Deterministic", time=100)
    msgList = [app.get_message("M.A"), app.get_message("M.B"), app.get_message("M.C"), app.get_message("M.D")]
    sort(msgList)  # remove this to make fcfs
    for i in msgList:
        pop.set_src_control({"model": "sensor-device", "number": 1, "message": i,
                             "distribution": dDistribution})  # 5.1}})
        # pop.set_src_control({"model": "sensor-device", "number": 1, "message": app.get_message("M.B"),
        #                      "distribution": dDistribution})  # 5.1}})
    """
    SELECTOR algorithm
    """
    # Their "selector" is actually the shortest way, there is not type of orchestration algorithm.
    # This implementation is already created in selector.class,called: First_ShortestPath



    selectorPath = MinimunPath()

    print("Selector Path" + str(selectorPath))

    """
    SIMULATION ENGINE
    """

    stop_time = simulated_time
    s = Sim(t, default_results_path="results/" + "sim_trace")

    s.deploy_app2(app, placement, pop, selectorPath)

    """
    RUNNING - last step
    """
    s.run(stop_time, show_progress_monitor=False)
    s.print_debug_assignaments()

    # s.draw_allocated_topology() # for debugging


def sort(msgList):
    if msgList is not None:

        if len(msgList) != 0:

            n = len(msgList)

            # Traverse through all array elements
            for i in range(n - 1):
                # range(n) also work but outer loop will repeat one time more than needed.

                # Last i elements are already in place
                for j in range(0, n - i - 1):

                    # traverse the array from 0 to n-i-1
                    # Swap if the element found is greater
                    # than the next element

                    if (msgList[j]).inst > (msgList[j + 1]).inst:
                        msgList[j], msgList[j + 1] = msgList[j + 1], msgList[j]


if __name__ == '__main__':
    import logging.config
    import os

    logging.config.fileConfig(os.getcwd() + '/logging.ini')

    start_time = time.time()
    main(simulated_time=1000)

    print("\n--- %s seconds ---" % (time.time() - start_time))

    ## Finally, you can analyse the results:
    print("-" * 20)
    print("Results:")
    print("-" * 20)
    m = Stats(defaultPath="results/sim_trace")  # Same name of the results
    time_loops = [["M.A", "M.A2"], ["M.B", "M.B2"], ["M.C", "M.C2"], ["M.D", "M.D2"]]
    m.showResults2(1000, time_loops=time_loops)

    print("\t- Network saturation -")
    # print("\t\tAverage waiting messages : %i" % m.average_messages_not_transmitted())
    print("\t\t Bytes Transmitted : %i" % m.bytes_transmitted())
    # print("\t\tPeak of waiting messages : %i" % m.peak_messages_not_transmitted())

    # print("\t\tTOTAL messages not transmitted: %i" % m.messages_not_transmitted())
    t = Topology()
    t_json = create_json_topology()
    t.load(t_json)
    print("\t\t Energy " + str(m.get_watt(1000, t)))

#    print("\t\t get_cost_cloud" + str(m.get_cost_cloud(t)))

    print("\t\t Show Results")
    m.showResults(1000, t, time_loops=time_loops)

    # print("\t\t Latency " + m.get_latency())
    print("\n\t- Stats of each service deployed -")

    # Throughput is a measure of how many units of information a system can process in a given amount of time.

    # print (m.get_df_modules())
    # print (m.get_df_service_utilization("ServiceA",1000))

    # print ("\n\t- Stats of each DEVICE -")

    # TODO
