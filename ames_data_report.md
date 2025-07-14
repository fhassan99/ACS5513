# Deliverable 1: Data Report  
*Petabyte Pirates – Deliverable 1*  
*ACS-5513 · Applied Machine Learning*

---

## General Summary of the Data 

This project uses the Ames Housing dataset, comprising nearly 3,000 residential real estate transactions from 2006 to mid-2010. After removing outliers and cleaning data, 2,789 observations remain. The dataset originally contains 82 features, which are reduced through cleaning and engineering to a focused set of retained raw features, engineered features, ordinally encoded variables, and significant one-hot encoded dummy variables. The primary target for prediction is the sale price of each home.

| Item | Value |
| --- | --- |
| **Raw file** | `AmesHousing.csv` (Kaggle ID `prevek18/ames-housing-dataset`) |
| **Observations** | 2,930 rows (2,793 after outlier removal) |
| **Columns** | 81 raw features → 13 retained, 10 engineered, 6 ordinally encoded, and 61 significant one-hot dummies |
| **Target** | `SalePrice` (USD) |
| **Date range** | 2006 – 2010 (7 months of 2010) |
| **Granularity** | One row per residential real-estate transaction |

---

## Data Quality Summary

Substantial and comprehensive data cleaning was performed to ensure high-quality analysis. Unique identifier columns were dropped, and features with excessive missing values or near-constant values were removed. Outliers in sale price were identified and excluded using the 1.5×IQR rule, resulting in a more robust dataset. All string-based 'NaN' values were properly recast as true missing values. The final cleaned dataset is free of duplicates and ready for modeling.

| Check | Result | Notes |
| --- | --- | --- |
| Unique identifiers | 2 columns dropped | `Order` and `PID` |
| Missing values | 5 columns dropped | >60% null, e.g. `Pool QC`, `Alley`, `Fence` |
| Near-constant columns | 8 columns dropped | `Land Contour`, `Land Slope`, `Condition 2`, etc. (>90% identical) |
| Outliers | 137 rows above \$339,500 or below \$3,500 removed | Based on 1.5 × IQR rule |
| Duplicate rows | None |
| Mixed types | ‘NaN’ strings recast to true `NaN` in 23 object columns |
| Final frame for Deliverable 1 | 2,789 observations with selected features |

---

## Target Variable – `SalePrice`

The sale price distribution was initially highly right-skewed, violating normality assumptions. Outlier removal significantly reduced skewness, and a log transformation was tested but did not improve normality as much as expected. For this phase, the analysis proceeds with the trimmed, untransformed sale price, with the option to revisit transformations in future modeling stages.

| Statistic | Raw (w/ outliers) | After outlier trim | Log-transformed |
| --- | ---: | ---: | ---: |
| Skewness | **1.74** | **0.67** | **–0.52** |
| D’Agostino-Pearson | 1,074 (p < 0.001) | 177 (p < 0.001) | 237 (p < 0.001) |

> *Decision*: We retain the **trimmed, un-logged `SalePrice`** for Deliverable 1; log-transform will be revisited in Phase 2 after residual diagnostics.

---

## Individual Variables (Top Examples)

Feature selection was guided by statistical correlation and domain relevance. Engineered features like total square footage (including garage) and overall quality show the strongest relationships with sale price. Categorical variables such as neighborhood and kitchen quality also provide significant predictive power, while low-signal features like lot area and roof style were dropped or bundled. Full feature-level decisions are documented in the [data dictionary](https://docs.google.com/spreadsheets/d/1zRmdRlc2efk0RiQ3xv9OARQlnGgF3sbfwbhnpNbcv7Y/edit?gid=1233168720#gid=1233168720).

| Feature | Type | Key observations |
| --- | --- | --- |
| **Total SF + Garage** | Engineered (numeric) | Highest linear correlation with SalePrice ( *r* = 0.82) |
| **Overall Qual** | Raw ordinal (1-10) | Strong monotonic influence ( *r* = 0.79); kept |
| **Neighborhood** | Nominal → one-hot | Distinct price bands; 19 dummies kept after p-biserial screening |
| **Kitchen Qual** | Ordinal → mapped 1-5 | Median jumps \$40-60 k per quality tier |
| **Has Garage** | Binary | Homes w/ garage sell \$26 k higher on average |
| **Lot Area** | Raw numeric | Low signal ( *r* = 0.24) → dropped |
| **Roof Style** | Nominal | Weak separation; only `Hip` retained, others bundled as “Other” |

---

## Variable ranking (numeric Pearson *r* with SalePrice)

| Rank | Feature | *r* |
| ---: | --- | ---: |
| 1 | Qual x SF | **0.82** |
| 2 | Overall Qual | 0.79 |
| 3 | Total SF Plus Garage | 0.77 |
| 4 | Total SF | 0.74 |
| 5 | Exter Qual_Ord | 0.66 |
| 6 | Gr Liv Area | 0.65 |
| 7 | Kitchen Qual_Ord | 0.63 |
| 8 | Garage Cars | 0.63 |
| 9 | Garage Area | 0.61 |
| 10 | Total Baths | 0.60 |

## Individual Variables (Bottom Examples)

Several variables show surprisingly weak or negative correlations with sale price, revealing important insights about the housing market:

| Feature | Type | Key observations |
| --- | --- | --- |
| **House Age** | Engineered (numeric) | Strong negative correlation (*r* = -0.59); newer homes command premium |
| **Remodel Age** | Engineered (numeric) | Negative correlation (*r* = -0.56); recent renovations boost value |
| **Overall Cond** | Raw ordinal (1-10) | Surprisingly weak (*r* = -0.06); condition matters less than quality |
| **Has Remodeled** | Binary | Negative correlation (*r* = -0.09); counterintuitive but may reflect older homes |
| **Kitchen AbvGr** | Raw numeric | Negative correlation (*r* = -0.12); more kitchens don't add value |
| **Bedroom AbvGr** | Raw numeric | Weak positive (*r* = 0.16); more bedrooms don't strongly predict price |
| **Has Pool** | Binary | Nearly zero correlation (*r* = 0.05); pools don't add significant value in Iowa |

> *Note: Some negative correlations (age-related) are expected, while others (condition, remodeling) reveal market nuances that warrant further investigation in modeling phases.*

---

## Relationship between Explanatory Variables and Target Variable  

* **Size × Quality** – The engineered `Qual × SF` captures 80% of variance in a univariate regression (Train R² = 0.799, Test R² = 0.771).  
* **Neighborhood Effect** – Premium clusters (e.g., `NoRidge`, `NWAmes`, and `Greens`) show significantly higher median prices compared to other areas.  
* **Seasonality** – Q2 & Q3 sales volume nearly double Q4, but median price drift by month is < \$8 k → we defer seasonal adjustment.  
* **Garage & Basement** – Presence and finish quality of these features lifts price; binary flags retained, low-signal ordinal garage quality dropped.  

> *Note: The relationship between explanatory variables and target variable is complex. The engineered `Qual × SF` captures 80% of variance in a univariate regression (Train R² = 0.799, Test R² = 0.771). The premium clusters (`NoRidge`, `NWAmes`, and `Greens`) add \$70-90 k over the city-wide median. The seasonality is not significant, as Q2 & Q3 sales volume nearly double Q4, but median price drift by month is <\$8 k. The garage and basement features are significant, as they lift price; binary flags retained, low-signal ordinal garage quality dropped.*
