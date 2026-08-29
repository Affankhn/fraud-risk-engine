# Fraud Risk Engine: Data Dictionary

## Dataset overview

One row represents one transaction submitted for a fraud-risk decision.

The first version of the project will use synthetic data so that the repository remains reproducible and does not expose private financial information.

## Columns

| Column | Type | Description | Example |
|---|---|---|---|
| `transaction_id` | string | Unique transaction identifier | `txn_000001` |
| `transaction_timestamp` | datetime | Time the transaction was submitted | `2026-01-15 14:32:00` |
| `transaction_amount` | float | Transaction amount in US dollars | `125.75` |
| `account_age_days` | integer | Number of days since the account was created | `420` |
| `transactions_last_hour` | integer | Number of transactions from the account during the preceding hour | `3` |
| `distance_from_home_km` | float | Distance between the transaction and the customer's typical location | `12.4` |
| `device_seen_before` | boolean | Whether the device has previously been associated with the account | `true` |
| `is_international` | boolean | Whether the transaction occurs outside the account's home country | `false` |
| `merchant_category` | category | General merchant classification | `grocery` |
| `hour_of_day` | integer | Hour extracted from the transaction timestamp | `14` |
| `is_fraud` | integer | Binary target: 1 for fraud, 0 for legitimate | `0` |

## Feature assumptions

### Transaction amount

Fraud risk may increase for unusually large transactions, but large amounts are not automatically fraudulent.

The synthetic generator should produce many ordinary transactions and fewer very large transactions. A right-skewed distribution is more realistic than a uniform distribution.

### Account age

New accounts may have greater risk because they have less established history.

Older accounts can still be compromised, so account age should influence fraud probability without determining it completely.

### Recent transaction velocity

A sudden sequence of transactions may indicate automated abuse or testing of stolen credentials.

Higher values should generally increase fraud probability.

### Distance from home

Transactions far from the customer's typical location may be unusual.

Distance alone is insufficient because legitimate customers travel.

### Device familiarity

A previously unseen device can increase risk, particularly when combined with other unusual behavior.

A new device should not automatically cause a fraud classification.

### International activity

International transactions may carry additional risk in this simplified dataset.

This feature must be interpreted carefully because international activity can be completely legitimate.

### Merchant category

Different merchant categories may have different synthetic risk levels.

The initial categories will be:

- `grocery`
- `travel`
- `electronics`
- `entertainment`
- `services`

### Hour of day

Very late-night or early-morning activity may have a different fraud rate from daytime transactions.

Time of day should be a weak signal rather than a decisive rule.

## Target generation

The synthetic target will be created probabilistically.

Each transaction will receive a fraud probability based on a combination of:

- transaction amount;
- account age;
- recent transaction velocity;
- distance from home;
- device familiarity;
- international activity;
- merchant category;
- time of day;
- random noise.

The target will then be sampled from that probability.

This means two transactions with identical features do not always need to receive identical outcomes.

## Expected target imbalance

Fraud should be uncommon.

The initial target fraud rate will be approximately 1% to 3% of transactions.

This creates a realistic rare-event classification problem and demonstrates why accuracy is insufficient.

## Invalid or impossible values

The data-validation layer should eventually reject or flag:

- negative transaction amounts;
- negative account age;
- negative transaction velocity;
- negative distance;
- an hour outside 0 through 23;
- unsupported merchant categories;
- missing transaction identifiers;
- duplicate transaction identifiers;
- target values other than 0 or 1.

## Leakage exclusions

The dataset will not include post-decision variables such as:

- chargeback outcome;
- investigation resolution;
- reimbursement amount;
- manual-review decision;
- account closure following the transaction.

## Limitations

The relationships in this dataset are designed by the project author. They do not represent actual fraud patterns or the behavior of any financial institution.

Model performance will demonstrate whether the pipeline can recover synthetic patterns—not whether the model can detect real-world fraud.