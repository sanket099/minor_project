"""
    @author: isaac
"""
import random
import json
import networkx as nx
import argparse
from pathlib import Path
import time
import numpy as np

from my_core import Sim
from MyApplication import Application, Message

from yafs.population import *
from yafs.topology import Topology
from simpleSelection import FIFO
import matplotlib.pyplot as plt
from simpleSelection import RoundRobin
from simpleSelection import RoundRobin_scaled
from simpleSelection import CacheBasedSolution
from simpleSelection import CacheBasedSolution_scaled
from simplePlacement import CloudPlacement
from simpleSelection import CacheBasedSolution_onGoing
from MyStats import Stats
from yafs.distribution import deterministic_distribution
from yafs.application import fractional_selectivity

RANDOM_SEED = 1


def create_application():
    # APLICATION
    a = Application(name="SimpleCase")

    # (S) --> (ServiceA) --> (A)
    a.set_modules([{"Sensor": {"Type": Application.TYPE_SOURCE}},
                   {"ServiceA": {"RAM": 100, "Type": Application.TYPE_MODULE}},
                   # {"ServiceB": {"RAM": 10, "Type": Application.TYPE_MODULE}},
                   {"Actuator": {"Type": Application.TYPE_SINK}}
                   ])
    """
    Messages among MODULES (AppEdge in iFogSim)
    """
    m_a = Message("M.A", "Sensor", "ServiceA", instructions=900, bytes=900,broadcasting=False, msgType=1)
    m_a2 = Message("M.A2", "ServiceA", "Actuator", instructions=900, bytes=900,broadcasting=False, msgType=10)
    m_b = Message("M.B", "Sensor", "ServiceA", instructions=10000, bytes=100, broadcasting=False, msgType=1)
    m_b2 = Message("M.B2", "ServiceA", "Actuator", instructions=10000, bytes=100, broadcasting=False, msgType=11)

    m_c = Message("M.C", "Sensor", "ServiceA", instructions=500, bytes=200, broadcasting=False, msgType=2)
    m_c2 = Message("M.C2", "ServiceA", "Actuator", instructions=500, bytes=200, broadcasting=False, msgType=12)

    m_d = Message("M.D", "Sensor", "ServiceA", instructions=800, bytes=500, broadcasting=False, msgType=2)
    m_d2 = Message("M.D2", "ServiceA", "Actuator", instructions=800, bytes=500, broadcasting=False, msgType=12)

    m_e = Message("M.E", "Sensor", "ServiceA", instructions=5000, bytes=500, broadcasting=False, msgType=2)
    m_e2 = Message("M.E2", "ServiceA", "Actuator", instructions=5000, bytes=500, broadcasting=False, msgType=12)

    m_f = Message("M.F", "Sensor", "ServiceA", instructions=4900, bytes=500, broadcasting=False, msgType=2)
    m_f2 = Message("M.F2", "ServiceA", "Actuator", instructions=4900, bytes=500, broadcasting=False, msgType=12)

    m_g = Message("M.G", "Sensor", "ServiceA", instructions=5100, bytes=500, broadcasting=False, msgType=2)
    m_g2 = Message("M.G2", "ServiceA", "Actuator", instructions=5100, bytes=500, broadcasting=False, msgType=12)

    m_h = Message("M.H", "Sensor", "ServiceA", instructions=60000, bytes=500, broadcasting=False, msgType=2)
    m_h2 = Message("M.H2", "ServiceA", "Actuator", instructions=60000, bytes=500, broadcasting=False, msgType=12)

    m_i = Message("M.I", "Sensor", "ServiceA", instructions=300, bytes=500, broadcasting=False, msgType=2)
    m_i2 = Message("M.I2", "ServiceA", "Actuator", instructions=300, bytes=500, broadcasting=False, msgType=12)

    m_j = Message("M.J", "Sensor", "ServiceA", instructions=4000, bytes=500, broadcasting=False, msgType=2)
    m_j2 = Message("M.J2", "ServiceA", "Actuator", instructions=4000, bytes=500, broadcasting=False, msgType=12)

    m_k = Message("M.K", "Sensor", "ServiceA", instructions=5000, bytes=500, broadcasting=False, msgType=2)
    m_k2 = Message("M.K2", "ServiceA", "Actuator", instructions=5000, bytes=500, broadcasting=False, msgType=12)

    m_l = Message("M.L", "Sensor", "ServiceA", instructions=1800, bytes=500, broadcasting=False, msgType=2)
    m_l2 = Message("M.L2", "ServiceA", "Actuator", instructions=1800, bytes=500, broadcasting=False, msgType=12)

    m_m = Message("M.M", "Sensor", "ServiceA", instructions=2000, bytes=500, broadcasting=False, msgType=2)
    m_m2 = Message("M.M2", "ServiceA", "Actuator", instructions=2000, bytes=500, broadcasting=False, msgType=12)

    m_n = Message("M.N", "Sensor", "ServiceA", instructions=10000, bytes=500, broadcasting=False, msgType=2)
    m_n2 = Message("M.N2", "ServiceA", "Actuator", instructions=10000, bytes=500, broadcasting=False, msgType=12)
    m_o = Message("M.O", "Sensor", "ServiceA", instructions=100, bytes=500, broadcasting=False, msgType=2)
    m_o2 = Message("M.O2", "ServiceA", "Actuator", instructions=100, bytes=500, broadcasting=False, msgType=12)

    m_p = Message("M.P", "Sensor", "ServiceA", instructions=900, bytes=500, broadcasting=False, msgType=2)
    m_p2 = Message("M.P2", "ServiceA", "Actuator", instructions=900, bytes=500, broadcasting=False, msgType=12)

    m_q = Message("M.Q", "Sensor", "ServiceA", instructions=7000, bytes=500, broadcasting=False, msgType=2)
    m_q2 = Message("M.Q2", "ServiceA", "Actuator", instructions=7000, bytes=500, broadcasting=False, msgType=12)
    m_r = Message("M.R", "Sensor", "ServiceA", instructions=5000, bytes=500, broadcasting=False, msgType=2)
    m_r2 = Message("M.R2", "ServiceA", "Actuator", instructions=5000, bytes=500, broadcasting=False, msgType=12)

    m_s = Message("M.S", "Sensor", "ServiceA", instructions=600, bytes=500, broadcasting=False, msgType=2)
    m_s2 = Message("M.S2", "ServiceA", "Actuator", instructions=600, bytes=500, broadcasting=False, msgType=12)
    m_t = Message("M.T", "Sensor", "ServiceA", instructions=4000, bytes=500, broadcasting=False, msgType=2)
    m_t2 = Message("M.T2", "ServiceA", "Actuator", instructions=4000, bytes=500, broadcasting=False, msgType=12)

    m_u = Message("M.U", "Sensor", "ServiceA", instructions=20000, bytes=500, broadcasting=False, msgType=2)
    m_u2 = Message("M.U2", "ServiceA", "Actuator", instructions=20000, bytes=500, broadcasting=False, msgType=12)
    m_v = Message("M.V", "Sensor", "ServiceA", instructions=1000, bytes=500, broadcasting=False, msgType=2)
    m_v2 = Message("M.V2", "ServiceA", "Actuator", instructions=1000, bytes=500, broadcasting=False, msgType=12)

    m_w = Message("M.W", "Sensor", "ServiceA", instructions=1200, bytes=500, broadcasting=False, msgType=2)
    m_w2 = Message("M.W2", "ServiceA", "Actuator", instructions=1200, bytes=500, broadcasting=False, msgType=12)
    m_x = Message("M.X", "Sensor", "ServiceA", instructions=10000, bytes=500, broadcasting=False, msgType=2)
    m_x2 = Message("M.X2", "ServiceA", "Actuator", instructions=10000, bytes=500, broadcasting=False, msgType=12)

    m_y = Message("M.Y", "Sensor", "ServiceA", instructions=80, bytes=500, broadcasting=False, msgType=2)
    m_y2 = Message("M.Y2", "ServiceA", "Actuator", instructions=80, bytes=500, broadcasting=False, msgType=12)
    m_z = Message("M.Z", "Sensor", "ServiceA", instructions=3000, bytes=500, broadcasting=False, msgType=2)
    m_z2 = Message("M.Z2", "ServiceA", "Actuator", instructions=3000, bytes=500, broadcasting=False, msgType=12)

    m_aa = Message("M.AA", "Sensor", "ServiceA", instructions=900, bytes=900, broadcasting=False, msgType=0)
    m_aa2 = Message("M.AA2", "ServiceA", "Actuator", instructions=900, bytes=900, broadcasting=False, msgType=10)
    m_bb = Message("M.BB", "Sensor", "ServiceA", instructions=10000, bytes=100, broadcasting=False, msgType=1)
    m_bb2 = Message("M.BB2", "ServiceA", "Actuator", instructions=10000, bytes=100, broadcasting=False, msgType=11)

    m_cc = Message("M.CC", "Sensor", "ServiceA", instructions=500, bytes=200, broadcasting=False, msgType=2)
    m_cc2 = Message("M.CC2", "ServiceA", "Actuator", instructions=500, bytes=200, broadcasting=False, msgType=12)

    m_dd = Message("M.DD", "Sensor", "ServiceA", instructions=800, bytes=500, broadcasting=False, msgType=2)
    m_dd2 = Message("M.DD2", "ServiceA", "Actuator", instructions=800, bytes=500, broadcasting=False, msgType=12)

    m_ee = Message("M.EE", "Sensor", "ServiceA", instructions=5000, bytes=500, broadcasting=False, msgType=2)
    m_ee2 = Message("M.EE2", "ServiceA", "Actuator", instructions=5000, bytes=500, broadcasting=False, msgType=12)

    m_ff = Message("M.FF", "Sensor", "ServiceA", instructions=4900, bytes=500, broadcasting=False, msgType=2)
    m_ff2 = Message("M.FF2", "ServiceA", "Actuator", instructions=4900, bytes=500, broadcasting=False, msgType=12)

    m_gg = Message("M.GG", "Sensor", "ServiceA", instructions=5100, bytes=500, broadcasting=False, msgType=2)
    m_gg2 = Message("M.GG2", "ServiceA", "Actuator", instructions=5100, bytes=500, broadcasting=False, msgType=12)

    m_hh = Message("M.HH", "Sensor", "ServiceA", instructions=60000, bytes=500, broadcasting=False, msgType=2)
    m_hh2 = Message("M.HH2", "ServiceA", "Actuator", instructions=60000, bytes=500, broadcasting=False, msgType=12)

    m_ii = Message("M.II", "Sensor", "ServiceA", instructions=300, bytes=500, broadcasting=False, msgType=2)
    m_ii2 = Message("M.II2", "ServiceA", "Actuator", instructions=300, bytes=500, broadcasting=False, msgType=12)

    m_jj = Message("M.JJ", "Sensor", "ServiceA", instructions=4000, bytes=500, broadcasting=False, msgType=2)
    m_jj2 = Message("M.JJ2", "ServiceA", "Actuator", instructions=4000, bytes=500, broadcasting=False, msgType=12)

    m_kk = Message("M.KK", "Sensor", "ServiceA", instructions=5000, bytes=500, broadcasting=False, msgType=2)
    m_kk2 = Message("M.KK2", "ServiceA", "Actuator", instructions=5000, bytes=500, broadcasting=False, msgType=12)

    m_ll = Message("M.LL", "Sensor", "ServiceA", instructions=1800, bytes=500, broadcasting=False, msgType=2)
    m_ll2 = Message("M.LL2", "ServiceA", "Actuator", instructions=1800, bytes=500, broadcasting=False, msgType=12)

    m_mm = Message("M.MM", "Sensor", "ServiceA", instructions=2000, bytes=500, broadcasting=False, msgType=2)
    m_mm2 = Message("M.MM2", "ServiceA", "Actuator", instructions=2000, bytes=500, broadcasting=False, msgType=12)

    m_nn = Message("M.NN", "Sensor", "ServiceA", instructions=10000, bytes=500, broadcasting=False, msgType=2)
    m_nn2 = Message("M.NN2", "ServiceA", "Actuator", instructions=10000, bytes=500, broadcasting=False, msgType=12)
    m_oo = Message("M.OO", "Sensor", "ServiceA", instructions=100, bytes=500, broadcasting=False, msgType=2)
    m_oo2 = Message("M.OO2", "ServiceA", "Actuator", instructions=100, bytes=500, broadcasting=False, msgType=12)

    m_pp = Message("M.PP", "Sensor", "ServiceA", instructions=900, bytes=500, broadcasting=False, msgType=2)
    m_pp2 = Message("M.PP2", "ServiceA", "Actuator", instructions=900, bytes=500, broadcasting=False, msgType=12)

    m_qq = Message("M.QQ", "Sensor", "ServiceA", instructions=7000, bytes=500, broadcasting=False, msgType=2)
    m_qq2 = Message("M.QQ2", "ServiceA", "Actuator", instructions=7000, bytes=500, broadcasting=False, msgType=12)
    m_rr = Message("M.RR", "Sensor", "ServiceA", instructions=5000, bytes=500, broadcasting=False, msgType=2)
    m_rr2 = Message("M.RR2", "ServiceA", "Actuator", instructions=5000, bytes=500, broadcasting=False, msgType=12)

    m_ss = Message("M.SS", "Sensor", "ServiceA", instructions=600, bytes=500, broadcasting=False, msgType=2)
    m_ss2 = Message("M.SS2", "ServiceA", "Actuator", instructions=600, bytes=500, broadcasting=False, msgType=12)
    m_tt = Message("M.TT", "Sensor", "ServiceA", instructions=4000, bytes=500, broadcasting=False, msgType=2)
    m_tt2 = Message("M.TT2", "ServiceA", "Actuator", instructions=4000, bytes=500, broadcasting=False, msgType=12)

    m_uu = Message("M.UU", "Sensor", "ServiceA", instructions=20000, bytes=500, broadcasting=False, msgType=2)
    m_uu2 = Message("M.UU2", "ServiceA", "Actuator", instructions=20000, bytes=500, broadcasting=False, msgType=12)
    m_vv = Message("M.VV", "Sensor", "ServiceA", instructions=1000, bytes=500, broadcasting=False, msgType=2)
    m_vv2 = Message("M.VV2", "ServiceA", "Actuator", instructions=1000, bytes=500, broadcasting=False, msgType=12)

    m_ww = Message("M.WW", "Sensor", "ServiceA", instructions=1200, bytes=500, broadcasting=False, msgType=2)
    m_ww2 = Message("M.WW2", "ServiceA", "Actuator", instructions=1200, bytes=500, broadcasting=False, msgType=12)
    m_xx = Message("M.XX", "Sensor", "ServiceA", instructions=10000, bytes=500, broadcasting=False, msgType=2)
    m_xx2 = Message("M.XX2", "ServiceA", "Actuator", instructions=10000, bytes=500, broadcasting=False, msgType=12)

    m_yy = Message("M.YY", "Sensor", "ServiceA", instructions=80, bytes=500, broadcasting=False, msgType=2)
    m_yy2 = Message("M.YY2", "ServiceA", "Actuator", instructions=80, bytes=500, broadcasting=False, msgType=12)
    m_zz = Message("M.ZZ", "Sensor", "ServiceA", instructions=3000, bytes=500, broadcasting=False, msgType=2)
    m_zz2 = Message("M.ZZ2", "ServiceA", "Actuator", instructions=3000, bytes=500, broadcasting=False, msgType=12)

    m_aaa = Message("M.AAA", "Sensor", "ServiceA", instructions=900, bytes=900, broadcasting=False, msgType=0)
    m_aaa2 = Message("M.AAA2", "ServiceA", "Actuator", instructions=900, bytes=900, broadcasting=False, msgType=10)
    m_bbb = Message("M.BBB", "Sensor", "ServiceA", instructions=10000, bytes=100, broadcasting=False, msgType=1)
    m_bbb2 = Message("M.BBB2", "ServiceA", "Actuator", instructions=10000, bytes=100, broadcasting=False, msgType=11)

    m_ccc = Message("M.CCC", "Sensor", "ServiceA", instructions=500, bytes=200, broadcasting=False, msgType=2)
    m_ccc2 = Message("M.CCC2", "ServiceA", "Actuator", instructions=500, bytes=200, broadcasting=False, msgType=12)

    m_ddd = Message("M.DDD", "Sensor", "ServiceA", instructions=800, bytes=500, broadcasting=False, msgType=2)
    m_ddd2 = Message("M.DDD2", "ServiceA", "Actuator", instructions=800, bytes=500, broadcasting=False, msgType=12)

    m_eee = Message("M.EEE", "Sensor", "ServiceA", instructions=5000, bytes=500, broadcasting=False, msgType=2)
    m_eee2 = Message("M.EEE2", "ServiceA", "Actuator", instructions=5000, bytes=500, broadcasting=False, msgType=12)

    m_fff = Message("M.FFF", "Sensor", "ServiceA", instructions=4900, bytes=500, broadcasting=False, msgType=2)
    m_fff2 = Message("M.FFF2", "ServiceA", "Actuator", instructions=4900, bytes=500, broadcasting=False, msgType=12)

    m_ggg = Message("M.GGG", "Sensor", "ServiceA", instructions=5100, bytes=500, broadcasting=False, msgType=2)
    m_ggg2 = Message("M.GGG2", "ServiceA", "Actuator", instructions=5100, bytes=500, broadcasting=False, msgType=12)

    m_hhh = Message("M.HHH", "Sensor", "ServiceA", instructions=60000, bytes=500, broadcasting=False, msgType=2)
    m_hhh2 = Message("M.HHH2", "ServiceA", "Actuator", instructions=60000, bytes=500, broadcasting=False, msgType=12)

    m_iii = Message("M.III", "Sensor", "ServiceA", instructions=300, bytes=500, broadcasting=False, msgType=2)
    m_iii2 = Message("M.III2", "ServiceA", "Actuator", instructions=300, bytes=500, broadcasting=False, msgType=12)

    m_jjj = Message("M.JJJ", "Sensor", "ServiceA", instructions=4000, bytes=500, broadcasting=False, msgType=2)
    m_jjj2 = Message("M.JJJ2", "ServiceA", "Actuator", instructions=4000, bytes=500, broadcasting=False, msgType=12)

    m_kkk = Message("M.KKK", "Sensor", "ServiceA", instructions=5000, bytes=500, broadcasting=False, msgType=2)
    m_kkk2 = Message("M.KKK2", "ServiceA", "Actuator", instructions=5000, bytes=500, broadcasting=False, msgType=12)

    m_lll = Message("M.LLL", "Sensor", "ServiceA", instructions=1800, bytes=500, broadcasting=False, msgType=2)
    m_lll2 = Message("M.LLL2", "ServiceA", "Actuator", instructions=1800, bytes=500, broadcasting=False, msgType=12)

    m_mmm = Message("M.MMM", "Sensor", "ServiceA", instructions=2000, bytes=500, broadcasting=False, msgType=2)
    m_mmm2 = Message("M.MMM2", "ServiceA", "Actuator", instructions=2000, bytes=500, broadcasting=False, msgType=12)

    m_nnn = Message("M.NNN", "Sensor", "ServiceA", instructions=10000, bytes=500, broadcasting=False, msgType=2)
    m_nnn2 = Message("M.NNN2", "ServiceA", "Actuator", instructions=10000, bytes=500, broadcasting=False, msgType=12)
    m_ooo = Message("M.OOO", "Sensor", "ServiceA", instructions=100, bytes=500, broadcasting=False, msgType=2)
    m_ooo2 = Message("M.OOO2", "ServiceA", "Actuator", instructions=100, bytes=500, broadcasting=False, msgType=12)

    m_ppp = Message("M.PPP", "Sensor", "ServiceA", instructions=900, bytes=500, broadcasting=False, msgType=2)
    m_ppp2 = Message("M.PPP2", "ServiceA", "Actuator", instructions=900, bytes=500, broadcasting=False, msgType=12)

    m_qqq = Message("M.QQQ", "Sensor", "ServiceA", instructions=7000, bytes=500, broadcasting=False, msgType=2)
    m_qqq2 = Message("M.QQQ2", "ServiceA", "Actuator", instructions=7000, bytes=500, broadcasting=False, msgType=12)
    m_rrr = Message("M.RRR", "Sensor", "ServiceA", instructions=5000, bytes=500, broadcasting=False, msgType=2)
    m_rrr2 = Message("M.RRR2", "ServiceA", "Actuator", instructions=5000, bytes=500, broadcasting=False, msgType=12)

    m_sss = Message("M.SSS", "Sensor", "ServiceA", instructions=600, bytes=500, broadcasting=False, msgType=2)
    m_sss2 = Message("M.SSS2", "ServiceA", "Actuator", instructions=600, bytes=500, broadcasting=False, msgType=12)
    m_ttt = Message("M.TTT", "Sensor", "ServiceA", instructions=4000, bytes=500, broadcasting=False, msgType=2)
    m_ttt2 = Message("M.TTT2", "ServiceA", "Actuator", instructions=4000, bytes=500, broadcasting=False, msgType=12)

    m_uuu = Message("M.UUU", "Sensor", "ServiceA", instructions=20000, bytes=500, broadcasting=False, msgType=2)
    m_uuu2 = Message("M.UUU2", "ServiceA", "Actuator", instructions=20000, bytes=500, broadcasting=False, msgType=12)
    m_vvv = Message("M.VVV", "Sensor", "ServiceA", instructions=1000, bytes=500, broadcasting=False, msgType=2)
    m_vvv2 = Message("M.VVV2", "ServiceA", "Actuator", instructions=1000, bytes=500, broadcasting=False, msgType=12)

    m_www = Message("M.WWW", "Sensor", "ServiceA", instructions=1200, bytes=500, broadcasting=False, msgType=2)
    m_www2 = Message("M.WWW2", "ServiceA", "Actuator", instructions=1200, bytes=500, broadcasting=False, msgType=12)
    m_xxx = Message("M.XXX", "Sensor", "ServiceA", instructions=10000, bytes=500, broadcasting=False, msgType=2)
    m_xxx2 = Message("M.XXX2", "ServiceA", "Actuator", instructions=10000, bytes=500, broadcasting=False, msgType=12)

    m_yyy = Message("M.YYY", "Sensor", "ServiceA", instructions=80, bytes=500, broadcasting=False, msgType=2)
    m_yyy2 = Message("M.YYY2", "ServiceA", "Actuator", instructions=80, bytes=500, broadcasting=False, msgType=12)
    m_zzz = Message("M.ZZZ", "Sensor", "ServiceA", instructions=3000, bytes=500, broadcasting=False, msgType=2)
    m_zzz2 = Message("M.ZZZ2", "ServiceA", "Actuator", instructions=3000, bytes=500, broadcasting=False, msgType=12)

    ######################################################################

    m_aaaa = Message("M.AAAA", "Sensor", "ServiceA", instructions=900, bytes=900, broadcasting=False, msgType=0)
    m_aaaa2 = Message("M.AAAA2", "ServiceA", "Actuator", instructions=900, bytes=900, broadcasting=False, msgType=10)
    m_bbbb = Message("M.BBBB", "Sensor", "ServiceA", instructions=10000, bytes=100, broadcasting=False, msgType=1)
    m_bbbb2 = Message("M.BBBB2", "ServiceA", "Actuator", instructions=10000, bytes=100, broadcasting=False, msgType=11)

    m_cccc = Message("M.CCCC", "Sensor", "ServiceA", instructions=500, bytes=200, broadcasting=False, msgType=2)
    m_cccc2 = Message("M.CCCC2", "ServiceA", "Actuator", instructions=500, bytes=200, broadcasting=False, msgType=12)

    m_dddd = Message("M.DDDD", "Sensor", "ServiceA", instructions=800, bytes=500, broadcasting=False, msgType=2)
    m_dddd2 = Message("M.DDDD2", "ServiceA", "Actuator", instructions=800, bytes=500, broadcasting=False, msgType=12)

    m_eeee = Message("M.EEEE", "Sensor", "ServiceA", instructions=5000, bytes=500, broadcasting=False, msgType=2)
    m_eeee2 = Message("M.EEEE2", "ServiceA", "Actuator", instructions=5000, bytes=500, broadcasting=False, msgType=12)

    m_ffff = Message("M.FFFF", "Sensor", "ServiceA", instructions=4900, bytes=500, broadcasting=False, msgType=2)
    m_ffff2 = Message("M.FFFF2", "ServiceA", "Actuator", instructions=4900, bytes=500, broadcasting=False, msgType=12)

    m_gggg = Message("M.GGGG", "Sensor", "ServiceA", instructions=5100, bytes=500, broadcasting=False, msgType=2)
    m_gggg2 = Message("M.GGGG2", "ServiceA", "Actuator", instructions=5100, bytes=500, broadcasting=False, msgType=12)

    m_hhhh = Message("M.HHHH", "Sensor", "ServiceA", instructions=60000, bytes=500, broadcasting=False, msgType=2)
    m_hhhh2 = Message("M.HHHH2", "ServiceA", "Actuator", instructions=60000, bytes=500, broadcasting=False, msgType=12)

    m_iiii = Message("M.IIII", "Sensor", "ServiceA", instructions=300, bytes=500, broadcasting=False, msgType=2)
    m_iiii2 = Message("M.IIII2", "ServiceA", "Actuator", instructions=300, bytes=500, broadcasting=False, msgType=12)

    m_jjjj = Message("M.JJJJ", "Sensor", "ServiceA", instructions=4000, bytes=500, broadcasting=False, msgType=2)
    m_jjjj2 = Message("M.JJJJ2", "ServiceA", "Actuator", instructions=4000, bytes=500, broadcasting=False, msgType=12)

    m_kkkk = Message("M.KKKK", "Sensor", "ServiceA", instructions=5000, bytes=500, broadcasting=False, msgType=2)
    m_kkkk2 = Message("M.KKKK2", "ServiceA", "Actuator", instructions=5000, bytes=500, broadcasting=False, msgType=12)

    m_llll = Message("M.LLLL", "Sensor", "ServiceA", instructions=1800, bytes=500, broadcasting=False, msgType=2)
    m_llll2 = Message("M.LLLL2", "ServiceA", "Actuator", instructions=1800, bytes=500, broadcasting=False, msgType=12)

    m_mmmm = Message("M.MMMM", "Sensor", "ServiceA", instructions=2000, bytes=500, broadcasting=False, msgType=2)
    m_mmmm2 = Message("M.MMMM2", "ServiceA", "Actuator", instructions=2000, bytes=500, broadcasting=False, msgType=12)

    m_nnnn = Message("M.NNNN", "Sensor", "ServiceA", instructions=10000, bytes=500, broadcasting=False, msgType=2)
    m_nnnn2 = Message("M.NNNN2", "ServiceA", "Actuator", instructions=10000, bytes=500, broadcasting=False, msgType=12)
    m_oooo = Message("M.OOOO", "Sensor", "ServiceA", instructions=100, bytes=500, broadcasting=False, msgType=2)
    m_oooo2 = Message("M.OOOO2", "ServiceA", "Actuator", instructions=100, bytes=500, broadcasting=False, msgType=12)

    m_pppp = Message("M.PPPP", "Sensor", "ServiceA", instructions=900, bytes=500, broadcasting=False, msgType=2)
    m_pppp2 = Message("M.PPPP2", "ServiceA", "Actuator", instructions=900, bytes=500, broadcasting=False, msgType=12)

    m_qqqq = Message("M.QQQQ", "Sensor", "ServiceA", instructions=7000, bytes=500, broadcasting=False, msgType=2)
    m_qqqq2 = Message("M.QQQQ2", "ServiceA", "Actuator", instructions=7000, bytes=500, broadcasting=False, msgType=12)
    m_rrrr = Message("M.RRRR", "Sensor", "ServiceA", instructions=5000, bytes=500, broadcasting=False, msgType=2)
    m_rrrr2 = Message("M.RRRR2", "ServiceA", "Actuator", instructions=5000, bytes=500, broadcasting=False, msgType=12)

    m_ssss = Message("M.SSSS", "Sensor", "ServiceA", instructions=600, bytes=500, broadcasting=False, msgType=2)
    m_ssss2 = Message("M.SSSS2", "ServiceA", "Actuator", instructions=600, bytes=500, broadcasting=False, msgType=12)
    m_tttt = Message("M.TTTT", "Sensor", "ServiceA", instructions=4000, bytes=500, broadcasting=False, msgType=2)
    m_tttt2 = Message("M.TTTT2", "ServiceA", "Actuator", instructions=4000, bytes=500, broadcasting=False, msgType=12)

    m_uuuu = Message("M.UUUU", "Sensor", "ServiceA", instructions=20000, bytes=500, broadcasting=False, msgType=2)
    m_uuuu2 = Message("M.UUUU2", "ServiceA", "Actuator", instructions=20000, bytes=500, broadcasting=False, msgType=12)
    m_vvvv = Message("M.VVVV", "Sensor", "ServiceA", instructions=1000, bytes=500, broadcasting=False, msgType=2)
    m_vvvv2 = Message("M.VVVV2", "ServiceA", "Actuator", instructions=1000, bytes=500, broadcasting=False, msgType=12)

    m_wwww = Message("M.WWWW", "Sensor", "ServiceA", instructions=1200, bytes=500, broadcasting=False, msgType=2)
    m_wwww2 = Message("M.WWWW2", "ServiceA", "Actuator", instructions=1200, bytes=500, broadcasting=False, msgType=12)
    m_xxxx = Message("M.XXXX", "Sensor", "ServiceA", instructions=10000, bytes=500, broadcasting=False, msgType=2)
    m_xxxx2 = Message("M.XXXX2", "ServiceA", "Actuator", instructions=10000, bytes=500, broadcasting=False, msgType=12)

    m_yyyy = Message("M.YYYY", "Sensor", "ServiceA", instructions=80, bytes=500, broadcasting=False, msgType=2)
    m_yyyy2 = Message("M.YYYY2", "ServiceA", "Actuator", instructions=80, bytes=500, broadcasting=False, msgType=12)
    m_zzzz = Message("M.ZZZZ", "Sensor", "ServiceA", instructions=3000, bytes=500, broadcasting=False, msgType=2)
    m_zzzz2 = Message("M.ZZZZ2", "ServiceA", "Actuator", instructions=3000, bytes=500, broadcasting=False, msgType=12)

    m_aaaaa = Message("M.AAAAA", "Sensor", "ServiceA", instructions=900, bytes=900, broadcasting=False, msgType=0)
    m_aaaaa2 = Message("M.AAAAA2", "ServiceA", "Actuator", instructions=900, bytes=900, broadcasting=False, msgType=10)
    m_bbbbb = Message("M.BBBBB", "Sensor", "ServiceA", instructions=10000, bytes=100, broadcasting=False, msgType=1)
    m_bbbbb2 = Message("M.BBBBB2", "ServiceA", "Actuator", instructions=10000, bytes=100, broadcasting=False, msgType=11)

    m_ccccc = Message("M.CCCCC", "Sensor", "ServiceA", instructions=500, bytes=200, broadcasting=False, msgType=2)
    m_ccccc2 = Message("M.CCCCC2", "ServiceA", "Actuator", instructions=500, bytes=200, broadcasting=False, msgType=12)

    m_ddddd = Message("M.DDDDD", "Sensor", "ServiceA", instructions=800, bytes=500, broadcasting=False, msgType=2)
    m_ddddd2 = Message("M.DDDDD2", "ServiceA", "Actuator", instructions=800, bytes=500, broadcasting=False, msgType=12)

    m_eeeee = Message("M.EEEEE", "Sensor", "ServiceA", instructions=5000, bytes=500, broadcasting=False, msgType=2)
    m_eeeee2 = Message("M.EEEEE2", "ServiceA", "Actuator", instructions=5000, bytes=500, broadcasting=False, msgType=12)

    m_fffff = Message("M.FFFFF", "Sensor", "ServiceA", instructions=4900, bytes=500, broadcasting=False, msgType=2)
    m_fffff2 = Message("M.FFFFF2", "ServiceA", "Actuator", instructions=4900, bytes=500, broadcasting=False, msgType=12)

    m_ggggg = Message("M.GGGGG", "Sensor", "ServiceA", instructions=5100, bytes=500, broadcasting=False, msgType=2)
    m_ggggg2 = Message("M.GGGGG2", "ServiceA", "Actuator", instructions=5100, bytes=500, broadcasting=False, msgType=12)

    m_hhhhh = Message("M.HHHHH", "Sensor", "ServiceA", instructions=60000, bytes=500, broadcasting=False, msgType=2)
    m_hhhhh2 = Message("M.HHHHH2", "ServiceA", "Actuator", instructions=60000, bytes=500, broadcasting=False, msgType=12)

    m_iiiii = Message("M.IIIII", "Sensor", "ServiceA", instructions=300, bytes=500, broadcasting=False, msgType=2)
    m_iiiii2 = Message("M.IIIII2", "ServiceA", "Actuator", instructions=300, bytes=500, broadcasting=False, msgType=12)

    m_jjjjj = Message("M.JJJJJ", "Sensor", "ServiceA", instructions=4000, bytes=500, broadcasting=False, msgType=2)
    m_jjjjj2 = Message("M.JJJJJ2", "ServiceA", "Actuator", instructions=4000, bytes=500, broadcasting=False, msgType=12)

    m_kkkkk = Message("M.KKKKK", "Sensor", "ServiceA", instructions=5000, bytes=500, broadcasting=False, msgType=2)
    m_kkkkk2 = Message("M.KKKKK2", "ServiceA", "Actuator", instructions=5000, bytes=500, broadcasting=False, msgType=12)

    m_lllll = Message("M.LLLLL", "Sensor", "ServiceA", instructions=1800, bytes=500, broadcasting=False, msgType=2)
    m_lllll2 = Message("M.LLLLL2", "ServiceA", "Actuator", instructions=1800, bytes=500, broadcasting=False, msgType=12)

    m_mmmmm = Message("M.MMMMM", "Sensor", "ServiceA", instructions=2000, bytes=500, broadcasting=False, msgType=2)
    m_mmmmm2 = Message("M.MMMMM2", "ServiceA", "Actuator", instructions=2000, bytes=500, broadcasting=False, msgType=12)

    m_nnnnn = Message("M.NNNNN", "Sensor", "ServiceA", instructions=10000, bytes=500, broadcasting=False, msgType=2)
    m_nnnnn2 = Message("M.NNNNN2", "ServiceA", "Actuator", instructions=10000, bytes=500, broadcasting=False, msgType=12)
    m_ooooo = Message("M.OOOOO", "Sensor", "ServiceA", instructions=100, bytes=500, broadcasting=False, msgType=2)
    m_ooooo2 = Message("M.OOOOO2", "ServiceA", "Actuator", instructions=100, bytes=500, broadcasting=False, msgType=12)

    m_ppppp = Message("M.PPPPP", "Sensor", "ServiceA", instructions=900, bytes=500, broadcasting=False, msgType=2)
    m_ppppp2 = Message("M.PPPPP2", "ServiceA", "Actuator", instructions=900, bytes=500, broadcasting=False, msgType=12)

    m_qqqqq = Message("M.QQQQQ", "Sensor", "ServiceA", instructions=7000, bytes=500, broadcasting=False, msgType=2)
    m_qqqqq2 = Message("M.QQQQQ2", "ServiceA", "Actuator", instructions=7000, bytes=500, broadcasting=False, msgType=12)
    m_rrrrr = Message("M.RRRRR", "Sensor", "ServiceA", instructions=5000, bytes=500, broadcasting=False, msgType=2)
    m_rrrrr2 = Message("M.RRRRR2", "ServiceA", "Actuator", instructions=5000, bytes=500, broadcasting=False, msgType=12)

    m_sssss = Message("M.SSSSS", "Sensor", "ServiceA", instructions=600, bytes=500, broadcasting=False, msgType=2)
    m_sssss2 = Message("M.SSSSS2", "ServiceA", "Actuator", instructions=600, bytes=500, broadcasting=False, msgType=12)
    m_ttttt = Message("M.TTTTT", "Sensor", "ServiceA", instructions=4000, bytes=500, broadcasting=False, msgType=2)
    m_ttttt2 = Message("M.TTTTT2", "ServiceA", "Actuator", instructions=4000, bytes=500, broadcasting=False, msgType=12)

    m_uuuuu = Message("M.UUUUU", "Sensor", "ServiceA", instructions=20000, bytes=500, broadcasting=False, msgType=2)
    m_uuuuu2 = Message("M.UUUUU2", "ServiceA", "Actuator", instructions=20000, bytes=500, broadcasting=False, msgType=12)
    m_vvvvv = Message("M.VVVVV", "Sensor", "ServiceA", instructions=1000, bytes=500, broadcasting=False, msgType=2)
    m_vvvvv2 = Message("M.VVVVV2", "ServiceA", "Actuator", instructions=1000, bytes=500, broadcasting=False, msgType=12)

    m_wwwww = Message("M.WWWWW", "Sensor", "ServiceA", instructions=1200, bytes=500, broadcasting=False, msgType=2)
    m_wwwww2 = Message("M.WWWWW2", "ServiceA", "Actuator", instructions=1200, bytes=500, broadcasting=False, msgType=12)
    m_xxxxx = Message("M.XXXXX", "Sensor", "ServiceA", instructions=10000, bytes=500, broadcasting=False, msgType=2)
    m_xxxxx2 = Message("M.XXXXX2", "ServiceA", "Actuator", instructions=10000, bytes=500, broadcasting=False, msgType=12)

    m_yyyyy = Message("M.YYYYY", "Sensor", "ServiceA", instructions=80, bytes=500, broadcasting=False, msgType=2)
    m_yyyyy2 = Message("M.YYYYY2", "ServiceA", "Actuator", instructions=80, bytes=500, broadcasting=False, msgType=12)
    m_zzzzz = Message("M.ZZZZZ", "Sensor", "ServiceA", instructions=3000, bytes=500, broadcasting=False, msgType=2)
    m_zzzzz2 = Message("M.ZZZZZ2", "ServiceA", "Actuator", instructions=3000, bytes=500, broadcasting=False, msgType=12)

    m_aaaaaa = Message("M.A", "Sensor", "ServiceA", instructions=900, bytes=900, broadcasting=False, msgType=0)
    m_aaaaaa2 = Message("M.A2", "ServiceA", "Actuator", instructions=900, bytes=900, broadcasting=False, msgType=10)
    m_bbbbbb = Message("M.B", "Sensor", "ServiceA", instructions=10000, bytes=100, broadcasting=False, msgType=1)
    m_bbbbbb2 = Message("M.B2", "ServiceA", "Actuator", instructions=10000, bytes=100, broadcasting=False, msgType=11)

    m_cccccc = Message("M.C", "Sensor", "ServiceA", instructions=500, bytes=200, broadcasting=False, msgType=2)
    m_cccccc2 = Message("M.C2", "ServiceA", "Actuator", instructions=500, bytes=200, broadcasting=False, msgType=12)

    m_dddddd = Message("M.D", "Sensor", "ServiceA", instructions=800, bytes=500, broadcasting=False, msgType=2)
    m_dddddd2 = Message("M.D2", "ServiceA", "Actuator", instructions=800, bytes=500, broadcasting=False, msgType=12)

    m_eeeeee = Message("M.E", "Sensor", "ServiceA", instructions=5000, bytes=500, broadcasting=False, msgType=2)
    m_eeeeee2 = Message("M.E2", "ServiceA", "Actuator", instructions=5000, bytes=500, broadcasting=False, msgType=12)

    m_ffffff = Message("M.F", "Sensor", "ServiceA", instructions=4900, bytes=500, broadcasting=False, msgType=2)
    m_ffffff2 = Message("M.F2", "ServiceA", "Actuator", instructions=4900, bytes=500, broadcasting=False, msgType=12)

    m_gggggg = Message("M.G", "Sensor", "ServiceA", instructions=5100, bytes=500, broadcasting=False, msgType=2)
    m_gggggg2 = Message("M.G2", "ServiceA", "Actuator", instructions=5100, bytes=500, broadcasting=False, msgType=12)

    m_hhhhhh = Message("M.H", "Sensor", "ServiceA", instructions=60000, bytes=500, broadcasting=False, msgType=2)
    m_hhhhhh2 = Message("M.H2", "ServiceA", "Actuator", instructions=60000, bytes=500, broadcasting=False, msgType=12)

    m_iiiiii= Message("M.I", "Sensor", "ServiceA", instructions=300, bytes=500, broadcasting=False, msgType=2)
    m_iiiiii2 = Message("M.I2", "ServiceA", "Actuator", instructions=300, bytes=500, broadcasting=False, msgType=12)

    m_jjjjjj = Message("M.J", "Sensor", "ServiceA", instructions=4000, bytes=500, broadcasting=False, msgType=2)
    m_jjjjjj2 = Message("M.J2", "ServiceA", "Actuator", instructions=4000, bytes=500, broadcasting=False, msgType=12)

    m_kkkkkk = Message("M.K", "Sensor", "ServiceA", instructions=5000, bytes=500, broadcasting=False, msgType=2)
    m_kkkkkk2 = Message("M.K2", "ServiceA", "Actuator", instructions=5000, bytes=500, broadcasting=False, msgType=12)

    m_llllll = Message("M.L", "Sensor", "ServiceA", instructions=1800, bytes=500, broadcasting=False, msgType=2)
    m_llllll2 = Message("M.L2", "ServiceA", "Actuator", instructions=1800, bytes=500, broadcasting=False, msgType=12)

    m_mmmmmm = Message("M.M", "Sensor", "ServiceA", instructions=2000, bytes=500, broadcasting=False, msgType=2)
    m_mmmmmm2 = Message("M.M2", "ServiceA", "Actuator", instructions=2000, bytes=500, broadcasting=False, msgType=12)

    m_nnnnnn = Message("M.N", "Sensor", "ServiceA", instructions=10000, bytes=500, broadcasting=False, msgType=2)
    m_nnnnnn2 = Message("M.N2", "ServiceA", "Actuator", instructions=10000, bytes=500, broadcasting=False, msgType=12)
    m_oooooo = Message("M.O", "Sensor", "ServiceA", instructions=100, bytes=500, broadcasting=False, msgType=2)
    m_oooooo2 = Message("M.O2", "ServiceA", "Actuator", instructions=100, bytes=500, broadcasting=False, msgType=12)

    m_pppppp = Message("M.P", "Sensor", "ServiceA", instructions=900, bytes=500, broadcasting=False, msgType=2)
    m_pppppp2 = Message("M.P2", "ServiceA", "Actuator", instructions=900, bytes=500, broadcasting=False, msgType=12)

    m_qqqqqq = Message("M.Q", "Sensor", "ServiceA", instructions=7000, bytes=500, broadcasting=False, msgType=2)
    m_qqqqqq2 = Message("M.Q2", "ServiceA", "Actuator", instructions=7000, bytes=500, broadcasting=False, msgType=12)
    m_rrrrrr = Message("M.R", "Sensor", "ServiceA", instructions=5000, bytes=500, broadcasting=False, msgType=2)
    m_rrrrrr2 = Message("M.R2", "ServiceA", "Actuator", instructions=5000, bytes=500, broadcasting=False, msgType=12)

    m_ssssss = Message("M.S", "Sensor", "ServiceA", instructions=600, bytes=500, broadcasting=False, msgType=2)
    m_ssssss2 = Message("M.S2", "ServiceA", "Actuator", instructions=600, bytes=500, broadcasting=False, msgType=12)
    m_tttttt = Message("M.T", "Sensor", "ServiceA", instructions=4000, bytes=500, broadcasting=False, msgType=2)
    m_tttttt2 = Message("M.T2", "ServiceA", "Actuator", instructions=4000, bytes=500, broadcasting=False, msgType=12)

    m_uuuuuu = Message("M.U", "Sensor", "ServiceA", instructions=20000, bytes=500, broadcasting=False, msgType=2)
    m_uuuuuu2 = Message("M.U2", "ServiceA", "Actuator", instructions=20000, bytes=500, broadcasting=False, msgType=12)
    m_vvvvvv = Message("M.V", "Sensor", "ServiceA", instructions=1000, bytes=500, broadcasting=False, msgType=2)
    m_vvvvvv2 = Message("M.V2", "ServiceA", "Actuator", instructions=1000, bytes=500, broadcasting=False, msgType=12)

    m_wwwwww = Message("M.W", "Sensor", "ServiceA", instructions=1200, bytes=500, broadcasting=False, msgType=2)
    m_wwwwww2 = Message("M.W2", "ServiceA", "Actuator", instructions=1200, bytes=500, broadcasting=False, msgType=12)
    m_xxxxxx = Message("M.X", "Sensor", "ServiceA", instructions=10000, bytes=500, broadcasting=False, msgType=2)
    m_xxxxxx2 = Message("M.X2", "ServiceA", "Actuator", instructions=10000, bytes=500, broadcasting=False, msgType=12)

    m_yyyyyy = Message("M.Y", "Sensor", "ServiceA", instructions=80, bytes=500, broadcasting=False, msgType=2)
    m_yyyyyy2 = Message("M.Y2", "ServiceA", "Actuator", instructions=80, bytes=500, broadcasting=False, msgType=12)
    m_zzzzzz = Message("M.Z", "Sensor", "ServiceA", instructions=3000, bytes=500, broadcasting=False, msgType=2)
    m_zzzzzz2 = Message("M.Z2", "ServiceA", "Actuator", instructions=3000, bytes=500, broadcasting=False, msgType=12)

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
    #
    # ##
    #
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
    #
    # #########################
    #
    a.add_source_messages(m_aaaa)
    a.add_source_messages(m_bbbb)

    a.add_source_messages(m_cccc)
    a.add_source_messages(m_dddd)

    a.add_source_messages(m_eeee)
    a.add_source_messages(m_ffff)

    a.add_source_messages(m_gggg)
    a.add_source_messages(m_hhhh)

    a.add_source_messages(m_iiii)
    a.add_source_messages(m_jjjj)

    a.add_source_messages(m_kkkk)
    a.add_source_messages(m_llll)
    a.add_source_messages(m_mmmm)
    a.add_source_messages(m_nnnn)
    a.add_source_messages(m_oooo)
    a.add_source_messages(m_pppp)
    a.add_source_messages(m_qqqq)
    a.add_source_messages(m_rrrr)
    a.add_source_messages(m_ssss)
    a.add_source_messages(m_tttt)
    a.add_source_messages(m_uuuu)
    a.add_source_messages(m_vvvv)
    a.add_source_messages(m_wwww)
    a.add_source_messages(m_xxxx)
    a.add_source_messages(m_yyyy)
    a.add_source_messages(m_zzzz)

    a.add_source_messages(m_aaaaa)
    a.add_source_messages(m_bbbbb)

    a.add_source_messages(m_ccccc)
    a.add_source_messages(m_ddddd)

    a.add_source_messages(m_eeeee)
    a.add_source_messages(m_fffff)

    a.add_source_messages(m_ggggg)
    a.add_source_messages(m_hhhhh)

    a.add_source_messages(m_iiiii)
    a.add_source_messages(m_jjjjj)

    a.add_source_messages(m_kkkkk)
    a.add_source_messages(m_lllll)
    a.add_source_messages(m_mmmmm)
    a.add_source_messages(m_nnnnn)
    a.add_source_messages(m_ooooo)
    a.add_source_messages(m_ppppp)
    a.add_source_messages(m_qqqqq)
    a.add_source_messages(m_rrrrr)
    a.add_source_messages(m_sssss)
    a.add_source_messages(m_ttttt)
    a.add_source_messages(m_uuuuu)
    a.add_source_messages(m_vvvvv)
    a.add_source_messages(m_wwwww)
    a.add_source_messages(m_xxxxx)
    a.add_source_messages(m_yyyyy)
    a.add_source_messages(m_zzzzz)

    #

    a.add_source_messages(m_aaaaaa)
    a.add_source_messages(m_bbbbbb)

    a.add_source_messages(m_cccccc)
    a.add_source_messages(m_dddddd)

    a.add_source_messages(m_eeeeee)
    a.add_source_messages(m_ffffff)

    a.add_source_messages(m_gggggg)
    a.add_source_messages(m_hhhhhh)

    a.add_source_messages(m_iiiiii)
    a.add_source_messages(m_jjjjjj)

    a.add_source_messages(m_kkkkkk)
    a.add_source_messages(m_llllll)
    a.add_source_messages(m_mmmmmm)
    a.add_source_messages(m_nnnnnn)
    a.add_source_messages(m_oooooo)
    a.add_source_messages(m_pppppp)
    a.add_source_messages(m_qqqqqq)
    a.add_source_messages(m_rrrrrr)
    a.add_source_messages(m_ssssss)
    a.add_source_messages(m_tttttt)
    a.add_source_messages(m_uuuuuu)
    a.add_source_messages(m_vvvvvv)
    a.add_source_messages(m_wwwwww)
    a.add_source_messages(m_xxxxxx)
    a.add_source_messages(m_yyyyyy)
    a.add_source_messages(m_zzzzzz)

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
    #
    # ##################################################################################
    #
    a.add_service_module("ServiceA", m_aaaa, m_aaaa2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_bbbb, m_bbbb2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_cccc, m_cccc2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_dddd, m_dddd2, fractional_selectivity, threshold=1.0)

    a.add_service_module("ServiceA", m_eeee, m_eeee2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_ffff, m_ffff2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_gggg, m_gggg2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_hhhh, m_hhhh2, fractional_selectivity, threshold=1.0)

    a.add_service_module("ServiceA", m_iiii, m_iiii2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_jjjj, m_jjjj2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_kkkk, m_kkkk2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_llll, m_llll2, fractional_selectivity, threshold=1.0)

    a.add_service_module("ServiceA", m_mmmm, m_mmmm2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_nnnn, m_nnnn2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_oooo, m_oooo2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_pppp, m_pppp2, fractional_selectivity, threshold=1.0)

    a.add_service_module("ServiceA", m_qqqq, m_qqqq2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_rrrr, m_rrrr2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_ssss, m_ssss2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_tttt, m_tttt2, fractional_selectivity, threshold=1.0)

    a.add_service_module("ServiceA", m_uuuu, m_uuuu2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_vvvv, m_vvvv2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_wwww, m_wwww2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_xxxx, m_xxxx2, fractional_selectivity, threshold=1.0)

    a.add_service_module("ServiceA", m_yyyy, m_yyyy2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_zzzz, m_zzzz2, fractional_selectivity, threshold=1.0)

    a.add_service_module("ServiceA", m_aaaaa, m_aaaaa2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_bbbbb, m_bbbbb2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_ccccc, m_ccccc2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_ddddd, m_ddddd2, fractional_selectivity, threshold=1.0)

    a.add_service_module("ServiceA", m_eeeee, m_eeeee2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_fffff, m_fffff2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_ggggg, m_ggggg2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_hhhhh, m_hhhhh2, fractional_selectivity, threshold=1.0)

    a.add_service_module("ServiceA", m_iiiii, m_iiiii2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_jjjjj, m_jjjjj2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_kkkkk, m_kkkkk2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_lllll, m_lllll2, fractional_selectivity, threshold=1.0)

    a.add_service_module("ServiceA", m_mmmmm, m_mmmmm2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_nnnnn, m_nnnnn2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_ooooo, m_ooooo2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_ppppp, m_ppppp2, fractional_selectivity, threshold=1.0)

    a.add_service_module("ServiceA", m_qqqqq, m_qqqqq2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_rrrrr, m_rrrrr2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_sssss, m_sssss2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_ttttt, m_ttttt2, fractional_selectivity, threshold=1.0)

    a.add_service_module("ServiceA", m_uuuuu, m_uuuuu2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_vvvvv, m_vvvvv2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_wwwww, m_wwwww2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_xxxxx, m_xxxxx2, fractional_selectivity, threshold=1.0)

    a.add_service_module("ServiceA", m_yyyyy, m_yyyyy2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_zzzzz, m_zzzzz2, fractional_selectivity, threshold=1.0)

    ####

    a.add_service_module("ServiceA", m_aaaaaa, m_aaaaaa2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_bbbbbb, m_bbbbbb2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_cccccc, m_cccccc2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_dddddd, m_dddddd2, fractional_selectivity, threshold=1.0)

    a.add_service_module("ServiceA", m_eeeeee, m_eeeeee2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_ffffff, m_ffffff2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_gggggg, m_gggggg2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_hhhhhh, m_hhhhhh2, fractional_selectivity, threshold=1.0)

    a.add_service_module("ServiceA", m_iiiiii, m_iiiiii2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_jjjjjj, m_jjjjjj2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_kkkkkk, m_kkkkkk2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_llllll, m_llllll2, fractional_selectivity, threshold=1.0)

    a.add_service_module("ServiceA", m_mmmmmm, m_mmmmmm2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_nnnnnn, m_nnnnnn2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_oooooo, m_oooooo2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_pppppp, m_pppppp2, fractional_selectivity, threshold=1.0)

    a.add_service_module("ServiceA", m_qqqqqq, m_qqqqqq2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_rrrrrr, m_rrrrrr2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_ssssss, m_ssssss2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_tttttt, m_tttttt2, fractional_selectivity, threshold=1.0)

    a.add_service_module("ServiceA", m_uuuuuu, m_uuuuuu2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_vvvvvv, m_vvvvvv2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_wwwwww, m_wwwwww2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_xxxxxx, m_xxxxxx2, fractional_selectivity, threshold=1.0)

    a.add_service_module("ServiceA", m_yyyyyy, m_yyyyyy2, fractional_selectivity, threshold=1.0)
    a.add_service_module("ServiceA", m_zzzzzz, m_zzzzzz2, fractional_selectivity, threshold=1.0)


    return a


# def create_json_topology():
#     """
#        TOPOLOGY DEFINITION
#        Some attributes of fog entities (nodes) are approximate
#        """
#
#     ## MANDATORY FIELDS
#     topology_json = {}
#     topology_json["entity"] = []
#     topology_json["link"] = []
#
#     cloud_dev = {"id": 0, "model": "cloud", "mytag": "cloud", "IPT": 500 , "RAM": 40000, "COST": 3,
#                  "WATT": 200.0}
#     cloud_dev2 = {"id": 3, "model": "cloud", "mytag": "cloud", "IPT": 100, "RAM": 40000, "COST": 3,
#                   "WATT": 200.0}
#     cloud_dev3 = {"id": 4, "model": "cloud", "mytag": "cloud", "IPT": 800, "RAM": 40000, "COST": 3,
#                   "WATT": 200.0}
#     sensor_dev = {"id": 1, "model": "sensor-device", "IPT": 100, "RAM": 4000, "COST": 3, "WATT": 40.0}
#     actuator_dev = {"id": 2, "model": "actuator-device", "IPT": 100, "RAM": 4000, "COST": 3, "WATT": 40.0}
#
#     # if ipt of node is less than instructions of message, send to another node and store in hm
#
#     link1 = {"s": 1, "d": 0, "BW": 1, "PR": 1}
#     link2 = {"s": 0, "d": 2, "BW": 1, "PR": 1}
#     link3 = {"s": 1, "d": 3, "BW": 1, "PR": 1}
#     link4 = {"s": 3, "d": 2, "BW": 1, "PR": 1}
#     link5 = {"s": 1, "d": 4, "BW": 1, "PR": 1}
#     link6 = {"s": 4, "d": 2, "BW": 1, "PR": 1}
#
#     topology_json["entity"].append(cloud_dev)
#     topology_json["entity"].append(cloud_dev2)
#     topology_json["entity"].append(cloud_dev3)
#
#     topology_json["entity"].append(sensor_dev)
#     topology_json["entity"].append(actuator_dev)
#     topology_json["link"].append(link1)
#     topology_json["link"].append(link2)
#     topology_json["link"].append(link3)
#     topology_json["link"].append(link4)
#     topology_json["link"].append(link5)
#     topology_json["link"].append(link6)
#
#     return topology_json


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
    dataNetwork = json.load(open('my_network_two.json'))
    t.load(dataNetwork)

    # t = Topology()
    # t_json = create_json_topology()
    # t.load(t_json)

    nx.write_gexf(t.G,
                  folder_results + "graph_main2")  # you can export the Graph in multiples format to view in tools likFFe Gephi, and so on.
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
    pop.set_sink_control({"model": "actuator-device", "number": 1, "module": app.get_sink_modules()})

    # In addition, a source includes a distribution function:
    dDistribution = deterministic_distribution(name="Deterministic", time=100)
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
               app.get_message("M.Y"), app.get_message("M.Z"),

               app.get_message("M.AA"), app.get_message("M.BB"),
               app.get_message("M.CC"), app.get_message("M.DD"),
               app.get_message("M.EE"), app.get_message("M.FF"),
               app.get_message("M.GG"), app.get_message("M.HH"),
               app.get_message("M.II"), app.get_message("M.JJ"),
               app.get_message("M.KK"), app.get_message("M.LL"),
               app.get_message("M.MM"), app.get_message("M.NN"),
               app.get_message("M.OO"), app.get_message("M.PP"),
               app.get_message("M.QQ"), app.get_message("M.RR"),
               app.get_message("M.SS"), app.get_message("M.TT"),
               app.get_message("M.UU"), app.get_message("M.VV"),
               app.get_message("M.WW"), app.get_message("M.XX"),
               app.get_message("M.YY"), app.get_message("M.ZZ"),

               app.get_message("M.AAA"), app.get_message("M.BBB"),
               app.get_message("M.CCC"), app.get_message("M.DDD"),
               app.get_message("M.EEE"), app.get_message("M.FFF"),
               app.get_message("M.GGG"), app.get_message("M.HHH"),
               app.get_message("M.III"), app.get_message("M.JJJ"),
               app.get_message("M.KKK"), app.get_message("M.LLL"),
               app.get_message("M.MMM"), app.get_message("M.NNN"),
               app.get_message("M.OOO"), app.get_message("M.PPP"),
               app.get_message("M.QQQ"), app.get_message("M.RRR"),
               app.get_message("M.SSS"), app.get_message("M.TTT"),
               app.get_message("M.UUU"), app.get_message("M.VVV"),
               app.get_message("M.WWW"), app.get_message("M.XXX"),
               app.get_message("M.YYY"), app.get_message("M.ZZZ"),

               app.get_message("M.AAAA"), app.get_message("M.BBBB"),
               app.get_message("M.CCCC"), app.get_message("M.DDDD"),
               app.get_message("M.EEEE"), app.get_message("M.FFFF"),
               app.get_message("M.GGGG"), app.get_message("M.HHHH"),
               app.get_message("M.IIII"), app.get_message("M.JJJJ"),
               app.get_message("M.KKKK"), app.get_message("M.LLLL"),
               app.get_message("M.MMMM"), app.get_message("M.NNNN"),
               app.get_message("M.OOOO"), app.get_message("M.PPPP"),
               app.get_message("M.QQQQ"), app.get_message("M.RRRR"),
               app.get_message("M.SSSS"), app.get_message("M.TTTT"),
               app.get_message("M.UUUU"), app.get_message("M.VVVV"),
               app.get_message("M.WWWW"), app.get_message("M.XXXX"),
               app.get_message("M.YYYY"), app.get_message("M.ZZZZ"),

               app.get_message("M.AAAAA"), app.get_message("M.BBBBB"),
               app.get_message("M.CCCCC"), app.get_message("M.DDDDD"),
               app.get_message("M.EEEEE"), app.get_message("M.FFFFF"),
               app.get_message("M.GGGGG"), app.get_message("M.HHHHH"),
               app.get_message("M.IIIII"), app.get_message("M.JJJJJ"),
               app.get_message("M.KKKKK"), app.get_message("M.LLLLL"),
               app.get_message("M.MMMMM"), app.get_message("M.NNNNN"),
               app.get_message("M.OOOOO"), app.get_message("M.PPPPP"),
               app.get_message("M.QQQQQ"), app.get_message("M.RRRRR"),
               app.get_message("M.SSSSS"), app.get_message("M.TTTTT"),
               app.get_message("M.UUUUU"), app.get_message("M.VVVVV"),
               app.get_message("M.WWWWW"), app.get_message("M.XXXXX"),
               app.get_message("M.YYYYY"), app.get_message("M.ZZZZZ")
               ]
    #sort(msgList) # remove this to make fcfs

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


    selectorPath = CacheBasedSolution_onGoing()

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
def search():
    pass


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

    # print("\n--- %s seconds ---" % (time.time() - start_time))
    #
    # ## Finally, you can analyse the results:
    #
    # t = Topology()
    # dataNetwork = json.load(open('my_network_two.json'))
    # t.load(dataNetwork)
    #
    # print("-" * 20)
    # print("Results:")
    # print("-" * 20)
    # m = Stats(defaultPath="results/sim_trace", topology = t)  # Same name of the results
    # time_loops = [["M.A", "M.A2"], ["M.B", "M.B2"], ["M.C", "M.C2"], ["M.D", "M.D2"],
    #               ["M.E", "M.E2"], ["M.F", "M.F2"], ["M.G", "M.G2"], ["M.H", "M.H2"],
    #               ["M.I", "M.I2"], ["M.J", "M.J2"], ["M.K", "M.K2"], ["M.L", "M.L2"],
    #               ["M.M", "M.M2"], ["M.N", "M.N2"], ["M.O", "M.O2"], ["M.P", "M.P2"],
    #               ["M.Q", "M.Q2"], ["M.R", "M.R2"], ["M.S", "M.S2"], ["M.T", "M.T2"],
    #               ["M.U", "M.U2"], ["M.V", "M.V2"], ["M.W", "M.W2"], ["M.X", "M.X2"],
    #               ["M.Y", "M.Y2"], ["M.Z", "M.Z2"]]
    # # time_loops = ["M.A", "M.B","M.C", "M.D","M.E", "M.F","M.G", "M.H","M.I", "M.J",
    # #                "M.K", "M.L","M.M", "M.N","M.O", "M.P","M.Q", "M.R","M.S", "M.T",
    # #                "M.U", "M.V","M.W", "M.X","M.Y", "M.Z",
    # #               "M.A2", "M.B2", "M.C2", "M.D2", "M.E2", "M.F2", "M.G2", "M.H2", "M.I2", "M.J2",
    # #               "M.K2", "M.L2", "M.M2", "M.N2", "M.O2", "M.P2", "M.Q2", "M.R2", "M.S2", "M.T2",
    # #               "M.U2", "M.V2", "M.W2", "M.X2", "M.Y2", "M.Z2"
    # #               ]
    # m.showResults2(1000,  time_loops=time_loops)
    #
    # print("\t- Network saturation -")
    # # print("\t\tAverage waiting messages : %i" % m.average_messages_not_transmitted())
    # print("\t\t Bytes Transmitted : %i" % m.bytes_transmitted())
    # # print("\t\tPeak of waiting messages : %i" % m.peak_messages_not_transmitted())
    #
    # # print("\t\tTOTAL messages not transmitted: %i" % m.messages_not_transmitted())
    #
    # print("\t\t Energy " + str(m.get_watt(1000, t)))
    #
    # #    print("\t\t get_cost_cloud" + str(m.get_cost_cloud(t)))
    #
    # # print("\t\t Show Results")
    # # m.showResults(1000, t, time_loops=time_loops)
    #
    # # print("\t\t Latency " + m.get_latency())
    # print("\n\t- Stats of each service deployed -")
    #
    # # Throughput is a measure of how many units of information a system can process in a given amount of time.
    #
    # # print (m.get_df_modules())
    # # print (m.get_df_service_utilization("ServiceA",1000))
    #
    # # print ("\n\t- Stats of each DEVICE -")
    #
    # # TODO
