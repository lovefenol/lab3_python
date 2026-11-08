import numpy as np

expenses = np.array([3200, 3100, 2600, 1900, 1500, 1300, 1250, 1400, 1800, 2300, 2900, 3500])

winter = expenses[[11, 0, 1]].sum()

summer = expenses[5:8].sum()

print("расходы:", *expenses)
print(f"зима: {winter}, лето: {summer}")
if winter > summer:
    print("больше тратится зимой")
elif summer > winter:
    print("больше тратится летом")
else:
    print("расходы зимой и летом одинаковы")

max_months = np.where(expenses == expenses.max())[0] + 1
print(f"максимум ({expenses.max()}) в месяцах:", *max_months)