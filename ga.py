import re
jans='{"url":"/watch?v=ozSQPSnQOSQ'
print(re.findall('\"/watch\\?v=(.{11})',jans))
jans=[1,2,3,4]
print(jans.pop(0))
print(jans)