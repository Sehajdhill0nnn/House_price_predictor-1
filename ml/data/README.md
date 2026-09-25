# Dataset

Download the Kaggle Ames Housing `train.csv` into this directory. The expected source is the House Prices: Advanced Regression Techniques dataset, with `SalePrice` as its target.

Run from the repository root:

```bash
python ml/download_data.py
```

The training code intentionally validates the selected feature columns before fitting, so a malformed or unrelated CSV fails with a clear message.
