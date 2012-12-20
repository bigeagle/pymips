#!/usr/bin/env python2
# -*- coding:utf-8 -*-

import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

sys.path.insert(0, ROOT)

import unittest

from myhdl import Signal, intbv, Simulation, delay
from pymips.dlx import dlx, load_data_memory
from pymips.data_memory import group, m2int

class DLXTestBench(unittest.TestCase):
    def setUp(self):
        self.data_mem = [Signal(intbv(0)[8:]) for i in range(4096)]
        self.reg_mem = [Signal(intbv(i, min=-(2 ** 31), max=2 ** 31 - 1)) for i in range(32)]
        self.zreg_mem = [Signal(intbv(0, min=-(2 ** 31), max=2 ** 31 - 1)) for i in range(32)]

    def test_mem(self):
        dlx_instance = dlx(program=os.path.join(ROOT, 'programs/test1.txt'), data_mem=self.data_mem, reg_mem=self.reg_mem)

        def test():
            #yield delay(10)
            #self.assertEqual(self.reg_mem[5].val, 0)
            yield delay(14)
            self.assertEqual(self.reg_mem[2].val, 255)
            yield delay(2)
            self.assertEqual(self.reg_mem[3].val, 254)
            yield delay(6)
            self.assertEqual(self.reg_mem[4].val, -1)
            yield delay(4)
            self.assertEqual(self.reg_mem[6].val, 254)
            yield delay(4)
            self.assertEqual(self.reg_mem[7].val, 254)
            yield delay(6)
            self.assertEqual(self.reg_mem[8].val, 254)

        check = test()
        sim = Simulation(dlx_instance, check)
        sim.run(30, quiet=True)

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
        sim.run(30, quiet=True)

    def test_branch(self):
        dlx_instance = dlx(program=os.path.join(ROOT, 'programs/test3.txt'), data_mem=self.data_mem, reg_mem=self.reg_mem)

        def test():
            yield delay(10)
            self.assertEqual(self.reg_mem[2].val, 2)
            yield delay(2)
            self.assertEqual(self.reg_mem[3].val, 3)
            yield delay(2)
            self.assertEqual(self.reg_mem[4].val, 4)
            yield delay(2)
            self.assertEqual(self.reg_mem[6].val, 6)
            yield delay(2)
            self.assertEqual(self.reg_mem[7].val, 5)
            yield delay(2)
            self.assertEqual(self.reg_mem[5].val, 1)
            yield delay(2)
            self.assertEqual(self.reg_mem[3].val, 7)
            yield delay(2)
            self.assertEqual(self.reg_mem[5].val, 2)
            yield delay(4)
            self.assertEqual(self.reg_mem[7].val, 11)
            yield delay(4)
            self.assertEqual(self.reg_mem[5].val, 4)
            yield delay(6)
            self.assertEqual(self.reg_mem[5].val, 0)
            yield delay(4)
            self.assertEqual(self.reg_mem[7].val, 13)
            yield delay(10)
            self.assertEqual(self.reg_mem[8].val, 11)
            yield delay(14)
            self.assertEqual(self.reg_mem[8].val, 12)
            yield delay(22)
            self.assertEqual(self.reg_mem[8].val, 13)
            yield delay(14)
            self.assertEqual(self.reg_mem[8].val, 14)

        check = test()
        sim = Simulation(dlx_instance, check)
        sim.run(120, quiet=True)

    #def test_immediate(self):
    #        dlx_instance = dlx(program=os.path.join(ROOT, 'programs/test4.txt'), data_mem=self.data_mem, reg_mem=self.reg_mem)

    #        def test():
    #            yield delay(10)
    #            self.assertEqual(self.reg_mem[1].val, 6)
    #            yield delay(2)
    #            self.assertEqual(self.reg_mem[2].val, 19)
    #            yield delay(2)
    #            self.assertEqual(self.reg_mem[1].val, 22)
    #            yield delay(2)
    #            self.assertEqual(self.reg_mem[5].val, 54)
    #            yield delay(2)
    #            self.assertEqual(self.data_mem[23].val, 22)
    #            yield delay(2)
    #            self.assertEqual(self.reg_mem[4].val, 22)
    #            yield delay(2)
    #            self.assertEqual(self.reg_mem[1].val, 21)
    #            yield delay(2)
    #            self.assertEqual(self.reg_mem[1].val, -32490)
    #            yield delay(2)
    #            self.assertEqual(self.reg_mem[1].val, -65001)

    #        check = test()
    #        sim = Simulation(dlx_instance, check)
    #        sim.run(25, quiet=True)

    #def test_ori_andi(self):
    #    dlx_instance = dlx(program=os.path.join(ROOT, 'programs/test5.txt'), data_mem=self.data_mem, reg_mem=self.reg_mem)

    #    def test():
    #        yield delay(10)
    #        self.assertEqual(self.reg_mem[1].val, 0)
    #        yield delay(4)
    #        self.assertEqual(self.reg_mem[1].val, 65536)
    #        yield delay(2)
    #        self.assertEqual(self.reg_mem[1].val, 69571)
    #        yield delay(2)
    #        self.assertEqual(self.data_mem[3].val, 69571)
    #        yield delay(2)
    #        self.assertEqual(self.reg_mem[1], 1)

    #    check = test()
    #    sim = Simulation(dlx_instance, check)
    #    sim.run(30, quiet=True)

    def test_jump(self):
            dlx_instance = dlx(program=os.path.join(ROOT, 'programs/test6.txt'), data_mem=self.data_mem, reg_mem=self.reg_mem)

            def test():
                yield delay(10)
                self.assertEqual(self.reg_mem[5].val, 0)
                yield delay(2)
                self.assertEqual(self.reg_mem[3].val, 8)
                yield delay(2)
                self.assertEqual(self.reg_mem[5].val, 4)
                yield delay(2)
                self.assertEqual(self.reg_mem[2].val, -4)
                yield delay(6)
                self.assertEqual(self.reg_mem[31].val, 7)
                yield delay(12)
                self.assertEqual(self.reg_mem[5].val, 8)
                yield delay(2)
                self.assertEqual(self.reg_mem[2].val, 0)
                yield delay(2)
                self.assertEqual(self.reg_mem[31].val, 24)
                yield delay(6)
                self.assertEqual(self.reg_mem[31].val, 52)
                yield delay(6)
                self.assertEqual(self.reg_mem[31].val, 7)

            check = test()
            sim = Simulation(dlx_instance, check)
            sim.run(60, quiet=True)

    def test_shift(self):
        dlx_instance = dlx(program=os.path.join(ROOT, 'programs/test7.txt'), data_mem=self.data_mem, reg_mem=self.reg_mem)

        def test():
            yield delay(10)
            self.assertEqual(self.reg_mem[5].val, 0)
            yield delay(2)
            self.assertEqual(self.reg_mem[3].val, 8)
            yield delay(4)
            self.assertEqual(self.reg_mem[2].val, -16776978)
            yield delay(2)
            self.assertEqual(self.reg_mem[7], -536863296)
            yield delay(2)
            self.assertEqual(self.reg_mem[7], 60928)
            yield delay(2)
            self.assertEqual(self.reg_mem[7], 133693447)
            yield delay(2)
            self.assertEqual(self.reg_mem[7], -524281)
            yield delay(2)
            self.assertEqual(self.reg_mem[7], -65536)

        check = test()
        sim = Simulation(dlx_instance, check)
        sim.run(30, quiet=True)

    def test_arithmetic(self):
        dlx_instance = dlx(program=os.path.join(ROOT, 'programs/test8.txt'), data_mem=self.data_mem, reg_mem=self.zreg_mem)

        def test():
            yield delay(10)
            self.assertEqual(self.zreg_mem[2].val, 5)
            yield delay(2)
            self.assertEqual(self.zreg_mem[3].val, 6)
            yield delay(2)
            self.assertEqual(self.zreg_mem[4].val, 1)
            yield delay(2)
            self.assertEqual(self.zreg_mem[4].val, 0)
            yield delay(2)
            self.assertEqual(self.zreg_mem[3].val, 6)
            yield delay(2)
            self.assertEqual(self.zreg_mem[2].val, 1)
            yield delay(2)
            self.assertEqual(self.zreg_mem[3].val, 0)

        check = test()
        sim = Simulation(dlx_instance, check)
        sim.run(30, quiet=True)

    def test_merge_sort(self):
        ram = load_data_memory(os.path.join(ROOT, 'programs/hash/ram.txt'))
        dlx_instance = dlx(program=os.path.join(ROOT, 'programs/hash/rom.txt'), data_mem=ram, reg_mem=self.zreg_mem)

        def test():
            yield delay(1480*2)
            cared = ram[-80:]
            data = group(cared, 4)
            string = ' '.join(map(m2int, data))
            self.assertEqual(string, "262144 0 -645 -22 7 9 11 13 31 37 64 86 111 282 502 502 502 733 262144 0")
            print 'stack: %s' % string

        check = test()
        sim = Simulation(dlx_instance, check)
        sim.run(1480*2, quiet=True)


def main():
    unittest.main()

if __name__ == '__main__':
    main()

# vim: ts=4 sw=4 sts=4 expandtab
