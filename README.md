# ATP Tennis — Match Duration Prediction

Binary classification project to predict whether an ATP tennis match ends in **2 sets or 3 sets**, using player and match features extracted from historical ATP data.

## Problem

Given pre-match information (player rankings, age, prize money, round, surface context, etc.), can we predict whether a match will be decided in 2 sets or 3 sets?

This is a class-imbalanced problem: roughly 70% of matches end in 2 sets.

## Dataset

**Source:** ATP historical match and ranking data (1968–2024).

The raw database (`atp_db.csv`, ~385 MB) is not included due to size constraints. The preprocessed dataset used for modelling (`df_japan_final.xlsx`) is included.

**External reference files included:**

| File | Description |
|------|-------------|
| `EXTERNAL_countries.csv` | Country codes |
| `EXTERNAL_players.csv` | Player metadata |
| `EXTERNAL_players_fullname.csv` | Player full names |

## Features

| Feature | Description |
|---------|-------------|
| `Prize` | Tournament prize money |
| `AgeDiff` | Age difference between players |
| `RankDifference` | ATP ranking difference |
| `PlayerWins` | Historical wins of the player |
| `OpponentWins` | Historical wins of the opponent |
| `DiffHand` | Whether players have different dominant hands (binary) |
| `HomeFactor` | Whether the player is playing in their home country (binary) |
| `RoundRobin` | Round robin stage (binary) |
| `RoundQualifying` | Qualifying round (binary) |
| `RoundPreFinals` | Semi-final stage (binary) |
| `RoundFinals` | Final (binary) |

**Target:** `Sets` → 0 (2 sets) or 1 (3 sets)

## Models

13 models were trained and evaluated, exploring different algorithms and class imbalance strategies:

| Model | Algorithm | Imbalance Strategy | Accuracy | AUC |
|-------|-----------|-------------------|----------|-----|
| 0 | Logistic Regression | None (baseline) | 0.704 | 0.547 |
| 1 | Logistic Regression | Balanced weights | 0.480 | 0.553 |
| 2 | Logistic Regression | Balanced + normalised | 0.484 | 0.560 |
| 3 | Decision Tree (depth=3) | Balanced weights | 0.563 | **0.564** |
| 4 | Random Forest | Balanced weights | 0.529 | 0.558 |
| 5 | XGBoost | `scale_pos_weight` | 0.558 | 0.545 |
| 6 | Neural Network (MLP) | SMOTE + normalised | 0.533 | 0.498 |
| 7 | Random Forest | Undersampling | 0.526 | 0.531 |
| 8 | Logistic Regression | Undersampling + normalised | 0.536 | 0.528 |
| 9–12 | Reduced versions (top 6 features) | Various | — | — |

**Best model:** Decision Tree (depth=3) with AUC = 0.564 and balanced recall across both classes.

The task proved inherently difficult — all models struggled to predict 3-set matches, reflecting the noise and unpredictability of tennis outcomes even with pre-match information.

## Files

```
├── 01_data_preparation.ipynb    # Data cleaning, feature engineering, EDA
├── 02_modeling.ipynb            # 13 classification models + comparative evaluation
├── df_japan_final.xlsx          # Preprocessed dataset (used by modeling notebook)
├── EXTERNAL_countries.csv       # Country reference
├── EXTERNAL_players.csv         # Player reference
├── EXTERNAL_players_fullname.csv
└── scripts/
    ├── merge_matches.py         # Merges year-by-year ATP match CSVs
    └── merge_rankings.py        # Merges decade-by-decade ATP ranking CSVs
```

## Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)

**Libraries:** `pandas`, `numpy`, `scikit-learn`, `xgboost`, `imbalanced-learn`, `matplotlib`, `seaborn`, `statsmodels`
