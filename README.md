# A MIPS processor implemented with Python

## Introduction

PyMIPS is an implementation of a 5-stage pipelined processor developed for my _Structural Integrated Circuit Design_'s course project.

It's not tested on hardware yet, but i've converted it to Verilog and simulated with Modelsim, and passed 2 simple programs(_merge sort_ and _pi evaluation_) disassemblyed from real MIPS programs.

At the beginning of my course project i was not a bit familar with MIPS, and i was tring to implement a MIPS simulator in Python which describes MIPS at behavioral level without any RTL level description such as pipeline, which is only to help me learn MIPS instruction and mechanism. Then i search "MIPS" on github and found mgaitan's [pymips](https://github.com/mgaitan/pymips) project which implement a pipelined MIPS at RTL, so i forked this project and fixed some bugs and  implemented almost the whole MIPS instruction set except for floating point and intterruption, so that a normal MIPS program can run in pymips. 

## Install and Run

It was implemented with python's [myHDL](http://myhdl.org/) and it is the only depencency. So try in following steps:

    $ git clone git://github.com/mgaitan/pymips.git
    $ cd pymips
    $ pip install -r requirements.txt

And run with `dlx.py`
    
    $ ./dlx.py --debug --program ../programs/pi/rom.txt --data ../programs/pi/ram.txt --step 36000
  
where `--program` specify data in instruction memory and `--data` specify data in data memory, `--step` specifies amount of clock cycles to simulate.


## Documentation

The original pymips project has a report written in spanish describing the main architecture and design, but github recently stopped download service, so i've uploaded that to [dropbox](http://dl.dropbox.com/u/4574342/pymips.pdf). With the help of google translate, it's very easy to understand. And I will also publish a design report in Chinese as my course project report.

## Verilog

It's **NOT** a happy story when i convert this python project into verilog, although myHDL was claimed to be easy to convert to verilog and VHDL. The `dlx.py` was converted as a **single** file with more than 9000 lines! And it has syntax errors which cannot pass compilation!

So I converted every module in this project to Verilog with myHDL, and thank god they have a few syntax errors which are easy to debug, and then i rewrited the `dlx.py` in verilog manually as `mips_top.v` and `tb_mips.v` and simulated with ModelSim and passed all tests.

