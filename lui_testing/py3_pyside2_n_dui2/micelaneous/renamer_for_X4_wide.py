#Copy/Pasted from claude.ai

import os

directory = "."  # Change this to your directory path

for i in range(1, 101):
    group = (i - 1) // 20 + 1          # Groups 1–5
    new_index = (i - 1) % 20 + 1       # Resets 1–20 within each group

    old_name = f"X4_wide_M1S4_2_{i:04d}.cbf"
    new_name = f"X4_wide_M1S4_{group}_{new_index:04d}.cbf"

    old_path = os.path.join(directory, old_name)
    new_path = os.path.join(directory, new_name)

    if os.path.exists(old_path):
        os.rename(old_path, new_path)
        print(f"Renamed: {old_name} → {new_name}")
    else:
        print(f"Skipped (not found): {old_name}")
