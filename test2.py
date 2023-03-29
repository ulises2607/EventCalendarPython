from calendar import month, monthrange, monthcalendar

print(month(2023,3))

print(month)

print(monthrange(2023,3))

mes_calendar = monthcalendar(2023, 4)

print(mes_calendar)

print([fecha_num for sublist in mes_calendar for fecha_num in sublist])

numeros = []

for i in mes_calendar:
    for j in i:
        numeros.append(j)

print(f"La lista de numeros: {numeros}")



