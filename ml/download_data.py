"""Download the Ames Housing train.csv used by the project."""
from pathlib import Path
from sklearn.datasets import fetch_openml

DATA_DIR = Path(__file__).parent / "data"

def main() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    destination = DATA_DIR / "train.csv"
    print(f"Downloading Ames-compatible data to {destination}...")
    frame = fetch_openml(name="house_prices", as_frame=True, parser="auto").frame
    frame.to_csv(destination, index=False)
    print("Dataset downloaded. Verify that SalePrice and the selected Ames columns are present.")


if __name__ == "__main__":
    main()
