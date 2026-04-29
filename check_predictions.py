"""Quick script to check recent predictions"""
import sys
sys.path.insert(0, 'src')
from database import PredictionDatabase

db = PredictionDatabase('data/predictions.db')
preds = db.get_all_predictions(10)

print("\n" + "=" * 100)
print("RECENT PREDICTIONS")
print("=" * 100)
print(f"{'ID':<5} {'Type':<18} {'Prediction':<12} {'Confidence':<12} {'Risk Level':<15}")
print("-" * 100)

for p in preds:
    pred_type = p.get('prediction_type', 'manual')
    type_label = '🩺 Symptom' if pred_type == 'symptom' else '📊 Manual'
    risk = 'N/A'
    if p.get('risk_assessment'):
        risk = p['risk_assessment'].get('risk_level', 'N/A')
    
    print(f"#{p['id']:<4} {type_label:<18} {p['prediction_label']:<12} {p['confidence']*100:>6.1f}%      {risk:<15}")

print("-" * 100)
print(f"Total: {len(preds)} predictions")

# Count by type
symptom_count = sum(1 for p in preds if p.get('prediction_type') == 'symptom')
manual_count = len(preds) - symptom_count

print(f"\nBreakdown:")
print(f"  - Symptom-based: {symptom_count}")
print(f"  - Manual input:  {manual_count}")
print("=" * 100 + "\n")
