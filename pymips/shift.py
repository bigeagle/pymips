#!/usr/bin/env python2
# -*- coding:utf-8 -*-

from myhdl import always_comb, intbv, bin, enum, concat

shift_op = enum(
    'NNOP',
    'LL',
    'RL',
    'RA',
    encoding='binary'
)


def shift(op, amount, control, out):
    """
    shifter
    op: num to be shifted
    amount: shift amount
    control: control code
    out: result
    """
    @always_comb
    def logic():
        if control == shift_op.NNOP:
            out.next = 0
        elif control == shift_op.LL:
            if amount == 0:
                out.next = op
            elif amount == 1:
                out.next = concat(op[31:], intbv(0)[1:]).signed()
            elif amount == 2:
                out.next = concat(op[30:], intbv(0)[2:]).signed()
            elif amount == 3:
                out.next = concat(op[29:], intbv(0)[3:]).signed()
            elif amount == 4:
                out.next = concat(op[28:], intbv(0)[4:]).signed()
            elif amount == 5:
                out.next = concat(op[27:], intbv(0)[5:]).signed()
            elif amount == 6:
                out.next = concat(op[26:], intbv(0)[6:]).signed()
            elif amount == 7:
                out.next = concat(op[25:], intbv(0)[7:]).signed()
            elif amount == 8:
                out.next = concat(op[24:], intbv(0)[8:]).signed()
            elif amount == 9:
                out.next = concat(op[23:], intbv(0)[9:]).signed()
            elif amount == 10:
                out.next = concat(op[22:], intbv(0)[10:]).signed()
            elif amount == 11:
                out.next = concat(op[21:], intbv(0)[11:]).signed()
            elif amount == 12:
                out.next = concat(op[20:], intbv(0)[12:]).signed()
            elif amount == 13:
                out.next = concat(op[19:], intbv(0)[13:]).signed()
            elif amount == 14:
                out.next = concat(op[18:], intbv(0)[14:]).signed()
            elif amount == 15:
                out.next = concat(op[17:], intbv(0)[15:]).signed()
            elif amount == 16:
                out.next = concat(op[16:], intbv(0)[16:]).signed()
            elif amount == 17:
                out.next = concat(op[15:], intbv(0)[17:]).signed()
            elif amount == 18:
                out.next = concat(op[14:], intbv(0)[18:]).signed()
            elif amount == 19:
                out.next = concat(op[13:], intbv(0)[19:]).signed()
            elif amount == 20:
                out.next = concat(op[12:], intbv(0)[20:]).signed()
            elif amount == 21:
                out.next = concat(op[11:], intbv(0)[21:]).signed()
            elif amount == 22:
                out.next = concat(op[10:], intbv(0)[22:]).signed()
            elif amount == 23:
                out.next = concat(op[9:], intbv(0)[23:]).signed()
            elif amount == 24:
                out.next = concat(op[8:], intbv(0)[24:]).signed()
            elif amount == 25:
                out.next = concat(op[7:], intbv(0)[25:]).signed()
            elif amount == 26:
                out.next = concat(op[6:], intbv(0)[26:]).signed()
            elif amount == 27:
                out.next = concat(op[5:], intbv(0)[27:]).signed()
            elif amount == 28:
                out.next = concat(op[4:], intbv(0)[28:]).signed()
            elif amount == 29:
                out.next = concat(op[3:], intbv(0)[29:]).signed()
            elif amount == 30:
                out.next = concat(op[2:], intbv(0)[30:]).signed()
            elif amount == 31:
                out.next = concat(op[1:], intbv(0)[31:]).signed()

        elif control == shift_op.RL:
            if amount == 0:
                out.next = op
            elif amount == 1:
                out.next = concat(intbv(0)[1:], op[32:1]).signed()
            elif amount == 2:
                out.next = concat(intbv(0)[2:], op[32:2]).signed()
            elif amount == 3:
                out.next = concat(intbv(0)[3:], op[32:3]).signed()
            elif amount == 4:
                out.next = concat(intbv(0)[4:], op[32:4]).signed()
            elif amount == 5:
                out.next = concat(intbv(0)[5:], op[32:5]).signed()
            elif amount == 6:
                out.next = concat(intbv(0)[6:], op[32:6]).signed()
            elif amount == 7:
                out.next = concat(intbv(0)[7:], op[32:7]).signed()
            elif amount == 8:
                out.next = concat(intbv(0)[8:], op[32:8]).signed()
            elif amount == 9:
                out.next = concat(intbv(0)[9:], op[32:9]).signed()
            elif amount == 10:
                out.next = concat(intbv(0)[10:], op[32:10]).signed()
            elif amount == 11:
                out.next = concat(intbv(0)[11:], op[32:11]).signed()
            elif amount == 12:
                out.next = concat(intbv(0)[12:], op[32:12]).signed()
            elif amount == 13:
                out.next = concat(intbv(0)[13:], op[32:13]).signed()
            elif amount == 14:
                out.next = concat(intbv(0)[14:], op[32:14]).signed()
            elif amount == 15:
                out.next = concat(intbv(0)[15:], op[32:15]).signed()
            elif amount == 16:
                out.next = concat(intbv(0)[16:], op[32:16]).signed()
            elif amount == 17:
                out.next = concat(intbv(0)[17:], op[32:17]).signed()
            elif amount == 18:
                out.next = concat(intbv(0)[18:], op[32:18]).signed()
            elif amount == 19:
                out.next = concat(intbv(0)[19:], op[32:19]).signed()
            elif amount == 20:
                out.next = concat(intbv(0)[20:], op[32:20]).signed()
            elif amount == 21:
                out.next = concat(intbv(0)[21:], op[32:21]).signed()
            elif amount == 22:
                out.next = concat(intbv(0)[22:], op[32:22]).signed()
            elif amount == 23:
                out.next = concat(intbv(0)[23:], op[32:23]).signed()
            elif amount == 24:
                out.next = concat(intbv(0)[24:], op[32:24]).signed()
            elif amount == 25:
                out.next = concat(intbv(0)[25:], op[32:25]).signed()
            elif amount == 26:
                out.next = concat(intbv(0)[26:], op[32:26]).signed()
            elif amount == 27:
                out.next = concat(intbv(0)[27:], op[32:27]).signed()
            elif amount == 28:
                out.next = concat(intbv(0)[28:], op[32:28]).signed()
            elif amount == 29:
                out.next = concat(intbv(0)[29:], op[32:29]).signed()
            elif amount == 30:
                out.next = concat(intbv(0)[30:], op[32:30]).signed()
            elif amount == 31:
                out.next = concat(intbv(0)[31:], op[32:31]).signed()

        elif control == shift_op.RA:
            if amount == 0:
                out.next = op
            elif amount == 1:
                out.next = concat(intbv(op[32:31].signed())[1:], op[32:1]).signed()
            elif amount == 2:
                out.next = concat(intbv(op[32:31].signed())[2:], op[32:2]).signed()
            elif amount == 3:
                out.next = concat(intbv(op[32:31].signed())[3:], op[32:3]).signed()
            elif amount == 4:
                out.next = concat(intbv(op[32:31].signed())[4:], op[32:4]).signed()
            elif amount == 5:
                out.next = concat(intbv(op[32:31].signed())[5:], op[32:5]).signed()
            elif amount == 6:
                out.next = concat(intbv(op[32:31].signed())[6:], op[32:6]).signed()
            elif amount == 7:
                out.next = concat(intbv(op[32:31].signed())[7:], op[32:7]).signed()
            elif amount == 8:
                out.next = concat(intbv(op[32:31].signed())[8:], op[32:8]).signed()
            elif amount == 9:
                out.next = concat(intbv(op[32:31].signed())[9:], op[32:9]).signed()
            elif amount == 10:
                out.next = concat(intbv(op[32:31].signed())[10:], op[32:10]).signed()
            elif amount == 11:
                out.next = concat(intbv(op[32:31].signed())[11:], op[32:11]).signed()
            elif amount == 12:
                out.next = concat(intbv(op[32:31].signed())[12:], op[32:12]).signed()
            elif amount == 13:
                out.next = concat(intbv(op[32:31].signed())[13:], op[32:13]).signed()
            elif amount == 14:
                out.next = concat(intbv(op[32:31].signed())[14:], op[32:14]).signed()
            elif amount == 15:
                out.next = concat(intbv(op[32:31].signed())[15:], op[32:15]).signed()
            elif amount == 16:
                out.next = concat(intbv(op[32:31].signed())[16:], op[32:16]).signed()
            elif amount == 17:
                out.next = concat(intbv(op[32:31].signed())[17:], op[32:17]).signed()
            elif amount == 18:
                out.next = concat(intbv(op[32:31].signed())[18:], op[32:18]).signed()
            elif amount == 19:
                out.next = concat(intbv(op[32:31].signed())[19:], op[32:19]).signed()
            elif amount == 20:
                out.next = concat(intbv(op[32:31].signed())[20:], op[32:20]).signed()
            elif amount == 21:
                out.next = concat(intbv(op[32:31].signed())[21:], op[32:21]).signed()
            elif amount == 22:
                out.next = concat(intbv(op[32:31].signed())[22:], op[32:22]).signed()
            elif amount == 23:
                out.next = concat(intbv(op[32:31].signed())[23:], op[32:23]).signed()
            elif amount == 24:
                out.next = concat(intbv(op[32:31].signed())[24:], op[32:24]).signed()
            elif amount == 25:
                out.next = concat(intbv(op[32:31].signed())[25:], op[32:25]).signed()
            elif amount == 26:
                out.next = concat(intbv(op[32:31].signed())[26:], op[32:26]).signed()
            elif amount == 27:
                out.next = concat(intbv(op[32:31].signed())[27:], op[32:27]).signed()
            elif amount == 28:
                out.next = concat(intbv(op[32:31].signed())[28:], op[32:28]).signed()
            elif amount == 29:
                out.next = concat(intbv(op[32:31].signed())[29:], op[32:29]).signed()
            elif amount == 30:
                out.next = concat(intbv(op[32:31].signed())[30:], op[32:30]).signed()
            elif amount == 31:
                out.next = concat(intbv(op[32:31].signed())[31:], op[32:31]).signed()

    return logic

# vim: ts=4 sw=4 sts=4 expandtab
