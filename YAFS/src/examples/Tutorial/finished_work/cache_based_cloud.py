"""
    @author: isaac
"""
import random
import networkx as nx
import argparse
from pathlib import Path
import time
import numpy as np
import pandas as pd


from my_core import Sim
from MyApplication import Application, Message

from yafs.population import *
from yafs.topology import Topology
from simpleSelectionWithCloud import CacheBasedSolutionWithCloud


from simpleSelection import FIFO
import matplotlib.pyplot as plt
from simpleSelection import RoundRobin
from simpleSelection import CacheBasedSolution
from simpleSelectionWithCloud import RoundRobinCloud
from simpleSelectionWithCloud import FIFOCloud
from simplePlacement import CloudPlacement
from MyStats import Stats
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
    m_a = Message("M.A", "Sensor", "ServiceA", instructions=6000, bytes=6000, broadcasting=False, msgType=1)
    m_a2 = Message("M.A2", "ServiceA", "Actuator", instructions=6000, bytes=6000, broadcasting=False, msgType=1)
    m_b = Message("M.B", "Sensor", "ServiceA", instructions=2000, bytes=2000, broadcasting=False, msgType=3)
    m_b2 = Message("M.B2", "ServiceA", "Actuator", instructions=2000, bytes=2000, broadcasting=False, msgType=3)

    m_c = Message("M.C", "Sensor", "ServiceA", instructions=500, bytes=200, broadcasting=False, msgType=2)
    m_c2 = Message("M.C2", "ServiceA", "Actuator", instructions=500, bytes=200, broadcasting=False, msgType=2)

    m_d = Message("M.D", "Sensor", "ServiceA", instructions=800, bytes=500, broadcasting=False, msgType=1)
    m_d2 = Message("M.D2", "ServiceA", "Actuator", instructions=800, bytes=500, broadcasting=False, msgType=1)

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

    cloud = {"id": 5, "model": "cloud", "mytag": "cloud", "IPT": 100000, "RAM": 4000000, "COST": 10000,
                  "WATT": 20000.0}


    sensor_dev = {"id": 1, "model": "sensor-device", "IPT": 100, "RAM": 4000, "COST": 3, "WATT": 40.0}
    actuator_dev = {"id": 2, "model": "actuator-device", "IPT": 100, "RAM": 4000, "COST": 3, "WATT": 40.0}

    # if ipt of node is less than instructions of message, send to another node and store in hm

    link1 = {"s": 1, "d": 0, "BW": 1, "PR": 1}
    link2 = {"s": 0, "d": 2, "BW": 1, "PR": 1}
    link3 = {"s": 1, "d": 3, "BW": 1, "PR": 1}
    link4 = {"s": 3, "d": 2, "BW": 1, "PR": 1}
    link5 = {"s": 1, "d": 4, "BW": 1, "PR": 1}
    link6 = {"s": 4, "d": 2, "BW": 1, "PR": 1}

    link7 = {"s": 1, "d": 5, "BW": 1, "PR": 10}
    link8 = {"s": 5, "d": 2, "BW": 1, "PR": 10}

    topology_json["entity"].append(cloud_dev)
    topology_json["entity"].append(cloud_dev2)
    topology_json["entity"].append(cloud_dev3)
    topology_json["entity"].append(cloud)

    topology_json["entity"].append(sensor_dev)
    topology_json["entity"].append(actuator_dev)
    topology_json["link"].append(link1)
    topology_json["link"].append(link2)
    topology_json["link"].append(link3)
    topology_json["link"].append(link4)
    topology_json["link"].append(link5)
    topology_json["link"].append(link6)

    topology_json["link"].append(link7)
    topology_json["link"].append(link8)

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
                  folder_results + "graph_cache_based")  # you can export the Graph in multiples format to view in tools likFFe Gephi, and so on.
    nx.draw(t.G, with_labels=True)
    plt.savefig(folder_results + "graph_cache_based.png")
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
    dDistribution = deterministic_distribution(name="Deterministic", time=100)
    # pop = SimpleDynamicChanges(2, name="Dynamic", activation_dist=dDistribution)
    # For each type of sink modules we set a deployment on some type of devices
    # A control sink consists on:
    #  args:
    #     model (str): identifies the device or devices where the sink is linked
    #     number (int): quantity of sinks linked in each device
    #     module (str): identifies the module from the app who receives the messages
    pop.set_sink_control({"model": "actuator-device", "number": 1, "module": app.get_sink_modules()})

    # In addition, a source includes a distribution function:

    msgList = [app.get_message("M.A"), app.get_message("M.B"), app.get_message("M.C"), app.get_message("M.D")]
    #sort(msgList) # remove this to make fcfs
    # sortQueue(msgList) # UNCOMMENT TO ENABLE DPTO

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

    selectorPath = CacheBasedSolutionWithCloud()
    #selectorPath = FIFOCloud()
    #selectorPath = RoundRobinCloud()

    """
    SIMULATION ENGINE
    """

    stop_time = simulated_time
    s = Sim(t, default_results_path=folder_results + "sim_trace")

    s.deploy_app2(app, placement, pop, selectorPath)

    """
    RUNNING - last step
    """
    s.run(stop_time, show_progress_monitor=False)

    s.print_debug_assignaments()

    # s.draw_allocated_topology() # for debugging

def sortQueue(msgList):
    # message list
    if msgList is not None:

        if len(msgList) != 0:

            n = len(msgList)
            for i in range(n - 1):

                for j in range(0, n - i - 1):

                    if (msgList[j]).msgType < (msgList[j + 1]).msgType:
                        msgList[j], msgList[j + 1] = msgList[j + 1], msgList[j]

    # rules



def search():
    pass


def sort(msgList):
    if msgList is not None:

        if len(msgList) != 0:

            n = len(msgList)
            for i in range(n - 1):

                for j in range(0, n - i - 1):

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
    t = Topology()
    t_json = create_json_topology()
    t.load(t_json)
    print("-" * 20)
    print("Results:")
    print("-" * 20)
    m = Stats(defaultPath="results/sim_trace")  # Same name of the results
    time_loops = [["M.A", "M.A2"], ["M.B", "M.B2"], ["M.C", "M.C2"], ["M.D", "M.D2"]]
    m.showResults2(1000, time_loops=time_loops)

    print("\t- Network saturation -")

    print("\t\t Bytes Transmitted : %i" % m.bytes_transmitted())

    energy = m.get_watt(1000, t)
    totalenergy = 0
    countnodes = 0
    for node in energy:
        if energy[node]["watt"] == 0.0:
            continue
        totalenergy += energy[node]["watt"]
        countnodes += 1
    print("----------------------------------------")
    print("ENERGY")
    print("Energy : " + str(totalenergy / countnodes))

    ## results
    print("----------------------------------------")
    print("LATENCY")
    folder_results = Path("results/")
    folder_results.mkdir(parents=True, exist_ok=True)
    folder_results = str(folder_results) + "/"
    path = folder_results + "sim_trace.csv"
    info = pd.read_csv(path)
    data = pd.DataFrame(info)
    latency = data['latency'].sum() + data['time_response'].sum()
    count = data.shape[0]
    avg = latency / count
    print("Latency : " + str(avg))
    throughput = data["throughput"].sum()/count
    print("----------------------------------------")
    print("THROUGHPUT")
    print("Throughput : " + str(throughput))
