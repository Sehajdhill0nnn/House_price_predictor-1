"""Generate report-ready exploratory plots from the Ames dataset."""
from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns

from preprocessing import FEATURES, TARGET, load_dataset

OUTPUT = Path(__file__).parent / "outputs"


def main() -> None:
    OUTPUT.mkdir(exist_ok=True)
    data = load_dataset()
    sns.set_theme(style="whitegrid")
    for column, filename, title in [
        (TARGET, "sale_price_distribution.png", "Sale Price Distribution"),
        ("GrLivArea", "living_area_vs_price.png", "Living Area vs Sale Price"),
        ("OverallQual", "quality_vs_price.png", "Overall Quality vs Sale Price"),
        ("YearBuilt", "year_built_vs_price.png", "Year Built vs Sale Price"),
    ]:
        plt.figure(figsize=(9, 5))
        if column == TARGET:
            sns.histplot(data[column], kde=True)
        else:
            sns.scatterplot(data=data, x=column, y=TARGET, alpha=0.45)
        plt.title(title)
        plt.tight_layout()
        plt.savefig(OUTPUT / filename, dpi=160)
        plt.close()
    plt.figure(figsize=(10, 8))
    sns.heatmap(data[FEATURES + [TARGET]].select_dtypes("number").corr(), cmap="vlag", center=0)
    plt.title("Numerical Feature Correlation")
    plt.tight_layout()
    plt.savefig(OUTPUT / "correlation_heatmap.png", dpi=160)
    plt.close()
    data.isna().sum().sort_values(ascending=False).head(20).to_csv(OUTPUT / "missing_values.csv")


if __name__ == "__main__":
    main()
