# Fraud Risk Engine: Problem Definition

## Business problem

Financial institutions must evaluate transactions quickly while balancing two competing risks:

1. Approving a fraudulent transaction can create financial loss.
2. Blocking a legitimate transaction can frustrate customers and interrupt valid activity.

The goal of this project is to estimate the probability that an individual transaction is fraudulent using information available at transaction time.

## Unit of observation

One row represents one transaction submitted for a fraud-risk decision.

A single account may generate multiple transactions, but each transaction receives its own prediction.

## Prediction target

The target is:

`is_fraud`

It is a binary variable:

- `1`: the transaction was fraudulent.
- `0`: the transaction was legitimate.

This is a binary classification problem.

## Prediction time

The prediction is generated when the transaction is submitted, before its final fraud outcome is known.

Only information available at or before that moment may be used as a model feature.

## Candidate features

Potential transaction-time features include:

- transaction amount;
- transaction hour;
- account age;
- number of recent transactions;
- distance from the customer's typical location;
- whether the device was previously observed;
- whether the transaction is international;
- merchant category.

## Potential leakage

The following variables would not be valid model features because they occur after the prediction decision:

- confirmed fraud investigation outcome;
- chargeback date;
- investigation resolution;
- reimbursement amount;
- account closure caused by the transaction;
- manual-review result completed after prediction.

Including these variables could produce excellent evaluation results while creating a model that cannot operate in the real world.

## Model output

The model will return a fraud probability between 0 and 1.

Example:

`fraud_probability = 0.82`

This means the model estimates an 82% probability of fraud based on the available features. It does not necessarily mean the final decision must be “fraud.”

A decision threshold will convert the probability into an operational action.

## Initial decision policy

The first version will use two simplified actions:

- `approve`: allow the transaction;
- `review`: send the transaction for additional review.

A later version could introduce separate approve, review, and decline thresholds.

## Error tradeoffs

### False positive

The model flags a legitimate transaction for review.

Possible consequences:

- customer friction;
- delayed purchase;
- manual-review cost;
- customer dissatisfaction;
- lost revenue.

### False negative

The model approves a fraudulent transaction.

Possible consequences:

- direct financial loss;
- reimbursement expense;
- investigation cost;
- regulatory risk;
- damage to customer trust.

False positives and false negatives do not necessarily have equal business costs.

## Evaluation strategy

Accuracy will not be the primary metric because fraud is expected to be uncommon.

The project will evaluate:

- precision;
- recall;
- F1 score;
- ROC AUC;
- precision-recall curve;
- average precision;
- confusion matrix;
- expected decision cost at different thresholds.

## Success criteria

The initial model should:

1. perform better than a naive baseline;
2. identify a meaningful share of fraudulent transactions;
3. keep legitimate transactions sent to review within a defensible range;
4. produce reproducible evaluation results;
5. expose its assumptions and limitations clearly;
6. support a configurable decision threshold.

These criteria are educational and illustrative because the project uses synthetic data rather than production financial data.

## Key limitation

Performance on synthetic data does not demonstrate performance against real fraud.

The project demonstrates modeling methodology, software design, evaluation discipline, and production-oriented implementation.