import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

scenarios = [
    {
        "name": "Scenario 1: Muscle Gain (Male, 80kg, Active)",
        "payload": {
            "goal": "gain muscle",
            "body_metrics": "180cm 80kg",
            "activity_level": "active",
            "diet_type": "none",
            "allergies": "no",
            "allergy_items": "",
            "meals_per_day": 4,
            "medical_conditions": "none",
            "age": 25,
            "gender": "male"
        }
    },
    {
        "name": "Scenario 2: Weight Loss (Female, 80kg, Low Activity)",
        "payload": {
            "goal": "lose weight",
            "body_metrics": "170cm 80kg",
            "activity_level": "low",
            "diet_type": "vegetarian",
            "allergies": "yes",
            "allergy_items": "peanuts",
            "meals_per_day": 3,
            "medical_conditions": "none",
            "age": 30,
            "gender": "female"
        }
    },
    {
        "name": "Scenario 3: Keto & Dairy-Free (Male, 95kg, Moderate Activity)",
        "payload": {
            "goal": "lose weight",
            "body_metrics": "185cm 95kg",
            "activity_level": "moderate",
            "diet_type": "keto",
            "allergies": "yes",
            "allergy_items": "dairy",
            "meals_per_day": 3,
            "medical_conditions": "none",
            "age": 45,
            "gender": "male"
        }
    },
    {
        "name": "Scenario 4: High Protein Athlete (Male, 85kg, Active)",
        "payload": {
            "goal": "gain muscle",
            "body_metrics": "182cm 85kg",
            "activity_level": "active",
            "diet_type": "none",
            "allergies": "no",
            "allergy_items": "",
            "meals_per_day": 5,
            "medical_conditions": "none",
            "age": 22,
            "gender": "male"
        }
    },
    {
        "name": "Scenario 5: Vegan Weight Loss (Female, 70kg, Moderate)",
        "payload": {
            "goal": "lose weight",
            "body_metrics": "165cm 70kg",
            "activity_level": "moderate",
            "diet_type": "vegan",
            "allergies": "no",
            "allergy_items": "",
            "meals_per_day": 3,
            "medical_conditions": "none",
            "age": 28,
            "gender": "female"
        }
    }
]

def run_test():
    for scenario in scenarios:
        print(f"\n--- Running {scenario['name']} ---")
        try:
            response = requests.post(f"{BASE_URL}/generate-meal-plan", json=scenario['payload'])
            if response.status_code == 200:
                result = response.json()
                print("SUCCESS")
                meal_plan = result['meal_plan']
                summary = meal_plan['summary']
                breakdown = meal_plan['nutrition_breakdown']
                
                print(f"Target: {summary['target_calories']} kcal, {summary['target_protein_g']}g Protein")
                print(f"Actual: {breakdown['total_calories']} kcal, {breakdown['total_protein_g']}g Protein")
                
                diff_cal = abs(breakdown['total_calories'] - summary['target_calories'])
                diff_prot = abs(breakdown['total_protein_g'] - summary['target_protein_g'])
                
                print(f"Diff: {diff_cal} kcal, {diff_prot}g Protein")
                
                if diff_cal <= 100 and diff_prot <= 15:
                    print("RESULT: PASS (Within acceptable deviation)")
                else:
                    print("RESULT: MARGINAL (Outside tight tolerances)")
                
                # Check diet type compliance (basic check)
                diet_type = scenario['payload']['diet_type'].lower()
                if diet_type == "vegetarian":
                    meat_keywords = ["chicken", "beef", "pork", "steak", "fish", "salmon", "shrimp"]
                    meals_text = json.dumps(meal_plan['meals']).lower()
                    if any(kw in meals_text for kw in meat_keywords):
                        print("WARNING: Possible meat found in vegetarian plan!")
                
                print(f"\nMeals ({len(meal_plan['meals'])} total):")
                for meal in meal_plan['meals']:
                    print(f"- {meal['meal_name']}: {meal['meal_totals']['calories']} kcal")
                    for item in meal['items']:
                        print(f"  * {item['food']} ({item['portion']})")
            else:
                print(f"FAILED: Status {response.status_code}")
                try:
                    error_detail = response.json().get('message', response.text)
                    print(f"Error: {error_detail}")
                except:
                    print(f"Error: {response.text}")
        except Exception as e:
            print(f"ERROR: {str(e)}")
        
        # Add delay to avoid rate limiting
        import time
        time.sleep(2)

if __name__ == "__main__":
    run_test()
