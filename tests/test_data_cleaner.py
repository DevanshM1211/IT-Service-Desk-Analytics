import numpy as np
import pandas as pd

from data_cleaner import fill_missing_values


def test_fill_missing_values_mean_only_numeric_columns():
    df = pd.DataFrame(
        {
            "numeric_col": [1.0, np.nan, 3.0],
            "text_col": ["a", None, "c"],
        }
    )

    result = fill_missing_values(df, strategy="mean")

    assert result["numeric_col"].isna().sum() == 0
    assert result["text_col"].isna().sum() == 1
