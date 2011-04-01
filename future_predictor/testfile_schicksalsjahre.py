#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logic
import storage
import json

l = logic.logic()

print("answer "+l.getschicksalsjahre("12.2.2000"))
print("answer "+l.getschicksalsjahre("12. januar 2000"))
print("answer "+l.getschicksalsjahre("1.1.1987"))
print("answer "+l.getschicksalsjahre("12. februar 2000"))
print("answer "+l.getschicksalsjahre("12.4.1967"))
print("answer "+l.getschicksalsjahre("20.2.2000"))
print("answer "+l.getschicksalsjahre("6.sda3 33 sd84"))


print("tenendenz "+l.getwochentendenz())
print("tenendenz "+l.getwochentendenz())
print("tenendenz "+l.getwochentendenz())

print(l.gettageswerte('Steinbock'))
print(l.gettageswerte('stier'))
print(l.gettageswerte('jungfrau'))
print(l.gettageswerte('bär'))

print(l.gettageshoroskop('Steinbock'))
print(l.gettageshoroskop('stier'))
print(l.gettageshoroskop('jungfrau'))
print(l.gettageshoroskop('bär'))