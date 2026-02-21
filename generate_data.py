import csv
import random
from datetime import date

random.seed(42)

# --- Rep profiles ---
# Each rep: region, product preference weights (Enterprise, Professional, Starter),
# base deals per month, base deal size range, trajectory
REPS = {
    # NORTHEAST - steady and reliable
    "Maria Lopez":      {"region": "Northeast", "prefs": [0.5, 0.3, 0.2], "deals_per_month": (2, 3), "base_revenue": (8000, 25000),  "trajectory": "star"},
    "James Wilson":     {"region": "Northeast", "prefs": [0.3, 0.4, 0.3], "deals_per_month": (1, 3), "base_revenue": (5000, 15000),  "trajectory": "stable"},
    "Priya Sharma":     {"region": "Northeast", "prefs": [0.2, 0.5, 0.3], "deals_per_month": (1, 3), "base_revenue": (4000, 12000),  "trajectory": "stable"},

    # WEST - volatile, high upside
    "Jake Chen":        {"region": "West", "prefs": [0.6, 0.2, 0.2], "deals_per_month": (1, 3), "base_revenue": (10000, 35000), "trajectory": "stable"},
    "Samantha Reed":    {"region": "West", "prefs": [0.3, 0.4, 0.3], "deals_per_month": (1, 3), "base_revenue": (5000, 18000),  "trajectory": "declining"},
    "Carlos Mendez":    {"region": "West", "prefs": [0.2, 0.3, 0.5], "deals_per_month": (1, 3), "base_revenue": (3000, 10000),  "trajectory": "stable"},
    "Aisha Patel":      {"region": "West", "prefs": [0.1, 0.2, 0.7], "deals_per_month": (2, 3), "base_revenue": (2000, 8000),   "trajectory": "specialist_starter"},

    # SOUTHEAST - growing region
    "David Kim":        {"region": "Southeast", "prefs": [0.4, 0.3, 0.3], "deals_per_month": (1, 3), "base_revenue": (6000, 20000),  "trajectory": "growing"},
    "Rachel Torres":    {"region": "Southeast", "prefs": [0.3, 0.4, 0.3], "deals_per_month": (1, 3), "base_revenue": (5000, 15000),  "trajectory": "stable"},
    "Marcus Johnson":   {"region": "Southeast", "prefs": [0.2, 0.3, 0.5], "deals_per_month": (1, 3), "base_revenue": (3000, 10000),  "trajectory": "stable"},
    "Emily Nguyen":     {"region": "Southeast", "prefs": [0.3, 0.4, 0.3], "deals_per_month": (1, 2), "base_revenue": (4000, 12000),  "trajectory": "new_hire"},  # starts Q3 2024

    # MIDWEST - underperforming
    "Brian O'Sullivan":  {"region": "Midwest", "prefs": [0.2, 0.4, 0.4], "deals_per_month": (1, 2), "base_revenue": (3000, 10000),  "trajectory": "stable"},
    "John Martinez":     {"region": "Midwest", "prefs": [0.3, 0.3, 0.4], "deals_per_month": (1, 2), "base_revenue": (4000, 12000),  "trajectory": "declining"},
    "Lisa Chang":        {"region": "Midwest", "prefs": [0.3, 0.4, 0.3], "deals_per_month": (1, 2), "base_revenue": (4000, 11000),  "trajectory": "stable"},
    "Tom Bradley":       {"region": "Midwest", "prefs": [0.4, 0.3, 0.3], "deals_per_month": (1, 2), "base_revenue": (5000, 14000),  "trajectory": "growing"},
}

PRODUCTS = ["Enterprise", "Professional", "Starter"]
DEAL_TYPES = ["New", "Renewal", "Upsell"]

# Product-level units and pricing
# Enterprise: few units, high price. Starter: many units, low price.
PRODUCT_UNITS = {
    "Enterprise":    (1, 5),
    "Professional":  (3, 15),
    "Starter":       (5, 50),
}
PRODUCT_PRICE_PER_UNIT = {
    "Enterprise":    (4000, 8000),
    "Professional":  (800, 2000),
    "Starter":       (100, 400),
}

# Seasonal multipliers by quarter
SEASONAL = {1: 0.85, 2: 0.95, 3: 1.0, 4: 1.30}

# Regional trend multipliers (applied per quarter elapsed, 0-7)
# Southeast grows, Midwest flat-to-declining
REGION_TREND = {
    "Northeast": 1.01,
    "West":      1.00,
    "Southeast": 1.03,
    "Midwest":   0.99,
}


def quarter_index(y, m):
    """Returns 0-7 for Q1 2024 through Q4 2025."""
    return (y - 2024) * 4 + (m - 1) // 3


def trajectory_multiplier(trajectory, qi):
    """Performance multiplier based on rep trajectory and quarter index (0-7)."""
    if trajectory == "stable":
        return 1.0
    elif trajectory == "star":
        # Strong and consistent, slight upward
        return 1.1 + qi * 0.02
    elif trajectory == "growing":
        return 0.85 + qi * 0.05
    elif trajectory == "declining":
        return 1.15 - qi * 0.06
    elif trajectory == "new_hire":
        # Ramps up from low starting point
        # qi 2 = Q3 2024 (their first quarter)
        months_active = qi - 2
        if months_active < 0:
            return 0  # not hired yet
        return 0.5 + months_active * 0.1
    elif trajectory == "specialist_starter":
        return 1.0
    return 1.0


def generate_rows():
    rows = []

    for year in [2024, 2025]:
        for month in range(1, 13):
            qi = quarter_index(year, month)
            q_label = f"Q{(month - 1) // 3 + 1}"
            season = SEASONAL[(month - 1) // 3 + 1]

            for rep_name, profile in REPS.items():
                traj_mult = trajectory_multiplier(profile["trajectory"], qi)
                if traj_mult == 0:
                    continue  # rep not hired yet

                region = profile["region"]
                region_trend = REGION_TREND[region] ** qi

                # --- Maria's West anomaly: Q3 2025 ---
                # She's Northeast, but let's say she temporarily helped West
                # Actually, let's keep her in NE and instead make Jake Chen
                # have the big Q3 2025 spike in West
                is_jake_spike = (rep_name == "Jake Chen" and year == 2025
                                 and month in [7, 8, 9])

                # Number of deals this month
                lo, hi = profile["deals_per_month"]
                base_deals = random.randint(lo, hi)

                # Apply multipliers to deal count
                deal_mult = traj_mult * season * region_trend
                if is_jake_spike:
                    deal_mult *= 3.0  # big spike

                num_deals = max(1, int(base_deals * deal_mult + random.gauss(0, 0.5)))

                for _ in range(num_deals):
                    # Pick product
                    if profile["trajectory"] == "specialist_starter":
                        product = random.choices(PRODUCTS, weights=[0.05, 0.05, 0.90])[0]
                    else:
                        product = random.choices(PRODUCTS, weights=profile["prefs"])[0]

                    # If Jake spike, heavily weight Enterprise
                    if is_jake_spike:
                        product = random.choices(PRODUCTS, weights=[0.8, 0.15, 0.05])[0]

                    # Units
                    u_lo, u_hi = PRODUCT_UNITS[product]
                    units = random.randint(u_lo, u_hi)

                    # Revenue = units * price_per_unit with noise
                    p_lo, p_hi = PRODUCT_PRICE_PER_UNIT[product]
                    price_per_unit = random.uniform(p_lo, p_hi)

                    # Jake's spike deals are bigger (large client)
                    if is_jake_spike and product == "Enterprise":
                        units = random.randint(3, 5)
                        price_per_unit = random.uniform(6000, 9000)

                    # Apply trajectory and regional multipliers to revenue too
                    revenue = units * price_per_unit * traj_mult * region_trend
                    # Add some noise (+-15%)
                    revenue *= random.uniform(0.85, 1.15)
                    revenue = round(revenue)

                    # Deal type distribution
                    if qi < 2:
                        deal_type = random.choices(DEAL_TYPES, weights=[0.6, 0.2, 0.2])[0]
                    else:
                        deal_type = random.choices(DEAL_TYPES, weights=[0.35, 0.35, 0.30])[0]

                    d = date(year, month, random.randint(1, 28))

                    rows.append({
                        "date": d.isoformat(),
                        "quarter": f"{year}-{q_label}",
                        "region": region,
                        "sales_rep": rep_name,
                        "product": product,
                        "deal_type": deal_type,
                        "units_sold": units,
                        "revenue": revenue,
                    })

    return rows


def add_dirt(rows):
    """Add realistic data quality issues."""
    # Misspell "John Martinez" in ~8 rows
    john_rows = [i for i, r in enumerate(rows) if r["sales_rep"] == "John Martinez"]
    for i in random.sample(john_rows, min(8, len(john_rows))):
        rows[i]["sales_rep"] = "Jonh Martinez"

    # Set revenue to empty in 4 random rows
    blanks = random.sample(range(len(rows)), 4)
    for i in blanks:
        rows[i]["revenue"] = ""

    # Duplicate one row
    dup = random.choice(rows).copy()
    rows.append(dup)

    return rows


def main():
    rows = generate_rows()
    rows = add_dirt(rows)
    random.shuffle(rows)

    out = "sales_data.csv"
    fields = ["date", "quarter", "region", "sales_rep", "product", "deal_type", "units_sold", "revenue"]
    with open(out, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {out}")

    # Quick sanity checks
    valid_revenue = [r["revenue"] for r in rows if r["revenue"] != ""]
    total_rev = sum(float(v) for v in valid_revenue)
    reps = set(r["sales_rep"] for r in rows)
    regions = set(r["region"] for r in rows)
    products = set(r["product"] for r in rows)
    print(f"Total revenue: ${total_rev:,.0f}")
    print(f"Reps: {len(reps)} ({', '.join(sorted(reps))})")
    print(f"Regions: {sorted(regions)}")
    print(f"Products: {sorted(products)}")
    print(f"Date range: {min(r['date'] for r in rows)} to {max(r['date'] for r in rows)}")

    # Check Jake spike
    jake_q3 = [r for r in rows if r["sales_rep"] == "Jake Chen"
                and r["quarter"] == "2025-Q3" and r["revenue"] != ""]
    jake_other = [r for r in rows if r["sales_rep"] == "Jake Chen"
                  and r["quarter"] != "2025-Q3" and r["revenue"] != ""]
    if jake_q3 and jake_other:
        avg_q3 = sum(float(r["revenue"]) for r in jake_q3) / len(jake_q3)
        avg_other = sum(float(r["revenue"]) for r in jake_other) / len(jake_other)
        print(f"Jake Chen avg deal: Q3-2025 ${avg_q3:,.0f} vs other ${avg_other:,.0f} ({len(jake_q3)} vs {len(jake_other)} deals)")

    # Check dirt
    jonh = [r for r in rows if r["sales_rep"] == "Jonh Martinez"]
    empty_rev = [r for r in rows if r["revenue"] == ""]
    print(f"Misspelled 'Jonh': {len(jonh)} rows")
    print(f"Missing revenue: {len(empty_rev)} rows")


if __name__ == "__main__":
    main()
