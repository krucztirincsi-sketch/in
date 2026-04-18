import backend.atomic_functions as af

data = [
    {"date": "2023-01-01", "amt": 10},
    {"date": "2023-01-02", "amt": 20}
]

html_kpi = af.render_kpi_card("Total", 30, trend="+10%")
assert "Total" in html_kpi and "30" in html_kpi

html_table = af.render_interactive_table("My Table", data)
assert "DataTable()" in html_table and "2023-01-01" in html_table

print("UI atomic functions work.")
