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
print("answer "+l.getschicksalsjahre("6.5.1984"))


print("tenendenz "+l.getwochentendenz())
print("tenendenz "+l.getwochentendenz())
print("tenendenz "+l.getwochentendenz())