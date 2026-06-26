# ATP Tennis — Match Duration Prediction (Japan)

Binary classification project to predict whether an ATP tennis match played in Japan ends in **2 sets or 3 sets**, following the CRISP-DM methodology.

## Business Context

The ability to predict match duration has practical value for multiple stakeholders in professional tennis:
- **Coaches and athletes** — strategic preparation and physical effort management
- **Performance analysts** — identifying patterns linked to player profiles and match conditions
- **Betting companies** — improving odds accuracy for match duration
- **Event organisers and broadcasters** — optimising scheduling and resource allocation
- **Sponsorship and marketing** — maximising brand exposure during high-audience moments

## Dataset

**Primary source:** ATP Tour historical match data (~1.3M matches). The raw data existed as **individual JSON files per year (1968–2024)**. These were imported into a **MongoDB** database — which handles JSON natively — and then exported as year-by-year CSVs, resulting in **57 separate match CSV files** and **decade-by-decade ranking files**. The `scripts/` folder contains the scripts used to merge all of these into single flat files before any analysis.

**Japan subset:** 21,375 matches, 16 original variables. The primary dataset alone was insufficient for modelling: it lacked player nationality, full ranking history, and hand dominance. Three external sources were used to enrich it:

| External file | Purpose |
|---------------|---------|
| `EXTERNAL_players.csv` | ~65K ATP players with nationality and hand dominance — used to fill `BornCountry`, `PlayerCountry`, `OpponentCountry`, `PlayerHand`, `OpponentHand`, `PlayerHeight`, `OpponentHeight`, `PlayerDOB`, `OpponentDOB` |
| `EXTERNAL_players_fullname.csv` | Full name lookup for players whose names in the main dataset were abbreviated or inconsistent — needed to match records across sources |
| `EXTERNAL_countries.csv` | ISO country code → full country name mapping — used to standardise the nationality fields extracted from the players file |

The large raw files (`atp_db.csv`, `EXTERNAL_matches.csv`, `EXTERNAL_rankings.csv`) are not included due to size — see the Files section.

**Original variables in the Japan subset:**

| Variable | Description | Null % |
|----------|-------------|--------|
| `PlayerName` | Main player name | 0% |
| `Born` | Player birthplace (city, country) | 29.5% |
| `Height` | Player height (cm) | 29.7% |
| `Hand` | Dominant hand | 13.5% |
| `Tournament` | Tournament name | 0% |
| `Location` | City and country | 0% |
| `Date` | Tournament start and end date (combined) | 0% |
| `Ground` | Court surface (Hard, Clay, Grass) | 0% |
| `Prize` | Tournament prize money | 2.0% |
| `GameRound` | Round (Quarter-finals, Semi-finals, etc.) | 0% |
| `GameRank` | Opponent's current ranking | 2.0% |
| `Opponent` | Opponent name | 0% |
| `WL` | Match result (W/L) | 2.0% |
| `Score` | Set-by-set score | 2.0% |

**Target variable:** `Sets` — whether the match ended in 2 sets (0) or 3 sets (1). ~70% of matches end in 2 sets (class imbalance).

## Data Preparation

Extensive feature engineering was applied across 15 steps:

| Step | Description |
|------|-------------|
| `BornCountry` | Extracted from `Born`; matched against external player database (~65K players); 35 players filled manually |
| `PlayerCountry` / `OpponentCountry` | Country linked to each player and opponent via name matching; 67 opponents filled manually |
| Country name conversion | ISO code → full country name via `EXTERNAL_countries.csv` |
| `Player_ID` / `Opponent_ID` | Unique player identifier |
| `Sets` | Target variable derived from `Score` — 2 or 3 sets completed |
| `StartDate` / `EndDate` | Separated from the combined `Date` field |
| `PlayerRank` / `OpponentRank` / `RankDifference` | Matched via `EXTERNAL_rankings.csv`; missing values filled from `FILLED_rankings.xlsx` |
| `HomeFactor` | Binary — whether the player is Japanese (playing on home soil) |
| `PlayerHand` / `OpponentHand` / `DiffHand` | Dominant hand extracted; `DiffHand` = 1 if players use different hands |
| `Prize` | Standardised to numeric (USD) |
| `Tournament` | Cleaned and standardised |
| `PlayerHeight` / `OpponentHeight` / `HeightDifference` | Height matched from external data |
| `PlayerDOB` / `OpponentDOB` / `AgeDiff` | Age difference at match date |
| Round binary indicators | `RoundRobin`, `RoundQualifying`, `RoundPreFinals`, `RoundFinals` |
| `PlayerWins` / `OpponentWins` / `WinDiff` | Historical win counts up to match date |

**Final cleaning:** removed 5-set matches, exact duplicates, mirror duplicates (player ↔ opponent), and irrelevant columns.

## Exploratory Data Analysis

- Correlation matrix and VIF analysis to detect multicollinearity — all features passed (VIF < 5)
- Distribution of `Sets`: ~70% end in 2 sets (imbalanced)
- Round type vs. Sets: finals and semi-finals tend to go to more sets
- `HeightDiff`, `AgeDiff`, `DiffHand`, `Ground`, `HomeFactor` analysed against the target

## Models

13 models were trained and compared, exploring different algorithms and class-imbalance strategies:

| Model | Algorithm | Strategy | Accuracy | AUC |
|-------|-----------|----------|----------|-----|
| 0 | Logistic Regression | None (baseline) | 0.704 | 0.547 |
| 1 | Logistic Regression | Balanced weights | 0.480 | 0.553 |
| 2 | Logistic Regression | Balanced + normalised | 0.484 | 0.560 |
| **3** | **Decision Tree (depth=3)** | **Balanced weights** | **0.563** | **0.564** |
| 4 | Random Forest | Balanced weights | 0.529 | 0.558 |
| 5 | XGBoost | `scale_pos_weight` | 0.558 | 0.545 |
| 6 | Neural Network (MLP) | SMOTE + normalised | 0.533 | 0.498 |
| 7 | Random Forest | Undersampling | 0.526 | 0.531 |
| 8 | Logistic Regression | Undersampling + normalised | 0.536 | 0.528 |
| 9 | Logistic Regression (top 6) | Balanced + normalised | 0.510 | 0.512 |
| 10 | Decision Tree (top 6) | Balanced weights | 0.475 | 0.556 |
| 11 | Random Forest (top 6) | Undersampling | 0.527 | 0.534 |
| 12 | Logistic Regression (top 6) | Undersampling + normalised | 0.493 | 0.555 |

**Best model:** Decision Tree (depth=3) with **AUC = 0.564** and the most balanced recall across both classes.

Models 9–12 used the top 6 most important features identified from variable importance analysis across models 1–8.

## Conclusions

All models struggled to reliably predict 3-set matches, reflecting the inherent unpredictability of tennis. The class imbalance (70/30) was the main modelling challenge — the baseline model simply predicted 2 sets for every match, achieving 70% accuracy while completely missing 3-set games. Balancing techniques improved recall for 3-set matches but reduced overall accuracy. The Decision Tree offered the best trade-off between interpretability and balanced performance.

## Files

```
├── 01_data_preparation.ipynb
│   # Loads the Japan subset from atp_db.csv, applies all 15 feature engineering
│   # steps using the external files, and exports df_japan_final.xlsx
│
├── 02_modeling.ipynb
│   # Trains and evaluates 13 classification models; includes confusion matrices,
│   # ROC curves, variable importance plots, and comparative AUC table
│
├── df_japan_final.xlsx
│   # Fully preprocessed dataset — output of 01_data_preparation.ipynb.
│   # This is the file fed directly into 02_modeling.ipynb.
│
├── EXTERNAL_players.csv
│   # ~65K ATP players with nationality (BornCountry), dominant hand, height,
│   # and date of birth. Used to enrich both PlayerName and Opponent fields.
│   # 35 players not found here were filled manually.
│
├── EXTERNAL_players_fullname.csv
│   # Maps abbreviated or inconsistent player names in atp_db.csv to their
│   # canonical full names, enabling reliable joins with EXTERNAL_players.csv.
│
├── EXTERNAL_countries.csv
│   # ISO 3166 country code → full country name. Used to convert the raw
│   # nationality codes from EXTERNAL_players.csv into readable labels.
│
└── scripts/
    ├── merge_matches.py
    │   # The raw ATP match data was distributed as 57 separate CSV files,
    │   # one per year from 1968 to 2024. This script concatenates them into
    │   # the single atp_db.csv used throughout the project.
    │
    └── merge_rankings.py
        # ATP ranking data was split by decade. This script merges the
        # decade files into EXTERNAL_rankings.csv, which is then used in
        # data preparation to derive PlayerRank, OpponentRank, and RankDifference.
```

> Large files not included: `atp_db.csv` (~385 MB), `EXTERNAL_matches.csv` (40 MB), `EXTERNAL_rankings.csv` (79 MB).

## Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)

**Libraries:** `pandas`, `numpy`, `scikit-learn`, `xgboost`, `imbalanced-learn`, `matplotlib`, `seaborn`, `statsmodels`
