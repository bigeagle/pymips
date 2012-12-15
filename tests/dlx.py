#!/usr/bin/env python2
# -*- coding:utf-8 -*-

#import sys
#sys.path.insert(0, '../')
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

import unittest

from myhdl import Signal, intbv, Simulation, delay
from pymips.dlx import dlx


class DLXTestBench(unittest.TestCase):
    def setUp(self):
        self.data_mem = [Signal(intbv(2*i, min=-(2 ** 31), max=2 ** 31 - 1)) for i in range(1024)]
        self.reg_mem = [Signal(intbv(i, min=-(2 ** 31), max=2 ** 31 - 1)) for i in range(32)]

    def test_lw_sw(self):
        dlx_instance = dlx(program=os.path.join(ROOT, 'programs/test1.txt'), data_mem=self.data_mem, reg_mem=self.reg_mem)
        def test():
            yield delay(10)
            self.assertEqual(self.reg_mem[1].val, 12)
            yield delay(4)
            self.assertEqual(self.reg_mem[1].val, 15)
            yield delay(2)
            self.assertEqual(self.data_mem[20].val, 15)
            yield delay(4)
            self.assertEqual(self.reg_mem[1].val, 6)
            yield delay(4)
            self.assertEqual(self.data_mem[11], 6)

        check = test()
        sim = Simulation(dlx_instance, check)
        sim.run(30)

    def test_competition(self):
        dlx_instance = dlx(program=os.path.join(ROOT, 'programs/test2.txt'), data_mem=self.data_mem, reg_mem=self.reg_mem)
        def test():
            yield delay(10)
            self.assertEqual(self.reg_mem[1].val, 5)
            yield delay(2)
            self.assertEqual(self.reg_mem[5].val, 1)
            yield delay(10)
            self.assertEqual(self.reg_mem[3].val, 7)

        check = test()
        sim = Simulation(dlx_instance, check)
        sim.run(30)

    def test_branch(self):
        dlx_instance = dlx(program=os.path.join(ROOT, 'programs/test3.txt'), data_mem=self.data_mem, reg_mem=self.reg_mem)
        def test():
            yield delay(10)
            self.assertEqual(self.reg_mem[1].val, 5)
            yield delay(2)
            self.assertEqual(self.reg_mem[5].val, 1)
            yield delay(2)
            self.assertEqual(self.reg_mem[3].val, 7)
            yield delay(2)
            self.assertEqual(self.reg_mem[5].val, 2)
            yield delay(8)
            self.assertEqual(self.reg_mem[5].val, 4)
            yield delay(10)
            self.assertEqual(self.reg_mem[5].val, 20)

        check = test()
        sim = Simulation(dlx_instance, check)
        sim.run(40)

def main():
    unittest.main()

if __name__ == '__main__':
    main()

# vim: ts=4 sw=4 sts=4 expandtab
