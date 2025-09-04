import math

print("Exponent to scientific notation calculator")
base = float(input("Base: "))
power = float(input("Power: "))
log1 = math.log10(base)*power
p2 = int(log1)
p1 = log1-p2
x = 10**p1
if x <= 1:
    x*=10
    p2-=1
elif x > 10:
    x/=10
    p2+=1
y = round(x,4)
print(f"The answer in scientific notation is {y} x 10^{p2}")
        
