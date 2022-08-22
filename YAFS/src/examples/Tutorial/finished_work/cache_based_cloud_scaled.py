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
from simpleSelectionWithCloud import CacheBasedSolutionWithCloudScaled
from simpleSelection import FIFO
from simpleSelectionWithCloud import FIFOCloudScaled
import matplotlib.pyplot as plt
from simpleSelection import RoundRobin
from simpleSelection import CacheBasedSolution
from simpleSelectionWithCloud import RoundRobinCloud
from simpleSelectionWithCloud import RoundRobinCloudScaled
from simplePlacement import CloudPlacement
from MyStats import Stats
from yafs.distribution import deterministic_distribution
from yafs.application import fractional_selectivity
import json

RANDOM_SEED = 1
def create_application_test():
    random.seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)
    a = Application(name="SimpleCase")

    # (S) --> (ServiceA) --> (A)
    a.set_modules([{"Sensor": {"Type": Application.TYPE_SOURCE}},
                   {"ServiceA": {"RAM": 10, "Type": Application.TYPE_MODULE}},
                   # {"ServiceB": {"RAM": 10, "Type": Application.TYPE_MODULE}},
                   {"Actuator": {"Type": Application.TYPE_SINK}}
                   ])

    n = 100
    c = 65
    for i in range(1,n):
        if(i <= 26):
            create_message(a, i, c)
            c += 1
        else:
            create_message(a, i, 0)

    return a
def getMessageName():
    ascii_value = random.randint(65, 90)
    return chr(ascii_value)

def get_message_bytes():
    return random.randint(1,2)
def getFirst26Messages(ascii_id):
    return chr(ascii_id)
def create_message(a, i, asc):
    if(i > 26 ):
        message_name = "M." + getMessageName()
    else:
        message_name = "M." + getFirst26Messages(asc)
    message_ins = random_value()
    message_bytes = random_value()
    message_type = random.randint(1, 3)
    m_a = Message( message_name, "Sensor", "ServiceA", message_ins, bytes=message_bytes, broadcasting=False, msgType=message_type)
    m_a2 = Message( message_name + "2", "ServiceA", "Actuator", message_ins, bytes=message_bytes, broadcasting=False, msgType=message_type)
    a.add_source_messages(m_a)
    a.add_service_module("ServiceA", m_a, m_a2, fractional_selectivity, threshold=1.0)

def random_value():
    return random.randint(1000, 60000)

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
    m_a = Message("M.A" , "Sensor", "ServiceA", random_value(), bytes=900, broadcasting=False, msgType=1)
    m_a2 = Message("M.A2", "ServiceA", "Actuator", random_value(), bytes=900, broadcasting=False, msgType=1)
    m_b = Message("M.B", "Sensor", "ServiceA", random_value(), bytes=100, broadcasting=False, msgType=3)
    m_b2 = Message("M.B2", "ServiceA", "Actuator", random_value(), bytes=100, broadcasting=False, msgType=3)

    m_c = Message("M.C", "Sensor", "ServiceA", random_value() ,bytes=200, broadcasting=False, msgType=2)
    m_c2 = Message("M.C2", "ServiceA", "Actuator", random_value() ,bytes=200, broadcasting=False, msgType=2)

    m_d = Message("M.D", "Sensor", "ServiceA", random_value(), bytes=500, broadcasting=False, msgType=2)
    m_d2 = Message("M.D2", "ServiceA", "Actuator", random_value() ,bytes=500, broadcasting=False, msgType=2)

    m_e = Message("M.E", "Sensor", "ServiceA", random_value(), bytes=500, broadcasting=False, msgType=2)
    m_e2 = Message("M.E2", "ServiceA", "Actuator", random_value(), bytes=500, broadcasting=False, msgType=2)

    m_f = Message("M.F", "Sensor", "ServiceA", random_value(), bytes=500, broadcasting=False, msgType=3)
    m_f2 = Message("M.F2", "ServiceA", "Actuator", random_value(), bytes=500, broadcasting=False, msgType=3)

    m_g = Message("M.G", "Sensor", "ServiceA", random_value(), bytes=500, broadcasting=False, msgType=1)
    m_g2 = Message("M.G2", "ServiceA", "Actuator", random_value(), bytes=500, broadcasting=False, msgType=1)

    m_h = Message("M.H", "Sensor", "ServiceA", random_value(), bytes=500, broadcasting=False, msgType=2)
    m_h2 = Message("M.H2", "ServiceA", "Actuator", random_value(), bytes=500, broadcasting=False, msgType=2)

    m_i = Message("M.I", "Sensor", "ServiceA", random_value() ,bytes=500, broadcasting=False, msgType=1)
    m_i2 = Message("M.I2", "ServiceA", "Actuator", random_value(), bytes=500, broadcasting=False, msgType=1)

    m_j = Message("M.J", "Sensor", "ServiceA", random_value(), bytes=500, broadcasting=False, msgType=3)
    m_j2 = Message("M.J2", "ServiceA", "Actuator", random_value(), bytes=500, broadcasting=False, msgType=3)

    m_k = Message("M.K", "Sensor", "ServiceA", random_value(), bytes=500, broadcasting=False, msgType=3)
    m_k2 = Message("M.K2", "ServiceA", "Actuator", random_value(), bytes=500, broadcasting=False, msgType=3)

    m_l = Message("M.L", "Sensor", "ServiceA", random_value(), bytes=500, broadcasting=False, msgType=1)
    m_l2 = Message("M.L2", "ServiceA", "Actuator", random_value(), bytes=500, broadcasting=False, msgType=1)

    m_m = Message("M.M", "Sensor", "ServiceA", random_value(), bytes=500, broadcasting=False, msgType=2)
    m_m2 = Message("M.M2", "ServiceA", "Actuator", random_value(), bytes=500, broadcasting=False, msgType=2)

    m_n = Message("M.N", "Sensor", "ServiceA", random_value(), bytes=500, broadcasting=False, msgType=3)
    m_n2 = Message("M.N2", "ServiceA", "Actuator", random_value(), bytes=500, broadcasting=False, msgType=3)
    m_o = Message("M.O", "Sensor", "ServiceA", random_value(), bytes=500, broadcasting=False, msgType=2)
    m_o2 = Message("M.O2", "ServiceA", "Actuator", random_value(), bytes=500, broadcasting=False, msgType=2)

    m_p = Message("M.P", "Sensor", "ServiceA", random_value(), bytes=500, broadcasting=False, msgType=2)
    m_p2 = Message("M.P2", "ServiceA", "Actuator", random_value(), bytes=500, broadcasting=False, msgType=2)

    m_q = Message("M.Q", "Sensor", "ServiceA", random_value(), bytes=500, broadcasting=False, msgType=1)
    m_q2 = Message("M.Q2", "ServiceA", "Actuator", random_value(), bytes=500, broadcasting=False, msgType=1)
    m_r = Message("M.R", "Sensor", "ServiceA", random_value(), bytes=500, broadcasting=False, msgType=1)
    m_r2 = Message("M.R2", "ServiceA", "Actuator", random_value(), bytes=500, broadcasting=False, msgType=1)

    m_s = Message("M.S", "Sensor", "ServiceA", random_value(), bytes=500, broadcasting=False, msgType=3)
    m_s2 = Message("M.S2", "ServiceA", "Actuator", random_value(), bytes=500, broadcasting=False, msgType=3)
    m_t = Message("M.T", "Sensor", "ServiceA", random_value(), bytes=500, broadcasting=False, msgType=3)
    m_t2 = Message("M.T2", "ServiceA", "Actuator", random_value(), bytes=500, broadcasting=False, msgType=3)

    m_u = Message("M.U", "Sensor", "ServiceA", random_value(), bytes=500, broadcasting=False, msgType=1)
    m_u2 = Message("M.U2", "ServiceA", "Actuator", random_value(), bytes=500, broadcasting=False, msgType=1)
    m_v = Message("M.V", "Sensor", "ServiceA", random_value(), bytes=500, broadcasting=False, msgType=2)
    m_v2 = Message("M.V2", "ServiceA", "Actuator", random_value(), bytes=500, broadcasting=False, msgType=2)

    m_w = Message("M.W", "Sensor", "ServiceA", random_value(), bytes=500, broadcasting=False, msgType=2)
    m_w2 = Message("M.W2", "ServiceA", "Actuator", random_value(), bytes=500, broadcasting=False, msgType=2)
    m_x = Message("M.X", "Sensor", "ServiceA", random_value(), bytes=500, broadcasting=False, msgType=2)
    m_x2 = Message("M.X2", "ServiceA", "Actuator", random_value(), bytes=500, broadcasting=False, msgType=2)

    m_y = Message("M.Y", "Sensor", "ServiceA", random_value(), bytes=500, broadcasting=False, msgType=2)
    m_y2 = Message("M.Y2", "ServiceA", "Actuator", random_value(), bytes=500, broadcasting=False, msgType=2)
    m_z = Message("M.Z", "Sensor", "ServiceA", random_value(), bytes=500, broadcasting=False, msgType=1)
    m_z2 = Message("M.Z2", "ServiceA", "Actuator", random_value(), bytes=500, broadcasting=False, msgType=1)

    m_aa = Message("M.A", "Sensor", "ServiceA", random_value(),  bytes=900, broadcasting=False, msgType=1)
    m_aa2 = Message("M.A2", "ServiceA", "Actuator", random_value(), bytes=900, broadcasting=False, msgType=1)
    m_bb = Message("M.B", "Sensor", "ServiceA", random_value(), bytes=100, broadcasting=False, msgType=1)
    m_bb2 = Message("M.B2", "ServiceA", "Actuator", random_value(), bytes=100, broadcasting=False, msgType=1)

    m_cc = Message("M.C", "Sensor", "ServiceA", random_value() , bytes=200, broadcasting=False, msgType=3)
    m_cc2 = Message("M.C2", "ServiceA", "Actuator", random_value() , bytes=200, broadcasting=False, msgType=3)

    m_dd = Message("M.D", "Sensor", "ServiceA", random_value() , bytes=500, broadcasting=False, msgType=3)
    m_dd2 = Message("M.D2", "ServiceA", "Actuator", random_value() , bytes=500, broadcasting=False, msgType=3)

    m_ee = Message("M.E", "Sensor", "ServiceA", random_value(), bytes=500, broadcasting=False, msgType=2)
    m_ee2 = Message("M.E2", "ServiceA", "Actuator", random_value(), bytes=500, broadcasting=False, msgType=2)

    m_ff = Message("M.F", "Sensor", "ServiceA", random_value(), bytes=500, broadcasting=False, msgType=1)
    m_ff2 = Message("M.F2", "ServiceA", "Actuator", random_value(), bytes=500, broadcasting=False, msgType=1)

    m_gg = Message("M.G", "Sensor", "ServiceA", random_value(), bytes=500, broadcasting=False, msgType=2)
    m_gg2 = Message("M.G2", "ServiceA", "Actuator", random_value(), bytes=500, broadcasting=False, msgType=2)

    m_hh = Message("M.H", "Sensor", "ServiceA", random_value(), bytes=500, broadcasting=False, msgType=3)
    m_hh2 = Message("M.H2", "ServiceA", "Actuator", random_value(), bytes=500, broadcasting=False, msgType=3)

    m_ii = Message("M.I", "Sensor", "ServiceA", random_value(), bytes=500, broadcasting=False, msgType=1)
    m_ii2 = Message("M.I2", "ServiceA", "Actuator", random_value() ,bytes=500, broadcasting=False, msgType=1)

    m_jj = Message("M.J", "Sensor", "ServiceA", random_value(), bytes=500, broadcasting=False, msgType=3)
    m_jj2 = Message("M.J2", "ServiceA", "Actuator", random_value(), bytes=500, broadcasting=False, msgType=3)

    m_kk = Message("M.K", "Sensor", "ServiceA", random_value(), bytes=500, broadcasting=False, msgType=1)
    m_kk2 = Message("M.K2", "ServiceA", "Actuator", random_value(), bytes=500, broadcasting=False, msgType=1)

    m_ll = Message("M.L", "Sensor", "ServiceA", random_value(), bytes=500, broadcasting=False, msgType=1)
    m_ll2 = Message("M.L2", "ServiceA", "Actuator", random_value(), bytes=500, broadcasting=False, msgType=1)

    m_mm = Message("M.M", "Sensor", "ServiceA", random_value(), bytes=500, broadcasting=False, msgType=2)
    m_mm2 = Message("M.M2", "ServiceA", "Actuator", random_value(), bytes=500, broadcasting=False, msgType=2)

    m_nn = Message("M.N", "Sensor", "ServiceA", random_value(), bytes=500, broadcasting=False, msgType=3)
    m_nn2 = Message("M.N2", "ServiceA", "Actuator", random_value(), bytes=500, broadcasting=False, msgType=3)
    m_oo = Message("M.O", "Sensor", "ServiceA", random_value() ,bytes=500, broadcasting=False, msgType=2)
    m_oo2 = Message("M.O2", "ServiceA", "Actuator", random_value() ,bytes=500, broadcasting=False, msgType=2)

    m_pp = Message("M.P", "Sensor", "ServiceA", random_value() ,bytes=500, broadcasting=False, msgType=2)
    m_pp2 = Message("M.P2", "ServiceA", "Actuator", random_value() ,bytes=500, broadcasting=False, msgType=2)

    m_qq = Message("M.Q", "Sensor", "ServiceA", random_value(), bytes=500, broadcasting=False, msgType=1)
    m_qq2 = Message("M.Q2", "ServiceA", "Actuator", random_value(), bytes=500, broadcasting=False, msgType=1)
    m_rr = Message("M.R", "Sensor", "ServiceA", random_value(), bytes=500, broadcasting=False, msgType=3)
    m_rr2 = Message("M.R2", "ServiceA", "Actuator", random_value(), bytes=500, broadcasting=False, msgType=3)

    m_ss = Message("M.S", "Sensor", "ServiceA", random_value() ,bytes=500, broadcasting=False, msgType=2)
    m_ss2 = Message("M.S2", "ServiceA", "Actuator", random_value() ,bytes=500, broadcasting=False, msgType=2)
    m_tt = Message("M.T", "Sensor", "ServiceA", random_value(), bytes=500, broadcasting=False, msgType=1)
    m_tt2 = Message("M.T2", "ServiceA", "Actuator", random_value(), bytes=500, broadcasting=False, msgType=1)

    m_uu = Message("M.U", "Sensor", "ServiceA", random_value(), bytes=500, broadcasting=False, msgType=1)
    m_uu2 = Message("M.U2", "ServiceA", "Actuator", random_value(), bytes=500, broadcasting=False, msgType=1)
    m_vv = Message("M.V", "Sensor", "ServiceA", random_value(), bytes=500, broadcasting=False, msgType=2)
    m_vv2 = Message("M.V2", "ServiceA", "Actuator", random_value(), bytes=500, broadcasting=False, msgType=2)

    m_ww = Message("M.W", "Sensor", "ServiceA", random_value(), bytes=500, broadcasting=False, msgType=3)
    m_ww2 = Message("M.W2", "ServiceA", "Actuator", random_value(), bytes=500, broadcasting=False, msgType=3)
    m_xx = Message("M.X", "Sensor", "ServiceA", random_value(), bytes=500, broadcasting=False, msgType=3)
    m_xx2 = Message("M.X2", "ServiceA", "Actuator", random_value(), bytes=500, broadcasting=False, msgType=3)

    m_yy = Message("M.Y", "Sensor", "ServiceA", random_value(), bytes=500, broadcasting=False, msgType=3)
    m_yy2 = Message("M.Y2", "ServiceA", "Actuator", random_value(), bytes=500, broadcasting=False, msgType=3)
    m_zz = Message("M.Z", "Sensor", "ServiceA", random_value(), bytes=500, broadcasting=False, msgType=2)
    m_zz2 = Message("M.Z2", "ServiceA", "Actuator", random_value(), bytes=500, broadcasting=False, msgType=2)

    m_aaa = Message("M.A", "Sensor", "ServiceA", random_value(), bytes=900, broadcasting=False, msgType=1)
    m_aaa2 = Message("M.A2", "ServiceA", "Actuator", random_value(), bytes=900, broadcasting=False, msgType=1)
    m_bbb = Message("M.B", "Sensor", "ServiceA", random_value(), bytes=100, broadcasting=False, msgType=1)
    m_bbb2 = Message("M.B2", "ServiceA", "Actuator", random_value(), bytes=100, broadcasting=False, msgType=1)

    m_ccc = Message("M.C", "Sensor", "ServiceA", random_value() ,bytes=200, broadcasting=False, msgType=1)
    m_ccc2 = Message("M.C2", "ServiceA", "Actuator", random_value(), bytes=200, broadcasting=False, msgType=1)

    m_ddd = Message("M.D", "Sensor", "ServiceA", random_value(), bytes=500, broadcasting=False, msgType=2)
    m_ddd2 = Message("M.D2", "ServiceA", "Actuator", random_value(), bytes=500, broadcasting=False, msgType=2)

    m_eee = Message("M.E", "Sensor", "ServiceA", random_value(), bytes=500, broadcasting=False, msgType=2)
    m_eee2 = Message("M.E2", "ServiceA", "Actuator", random_value(), bytes=500, broadcasting=False, msgType=2)

    m_fff = Message("M.F", "Sensor", "ServiceA", random_value(), bytes=500, broadcasting=False, msgType=3)
    m_fff2 = Message("M.F2", "ServiceA", "Actuator", random_value(), bytes=500, broadcasting=False, msgType=3)

    m_ggg = Message("M.G", "Sensor", "ServiceA", random_value(), bytes=500, broadcasting=False, msgType=1)
    m_ggg2 = Message("M.G2", "ServiceA", "Actuator", random_value(), bytes=500, broadcasting=False, msgType=1)

    m_hhh = Message("M.H", "Sensor", "ServiceA", random_value(), bytes=500, broadcasting=False, msgType=1)
    m_hhh2 = Message("M.H2", "ServiceA", "Actuator", random_value(), bytes=500, broadcasting=False, msgType=1)

    m_iii = Message("M.I", "Sensor", "ServiceA", random_value(), bytes=500, broadcasting=False, msgType=3)
    m_iii2 = Message("M.I2", "ServiceA", "Actuator", random_value(), bytes=500, broadcasting=False, msgType=3)

    m_jjj = Message("M.J", "Sensor", "ServiceA", random_value(), bytes=500, broadcasting=False, msgType=3)
    m_jjj2 = Message("M.J2", "ServiceA", "Actuator", random_value(), bytes=500, broadcasting=False, msgType=3)

    m_kkk = Message("M.K", "Sensor", "ServiceA", random_value(), bytes=500, broadcasting=False, msgType=2)
    m_kkk2 = Message("M.K2", "ServiceA", "Actuator", random_value(), bytes=500, broadcasting=False, msgType=2)

    m_lll = Message("M.L", "Sensor", "ServiceA", random_value(), bytes=500, broadcasting=False, msgType=2)
    m_lll2 = Message("M.L2", "ServiceA", "Actuator", random_value(), bytes=500, broadcasting=False, msgType=2)

    m_mmm = Message("M.M", "Sensor", "ServiceA", random_value(), bytes=500, broadcasting=False, msgType=2)
    m_mmm2 = Message("M.M2", "ServiceA", "Actuator", random_value(), bytes=500, broadcasting=False, msgType=2)

    m_nnn = Message("M.N", "Sensor", "ServiceA", random_value(), bytes=500, broadcasting=False, msgType=2)
    m_nnn2 = Message("M.N2", "ServiceA", "Actuator", random_value(), bytes=500, broadcasting=False, msgType=2)
    m_ooo = Message("M.O", "Sensor", "ServiceA", random_value(), bytes=500, broadcasting=False, msgType=1)
    m_ooo2 = Message("M.O2", "ServiceA", "Actuator", random_value() ,bytes=500, broadcasting=False, msgType=1)

    m_ppp = Message("M.P", "Sensor", "ServiceA", random_value() ,bytes=500, broadcasting=False, msgType=1)
    m_ppp2 = Message("M.P2", "ServiceA", "Actuator", random_value() ,bytes=500, broadcasting=False, msgType=1)

    m_qqq = Message("M.Q", "Sensor", "ServiceA", random_value(), bytes=500, broadcasting=False, msgType=2)
    m_qqq2 = Message("M.Q2", "ServiceA", "Actuator", random_value(), bytes=500, broadcasting=False, msgType=2)
    m_rrr = Message("M.R", "Sensor", "ServiceA", random_value(), bytes=500, broadcasting=False, msgType=2)
    m_rrr2 = Message("M.R2", "ServiceA", "Actuator", random_value(), bytes=500, broadcasting=False, msgType=2)

    m_sss = Message("M.S", "Sensor", "ServiceA", random_value(), bytes=500, broadcasting=False, msgType=2)
    m_sss2 = Message("M.S2", "ServiceA", "Actuator", random_value(), bytes=500, broadcasting=False, msgType=2)
    m_ttt = Message("M.T", "Sensor", "ServiceA", random_value(), bytes=500, broadcasting=False, msgType=3)
    m_ttt2 = Message("M.T2", "ServiceA", "Actuator", random_value(), bytes=500, broadcasting=False, msgType=3)

    m_uuu = Message("M.U", "Sensor", "ServiceA", random_value(), bytes=500, broadcasting=False, msgType=1)
    m_uuu2 = Message("M.U2", "ServiceA", "Actuator", random_value(), bytes=500, broadcasting=False, msgType=1)
    m_vvv = Message("M.V", "Sensor", "ServiceA", random_value(), bytes=500, broadcasting=False, msgType=2)
    m_vvv2 = Message("M.V2", "ServiceA", "Actuator", random_value(), bytes=500, broadcasting=False, msgType=2)

    m_www = Message("M.W", "Sensor", "ServiceA", random_value(), bytes=500, broadcasting=False, msgType=2)
    m_www2 = Message("M.W2", "ServiceA", "Actuator", random_value(), bytes=500, broadcasting=False, msgType=2)
    m_xxx = Message("M.X", "Sensor", "ServiceA", random_value(), bytes=500, broadcasting=False, msgType=3)
    m_xxx2 = Message("M.X2", "ServiceA", "Actuator", random_value(), bytes=500, broadcasting=False, msgType=3)

    m_yyy = Message("M.Y", "Sensor", "ServiceA", random_value(), bytes=500, broadcasting=False, msgType=1)
    m_yyy2 = Message("M.Y2", "ServiceA", "Actuator", random_value(), bytes=500, broadcasting=False, msgType=1)
    m_zzz = Message("M.Z", "Sensor", "ServiceA", random_value(), bytes=500, broadcasting=False, msgType=1)
    m_zzz2 = Message("M.Z2", "ServiceA", "Actuator", random_value(), bytes=500, broadcasting=False, msgType=1)

    """
    Defining which messages will be dynamically generated # the generation is controlled by Population algorithm
    """
    a.add_source_messages(m_a)
    a.add_source_messages(m_b)

    a.add_source_messages(m_c)
    a.add_source_messages(m_d)

    a.add_source_messages(m_e)
    a.add_source_messages(m_f)

    a.add_source_messages(m_g)
    a.add_source_messages(m_h)

    a.add_source_messages(m_i)
    a.add_source_messages(m_j)

    a.add_source_messages(m_k)
    a.add_source_messages(m_l)
    a.add_source_messages(m_m)
    a.add_source_messages(m_n)
    a.add_source_messages(m_o)
    a.add_source_messages(m_p)
    a.add_source_messages(m_q)
    a.add_source_messages(m_r)
    a.add_source_messages(m_s)
    a.add_source_messages(m_t)
    a.add_source_messages(m_u)
    a.add_source_messages(m_v)
    a.add_source_messages(m_w)
    a.add_source_messages(m_x)
    a.add_source_messages(m_y)
    a.add_source_messages(m_z)

    a.add_source_messages(m_aa)
    a.add_source_messages(m_bb)

    a.add_source_messages(m_cc)
    a.add_source_messages(m_dd)

    a.add_source_messages(m_ee)
    a.add_source_messages(m_ff)

    a.add_source_messages(m_gg)
    a.add_source_messages(m_hh)

    a.add_source_messages(m_ii)
    a.add_source_messages(m_jj)

    a.add_source_messages(m_kk)
    a.add_source_messages(m_ll)
    a.add_source_messages(m_mm)
    a.add_source_messages(m_nn)
    a.add_source_messages(m_oo)
    a.add_source_messages(m_pp)
    a.add_source_messages(m_qq)
    a.add_source_messages(m_rr)
    a.add_source_messages(m_ss)
    a.add_source_messages(m_tt)
    a.add_source_messages(m_uu)
    a.add_source_messages(m_vv)
    a.add_source_messages(m_ww)
    a.add_source_messages(m_xx)
    a.add_source_messages(m_yy)
    a.add_source_messages(m_zz)

    ##

    a.add_source_messages(m_aaa)
    a.add_source_messages(m_bbb)

    a.add_source_messages(m_ccc)
    a.add_source_messages(m_ddd)

    a.add_source_messages(m_eee)
    a.add_source_messages(m_fff)

    a.add_source_messages(m_ggg)
    a.add_source_messages(m_hhh)

    a.add_source_messages(m_iii)
    a.add_source_messages(m_jjj)

    a.add_source_messages(m_kkk)
    a.add_source_messages(m_lll)
    a.add_source_messages(m_mmm)
    a.add_source_messages(m_nnn)
    a.add_source_messages(m_ooo)
    a.add_source_messages(m_ppp)
    a.add_source_messages(m_qqq)
    a.add_source_messages(m_rrr)
    a.add_source_messages(m_sss)
    a.add_source_messages(m_ttt)
    a.add_source_messages(m_uuu)
    a.add_source_messages(m_vvv)
    a.add_source_messages(m_www)
    a.add_source_messages(m_xxx)
    a.add_source_messages(m_yyy)
    a.add_source_messages(m_zzz)

    """
    MODULES/SERVICES: Definition of Generators and Consumers (AppEdges and TupleMappings in iFogSim)
    """
    # MODULE SERVICES
    a.add_service_module("ServiceA", m_a, m_a2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_b, m_b2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_c, m_c2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_d, m_d2, fractional_selectivity, threshold=1.0)

    a.add_service_module("ServiceA", m_e, m_e2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_f, m_f2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_g, m_g2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_h, m_h2, fractional_selectivity, threshold=1.0)

    a.add_service_module("ServiceA", m_i, m_i2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_j, m_j2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_k, m_k2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_l, m_l2, fractional_selectivity, threshold=1.0)

    a.add_service_module("ServiceA", m_m, m_m2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_n, m_n2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_o, m_o2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_p, m_p2, fractional_selectivity, threshold=1.0)

    a.add_service_module("ServiceA", m_q, m_q2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_r, m_r2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_s, m_s2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_t, m_t2, fractional_selectivity, threshold=1.0)

    a.add_service_module("ServiceA", m_u, m_u2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_v, m_v2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_w, m_w2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_x, m_x2, fractional_selectivity, threshold=1.0)

    a.add_service_module("ServiceA", m_y, m_y2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_z, m_z2, fractional_selectivity, threshold=1.0)

    a.add_service_module("ServiceA", m_aa, m_aa2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_bb, m_bb2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_cc, m_cc2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_dd, m_dd2, fractional_selectivity, threshold=1.0)

    a.add_service_module("ServiceA", m_ee, m_ee2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_ff, m_ff2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_gg, m_gg2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_hh, m_hh2, fractional_selectivity, threshold=1.0)

    a.add_service_module("ServiceA", m_ii, m_ii2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_jj, m_jj2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_kk, m_kk2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_ll, m_ll2, fractional_selectivity, threshold=1.0)

    a.add_service_module("ServiceA", m_mm, m_mm2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_nn, m_nn2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_oo, m_oo2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_pp, m_pp2, fractional_selectivity, threshold=1.0)

    a.add_service_module("ServiceA", m_qq, m_qq2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_rr, m_rr2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_ss, m_ss2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_tt, m_tt2, fractional_selectivity, threshold=1.0)

    a.add_service_module("ServiceA", m_uu, m_uu2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_vv, m_vv2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_ww, m_ww2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_xx, m_xx2, fractional_selectivity, threshold=1.0)

    a.add_service_module("ServiceA", m_yy, m_yy2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_zz, m_zz2, fractional_selectivity, threshold=1.0)

    #####

    a.add_service_module("ServiceA", m_aaa, m_aaa2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_bbb, m_bbb2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_ccc, m_ccc2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_ddd, m_ddd2, fractional_selectivity, threshold=1.0)

    a.add_service_module("ServiceA", m_eee, m_eee2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_fff, m_fff2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_ggg, m_ggg2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_hhh, m_hhh2, fractional_selectivity, threshold=1.0)

    a.add_service_module("ServiceA", m_iii, m_iii2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_jjj, m_jjj2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_kkk, m_kkk2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_lll, m_lll2, fractional_selectivity, threshold=1.0)

    a.add_service_module("ServiceA", m_mmm, m_mmm2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_nnn, m_nnn2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_ooo, m_ooo2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_ppp, m_ppp2, fractional_selectivity, threshold=1.0)

    a.add_service_module("ServiceA", m_qqq, m_qqq2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_rrr, m_rrr2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_sss, m_sss2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_ttt, m_ttt2, fractional_selectivity, threshold=1.0)

    a.add_service_module("ServiceA", m_uuu, m_uuu2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_vvv, m_vvv2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_www, m_www2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_xxx, m_xxx2, fractional_selectivity, threshold=1.0)

    a.add_service_module("ServiceA", m_yyy, m_yyy2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_zzz, m_zzz2, fractional_selectivity, threshold=1.0)

    return a



# @profile
def main(simulated_time, app):


    folder_results = Path("results/")
    folder_results.mkdir(parents=True, exist_ok=True)
    folder_results = str(folder_results) + "/"

    """
    TOPOLOGY from a json
    """
    t = Topology()
    dataNetwork = json.load(open('my_network_cloud.json'))
    t.load(dataNetwork)
    nx.write_gexf(t.G,
                  folder_results + "graph_cache_based")  # you can export the Graph in multiples format to view in tools likFFe Gephi, and so on.
    nx.draw(t.G, with_labels=True)
    plt.savefig(folder_results + "graph_cache_based.png")
    """
    APPLICATION
    """
   # app = create_application()


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

    msgList = [app.get_message("M.A"), app.get_message("M.B"),
               app.get_message("M.C"), app.get_message("M.D"),
               app.get_message("M.E"), app.get_message("M.F"),
               app.get_message("M.G"), app.get_message("M.H"),
               app.get_message("M.I"), app.get_message("M.J"),
               app.get_message("M.K"), app.get_message("M.L"),
               app.get_message("M.M"), app.get_message("M.N"),
               app.get_message("M.O"), app.get_message("M.P"),
               app.get_message("M.Q"), app.get_message("M.R"),
               app.get_message("M.S"), app.get_message("M.T"),
               app.get_message("M.U"), app.get_message("M.V"),
               app.get_message("M.W"), app.get_message("M.X"),
               app.get_message("M.Y"), app.get_message("M.Z")
               ]
    #sort(msgList) # remove this to make fcfs
    #sortQueue(msgList)

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

    selectorPath = CacheBasedSolutionWithCloudScaled()
    #selectorPath= FIFOCloudScaled()
    #selectorPath=RoundRobinCloudScaled()

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
    app = create_application_test()

    main(simulated_time=1000, app=app)

    print("\n--- %s seconds ---" % (time.time() - start_time))

    ## Finally, you can analyse the results:
    t = Topology()
    dataNetwork = json.load(open('my_network_cloud.json'))
    t.load(dataNetwork)
    print("-" * 20)
    print("Results:")
    print("-" * 20)
    m = Stats(defaultPath="results/sim_trace")  # Same name of the results
    time_loops = [["M.A", "M.A2"], ["M.B", "M.B2"], ["M.C", "M.C2"], ["M.D", "M.D2"],
                  ["M.E", "M.E2"], ["M.F", "M.F2"], ["M.G", "M.G2"], ["M.H", "M.H2"],
                  ["M.I", "M.I2"], ["M.J", "M.J2"], ["M.K", "M.K2"], ["M.L", "M.L2"],
                  ["M.M", "M.M2"], ["M.N", "M.N2"], ["M.O", "M.O2"], ["M.P", "M.P2"],
                  ["M.Q", "M.Q2"], ["M.R", "M.R2"], ["M.S", "M.S2"], ["M.T", "M.T2"],
                  ["M.U", "M.U2"], ["M.V", "M.V2"], ["M.W", "M.W2"], ["M.X", "M.X2"],
                  ["M.Y", "M.Y2"], ["M.Z", "M.Z2"]]
    m.showResults2(1000, time_loops=time_loops)

    print("\t- Network saturation -")

    print("\t\t Bytes Transmitted : %i" % m.bytes_transmitted())

    energy = m.get_watt(1000, t)
    for i in range(1,54):
        if i not in energy:
            energy.update({i:{'model':'added','watt':0.0}})



    df=pd.DataFrame.from_dict(energy,orient="index")
    df.drop('model',inplace=True,axis=1)
    print(str(energy))
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

    thro = data['throughput'].count()
    throughput = data["throughput"].sum() / thro
    print("----------------------------------------")
    print("THROUGHPUT")
    print("Throughput : " + str(throughput))

    print("----------------------------------------")
    makespan = data['service'].sum() #Makespan or completion time is the total time taken to process a set of jobs for its complete execution. Minimization of makespan
    print("MAKESPAN")
    print("MAKESPAN : " + str(makespan))

    #energy output
    df.to_csv(folder_results+"energy.csv")
    #jain fairness index
    dest=data.groupby('TOPO.dst')['TOPO.dst'].agg('count').to_frame('count').reset_index()

    dest.drop([0], axis=0, inplace=True)
    dest['square'] = dest['count'] ** 2
    print(dest)
    fairness_index=(dest['count'].sum())**2/(51*dest['square'].sum())
    print("----------------------------------------")
    print("JAIN'S FAIRNESS INDEX")
    print("FI : " + str(fairness_index))