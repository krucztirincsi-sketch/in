import json

# ==========================================
# Atomic Data Functions
# ==========================================

def aggregate_by_category(data: list, category_field: str, amount_field: str) -> dict:
    """Aggregates an amount field by a given category field."""
    aggregated = {}
    for item in data:
        cat = item.get(category_field)
        amt = item.get(amount_field, 0)
        if cat:
            aggregated[cat] = aggregated.get(cat, 0) + amt
    return aggregated

def calculate_total(data: list, amount_field: str) -> float:
    """Calculates the sum of an amount field across a list of dictionaries."""
    return sum(item.get(amount_field, 0) for item in data)


# ==========================================
# Atomic UI Rendering Functions
# ==========================================

def render_bar_chart(title: str, data_dict: dict) -> str:
    """Renders a simple HTML/JS Bar Chart using Chart.js based on a dictionary of data."""
    labels = list(data_dict.keys())
    values = list(data_dict.values())

    # We use a unique ID so multiple charts can be rendered
    chart_id = f"chart_{hash(title) % 100000}"

    html = f"""
    <div class="card my-3 shadow-sm">
        <div class="card-body">
            <h5 class="card-title text-center">{title}</h5>
            <canvas id="{chart_id}"></canvas>
        </div>
    </div>
    <script>
    setTimeout(() => {{
        const ctx = document.getElementById('{chart_id}').getContext('2d');
        new Chart(ctx, {{
            type: 'bar',
            data: {{
                labels: {json.dumps(labels)},
                datasets: [{{
                    label: '{title}',
                    data: {json.dumps(values)},
                    backgroundColor: 'rgba(54, 162, 235, 0.6)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                }}]
            }},
            options: {{
                responsive: true,
                scales: {{ y: {{ beginAtZero: true }} }}
            }}
        }});
    }}, 100);
    </script>
    """
    return html

def render_pie_chart(title: str, data_dict: dict) -> str:
    """Renders a simple HTML/JS Pie Chart using Chart.js."""
    labels = list(data_dict.keys())
    values = list(data_dict.values())
    chart_id = f"pie_{hash(title) % 100000}"

    html = f"""
    <div class="card my-3 shadow-sm">
        <div class="card-body">
            <h5 class="card-title text-center">{title}</h5>
            <div style="max-width: 400px; margin: 0 auto;">
                <canvas id="{chart_id}"></canvas>
            </div>
        </div>
    </div>
    <script>
    setTimeout(() => {{
        const ctx = document.getElementById('{chart_id}').getContext('2d');
        new Chart(ctx, {{
            type: 'pie',
            data: {{
                labels: {json.dumps(labels)},
                datasets: [{{
                    data: {json.dumps(values)},
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.6)',
                        'rgba(54, 162, 235, 0.6)',
                        'rgba(255, 206, 86, 0.6)',
                        'rgba(75, 192, 192, 0.6)',
                        'rgba(153, 102, 255, 0.6)',
                        'rgba(255, 159, 64, 0.6)'
                    ]
                }}]
            }},
            options: {{ responsive: true }}
        }});
    }}, 100);
    </script>
    """
    return html

def render_summary_text(title: str, text: str, sentiment: str = "neutral") -> str:
    """Renders a textual summary. Sentiment can change styling."""
    color_class = "text-body"
    bg_class = "bg-light"

    if sentiment == "positive" or sentiment == "calm":
        color_class = "text-success"
        bg_class = "bg-success-subtle"
    elif sentiment == "negative" or sentiment == "anxious":
        color_class = "text-danger"
        bg_class = "bg-danger-subtle"

    html = f"""
    <div class="card my-3 shadow-sm {bg_class}">
        <div class="card-body">
            <h5 class="card-title {color_class}">{title}</h5>
            <p class="card-text fs-4 fw-bold">{text}</p>
        </div>
    </div>
    """
    return html

def render_table(title: str, data: list) -> str:
    """Renders a generic HTML table for a list of dictionaries."""
    if not data:
        return f"<div>No data available for {title}</div>"

    headers = list(data[0].keys())

    thead = "".join(f"<th>{h}</th>" for h in headers)

    tbody = ""
    for row in data:
        tbody += "<tr>" + "".join(f"<td>{row.get(h, '')}</td>" for h in headers) + "</tr>"

    html = f"""
    <div class="card my-3 shadow-sm">
        <div class="card-body">
            <h5 class="card-title">{title}</h5>
            <div class="table-responsive">
                <table class="table table-striped table-hover">
                    <thead><tr>{thead}</tr></thead>
                    <tbody>{tbody}</tbody>
                </table>
            </div>
        </div>
    </div>
    """
    return html

# Export a registry of available functions
AVAILABLE_FUNCTIONS = {
    "aggregate_by_category": aggregate_by_category,
    "calculate_total": calculate_total,
    "render_bar_chart": render_bar_chart,
    "render_pie_chart": render_pie_chart,
    "render_summary_text": render_summary_text,
    "render_table": render_table
}
