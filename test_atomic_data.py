import backend.atomic_functions as af

data = [
    {"date": "2023-01-01", "amt": 10},
    {"date": "2023-01-02", "amt": 20},
    {"date": "2023-01-03", "amt": 30}
]

assert af.calculate_average(data, "amt") == 20.0
assert len(af.filter_by_date(data, "date", "2023-01-02", "2023-01-03")) == 2
assert af.get_top_n(data, "amt", 1)[0]["amt"] == 30
print("Data atomic functions work.")
