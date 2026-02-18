from pathlib import Path

import pandas as pd

from visualize_charts import ServiceDeskChartGenerator


def test_priority_distribution_chart_creates_file(tmp_path: Path):
    df = pd.DataFrame(
        {
            "Priority": ["Critical", "High", "Medium", "Low"],
            "ticket_count": [10, 20, 40, 30],
            "percentage": [10.0, 20.0, 40.0, 30.0],
        }
    )

    output_dir = tmp_path / "charts"
    generator = ServiceDeskChartGenerator(output_dir=str(output_dir))
    generator.create_priority_distribution_chart(df)

    output_file = output_dir / "priority_distribution.png"
    assert output_file.exists()
