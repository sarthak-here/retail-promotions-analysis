# Dataset setup

The source data is confidential and must not be committed to Git.

Place authorized local copies of these files in this directory:

- `dim_campaigns.csv`
- `dim_products.csv`
- `dim_stores.csv`
- `fact_events.csv`

Expected columns:

| File | Columns |
|---|---|
| `dim_campaigns.csv` | `campaign_id`, `campaign_name`, `start_date`, `end_date` |
| `dim_products.csv` | `product_code`, `product_name`, `category` |
| `dim_stores.csv` | `store_id`, `city` |
| `fact_events.csv` | `event_id`, `store_id`, `campaign_id`, `product_code`, `base_price(before_promo)`, `quantity_sold(before_promo)`, `promo_type`, `base_price(after_promo)`, `quantity_sold(after_promo)` |

The root `.gitignore` blocks source data and generated outputs as a second line
of defense against accidental disclosure.

