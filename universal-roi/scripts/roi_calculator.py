#!/usr/bin/env python3
"""Calculate equal-period incremental ROI ledgers; Python standard library only."""
import argparse
import json
import math
import sys
from pathlib import Path


def number(value, label, nonnegative=False):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{label}: expected a finite number")
    if nonnegative and value < 0:
        raise ValueError(f"{label}: must be nonnegative")
    return value


def keys(obj, allowed, required, label):
    if not isinstance(obj, dict):
        raise ValueError(f"{label}: expected an object")
    missing, extra = required - obj.keys(), obj.keys() - allowed
    if missing or extra:
        raise ValueError(f"{label}: missing {sorted(missing)}, unsupported {sorted(extra)}")


def label(value, field):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field}: expected a nonempty string")
    return value


def ledger(value, field, length=None):
    if not isinstance(value, list) or len(value) < 2:
        raise ValueError(f"{field}: expected t=0 and at least one future period")
    if length is not None and len(value) != length:
        raise ValueError(f"{field}: inconsistent period count")
    return [number(x, f"{field}[{i}]", True) for i, x in enumerate(value)]


def cumulative(values):
    total, result = 0, []
    for value in values:
        total += value
        result.append(total)
    return result


def calculate(data):
    fields = {"currency", "period", "baseline", "discount_rate_per_period", "scenarios"}
    keys(data, fields, {"currency", "period", "baseline", "scenarios"}, "input")
    for field in ("currency", "period", "baseline"):
        label(data[field], field)
    rate = data.get("discount_rate_per_period")
    if rate is not None:
        number(rate, "discount_rate_per_period")
        if rate <= -1:
            raise ValueError("discount_rate_per_period: must be greater than -1")
    scenarios = data["scenarios"]
    if not isinstance(scenarios, list) or not scenarios:
        raise ValueError("scenarios: expected a nonempty list")
    output, names, length, probabilities = [], set(), None, []
    scenario_fields = {"name", "cash_benefits", "cash_costs", "noncash_benefits",
                       "opportunity_costs", "hours", "probability", "probability_basis"}
    for scenario in scenarios:
        keys(scenario, scenario_fields, {"name", "cash_benefits", "cash_costs"}, "scenario")
        name = label(scenario["name"], "scenario.name")
        if name in names:
            raise ValueError(f"duplicate scenario name: {name}")
        names.add(name)
        benefits = ledger(scenario["cash_benefits"], f"{name}.cash_benefits", length)
        length = len(benefits)
        costs = ledger(scenario["cash_costs"], f"{name}.cash_costs", length)
        noncash = ledger(scenario.get("noncash_benefits", [0] * length), f"{name}.noncash_benefits", length)
        opportunity = ledger(scenario.get("opportunity_costs", [0] * length), f"{name}.opportunity_costs", length)
        hours = ledger(scenario["hours"], f"{name}.hours", length) if "hours" in scenario else None
        probability = scenario.get("probability")
        if probability is not None:
            number(probability, f"{name}.probability", True)
            if probability > 1:
                raise ValueError(f"{name}.probability: must be <= 1")
            label(scenario.get("probability_basis"), f"{name}.probability_basis")
        elif "probability_basis" in scenario:
            raise ValueError(f"{name}: probability_basis requires probability")
        probabilities.append(probability)
        net = [b - c for b, c in zip(benefits, costs)]
        economic = [n + b - c for n, b, c in zip(net, noncash, opportunity)]
        running = cumulative(net)
        tolerance = 1e-10 * max(1, sum(benefits), sum(costs))
        negative = [i for i, value in enumerate(running) if value < -tolerance]
        # Recovery refers to observed negative cumulative cash, at period endpoints.
        first_recovery = next((i for i in range(negative[0] + 1, length)
                               if running[i] >= -tolerance), None) if negative else None
        sustained = next((i for i in range(negative[-1] + 1, length)
                          if running[i] >= -tolerance), None) if negative else None
        cost_total = sum(costs)
        economic_cost = cost_total + sum(opportunity)
        warnings = []
        if rate is None:
            warnings.append("No discount rate supplied; NPV not calculated.")
        if cost_total == 0:
            warnings.append("Cash ROI undefined because total cash costs are zero.")
        if not negative:
            warnings.append("No negative cumulative cash at period endpoints; payback is not applicable. Intraperiod funding may still be needed.")
        elif sustained is None:
            warnings.append("No sustained payback within the modeled horizon.")
        if any(n != 0 for n in noncash + opportunity):
            warnings.append("Economic metrics depend on supplied noncash valuations; they are not cash returns.")
        present_value = lambda values: sum(v / (1 + rate) ** i for i, v in enumerate(values)) if rate is not None else None
        output.append({
            "name": name,
            "cash_benefits_total": sum(benefits),
            "cash_costs_total": cost_total,
            "net_cash_benefit": sum(net),
            "cash_roi_percent": 100 * sum(net) / cost_total if cost_total else None,
            "cash_npv": present_value(net),
            "net_economic_benefit": sum(economic),
            "economic_roi_percent": 100 * sum(economic) / economic_cost if economic_cost else None,
            "economic_npv": present_value(economic),
            "noncash_benefits_total": sum(noncash),
            "opportunity_costs_total": sum(opportunity),
            "hours_total": sum(hours) if hours is not None else None,
            "incremental_funding_gap_at_period_ends": max(0, -min(running)),
            "first_recovery_period": first_recovery,
            "sustained_payback_period_within_horizon": sustained,
            "payback_status": "not_applicable" if not negative else ("recovered_within_horizon" if sustained is not None else "not_recovered_within_horizon"),
            "net_cash_by_period": net,
            "cumulative_net_cash": running,
            "probability": probability,
            "probability_basis": scenario.get("probability_basis"),
            "warnings": warnings,
        })
    supplied = [p is not None for p in probabilities]
    if any(supplied) and not all(supplied):
        raise ValueError("Supply probabilities for every scenario or for none")
    expected = None
    if all(supplied):
        if not math.isclose(sum(probabilities), 1, rel_tol=0, abs_tol=1e-9):
            raise ValueError("Scenario probabilities must sum to 1; they are never auto-normalized")
        expected = {
            "net_cash_benefit": sum(p * s["net_cash_benefit"] for p, s in zip(probabilities, output)),
            "cash_npv": sum(p * s["cash_npv"] for p, s in zip(probabilities, output)) if rate is not None else None,
            "modeled_probability_of_negative_total_cash": sum(p for p, s in zip(probabilities, output) if s["net_cash_benefit"] < 0),
            "note": "Valid only if supplied scenarios are mutually exclusive and collectively exhaustive; supplied probabilities are not verified by this script."
        }
    return {"currency": data["currency"], "period": data["period"], "baseline": data["baseline"],
            "horizon_periods": length - 1, "discount_rate_per_period": rate,
            "roi_denominator": "Sum of incremental cash costs over the entire horizon; not initial investment or annualized return.",
            "timing": "Index 0 is now; later entries occur at equal-period ends. Funding gap excludes baseline funding and intraperiod timing.",
            "scenarios": output, "probability_weighted": expected}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.input.read_text(encoding="utf-8"))
        result = json.dumps(calculate(data), ensure_ascii=False, indent=2, allow_nan=False)
        if args.output:
            with args.output.open("x", encoding="utf-8") as file:
                file.write(result + "\n")
        else:
            print(result)
    except (OSError, ValueError, TypeError, OverflowError, ZeroDivisionError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
