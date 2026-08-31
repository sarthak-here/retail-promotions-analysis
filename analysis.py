"""Reproducible analysis for the Codebasics retail promotions internship project."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "datasets"
OUTPUT_DIR = ROOT / "outputs"


def load_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    campaigns = pd.read_csv(DATA_DIR / "dim_campaigns.csv")
    products = pd.read_csv(DATA_DIR / "dim_products.csv")
    stores = pd.read_csv(DATA_DIR / "dim_stores.csv")
    events = pd.read_csv(DATA_DIR / "fact_events.csv")
    return campaigns, products, stores, events


def analyse() -> dict[str, object]:
    campaigns, products, stores, raw_events = load_data()
    business_key = ["store_id", "campaign_id", "product_code"]

    duplicate_rows_removed = int(raw_events.duplicated(business_key).sum())
    events = raw_events.drop_duplicates(business_key, keep="first").copy()

    missing_values_filled = int(events["quantity_sold(before_promo)"].isna().sum())
    median_for_imputation = float(events["quantity_sold(before_promo)"].median())
    events["quantity_sold(before_promo)"] = events[
        "quantity_sold(before_promo)"
    ].fillna(median_for_imputation)

    data = (
        events.merge(campaigns, on="campaign_id", validate="many_to_one")
        .merge(products, on="product_code", validate="many_to_one")
        .merge(stores, on="store_id", validate="many_to_one")
    )
    data["revenue_before"] = (
        data["base_price(before_promo)"] * data["quantity_sold(before_promo)"]
    )
    data["revenue_after"] = (
        data["base_price(after_promo)"] * data["quantity_sold(after_promo)"]
    )

    city_store_counts = stores.groupby("city")["store_id"].nunique().sort_values(ascending=False)

    category_prices = (
        data.groupby("category", as_index=False)["base_price(before_promo)"]
        .mean()
        .rename(columns={"base_price(before_promo)": "average_base_price_before"})
        .sort_values("average_base_price_before")
    )

    diwali = data[data["campaign_name"].eq("Diwali")]
    sankranti = data[data["campaign_name"].eq("Sankranti")]

    diwali_bogof_units = int(
        diwali.loc[diwali["promo_type"].eq("BOGOF"), "quantity_sold(after_promo)"].sum()
    )

    store_sales = (
        diwali.groupby(["store_id", "city"], as_index=False)["quantity_sold(after_promo)"]
        .sum()
        .sort_values("quantity_sold(after_promo)", ascending=False)
    )

    campaign_comparison = data.groupby("campaign_name", as_index=False).agg(
        units_before=("quantity_sold(before_promo)", "sum"),
        units_after=("quantity_sold(after_promo)", "sum"),
    )
    campaign_comparison["unit_increase"] = (
        campaign_comparison["units_after"] - campaign_comparison["units_before"]
    )
    campaign_comparison["isu_pct"] = (
        campaign_comparison["unit_increase"] / campaign_comparison["units_before"] * 100
    )

    product_ir = sankranti.groupby(["product_code", "product_name"], as_index=False).agg(
        revenue_before=("revenue_before", "sum"),
        revenue_after=("revenue_after", "sum"),
    )
    product_ir["ir_pct"] = (
        (product_ir["revenue_after"] - product_ir["revenue_before"])
        / product_ir["revenue_before"]
        * 100
    )
    product_ir = product_ir.sort_values("ir_pct", ascending=False)

    vizag_store_isu = (
        diwali[diwali["city"].eq("Visakhapatnam")]
        .groupby("store_id", as_index=False)
        .agg(
            units_before=("quantity_sold(before_promo)", "sum"),
            units_after=("quantity_sold(after_promo)", "sum"),
        )
    )
    vizag_store_isu["isu_pct"] = (
        (vizag_store_isu["units_after"] - vizag_store_isu["units_before"])
        / vizag_store_isu["units_before"]
        * 100
    )
    vizag_store_isu = vizag_store_isu.sort_values("isu_pct")

    sankranti_promos = sankranti.groupby("promo_type", as_index=False).agg(
        revenue_before=("revenue_before", "sum"),
        revenue_after=("revenue_after", "sum"),
        units_before=("quantity_sold(before_promo)", "sum"),
        units_after=("quantity_sold(after_promo)", "sum"),
    )
    sankranti_promos["ir_pct"] = (
        (sankranti_promos["revenue_after"] - sankranti_promos["revenue_before"])
        / sankranti_promos["revenue_before"]
        * 100
    )
    sankranti_promos["isu_pct"] = (
        (sankranti_promos["units_after"] - sankranti_promos["units_before"])
        / sankranti_promos["units_before"]
        * 100
    )
    negative_promos = sankranti_promos[
        sankranti_promos["ir_pct"].lt(0) & sankranti_promos["isu_pct"].lt(0)
    ].sort_values("ir_pct")

    lowest_category = category_prices.iloc[0]
    top_store = store_sales.iloc[0]
    top_campaign = campaign_comparison.sort_values("unit_increase", ascending=False).iloc[0]
    top_product = product_ir.iloc[0]
    lowest_vizag_store = vizag_store_isu.iloc[0]

    results: dict[str, object] = {
        "data_quality": {
            "raw_event_rows": int(len(raw_events)),
            "duplicate_rows_removed": duplicate_rows_removed,
            "clean_event_rows": int(len(events)),
            "missing_values_filled": missing_values_filled,
            "median_for_imputation": median_for_imputation,
        },
        "answers": {
            "q1_duplicate_rows_removed": duplicate_rows_removed,
            "q2_cities_with_more_than_5_stores": int((city_store_counts > 5).sum()),
            "q3_missing_values_filled": missing_values_filled,
            "q3_median_used": median_for_imputation,
            "q4_lowest_average_price_category": str(lowest_category["category"]),
            "q4_lowest_average_price": float(lowest_category["average_base_price_before"]),
            "q5_diwali_bogof_units_after": diwali_bogof_units,
            "q6_top_diwali_store": str(top_store["store_id"]),
            "q6_top_diwali_store_city": str(top_store["city"]),
            "q6_top_diwali_store_units_after": int(top_store["quantity_sold(after_promo)"]),
            "q7_campaign_with_greater_unit_increase": str(top_campaign["campaign_name"]),
            "q7_greater_unit_increase": float(top_campaign["unit_increase"]),
            "q8_top_sankranti_product": str(top_product["product_name"]),
            "q8_top_sankranti_product_code": str(top_product["product_code"]),
            "q8_ir_pct": float(top_product["ir_pct"]),
            "q9_lowest_vizag_diwali_store": str(lowest_vizag_store["store_id"]),
            "q9_isu_pct": float(lowest_vizag_store["isu_pct"]),
            "q10_negative_promo_types": negative_promos["promo_type"].tolist(),
        },
    }

    OUTPUT_DIR.mkdir(exist_ok=True)
    events.to_csv(OUTPUT_DIR / "fact_events_cleaned.csv", index=False)
    data.to_csv(OUTPUT_DIR / "analysis_dataset.csv", index=False)
    city_store_counts.rename("store_count").to_csv(OUTPUT_DIR / "city_store_counts.csv")
    category_prices.to_csv(OUTPUT_DIR / "category_prices.csv", index=False)
    store_sales.to_csv(OUTPUT_DIR / "diwali_store_sales.csv", index=False)
    campaign_comparison.to_csv(OUTPUT_DIR / "campaign_comparison.csv", index=False)
    product_ir.to_csv(OUTPUT_DIR / "sankranti_product_ir.csv", index=False)
    vizag_store_isu.to_csv(OUTPUT_DIR / "vizag_diwali_store_isu.csv", index=False)
    sankranti_promos.to_csv(OUTPUT_DIR / "sankranti_promo_performance.csv", index=False)
    (OUTPUT_DIR / "answers.json").write_text(
        json.dumps(results, indent=2), encoding="utf-8"
    )
    return results


if __name__ == "__main__":
    print(json.dumps(analyse(), indent=2))

