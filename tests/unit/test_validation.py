import pandas as pd
from examtrend_analyzer.core.validation import DatasetValidator

def test_missing_required_columns():
    issues = DatasetValidator().validate(pd.DataFrame({"year": [2024]}))
    assert any(issue.code == "MISSING_COLUMN" for issue in issues)
