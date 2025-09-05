import pandas as pd
import numpy as np
 
IN  = "master_climate_transformed2.csv"
OUT = "master_climate_transformed_clean.csv"
 
# Choose your policy
# - "analytics_safe": preserve meaningful NaNs, only fill where it's logically unambiguous
# - "display_zero_fill": fill remaining NaNs with zeroes for presentation (be cautious!)
MODE = "analytics_safe"   # or "display_zero_fill"
 
df = pd.read_csv(IN)
 
# Ensure expected types
if "Year" in df.columns:
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce").astype("Int64")
 
# ---------------------------------------------------------------------
# 1) CO2 growth: first-year rows have no previous year -> fill with 0
# ---------------------------------------------------------------------
if {"Country","Year","co2_growth_prct","co2_growth_abs"}.issubset(df.columns):
    df = df.sort_values(["Country","Year"])
    first_idx = df.groupby("Country")["Year"].idxmin()
    # Fill first-year growth as 0 (common convention)
    df.loc[first_idx, "co2_growth_prct"] = df.loc[first_idx, "co2_growth_prct"].fillna(0.0)
    df.loc[first_idx, "co2_growth_abs"]  = df.loc[first_idx, "co2_growth_abs"].fillna(0.0)
    # Keep your alias in sync if present
    if "co2_change_pct" in df.columns:
        df.loc[first_idx, "co2_change_pct"] = df.loc[first_idx, "co2_change_pct"].fillna(0.0)
 
# ---------------------------------------------------------------------
# 2) Temperature anomaly: fallback baseline for countries lacking 2001–2005
# ---------------------------------------------------------------------
if {"Country","Year","Temp_Mean","temp_anomaly"}.issubset(df.columns):
    # Primary baseline: 2001–2005 mean
    base_0105 = (df.loc[df["Year"].between(2001, 2005)]
                   .groupby("Country")["Temp_Mean"].mean())
 
    # Fallback baseline: first up to 5 years available per country
    def _fallback_baseline(group):
        g = group.sort_values("Year")
        return g["Temp_Mean"].iloc[:5].mean()  # may be <5 if limited data
 
    fb = df.groupby("Country", group_keys=False).apply(_fallback_baseline)
    fb_map = df["Country"].map(fb)
 
    # Vectorized fill: where anomaly is NaN but Temp_Mean exists
    tm = df["Temp_Mean"]
    base_map = df["Country"].map(base_0105)
    final_baseline = base_map.fillna(fb_map)        # use fallback where needed
 
    mask = df["temp_anomaly"].isna() & tm.notna()
    df.loc[mask, "temp_anomaly"] = tm[mask] - final_baseline[mask]
 
# ---------------------------------------------------------------------
# 3) Deforestation %: handle extent==0 and missing components
# ---------------------------------------------------------------------
if {"tree_cover_loss__ha","tree_cover_extent_2000__ha","deforestation_pct"}.issubset(df.columns):
    extent = df["tree_cover_extent_2000__ha"]
    loss   = df["tree_cover_loss__ha"]
    # Recompute safely to avoid divisions by zero
    safe_defor = (loss / extent * 100).replace([np.inf, -np.inf], np.nan)
    # If extent==0 and loss==0 -> 0% (nothing to lose)
    zero_ext_zero_loss = extent.eq(0) & loss.fillna(0).eq(0)
    safe_defor = safe_defor.where(~zero_ext_zero_loss, 0.0)
    # If extent==0 and loss>0 -> mathematically undefined; keep NaN in analytics mode
    # For display mode, you may choose to mark 100% or 0%; here we set 100% for visibility
    undefined_mask = extent.eq(0) & loss.fillna(0).gt(0)
    if MODE == "display_zero_fill":
        safe_defor = safe_defor.where(~undefined_mask, 100.0)
    df["deforestation_pct"] = safe_defor
 
    # Optional: clip to [0, 100]
    df["deforestation_pct"] = df["deforestation_pct"].clip(lower=0, upper=100)
 
# ---------------------------------------------------------------------
# 4) CO2 per-capita (calc) NaNs: fill from provided co2_per_capita if present
# ---------------------------------------------------------------------
if {"co2","population","co2_per_capita_calc"}.issubset(df.columns):
    # Recompute guard (population>0)
    pop = df["population"]
    df["co2_per_capita_calc"] = np.where(
        pop.notna() & (pop > 0),
        (df["co2"] * 1_000_000) / pop,
        np.nan
    )
    # If an official per-capita exists, fill remaining gaps from it
    if "co2_per_capita" in df.columns:
        df["co2_per_capita_calc"] = df["co2_per_capita_calc"].fillna(df["co2_per_capita"])
 
# ---------------------------------------------------------------------
# 5) Optional: forward-fill weather metrics within each country (only if you want)
#     Uncomment to use cautiously (can introduce bias if large gaps).
# ---------------------------------------------------------------------
# weather_cols = [c for c in ["Temp_Max","Temp_Min","Temp_Mean","Precipitation_Sum",
#                             "Windspeed_Max","Windgusts_Max","Sunshine_Duration"]
#                 if c in df.columns]
# if weather_cols:
#     df = df.sort_values(["Country","Year"])
#     df[weather_cols] = df.groupby("Country")[weather_cols].ffill()
 
# ---------------------------------------------------------------------
# 6) Display-mode catch-all: fill any remaining NaNs with 0 for presentation
# ---------------------------------------------------------------------
if MODE == "display_zero_fill":
    df = df.fillna(0)
 
# ---------------------------------------------------------------------
# 7) Quick null report & save
# ---------------------------------------------------------------------
null_report = (df.isna().mean() * 100).sort_values(ascending=False)
print("\nNull % by column (after cleanup):\n", null_report.round(2).to_string())
df.to_csv(OUT, index=False)
print(f"\nSaved: {OUT}")