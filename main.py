import matplotlib.pyplot as plt
from src.data_processing import load_profile_data

# --- Model Parameters ---
INPUT_FILE = "data/synthetic_profile_data.csv"
COMPENSATION_DEPTH_KM = 30.0
NUM_ITERATIONS = 4


def main():
    try:
        dist_m, topo_m, bouguer_ms2 = load_profile_data(INPUT_FILE)
        print("Data loaded successfully!")

    except FileNotFoundError:
        print(f"Error: The file '{INPUT_FILE}' was not found.")

    except Exception as e:
        print(f"An unexpected error occurred while loading data: {e}")


if __name__ == "__main__":
    main()
