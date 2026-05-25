hours:int = 15
minutes:int = 0
seconds:int = 0

hours %= 12

result_1:float
result_2:float
result_3:float


s_degrees:float = 360 / 60 * int(seconds)
m_degrees:float = (360 / 60 * int(minutes) + s_degrees / 60)
h_degrees:float = (360 / 12 * int(hours) + int(minutes) * 0.5 + int(seconds) * 1/120) 

if h_degrees - m_degrees >= 0:
    result_1 = h_degrees - m_degrees
else:
    result_1 = (h_degrees - m_degrees) * -1
if m_degrees - s_degrees >= 0:
    result_2 = m_degrees - s_degrees
else:
    result_2 = (m_degrees - s_degrees) * -1
if h_degrees - s_degrees >=0:
    result_3 = h_degrees - s_degrees
else:
    result_3 = (h_degrees - s_degrees) * -1

result_1 = min(result_1, 360 - result_1)
result_2 = min(result_2, 360 - result_2)
result_3 = min(result_3, 360 - result_3)
print("hours / minutes: ", result_1)
print("minutes / seconds: ", result_2)
print("hours / seconds: ", result_3)


