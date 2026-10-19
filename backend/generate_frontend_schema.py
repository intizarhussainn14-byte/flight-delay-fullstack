import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

metadata = json.loads(
    (ROOT / "models/model_metadata.json").read_text(encoding="utf-8")
)
sample = json.loads(
    (ROOT / "backend/test_payload.json").read_text(encoding="utf-8")
)

numeric = set(metadata["numeric_features"])

fields = [
    {
        "name": name,
        "label": name.replace("_", " "),
        "kind": "number" if name in numeric else "text",
    }
    for name in metadata["features"]
]

content = """// Generated from the trained model's metadata.
export interface Feature {
  name: string;
  label: string;
  kind: 'number' | 'text';
}

export const FEATURES: Feature[] = FIELDS_PLACEHOLDER;

export const SAMPLE: Record<string, string | number> = SAMPLE_PLACEHOLDER;
"""

content = content.replace(
    "FIELDS_PLACEHOLDER", json.dumps(fields, indent=2)
).replace(
    "SAMPLE_PLACEHOLDER", json.dumps(sample, indent=2)
)

output = ROOT / "frontend/src/app/feature-schema.ts"
output.write_text(content, encoding="utf-8")

print("Saved:", output)
print("Fields:", len(fields))
print("PASS: frontend schema generated")