# Data

The project uses reproducible synthetic transaction data.

Generate the dataset by running:

```bash
python -m fraud_risk.data.generate
```

The generated CSV is written to:

`data/processed/transactions.csv`

Generated data files are excluded from Git because they can be reproduced from the source code and random seed.

This README is tracked, while `data/processed/` is ignored.
