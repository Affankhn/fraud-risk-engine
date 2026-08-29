import argparse
from pathlib import Path

import numpy as np
import pandas as pd

MERCHANT_CATEGORIES = [
    "grocery",
    "travel",
    "electronics",
    "entertainment",
    "services",
]


def generate_transactions(
    number_of_rows: int = 10_000,
    random_seed: int = 42,
) -> pd.DataFrame:
    """Generate reproducible synthetic transaction data."""

    if number_of_rows <= 0:
        raise ValueError("number_of_rows must be greater than zero")

    random_generator = np.random.default_rng(random_seed)

    # Generate timestamps across one calendar year.
    start_date = pd.Timestamp("2025-01-01", tz="UTC")

    minutes_in_year = 365 * 24 * 60

    random_minutes = random_generator.integers(
        low=0,
        high=minutes_in_year,
        size=number_of_rows,
    )

    transaction_timestamps = start_date + pd.to_timedelta(
        random_minutes,
        unit="m",
    )

    hour_of_day = pd.DatetimeIndex(transaction_timestamps).hour.to_numpy()

    # Most transactions are moderate, while a small number are large.
    transaction_amount = random_generator.lognormal(
        mean=4.0,
        sigma=1.0,
        size=number_of_rows,
    )

    transaction_amount = np.round(transaction_amount, 2)

    # Account age ranges from new accounts to approximately ten years.
    account_age_days = random_generator.integers(
        low=0,
        high=3650,
        size=number_of_rows,
    )

    # Most accounts have few transactions within the preceding hour.
    transactions_last_hour = random_generator.poisson(
        lam=2.0,
        size=number_of_rows,
    )

    # Most transactions occur near home, with a long tail of distant activity.
    distance_from_home_km = random_generator.exponential(
        scale=35.0,
        size=number_of_rows,
    )

    distance_from_home_km = np.round(distance_from_home_km, 2)

    # Approximately 86% of transactions use a previously observed device.
    device_seen_before = random_generator.random(number_of_rows) < 0.86

    # Approximately 8% of transactions are international.
    is_international = random_generator.random(number_of_rows) < 0.08

    merchant_category = random_generator.choice(
        MERCHANT_CATEGORIES,
        size=number_of_rows,
        p=[0.34, 0.12, 0.18, 0.16, 0.20],
    )

    # Late-night activity is treated as a modest synthetic risk signal.
    is_late_night = ((hour_of_day <= 4) | (hour_of_day >= 23)).astype(int)

    category_risk = np.select(
        condlist=[
            merchant_category == "electronics",
            merchant_category == "travel",
        ],
        choicelist=[
            0.85,
            0.55,
        ],
        default=0.0,
    )

    # Combine feature effects on the log-odds scale.
    fraud_log_odds = (
        -5.7
        + 0.0045 * np.minimum(transaction_amount, 2500)
        - 0.0011 * np.minimum(account_age_days, 1500)
        + 0.31 * transactions_last_hour
        + 0.004 * np.minimum(distance_from_home_km, 1000)
        + 1.05 * (~device_seen_before)
        + 0.95 * is_international
        + 0.55 * is_late_night
        + category_risk
        + random_generator.normal(
            loc=0.0,
            scale=0.55,
            size=number_of_rows,
        )
    )

    # Convert log-odds into probabilities between 0 and 1.
    fraud_probability = 1 / (1 + np.exp(-fraud_log_odds))

    # Sample a binary outcome from each transaction's probability.
    is_fraud = random_generator.binomial(
        n=1,
        p=fraud_probability,
    )

    transactions = pd.DataFrame(
        {
            "transaction_timestamp": transaction_timestamps,
            "transaction_amount": transaction_amount,
            "account_age_days": account_age_days,
            "transactions_last_hour": transactions_last_hour,
            "distance_from_home_km": distance_from_home_km,
            "device_seen_before": device_seen_before,
            "is_international": is_international,
            "merchant_category": merchant_category,
            "hour_of_day": hour_of_day,
            "is_fraud": is_fraud,
        }
    )

    transactions = transactions.sort_values("transaction_timestamp").reset_index(
        drop=True
    )

    transactions.insert(
        0,
        "transaction_id",
        [
            f"txn_{row_number:08d}"
            for row_number in range(1, len(transactions) + 1)
        ],
    )

    return transactions


def save_transactions(
    transactions: pd.DataFrame,
    output_path: Path,
) -> None:
    """Save transactions to a CSV file."""

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    transactions.to_csv(
        output_path,
        index=False,
    )


def main() -> None:
    """Run the synthetic-data generator from the command line."""

    parser = argparse.ArgumentParser(
        description="Generate synthetic fraud transaction data."
    )

    parser.add_argument(
        "--rows",
        type=int,
        default=10_000,
        help="Number of transactions to generate.",
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed used for reproducibility.",
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/processed/transactions.csv"),
        help="Destination CSV path.",
    )

    arguments = parser.parse_args()

    transactions = generate_transactions(
        number_of_rows=arguments.rows,
        random_seed=arguments.seed,
    )

    save_transactions(
        transactions=transactions,
        output_path=arguments.output,
    )

    fraud_rate = transactions["is_fraud"].mean()

    print(f"Created {len(transactions):,} transactions at {arguments.output}")

    print(f"Fraud rate: {fraud_rate:.2%}")


if __name__ == "__main__":
    main()
