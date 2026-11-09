# Held Out Evaluation

This report records real local service calls against the frozen evaluation corpus. It does not claim that a score proves authorship.

## Run Details

Corpus: `evaluation/held_out.jsonl`

Corpus SHA256: `8bf7d68e194267c55c8cc7571f6ca16f18b36e50852dd6416705bc5182577f39`

Service: `http://127.0.0.1:5064`

Trials: 3

## Results

| Trial | Accepted | Human passages called AI | Human median | AI median | Difference | Criterion 1 | Criterion 2 |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| 1 | 40/40 | 0 | 0.461710 | 0.318185 | -0.143525 | pass | not met |
| 2 | 40/40 | 0 | 0.461710 | 0.318185 | -0.143525 | pass | not met |
| 3 | 40/40 | 0 | 0.461710 | 0.318185 | -0.143525 | pass | not met |

Criterion 1 passes only when all 20 human passages receive valid responses and no more than one is labelled AI.

Criterion 2 passes only when all 40 passages receive valid responses and the AI median is at least 0.20 above the human median.

Criterion 1 overall: pass.

Criterion 2 overall: not met.

## Exact Trial Data

### Trial 1

```json
{
  "trial": 1,
  "accepted": 40,
  "human_false_accusations": 0,
  "false_accusation_ids": [],
  "human_median": 0.46171,
  "ai_median": 0.318185,
  "median_difference": -0.143525,
  "criterion_1_pass": true,
  "criterion_2_pass": false,
  "rows": [
    {
      "id": "human_01",
      "origin": "human",
      "topic": "fantasy curiosity",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.503378,
      "model_score": 0.5193,
      "style_score": 0.5,
      "error": null
    },
    {
      "id": "human_02",
      "origin": "human",
      "topic": "time travel science",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.36728,
      "model_score": 0.3017,
      "style_score": 0.5203,
      "error": null
    },
    {
      "id": "human_03",
      "origin": "human",
      "topic": "ambition and study",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.45041,
      "model_score": 0.4121,
      "style_score": 0.5398,
      "error": null
    },
    {
      "id": "human_04",
      "origin": "human",
      "topic": "society and wealth",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.51232,
      "model_score": 0.5911,
      "style_score": 0.3285,
      "error": null
    },
    {
      "id": "human_05",
      "origin": "human",
      "topic": "schoolroom memory",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.38776,
      "model_score": 0.3505,
      "style_score": 0.4747,
      "error": null
    },
    {
      "id": "human_06",
      "origin": "human",
      "topic": "detective observation",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.36381,
      "model_score": 0.3801,
      "style_score": 0.3258,
      "error": null
    },
    {
      "id": "human_07",
      "origin": "human",
      "topic": "sea adventure",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.46353,
      "model_score": 0.2916,
      "style_score": 0.5,
      "error": null
    },
    {
      "id": "human_08",
      "origin": "human",
      "topic": "publishing gratitude",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.460345,
      "model_score": 0.2734,
      "style_score": 0.5,
      "error": null
    },
    {
      "id": "human_09",
      "origin": "human",
      "topic": "family sacrifice",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.42718,
      "model_score": 0.4663,
      "style_score": 0.3359,
      "error": null
    },
    {
      "id": "human_10",
      "origin": "human",
      "topic": "children fantasy",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.44883,
      "model_score": 0.2076,
      "style_score": 0.5,
      "error": null
    },
    {
      "id": "human_11",
      "origin": "human",
      "topic": "childhood growing up",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.51913,
      "model_score": 0.5593,
      "style_score": 0.4254,
      "error": null
    },
    {
      "id": "human_12",
      "origin": "human",
      "topic": "garden mystery",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.44438,
      "model_score": 0.4556,
      "style_score": 0.4182,
      "error": null
    },
    {
      "id": "human_13",
      "origin": "human",
      "topic": "rural community",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.450842,
      "model_score": 0.2191,
      "style_score": 0.5,
      "error": null
    },
    {
      "id": "human_14",
      "origin": "human",
      "topic": "historical documents",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.32074,
      "model_score": 0.2401,
      "style_score": 0.5089,
      "error": null
    },
    {
      "id": "human_15",
      "origin": "human",
      "topic": "art portrait",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.515208,
      "model_score": 0.5869,
      "style_score": 0.5,
      "error": null
    },
    {
      "id": "human_16",
      "origin": "human",
      "topic": "historical contrast",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.579975,
      "model_score": 0.957,
      "style_score": 0.5,
      "error": null
    },
    {
      "id": "human_17",
      "origin": "human",
      "topic": "language and dialect",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.478527,
      "model_score": 0.3773,
      "style_score": 0.5,
      "error": null
    },
    {
      "id": "human_18",
      "origin": "human",
      "topic": "dogs and north",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.463075,
      "model_score": 0.289,
      "style_score": 0.5,
      "error": null
    },
    {
      "id": "human_19",
      "origin": "human",
      "topic": "palace reflection",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.47179,
      "model_score": 0.3388,
      "style_score": 0.5,
      "error": null
    },
    {
      "id": "human_20",
      "origin": "human",
      "topic": "civic history",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.49746,
      "model_score": 0.4509,
      "style_score": 0.6061,
      "error": null
    },
    {
      "id": "ai_01",
      "origin": "ai",
      "topic": "fantasy curiosity",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.50683,
      "model_score": 0.4573,
      "style_score": 0.6224,
      "error": null
    },
    {
      "id": "ai_02",
      "origin": "ai",
      "topic": "time travel science",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.29998,
      "model_score": 0.3019,
      "style_score": 0.2955,
      "error": null
    },
    {
      "id": "ai_03",
      "origin": "ai",
      "topic": "ambition and study",
      "status": 201,
      "guess": "human",
      "combined_score": 0.23838,
      "model_score": 0.1635,
      "style_score": 0.4131,
      "error": null
    },
    {
      "id": "ai_04",
      "origin": "ai",
      "topic": "society and wealth",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.42451,
      "model_score": 0.4213,
      "style_score": 0.432,
      "error": null
    },
    {
      "id": "ai_05",
      "origin": "ai",
      "topic": "schoolroom memory",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.35515,
      "model_score": 0.2983,
      "style_score": 0.4878,
      "error": null
    },
    {
      "id": "ai_06",
      "origin": "ai",
      "topic": "detective observation",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.41866,
      "model_score": 0.3655,
      "style_score": 0.5427,
      "error": null
    },
    {
      "id": "ai_07",
      "origin": "ai",
      "topic": "sea adventure",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.45896,
      "model_score": 0.4403,
      "style_score": 0.5025,
      "error": null
    },
    {
      "id": "ai_08",
      "origin": "ai",
      "topic": "publishing gratitude",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.28213,
      "model_score": 0.2416,
      "style_score": 0.3767,
      "error": null
    },
    {
      "id": "ai_09",
      "origin": "ai",
      "topic": "family sacrifice",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.25563,
      "model_score": 0.2121,
      "style_score": 0.3572,
      "error": null
    },
    {
      "id": "ai_10",
      "origin": "ai",
      "topic": "children fantasy",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.29382,
      "model_score": 0.2112,
      "style_score": 0.4866,
      "error": null
    },
    {
      "id": "ai_11",
      "origin": "ai",
      "topic": "childhood growing up",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.44539,
      "model_score": 0.4003,
      "style_score": 0.5506,
      "error": null
    },
    {
      "id": "ai_12",
      "origin": "ai",
      "topic": "garden mystery",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.44229,
      "model_score": 0.387,
      "style_score": 0.5713,
      "error": null
    },
    {
      "id": "ai_13",
      "origin": "ai",
      "topic": "rural community",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.31436,
      "model_score": 0.2609,
      "style_score": 0.4391,
      "error": null
    },
    {
      "id": "ai_14",
      "origin": "ai",
      "topic": "historical documents",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.36665,
      "model_score": 0.3254,
      "style_score": 0.4629,
      "error": null
    },
    {
      "id": "ai_15",
      "origin": "ai",
      "topic": "art portrait",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.35467,
      "model_score": 0.334,
      "style_score": 0.4029,
      "error": null
    },
    {
      "id": "ai_16",
      "origin": "ai",
      "topic": "historical contrast",
      "status": 201,
      "guess": "human",
      "combined_score": 0.19741,
      "model_score": 0.1021,
      "style_score": 0.4198,
      "error": null
    },
    {
      "id": "ai_17",
      "origin": "ai",
      "topic": "language and dialect",
      "status": 201,
      "guess": "human",
      "combined_score": 0.2444,
      "model_score": 0.206,
      "style_score": 0.334,
      "error": null
    },
    {
      "id": "ai_18",
      "origin": "ai",
      "topic": "dogs and north",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.28528,
      "model_score": 0.2005,
      "style_score": 0.4831,
      "error": null
    },
    {
      "id": "ai_19",
      "origin": "ai",
      "topic": "palace reflection",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.30777,
      "model_score": 0.2454,
      "style_score": 0.4533,
      "error": null
    },
    {
      "id": "ai_20",
      "origin": "ai",
      "topic": "civic history",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.32201,
      "model_score": 0.2282,
      "style_score": 0.5409,
      "error": null
    }
  ]
}
```

### Trial 2

```json
{
  "trial": 2,
  "accepted": 40,
  "human_false_accusations": 0,
  "false_accusation_ids": [],
  "human_median": 0.46171,
  "ai_median": 0.318185,
  "median_difference": -0.143525,
  "criterion_1_pass": true,
  "criterion_2_pass": false,
  "rows": [
    {
      "id": "human_01",
      "origin": "human",
      "topic": "fantasy curiosity",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.503378,
      "model_score": 0.5193,
      "style_score": 0.5,
      "error": null
    },
    {
      "id": "human_02",
      "origin": "human",
      "topic": "time travel science",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.36728,
      "model_score": 0.3017,
      "style_score": 0.5203,
      "error": null
    },
    {
      "id": "human_03",
      "origin": "human",
      "topic": "ambition and study",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.45041,
      "model_score": 0.4121,
      "style_score": 0.5398,
      "error": null
    },
    {
      "id": "human_04",
      "origin": "human",
      "topic": "society and wealth",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.51232,
      "model_score": 0.5911,
      "style_score": 0.3285,
      "error": null
    },
    {
      "id": "human_05",
      "origin": "human",
      "topic": "schoolroom memory",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.38776,
      "model_score": 0.3505,
      "style_score": 0.4747,
      "error": null
    },
    {
      "id": "human_06",
      "origin": "human",
      "topic": "detective observation",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.36381,
      "model_score": 0.3801,
      "style_score": 0.3258,
      "error": null
    },
    {
      "id": "human_07",
      "origin": "human",
      "topic": "sea adventure",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.46353,
      "model_score": 0.2916,
      "style_score": 0.5,
      "error": null
    },
    {
      "id": "human_08",
      "origin": "human",
      "topic": "publishing gratitude",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.460345,
      "model_score": 0.2734,
      "style_score": 0.5,
      "error": null
    },
    {
      "id": "human_09",
      "origin": "human",
      "topic": "family sacrifice",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.42718,
      "model_score": 0.4663,
      "style_score": 0.3359,
      "error": null
    },
    {
      "id": "human_10",
      "origin": "human",
      "topic": "children fantasy",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.44883,
      "model_score": 0.2076,
      "style_score": 0.5,
      "error": null
    },
    {
      "id": "human_11",
      "origin": "human",
      "topic": "childhood growing up",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.51913,
      "model_score": 0.5593,
      "style_score": 0.4254,
      "error": null
    },
    {
      "id": "human_12",
      "origin": "human",
      "topic": "garden mystery",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.44438,
      "model_score": 0.4556,
      "style_score": 0.4182,
      "error": null
    },
    {
      "id": "human_13",
      "origin": "human",
      "topic": "rural community",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.450842,
      "model_score": 0.2191,
      "style_score": 0.5,
      "error": null
    },
    {
      "id": "human_14",
      "origin": "human",
      "topic": "historical documents",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.32074,
      "model_score": 0.2401,
      "style_score": 0.5089,
      "error": null
    },
    {
      "id": "human_15",
      "origin": "human",
      "topic": "art portrait",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.515208,
      "model_score": 0.5869,
      "style_score": 0.5,
      "error": null
    },
    {
      "id": "human_16",
      "origin": "human",
      "topic": "historical contrast",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.579975,
      "model_score": 0.957,
      "style_score": 0.5,
      "error": null
    },
    {
      "id": "human_17",
      "origin": "human",
      "topic": "language and dialect",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.478527,
      "model_score": 0.3773,
      "style_score": 0.5,
      "error": null
    },
    {
      "id": "human_18",
      "origin": "human",
      "topic": "dogs and north",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.463075,
      "model_score": 0.289,
      "style_score": 0.5,
      "error": null
    },
    {
      "id": "human_19",
      "origin": "human",
      "topic": "palace reflection",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.47179,
      "model_score": 0.3388,
      "style_score": 0.5,
      "error": null
    },
    {
      "id": "human_20",
      "origin": "human",
      "topic": "civic history",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.49746,
      "model_score": 0.4509,
      "style_score": 0.6061,
      "error": null
    },
    {
      "id": "ai_01",
      "origin": "ai",
      "topic": "fantasy curiosity",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.50683,
      "model_score": 0.4573,
      "style_score": 0.6224,
      "error": null
    },
    {
      "id": "ai_02",
      "origin": "ai",
      "topic": "time travel science",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.29998,
      "model_score": 0.3019,
      "style_score": 0.2955,
      "error": null
    },
    {
      "id": "ai_03",
      "origin": "ai",
      "topic": "ambition and study",
      "status": 201,
      "guess": "human",
      "combined_score": 0.23838,
      "model_score": 0.1635,
      "style_score": 0.4131,
      "error": null
    },
    {
      "id": "ai_04",
      "origin": "ai",
      "topic": "society and wealth",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.42451,
      "model_score": 0.4213,
      "style_score": 0.432,
      "error": null
    },
    {
      "id": "ai_05",
      "origin": "ai",
      "topic": "schoolroom memory",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.35515,
      "model_score": 0.2983,
      "style_score": 0.4878,
      "error": null
    },
    {
      "id": "ai_06",
      "origin": "ai",
      "topic": "detective observation",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.41866,
      "model_score": 0.3655,
      "style_score": 0.5427,
      "error": null
    },
    {
      "id": "ai_07",
      "origin": "ai",
      "topic": "sea adventure",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.45896,
      "model_score": 0.4403,
      "style_score": 0.5025,
      "error": null
    },
    {
      "id": "ai_08",
      "origin": "ai",
      "topic": "publishing gratitude",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.28213,
      "model_score": 0.2416,
      "style_score": 0.3767,
      "error": null
    },
    {
      "id": "ai_09",
      "origin": "ai",
      "topic": "family sacrifice",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.25563,
      "model_score": 0.2121,
      "style_score": 0.3572,
      "error": null
    },
    {
      "id": "ai_10",
      "origin": "ai",
      "topic": "children fantasy",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.29382,
      "model_score": 0.2112,
      "style_score": 0.4866,
      "error": null
    },
    {
      "id": "ai_11",
      "origin": "ai",
      "topic": "childhood growing up",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.44539,
      "model_score": 0.4003,
      "style_score": 0.5506,
      "error": null
    },
    {
      "id": "ai_12",
      "origin": "ai",
      "topic": "garden mystery",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.44229,
      "model_score": 0.387,
      "style_score": 0.5713,
      "error": null
    },
    {
      "id": "ai_13",
      "origin": "ai",
      "topic": "rural community",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.31436,
      "model_score": 0.2609,
      "style_score": 0.4391,
      "error": null
    },
    {
      "id": "ai_14",
      "origin": "ai",
      "topic": "historical documents",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.36665,
      "model_score": 0.3254,
      "style_score": 0.4629,
      "error": null
    },
    {
      "id": "ai_15",
      "origin": "ai",
      "topic": "art portrait",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.35467,
      "model_score": 0.334,
      "style_score": 0.4029,
      "error": null
    },
    {
      "id": "ai_16",
      "origin": "ai",
      "topic": "historical contrast",
      "status": 201,
      "guess": "human",
      "combined_score": 0.19741,
      "model_score": 0.1021,
      "style_score": 0.4198,
      "error": null
    },
    {
      "id": "ai_17",
      "origin": "ai",
      "topic": "language and dialect",
      "status": 201,
      "guess": "human",
      "combined_score": 0.2444,
      "model_score": 0.206,
      "style_score": 0.334,
      "error": null
    },
    {
      "id": "ai_18",
      "origin": "ai",
      "topic": "dogs and north",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.28528,
      "model_score": 0.2005,
      "style_score": 0.4831,
      "error": null
    },
    {
      "id": "ai_19",
      "origin": "ai",
      "topic": "palace reflection",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.30777,
      "model_score": 0.2454,
      "style_score": 0.4533,
      "error": null
    },
    {
      "id": "ai_20",
      "origin": "ai",
      "topic": "civic history",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.32201,
      "model_score": 0.2282,
      "style_score": 0.5409,
      "error": null
    }
  ]
}
```

### Trial 3

```json
{
  "trial": 3,
  "accepted": 40,
  "human_false_accusations": 0,
  "false_accusation_ids": [],
  "human_median": 0.46171,
  "ai_median": 0.318185,
  "median_difference": -0.143525,
  "criterion_1_pass": true,
  "criterion_2_pass": false,
  "rows": [
    {
      "id": "human_01",
      "origin": "human",
      "topic": "fantasy curiosity",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.503378,
      "model_score": 0.5193,
      "style_score": 0.5,
      "error": null
    },
    {
      "id": "human_02",
      "origin": "human",
      "topic": "time travel science",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.36728,
      "model_score": 0.3017,
      "style_score": 0.5203,
      "error": null
    },
    {
      "id": "human_03",
      "origin": "human",
      "topic": "ambition and study",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.45041,
      "model_score": 0.4121,
      "style_score": 0.5398,
      "error": null
    },
    {
      "id": "human_04",
      "origin": "human",
      "topic": "society and wealth",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.51232,
      "model_score": 0.5911,
      "style_score": 0.3285,
      "error": null
    },
    {
      "id": "human_05",
      "origin": "human",
      "topic": "schoolroom memory",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.38776,
      "model_score": 0.3505,
      "style_score": 0.4747,
      "error": null
    },
    {
      "id": "human_06",
      "origin": "human",
      "topic": "detective observation",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.36381,
      "model_score": 0.3801,
      "style_score": 0.3258,
      "error": null
    },
    {
      "id": "human_07",
      "origin": "human",
      "topic": "sea adventure",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.46353,
      "model_score": 0.2916,
      "style_score": 0.5,
      "error": null
    },
    {
      "id": "human_08",
      "origin": "human",
      "topic": "publishing gratitude",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.460345,
      "model_score": 0.2734,
      "style_score": 0.5,
      "error": null
    },
    {
      "id": "human_09",
      "origin": "human",
      "topic": "family sacrifice",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.42718,
      "model_score": 0.4663,
      "style_score": 0.3359,
      "error": null
    },
    {
      "id": "human_10",
      "origin": "human",
      "topic": "children fantasy",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.44883,
      "model_score": 0.2076,
      "style_score": 0.5,
      "error": null
    },
    {
      "id": "human_11",
      "origin": "human",
      "topic": "childhood growing up",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.51913,
      "model_score": 0.5593,
      "style_score": 0.4254,
      "error": null
    },
    {
      "id": "human_12",
      "origin": "human",
      "topic": "garden mystery",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.44438,
      "model_score": 0.4556,
      "style_score": 0.4182,
      "error": null
    },
    {
      "id": "human_13",
      "origin": "human",
      "topic": "rural community",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.450842,
      "model_score": 0.2191,
      "style_score": 0.5,
      "error": null
    },
    {
      "id": "human_14",
      "origin": "human",
      "topic": "historical documents",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.32074,
      "model_score": 0.2401,
      "style_score": 0.5089,
      "error": null
    },
    {
      "id": "human_15",
      "origin": "human",
      "topic": "art portrait",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.515208,
      "model_score": 0.5869,
      "style_score": 0.5,
      "error": null
    },
    {
      "id": "human_16",
      "origin": "human",
      "topic": "historical contrast",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.579975,
      "model_score": 0.957,
      "style_score": 0.5,
      "error": null
    },
    {
      "id": "human_17",
      "origin": "human",
      "topic": "language and dialect",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.478527,
      "model_score": 0.3773,
      "style_score": 0.5,
      "error": null
    },
    {
      "id": "human_18",
      "origin": "human",
      "topic": "dogs and north",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.463075,
      "model_score": 0.289,
      "style_score": 0.5,
      "error": null
    },
    {
      "id": "human_19",
      "origin": "human",
      "topic": "palace reflection",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.47179,
      "model_score": 0.3388,
      "style_score": 0.5,
      "error": null
    },
    {
      "id": "human_20",
      "origin": "human",
      "topic": "civic history",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.49746,
      "model_score": 0.4509,
      "style_score": 0.6061,
      "error": null
    },
    {
      "id": "ai_01",
      "origin": "ai",
      "topic": "fantasy curiosity",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.50683,
      "model_score": 0.4573,
      "style_score": 0.6224,
      "error": null
    },
    {
      "id": "ai_02",
      "origin": "ai",
      "topic": "time travel science",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.29998,
      "model_score": 0.3019,
      "style_score": 0.2955,
      "error": null
    },
    {
      "id": "ai_03",
      "origin": "ai",
      "topic": "ambition and study",
      "status": 201,
      "guess": "human",
      "combined_score": 0.23838,
      "model_score": 0.1635,
      "style_score": 0.4131,
      "error": null
    },
    {
      "id": "ai_04",
      "origin": "ai",
      "topic": "society and wealth",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.42451,
      "model_score": 0.4213,
      "style_score": 0.432,
      "error": null
    },
    {
      "id": "ai_05",
      "origin": "ai",
      "topic": "schoolroom memory",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.35515,
      "model_score": 0.2983,
      "style_score": 0.4878,
      "error": null
    },
    {
      "id": "ai_06",
      "origin": "ai",
      "topic": "detective observation",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.41866,
      "model_score": 0.3655,
      "style_score": 0.5427,
      "error": null
    },
    {
      "id": "ai_07",
      "origin": "ai",
      "topic": "sea adventure",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.45896,
      "model_score": 0.4403,
      "style_score": 0.5025,
      "error": null
    },
    {
      "id": "ai_08",
      "origin": "ai",
      "topic": "publishing gratitude",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.28213,
      "model_score": 0.2416,
      "style_score": 0.3767,
      "error": null
    },
    {
      "id": "ai_09",
      "origin": "ai",
      "topic": "family sacrifice",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.25563,
      "model_score": 0.2121,
      "style_score": 0.3572,
      "error": null
    },
    {
      "id": "ai_10",
      "origin": "ai",
      "topic": "children fantasy",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.29382,
      "model_score": 0.2112,
      "style_score": 0.4866,
      "error": null
    },
    {
      "id": "ai_11",
      "origin": "ai",
      "topic": "childhood growing up",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.44539,
      "model_score": 0.4003,
      "style_score": 0.5506,
      "error": null
    },
    {
      "id": "ai_12",
      "origin": "ai",
      "topic": "garden mystery",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.44229,
      "model_score": 0.387,
      "style_score": 0.5713,
      "error": null
    },
    {
      "id": "ai_13",
      "origin": "ai",
      "topic": "rural community",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.31436,
      "model_score": 0.2609,
      "style_score": 0.4391,
      "error": null
    },
    {
      "id": "ai_14",
      "origin": "ai",
      "topic": "historical documents",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.36665,
      "model_score": 0.3254,
      "style_score": 0.4629,
      "error": null
    },
    {
      "id": "ai_15",
      "origin": "ai",
      "topic": "art portrait",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.35467,
      "model_score": 0.334,
      "style_score": 0.4029,
      "error": null
    },
    {
      "id": "ai_16",
      "origin": "ai",
      "topic": "historical contrast",
      "status": 201,
      "guess": "human",
      "combined_score": 0.19741,
      "model_score": 0.1021,
      "style_score": 0.4198,
      "error": null
    },
    {
      "id": "ai_17",
      "origin": "ai",
      "topic": "language and dialect",
      "status": 201,
      "guess": "human",
      "combined_score": 0.2444,
      "model_score": 0.206,
      "style_score": 0.334,
      "error": null
    },
    {
      "id": "ai_18",
      "origin": "ai",
      "topic": "dogs and north",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.28528,
      "model_score": 0.2005,
      "style_score": 0.4831,
      "error": null
    },
    {
      "id": "ai_19",
      "origin": "ai",
      "topic": "palace reflection",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.30777,
      "model_score": 0.2454,
      "style_score": 0.4533,
      "error": null
    },
    {
      "id": "ai_20",
      "origin": "ai",
      "topic": "civic history",
      "status": 201,
      "guess": "unsure",
      "combined_score": 0.32201,
      "model_score": 0.2282,
      "style_score": 0.5409,
      "error": null
    }
  ]
}
```
