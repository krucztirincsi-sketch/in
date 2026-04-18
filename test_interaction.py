import backend.atomic_functions as af

data = [{"category": "Food", "amount": 10}]

html_table = af.render_interactive_table("My Table", data)
assert "Analyze category: Food" in html_table
assert "cursor: pointer;" in html_table

html_btn = af.render_action_button("Back", "Dashboard")
assert "window.slcTrigger('Dashboard')" in html_btn

filtered = af.filter_by_exact_match(data, "category", "Food")
assert len(filtered) == 1
assert len(af.filter_by_exact_match(data, "category", "Transport")) == 0

print("Interaction atomic functions work.")
