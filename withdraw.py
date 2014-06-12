#!/usr/bin/env python
# coding=iso-8859-1

# Cryptsy auto-withdraw cronjob
#
# Copyright © 2014 Scott Alfter
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import sys
sys.path.insert(0, './PyCryptsy/')
from PyCryptsy import PyCryptsy
from decimal import *
import ConfigParser
import pprint
import time

Config = ConfigParser.ConfigParser()
Config.read('./coinswitch.conf')

api=PyCryptsy(Config.get("Cryptsy", "key"), Config.get("Cryptsy", "secret"))
getcontext().prec=8

while True:
  balance=Decimal(api.Query("getinfo", {})["return"]["balances_available"]["BTC"])
  print "balance: "+str(balance)+" BTC"
  if (balance>0.01):
    print "withdrawal triggered"
    pprint.pprint(api.Query("makewithdrawal", {"address": Config.get("Cryptsy", "addr"), "amount": Config.get("Cryptsy", "minbal")}))
  time.sleep(float(Config.get("Misc", "interval")))
