import pytest
import json
from tutorial.validator import PostgresPlanParser
from tutorial.models import PlanTree

def test_pg_parser_simple():
    pg_json = """
    [
      {
        "Plan": {
          "Node Type": "Seq Scan",
          "Parallel Aware": false,
          "Relation Name": "users",
          "Alias": "users",
          "Startup Cost": 0.00,
          "Total Cost": 2.25,
          "Plan Rows": 125,
          "Plan Width": 36
        }
      }
    ]
    """
    parser = PostgresPlanParser()
    plan = parser.parse(pg_json)

    assert plan.operation == "Seq Scan"
    assert plan.options["Relation Name"] == "users"
    assert len(plan.children) == 0

def test_pg_parser_nested():
    pg_json = """
    [
      {
        "Plan": {
          "Node Type": "Aggregate",
          "Strategy": "Plain",
          "Partial Mode": "Simple",
          "Parallel Aware": false,
          "Startup Cost": 2.56,
          "Total Cost": 2.57,
          "Plan Rows": 1,
          "Plan Width": 8,
          "Plans": [
            {
              "Node Type": "Seq Scan",
              "Parent Relationship": "Outer",
              "Parallel Aware": false,
              "Relation Name": "users",
              "Alias": "users",
              "Startup Cost": 0.00,
              "Total Cost": 2.25,
              "Plan Rows": 125,
              "Plan Width": 0
            }
          ]
        }
      }
    ]
    """
    parser = PostgresPlanParser()
    plan = parser.parse(pg_json)

    assert plan.operation == "Aggregate"
    assert len(plan.children) == 1
    assert plan.children[0].operation == "Seq Scan"
    assert plan.children[0].options["Relation Name"] == "users"

def test_pg_parser_invalid_json():
    parser = PostgresPlanParser()
    with pytest.raises(ValueError, match="Failed to decode JSON output"):
        parser.parse("not a json")

def test_pg_parser_empty_list():
    parser = PostgresPlanParser()
    with pytest.raises(ValueError, match="Invalid PostgreSQL EXPLAIN JSON format"):
        parser.parse("[]")
