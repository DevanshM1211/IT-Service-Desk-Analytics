import pandas as pd

from metrics import calculate_sla_compliance


def test_calculate_sla_compliance_returns_percentage():
    df = pd.DataFrame(
        {
            "Is_Resolved": [True, True, True, False],
            "SLA_Met": [True, False, True, True],
        }
    )

    result = calculate_sla_compliance(df, resolved_col="Is_Resolved", sla_col="SLA_Met")

    assert result == (2 / 3) * 100
