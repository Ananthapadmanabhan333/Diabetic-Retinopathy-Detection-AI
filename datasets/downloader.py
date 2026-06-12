import os
import argparse
from pathlib import Path
import subprocess

DATASETS = {
    "aptos2019": "aptos2019-blindness-detection",
    "eyepacs": "diabetic-retinopathy-detection"
}

def download_kaggle_dataset(competition_name: str, out_dir: Path):
    """Downloads dataset using Kaggle CLI. Requires ~/.kaggle/kaggle.json to be set up."""
    print(f"Downloading {competition_name} to {out_dir}...")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # Run kaggle command
    try:
        subprocess.run(
            ["kaggle", "competitions", "download", "-c", competition_name, "-p", str(out_dir)],
            check=True
        )
        print("Download complete. Unzipping...")
        zip_path = out_dir / f"{competition_name}.zip"
        if zip_path.exists():
            subprocess.run(["unzip", "-q", str(zip_path), "-d", str(out_dir)], check=True)
            zip_path.unlink()
        print(f"Successfully prepared {competition_name}")
    except subprocess.CalledProcessError as e:
        print(f"Error downloading {competition_name}: {e}")
        print("Please ensure kaggle CLI is installed and configured (KAGGLE_USERNAME and KAGGLE_KEY).")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=str, choices=list(DATASETS.keys()) + ["all"], default="all")
    parser.add_argument("--out_dir", type=str, default="./data")
    args = parser.parse_args()

    base_out = Path(args.out_dir)
    
    targets = list(DATASETS.keys()) if args.dataset == "all" else [args.dataset]
    for target in targets:
        download_kaggle_dataset(DATASETS[target], base_out / target)
