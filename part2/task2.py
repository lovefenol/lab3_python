import numpy as np


def read_array(text):
    while True:
        try:
            arr = np.array(input(text).split(), dtype=float)
        except ValueError:
            print("нужно вводить только числа через пробел")
            continue
        if arr.size == 0:
            print("ничего не введено")
            continue
        if not np.all(np.isfinite(arr)) or np.any(arr <= 0):
            print("числа должны быть конечными и больше нуля")
            continue
        return arr

def read_int(text):
    while True:
        try:
            return int(input(text))
        except ValueError:
            print("нужно ввести целое число")

while True:
    lengths = read_array("длины участков: ")
    speeds = read_array("скорости на участках: ")
    if len(lengths) != len(speeds):
        print("количество длин и скоростей должно совпадать, введите заново")
        continue
    break

n = len(lengths)

while True:
    k = read_int("k (участок въезда): ")
    p = read_int("p (участок выезда): ")
    if k < 1 or p < 1 or k > n or p > n:
        print(f"номера участков должны быть от 1 до {n}")
    elif k > p:
        print("k не может быть больше p")
    else:
        break


seg_len = lengths[k - 1:p]
seg_speed = speeds[k - 1:p]
seg_time = seg_len / seg_speed
S = seg_len.sum()
T = seg_time.sum()
V = S / T
while True:
    try:
        t = float(input("t (часов после въезда): "))
    except ValueError:
        print("нужно ввести число")
        continue
    if t < 0:
        print("t не может быть отрицательным")
    elif t > T:
        print(f"t больше общего времени в пути ({T:.2f} ч)")
    else:
        break

print(f"S = {S:g} км, T = {T:.2f} ч, V = {V:.2f} км/ч")

# где автомобиль через t часов
end_time = np.cumsum(seg_time)   
start_time = np.concatenate(([0], end_time[:-1])) 
idx = np.searchsorted(end_time, t)
distance = (t - start_time[idx]) * seg_speed[idx]

print(f"через {t:g} ч автомобиль на участке {k + idx}, в {distance:.1f} км от его начала")