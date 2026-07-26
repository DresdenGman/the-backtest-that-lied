# Evidence Schema

`data/evidence.json` is the authoritative publication layer for all research claims. Every displayed metric, collapse, exhibit, and pipeline scenario traces back to this file.

## Top-Level Keys

### project
| Field | Required | Description |
|-------|----------|-------------|
| title | Yes | Project title |
| subtitle | Yes | Project subtitle |
| author | Yes | Author name |
| date | Yes | Publication date |
| repository | Yes | GitHub repository URL |

### metrics
| Field | Required | Description |
|-------|----------|-------------|
| value | Yes | Numeric metric value |
| unit | Yes | Unit of measurement |
| experiment_id | Yes | Unique experiment identifier |
| artifact | Yes | Relative path to source data |
| status | Yes | validated, invalid, rejected, observed, benchmark |
| period | No | Evaluation period |
| universe | No | Stock universe description |
| protocol | No | Validation protocol |

### Status Rules
- **validated**: Passed all pre-registered gates
- **invalid**: Failed validation, contains leakage or error
- **rejected**: Hypothesis disproven by evidence
- **observed**: Measured but not a pass/fail criterion
- **benchmark**: Reference value, not a strategy result

### collapses
| Field | Required | Description |
|-------|----------|-------------|
| id | Yes | Unique collapse identifier |
| title | Yes | Display title |
| belief | Yes | Initial belief before intervention |
| intervention | Yes | What was changed |
| before | Yes | Before state (metric reference or description) |
| after | Yes | After state (metric reference or description) |
| interpretation | Yes | What the collapse means |
| rule_adopted | No | Research rule created from this finding |

### percentage decline formula
```
relative_decline = (before - after) / abs(before)
```
Comparisons MUST NOT be calculated when units are incompatible.

### exhibits
| Field | Required | Description |
|-------|----------|-------------|
| letter | Yes | Exhibit identifier (A-G) |
| title | Yes | Display title |
| belief | Yes | What was believed |
| problem | Yes (primary) | What was wrong |
| detection | Yes (primary) | How it was found |
| fix | Yes (primary) | How it was corrected |
| before_metric | Yes (primary) | Reference to metrics key |
| after_metric | Yes (primary) | Reference to metrics key |

### pipeline_scenarios
| Field | Required | Description |
|-------|----------|-------------|
| id | Yes | Unique scenario identifier |
| label | Yes | Display label |
| description | Yes | What the scenario represents |
| status | Yes | validated or invalid |
| display_metric | No | Metrics key for live value |
| display_value | No | Fallback display value |

## Comparator Rules

1. Never compare metrics with incompatible units
2. Invalid results must be visibly labeled
3. Percentage declines must be computed, not hardcoded
4. Missing artifact paths must trigger visible error states
