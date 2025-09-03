import pandas as pd

# Load the consolidated dataset
df = pd.read_csv("datasets/consolidated_tree_cover.csv")

# --- Step 1: Clean country fields ---
df["Country Name"] = df["Country Name"].astype(str).str.strip()
df["Country Code"] = df["Country Code"].astype(str).str.upper().str.strip()

if "Global Annual Tree cover loss" in df.columns:
    df = df.drop(columns=["Global Annual Tree cover loss"])

# --- Step 2: Convert numeric columns safely ---
num_cols = [
    "tree_cover_extent_2000__ha",
    "area__ha",
    "tree_cover_loss__year",
    "tree_cover_loss__ha",
    "gross_emissions_co2e_all_gases__Mg"
]

for col in num_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# --- Step 3: Handle missing values ---
# Example: Fill missing years with 0, leave others as NaN
if "tree_cover_loss__year" in df.columns:
    df["tree_cover_loss__year"] = df["tree_cover_loss__year"].fillna(0)

# Example: Fill numeric NaNs with 0 (optional)
df[num_cols] = df[num_cols].fillna(0)

# --- Step 4: Remove duplicates ---
df = df.drop_duplicates(subset=["Country Name", "Country Code", "tree_cover_loss__year"])

# --- Step 5: Derived metrics (optional) ---
if "tree_cover_extent_2000__ha" in df.columns and "area__ha" in df.columns:
    df["pct_tree_cover_2000"] = (df["tree_cover_extent_2000__ha"] / df["area__ha"]) * 100

if "tree_cover_loss__ha" in df.columns and "tree_cover_extent_2000__ha" in df.columns:
    df["pct_loss_vs_extent"] = (df["tree_cover_loss__ha"] / df["tree_cover_extent_2000__ha"]) * 100

# --- Step 6: Save cleaned dataset ---
df.to_csv("consolidated_tree_cover_cleaned.csv", index=False)

print("✅ Data cleaning complete. Cleaned file saved as consolidated_tree_cover_cleaned.csv")
