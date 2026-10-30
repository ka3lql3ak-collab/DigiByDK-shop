# Get Fit With Me — product structure, programs and Stan store copy.
# Long-form chapters live in guides/*.md, exercise technique in library.py.
# Edit, then run:  python3 getfitwithme/_build/build.py

COACH = "Danielle Dawson"
BRAND = "Get Fit With Me"
HANDLE = "@getfitwithme"  # swap for your real handle
SITE = "https://ka3lql3ak-collab.github.io/DigiByDK-shop/getfitwithme"

STORE = {
    "bio": "Online fitness coach helping women get strong, build their glutes and walk into the gym with confidence. "
           "Evidence-based programs, nutrition guides and 1:1 coaching.",
    "tagline": "Lift heavy. Eat well. Show up for yourself.",
}

DISCLAIMER = ("This program is for educational purposes and is not medical advice. Consult your doctor before starting a new "
              "exercise or nutrition plan, especially if you are pregnant, injured or have a medical condition. Stop any exercise that causes pain.")


# ---------------------------------------------------------------- programs
def build_program(days, phases):
    """days: [(name, focus, [(exercise, role, per_side)])]; phases: [{name, phase, note, scheme:{role:(sets, reps, rest, rir)}}]"""
    weeks = []
    for ph in phases:
        wdays = []
        for name, focus, exs in days:
            ex = []
            for n, role, side in exs:
                s, r, rest, rir = ph["scheme"][role]
                ex.append({"n": n, "s": s, "r": r + (" /side" if side else ""), "rest": rest, "rir": rir, "role": role})
            wdays.append({"name": name, "focus": focus, "ex": ex})
        weeks.append({"name": ph["name"], "phase": ph["phase"], "note": ph["note"], "days": wdays})
    return weeks


GLUTE_DAYS = [
    ("Day 1 · Glute Strength", "Heavy hip extension: the foundation of glute size.", [
        ("Barbell Hip Thrust", "main", False), ("Romanian Deadlift", "main", False),
        ("Bulgarian Split Squat", "acc", True), ("Cable Kickback", "acc", True), ("Hip Abduction Machine", "fin", False)]),
    ("Day 2 · Upper Body Sculpt", "Back, shoulders and arms for a balanced, athletic shape.", [
        ("DB Chest Press", "main", False), ("Lat Pulldown", "main", False), ("Seated Cable Row", "acc", False),
        ("DB Shoulder Press", "acc", False), ("Lateral Raise", "acc", False), ("Tricep Rope Pushdown", "fin", False)]),
    ("Day 3 · Glute & Hamstring", "Stretch-focused work for the glutes and hamstrings.", [
        ("Smith Machine Squat", "main", False), ("Lying Hamstring Curl", "acc", False), ("Walking Lunges", "acc", True),
        ("45° Back Extension", "acc", False), ("Frog Pumps", "fin", False)]),
    ("Day 4 · Lower Body + Core", "Heavy pulls, single-leg strength and core.", [
        ("Sumo Deadlift", "main", False), ("Step-Ups", "acc", True), ("Single-Leg Hip Thrust", "acc", True),
        ("Leg Press", "acc", False), ("Weighted Plank", "fin", False), ("Hanging Knee Raise", "fin", False)]),
]
GLUTE_PHASES = [
    {"name": "Week 1", "phase": "Foundation", "note": "Calibration week. Learn each movement and find your working weights (Chapter 6).",
     "scheme": {"main": (3, "10–12", "2 min", "3"), "acc": (3, "12–15", "75s", "3"), "fin": (2, "15–20", "60s", "2")}},
    {"name": "Week 2", "phase": "Foundation", "note": "Same structure. Beat Week 1 by a rep or a few pounds on every exercise.",
     "scheme": {"main": (3, "10–12", "2 min", "2"), "acc": (3, "12–15", "75s", "2"), "fin": (2, "15–20", "60s", "1")}},
    {"name": "Week 3", "phase": "Build", "note": "Volume increases: an extra set on your main lifts. Expect some soreness this week.",
     "scheme": {"main": (4, "8–10", "2 min", "2"), "acc": (3, "10–12", "75s", "2"), "fin": (3, "15–20", "60s", "1")}},
    {"name": "Week 4", "phase": "Build", "note": "Double progression: add weight on any exercise where you hit the top of the range last week.",
     "scheme": {"main": (4, "8–10", "2 min", "1–2"), "acc": (3, "10–12", "75s", "1–2"), "fin": (3, "15–20", "60s", "0–1")}},
    {"name": "Week 5", "phase": "Strength", "note": "Heavier loads, lower reps, longer rest. Focus on bar speed and technique.",
     "scheme": {"main": (4, "6–8", "2.5 min", "2"), "acc": (3, "8–12", "90s", "2"), "fin": (3, "12–15", "60s", "1")}},
    {"name": "Week 6", "phase": "Strength", "note": "Push your main lifts. Film one set of hip thrusts and compare with the library cues.",
     "scheme": {"main": (4, "6–8", "2.5 min", "1–2"), "acc": (3, "8–12", "90s", "1–2"), "fin": (3, "12–15", "60s", "0–1")}},
    {"name": "Week 7", "phase": "Peak", "note": "Heaviest week of the program. Full rest periods. Bring a spotter for heavy sets.",
     "scheme": {"main": (5, "5", "3 min", "1–2"), "acc": (3, "8–10", "90s", "1"), "fin": (3, "12–15", "60s", "0")}},
    {"name": "Week 8", "phase": "Test", "note": "Reduced volume. Work up to a heavy 5 on main lifts, log PRs, then retake photos and measurements.",
     "scheme": {"main": (3, "Heavy 5", "3 min", "1"), "acc": (2, "10–12", "75s", "2"), "fin": (2, "15", "60s", "1")}},
]

PRESS_DAYS = [
    ("Day 1 · Heavy Push", "Heavy pressing: the main strength day.", [
        ("DB Chest Press", "main", False), ("Incline DB Press", "main", False), ("DB Shoulder Press", "acc", False),
        ("Bench Dips", "acc", False), ("Push-Ups", "fin", False)]),
    ("Day 2 · Pull + Posture", "A strong back builds a stronger press.", [
        ("Lat Pulldown", "main", False), ("Single-Arm DB Row", "main", True), ("Face Pulls", "acc", False),
        ("Rear Delt Fly", "acc", False), ("Hammer Curl", "fin", False)]),
    ("Day 3 · Volume Push", "Paused presses and isolation for volume.", [
        ("Paused DB Bench Press", "main", False), ("Machine Chest Press", "acc", False), ("Cable Fly", "acc", False),
        ("Arnold Press", "acc", False), ("Overhead Tricep Extension", "fin", False)]),
]
PRESS_PHASES = [
    {"name": "Week 1", "phase": "Foundation", "note": "Choose a weight you could press 12–13 times and do 10 clean reps.",
     "scheme": {"main": (3, "10", "2 min", "2–3"), "acc": (3, "12", "75s", "2"), "fin": (2, "AMRAP", "60s", "1")}},
    {"name": "Week 2", "phase": "Foundation", "note": "If every rep was clean last week, go up 2.5–5 lb per dumbbell.",
     "scheme": {"main": (3, "10", "2 min", "2"), "acc": (3, "12", "75s", "2"), "fin": (2, "AMRAP", "60s", "1")}},
    {"name": "Week 3", "phase": "Build", "note": "Heavier with an extra set. Use the kick-up technique from Chapter 3.",
     "scheme": {"main": (4, "8", "2.5 min", "2"), "acc": (3, "10", "75s", "1–2"), "fin": (3, "AMRAP", "60s", "0–1")}},
    {"name": "Week 4", "phase": "Build", "note": "Beat Week 3 by a rep or use the one-set-heavier bridge (Chapter 4).",
     "scheme": {"main": (4, "8", "2.5 min", "1–2"), "acc": (3, "10", "75s", "1"), "fin": (3, "AMRAP", "60s", "0")}},
    {"name": "Week 5", "phase": "Strength", "note": "Heavy fives. Spotter or filming recommended.",
     "scheme": {"main": (5, "5", "3 min", "1–2"), "acc": (3, "8–10", "90s", "1–2"), "fin": (2, "AMRAP", "60s", "0")}},
    {"name": "Week 6", "phase": "PR Week", "note": "Day 1: follow the PR Week Protocol (Chapter 10) and work up to a heavy 3. Log it on the PR Wall.",
     "scheme": {"main": (4, "Heavy 3", "3 min", "1"), "acc": (2, "10", "90s", "2"), "fin": (1, "AMRAP", "60s", "1")}},
]

STARTER_DAYS = [
    ("Workout A · Glute Wake-Up", "Activation and foundational patterns.", [
        ("Glute Bridge", "acc", False), ("Banded Lateral Walk", "acc", True), ("Goblet Squat", "main", False),
        ("Romanian Deadlift", "main", False), ("Dumbbell Kickback", "acc", True)]),
    ("Workout B · Glute Builder Lite", "A preview of the Glute Specialist Program.", [
        ("Barbell Hip Thrust", "main", False), ("Bulgarian Split Squat", "acc", True), ("Cable Kickback", "acc", True),
        ("Hip Abduction Machine", "acc", False), ("Frog Pumps", "fin", False)]),
    ("Workout C · Lower Body Burn", "Strength and single-leg work.", [
        ("Sumo Deadlift", "main", False), ("Step-Ups", "acc", True), ("Single-Leg Glute Bridge", "acc", True),
        ("Reverse Lunge", "acc", True), ("Fire Hydrants", "fin", True)]),
]
STARTER_PHASES = [{"name": "Week 1", "phase": "Starter", "note": "Do A, B and C this week with a rest day between each. Log your weights to beat them next week.",
                   "scheme": {"main": (3, "10–12", "90s", "2–3"), "acc": (3, "12–15", "60s", "2"), "fin": (2, "20", "45s", "1")}}]

CONF_DAYS = [
    ("Day 1 · Machines", "Guided machines: zero guesswork.", [
        ("Leg Press", "acc", False), ("Lat Pulldown", "acc", False), ("Machine Chest Press", "acc", False),
        ("Lying Hamstring Curl", "acc", False), ("Hip Abduction Machine", "acc", False), ("Treadmill Incline Walk", "fin", False)]),
    ("Day 2 · Dumbbells", "Claim a bench and a set of dumbbells.", [
        ("Goblet Squat", "acc", False), ("DB Chest Press", "acc", False), ("Single-Arm DB Row", "acc", True),
        ("Romanian Deadlift", "acc", False), ("DB Shoulder Press", "acc", False)]),
    ("Day 3 · Cables", "Learn the most versatile station in the gym.", [
        ("Cable Kickback", "acc", True), ("Seated Cable Row", "acc", False), ("Face Pulls", "acc", False),
        ("Tricep Rope Pushdown", "acc", False), ("Glute Bridge", "acc", False), ("Treadmill Incline Walk", "fin", False)]),
]
CONF_PHASES = [
    {"name": "Week 1", "phase": "Learn", "note": "Light weights. The only goal is to learn each station and leave proud.",
     "scheme": {"main": (2, "12", "90s", "3–4"), "acc": (2, "12", "75s", "3–4"), "fin": (1, "10 min", "—", "—")}},
    {"name": "Week 2", "phase": "Own It", "note": "Add a set and go slightly heavier. Same stations, more confidence.",
     "scheme": {"main": (3, "10–12", "90s", "2–3"), "acc": (3, "10–12", "75s", "2–3"), "fin": (1, "15 min", "—", "—")}},
]


# ---------------------------------------------------------------- 30-day challenge
def build_challenge():
    T = {
        "Glutes": [("Glute bridges", 15, ""), ("Donkey kicks", 12, " /side"), ("Fire hydrants", 12, " /side"), ("Sumo squats", 15, ""), ("Frog pumps", 20, "")],
        "Upper Body": [("Push-ups (incline or knees as needed)", 8, ""), ("Tricep dips", 10, ""), ("Shoulder taps", 16, ""), ("Plank up-downs", 8, ""), ("Superman pulls", 12, "")],
        "Core + Cardio": [("Mountain climbers", 20, ""), ("Bicycle crunches", 20, ""), ("Plank", 30, "s"), ("Leg raises", 10, ""), ("Jumping jacks", 30, "")],
        "Legs": [("Squats", 15, ""), ("Reverse lunges", 10, " /side"), ("Wall sit", 30, "s"), ("Calf raises", 20, ""), ("Squat jumps", 8, "")],
        "Full Body Burn": [("Burpees", 6, ""), ("Squat to press (dumbbells or water bottles)", 12, ""), ("Walking lunges", 10, " /side"), ("Push-ups", 8, ""), ("High knees", 30, "s")],
    }
    recovery = [("Brisk outdoor walk", "20–30 min"), ("Hip flexor stretch", "45s /side"), ("Pigeon stretch", "45s /side"), ("Cat-cow", "10 slow reps"), ("Child's pose", "60s")]
    reset = [("Sleep 7–9 hours tonight", "Recovery"), ("Meal prep 3+ meals for the week", "Nutrition"), ("10-minute full-body stretch", "Mobility"), ("Take your weekly progress photo", "Tracking")]
    order = ["Glutes", "Upper Body", "Core + Cardio", "Legs", "Full Body Burn", "Active Recovery", "Rest & Reset"]
    prompts = [
        "Why did you really start this challenge? Be specific. You'll come back to this on harder days.",
        "Name three things your body did for you today.",
        "What's one excuse you're officially retiring this month, and what will you replace it with?",
        "Describe how you want to feel walking into Day 30.",
        "Who are you doing this for? Write about why it needs to be you.",
        "What did you eat today that fueled you well? What would you swap tomorrow?",
        "Rest is productive. How are you recharging today?",
        "Which move felt easier today than it did on Day 1?",
        "Write the message you need to hear on your hardest day.",
        "What does 'strong' mean to you, physically and mentally?",
        "Rate your energy 1–10. What helped or hurt it today?",
        "What environment changes would make your habits easier (kitchen, phone, schedule)?",
        "Name a woman whose strength inspires you, and why.",
        "Two weeks done. What are you most proud of so far?",
        "Halfway. What's changed physically and mentally?",
        "What would you tell Day-1 you?",
        "What's your biggest non-scale victory this week?",
        "Where are you still holding back? What's the fear underneath it?",
        "How do you speak to yourself in the mirror lately? Rewrite one negative thought.",
        "Plan your Day 30 celebration. Make it meaningful.",
        "Write five things you appreciate about your body.",
        "Which habit from this challenge are you keeping for good, and how will you protect it?",
        "Has anyone noticed a change in you? How did it feel?",
        "What goal felt impossible a month ago but doesn't now?",
        "What's your favorite move from this challenge and why?",
        "What does your next 30 days look like? Write the plan.",
        "Write a thank-you note to your body.",
        "What does the woman who finishes this challenge believe about herself?",
        "Final Boss tomorrow. How are you preparing mentally?",
        "Compare Day 1 and Day 30: photos, energy, mindset. Write it all down.",
    ]
    days = []
    for i in range(30):
        wk = i // 7
        kind = order[i % 7]
        rounds = [3, 3, 4, 4, 4][wk]
        mult = 1 + 0.25 * wk
        if i == 28:
            kind, ex, rounds = "Final Boss", [(n, f"{round(r * 1.75)}{u}") for k in ("Glutes", "Legs", "Full Body Burn") for n, r, u in T[k][:2]], 3
        elif i == 29:
            kind, ex, rounds = "Show-Off Day", [("Repeat the Day 1 workout and compare", "Test"), ("Retake progress photos & measurements", "Track"), ("Share your results and tag me", "Celebrate")], 0
        elif kind == "Active Recovery":
            ex, rounds = recovery, 0
        elif kind == "Rest & Reset":
            ex, rounds = reset, 0
        else:
            ex = [(n, f"{round(r * mult)}{u}") for n, r, u in T[kind]]
        days.append({"t": kind, "rounds": rounds, "ex": [{"n": n, "r": r} for n, r in ex], "prompt": prompts[i]})
    return days


# ---------------------------------------------------------------- nutrition
MEALS = [
    {"name": "Monday", "meals": [("Breakfast", "Protein Overnight Oats", 42), ("Lunch", "Chicken Burrito Bowl", 60), ("Snack", "Greek yogurt + berries + 1 tbsp granola", 22), ("Dinner", "Air-Fryer Salmon, Sweet Potato & Green Beans", 33)]},
    {"name": "Tuesday", "meals": [("Breakfast", "3 eggs + 1 cup egg whites, spinach, 1 slice toast, fruit", 44), ("Lunch", "Tuna Salad Wrap + side salad", 34), ("Snack", "Protein shake + banana (post-workout)", 26), ("Dinner", "Turkey Taco Bowl", 32)]},
    {"name": "Wednesday", "meals": [("Breakfast", "Cottage Cheese Protein Pancakes", 31), ("Lunch", "Leftover Turkey Taco Bowl", 32), ("Snack", "String cheese + apple + 10 almonds", 10), ("Dinner", "Shrimp Stir-Fry", 43)]},
    {"name": "Thursday", "meals": [("Breakfast", "Protein Overnight Oats", 42), ("Lunch", "Chicken Burrito Bowl", 60), ("Snack", "Chocolate Protein Pudding", 35), ("Dinner", "Turkey Meatballs & Marinara", 42)]},
    {"name": "Friday", "meals": [("Breakfast", "Egg Bites (3) + fruit", 29), ("Lunch", "Leftover Turkey Meatballs", 42), ("Snack", "Beef jerky + grapes", 12), ("Dinner", "Planned flexible meal: protein first, enjoy it", 30)]},
    {"name": "Saturday", "meals": [("Breakfast", "Cottage Cheese Protein Pancakes", 31), ("Lunch", "Grilled chicken salad with quinoa, feta & lemon vinaigrette", 40), ("Snack", "Protein Mug Cake", 29), ("Dinner", "Jerk Chicken Rice Bowl", 42)]},
    {"name": "Sunday", "meals": [("Breakfast", "Breakfast burrito: eggs, egg whites, potatoes, turkey bacon, salsa", 38), ("Lunch", "Leftover Jerk Chicken Rice Bowl", 42), ("Snack", "Greek yogurt + berries", 20), ("Dinner", "Sheet-pan chicken, broccoli & potatoes (meal prep night)", 40)]},
]

RECIPES = [
    {"n": "Protein Overnight Oats", "t": "Breakfast", "time": "5 min + overnight", "m": (405, 42, 45, 7),
     "ing": ["½ cup old-fashioned oats", "1 scoop vanilla whey protein", "½ cup nonfat Greek yogurt", "½ cup unsweetened almond milk", "1 tsp chia seeds", "½ cup berries"],
     "steps": ["Stir oats, protein powder and chia seeds in a jar.", "Add yogurt and milk and mix until smooth (add a splash more milk if thick).", "Refrigerate overnight. Top with berries before eating.", "Make 5 jars on Sunday. They keep 4 days."]},
    {"n": "Chicken Burrito Bowl", "t": "Lunch", "time": "15 min (with prepped chicken)", "m": (565, 60, 58, 9),
     "ing": ["5 oz cooked chicken breast, chopped", "¾ cup cooked white or brown rice", "½ cup black beans, rinsed", "¼ cup pico de gallo or salsa", "1 cup shredded lettuce", "2 tbsp reduced-fat shredded cheese", "2 tbsp nonfat Greek yogurt (as sour cream)", "Lime, cumin, chili powder"],
     "steps": ["Season chicken with cumin, chili powder, garlic powder, salt and lime.", "Layer rice, beans, chicken and lettuce in a bowl.", "Top with pico, cheese and Greek yogurt."]},
    {"n": "Air-Fryer Salmon, Sweet Potato & Green Beans", "t": "Dinner", "time": "25 min", "m": (520, 33, 42, 23),
     "ing": ["5 oz salmon fillet", "6 oz sweet potato, cubed", "1 cup green beans", "1 tsp olive oil", "Garlic powder, paprika, salt, pepper, lemon"],
     "steps": ["Toss sweet potato with half the oil and seasonings. Air-fry at 400°F for 10 min.", "Add green beans and seasoned salmon to the basket.", "Air-fry 8–10 more minutes until the salmon flakes easily. Finish with lemon."]},
    {"n": "Turkey Taco Bowl", "t": "Dinner", "time": "20 min", "m": (390, 32, 28, 15),
     "ing": ["5 oz raw 93% lean ground turkey", "1 tbsp taco seasoning", "½ cup cooked rice", "¼ cup salsa", "Lettuce, onion, peppers", "2 tbsp reduced-fat cheese"],
     "steps": ["Brown the turkey in a nonstick pan, breaking it up.", "Add taco seasoning and a splash of water and simmer 3 minutes.", "Serve over rice and lettuce with salsa and cheese. (Or use lettuce cups.)"]},
    {"n": "Cottage Cheese Protein Pancakes", "t": "Breakfast", "time": "15 min", "m": (390, 31, 40, 9),
     "ing": ["½ cup oats", "½ cup low-fat cottage cheese", "1 egg + 2 egg whites", "½ tsp baking powder", "Cinnamon, vanilla", "½ cup berries + sugar-free syrup"],
     "steps": ["Blend everything except toppings until smooth.", "Cook ¼-cup portions on a medium-hot nonstick pan, about 2 minutes per side.", "Top with berries and syrup."]},
    {"n": "Shrimp Stir-Fry", "t": "Dinner", "time": "15 min", "m": (480, 43, 54, 10),
     "ing": ["6 oz raw shrimp, peeled", "2 cups stir-fry vegetables", "2 tsp sesame oil", "2 tbsp low-sodium soy sauce + 1 tsp honey", "Garlic, ginger, chili flakes", "¾ cup cooked jasmine rice"],
     "steps": ["Heat half the oil in a pan over high heat and cook the shrimp 1–2 min per side. Set aside.", "Add remaining oil and vegetables and stir-fry 4 minutes.", "Add garlic, ginger, soy and honey. Return the shrimp, toss and serve over rice."]},
    {"n": "Turkey Meatballs & Marinara", "t": "Dinner", "time": "30 min", "m": (575, 42, 62, 17),
     "ing": ["5 oz raw 93% lean ground turkey", "2 tbsp breadcrumbs", "1 egg white", "Italian seasoning, garlic, salt", "½ cup marinara", "2 oz dry pasta (or zucchini noodles)", "1 tbsp parmesan"],
     "steps": ["Mix turkey, breadcrumbs, egg white and seasonings. Roll into 6 balls.", "Bake at 400°F for 15–18 min.", "Warm the marinara, add the meatballs and serve over pasta with parmesan."]},
    {"n": "Egg Bites (makes 12)", "t": "Breakfast", "time": "30 min", "m": (295, 29, 5, 17),
     "ing": ["10 eggs", "1 cup liquid egg whites", "½ cup low-fat cottage cheese", "1 cup chopped spinach, peppers & onions", "½ cup shredded cheese", "Salt, pepper, garlic powder"],
     "steps": ["Blend eggs, egg whites and cottage cheese until smooth.", "Divide vegetables and cheese among 12 greased muffin cups and pour the egg mix over.", "Bake at 350°F for 20–25 min. Macros shown are for 3 bites. Keeps 4 days refrigerated."]},
    {"n": "Chocolate Protein Pudding", "t": "Snack", "time": "3 min", "m": (215, 35, 17, 1),
     "ing": ["1 cup nonfat Greek yogurt", "½ scoop chocolate whey protein", "1 tsp cocoa powder", "1 tsp honey"],
     "steps": ["Stir everything together until smooth.", "Chill 10 minutes for a thicker texture."]},
    {"n": "Jerk Chicken Rice Bowl", "t": "Dinner", "time": "30 min + marinating", "m": (545, 42, 49, 20),
     "ing": ["5 oz boneless skinless chicken thighs", "2 tbsp jerk marinade", "¾ cup rice & peas", "1 cup shredded cabbage", "1 tsp oil"],
     "steps": ["Marinate chicken at least 1 hour (overnight is best).", "Grill, air-fry or bake at 425°F for 18–22 min to 165°F internal.", "Sauté cabbage in oil with salt and pepper. Serve with rice & peas."]},
    {"n": "Protein Mug Cake", "t": "Snack", "time": "3 min", "m": (185, 29, 12, 3),
     "ing": ["1 scoop whey protein", "1 tbsp flour", "1 tbsp cocoa powder", "½ tsp baking powder", "1 egg white", "3 tbsp unsweetened almond milk"],
     "steps": ["Mix dry ingredients in a large mug.", "Stir in egg white and milk until smooth.", "Microwave 60–75 seconds. Don't overcook or it gets rubbery."]},
    {"n": "Tuna Salad Wrap", "t": "Lunch", "time": "5 min", "m": (260, 34, 21, 4),
     "ing": ["1 can (5 oz) tuna in water, drained", "3 tbsp nonfat Greek yogurt", "1 tsp Dijon mustard", "Diced celery & red onion", "1 high-fiber wrap", "Handful of spinach"],
     "steps": ["Mix tuna, yogurt, mustard, celery, onion, salt and pepper.", "Spread on the wrap with spinach and roll tightly."]},
]

GROCERY = [
    {"title": "Protein", "items": ["Chicken breast (3 lb)", "Boneless skinless chicken thighs (1.5 lb)", "93% lean ground turkey (2 lb)", "Salmon fillets (2)", "Frozen raw shrimp (1 bag)", "Eggs (2 dozen)", "Liquid egg whites (32 oz)", "Nonfat Greek yogurt (large tub)", "Low-fat cottage cheese", "Tuna packets/cans", "Turkey bacon", "Whey protein (vanilla + chocolate)", "Beef jerky", "String cheese"]},
    {"title": "Carbohydrates", "items": ["Old-fashioned oats", "Jasmine or brown rice", "Sweet potatoes", "White potatoes", "High-fiber wraps", "Whole-grain bread", "Pasta", "Quinoa", "Black beans", "Rice & peas (or kidney beans)", "Granola"]},
    {"title": "Produce", "items": ["Spinach", "Mixed greens / lettuce", "Broccoli", "Green beans", "Stir-fry vegetable mix", "Bell peppers & onions", "Cabbage", "Celery", "Berries", "Bananas", "Apples", "Grapes", "Lemons & limes"]},
    {"title": "Fats, Sauces & Seasonings", "items": ["Olive oil + sesame oil", "Almonds", "Chia seeds", "Reduced-fat shredded cheese", "Parmesan & feta", "Salsa / pico de gallo", "Marinara", "Jerk marinade", "Low-sodium soy sauce", "Honey", "Dijon mustard", "Taco & Italian seasoning", "Cocoa powder"]},
]

EATING_OUT = [
    {"q": "Chipotle", "a": "Bowl with double chicken, rice, fajita veggies, black beans, fresh tomato salsa and lettuce. Skip or go light on sour cream, cheese and chips. Roughly 60 g+ protein."},
    {"q": "Chick-fil-A", "a": "12-count grilled nuggets with a side salad or fruit cup, or the grilled chicken sandwich. Zesty Buffalo is one of the lower-calorie sauces."},
    {"q": "Starbucks", "a": "Egg-white egg bites or the Protein Box. Add protein cold foam to your coffee or choose a protein drink."},
    {"q": "Subway / sandwich shops", "a": "Double meat (chicken, turkey or steak) on a 6-inch or as a salad, extra veggies, mustard or light sauce."},
    {"q": "Wings night", "a": "Dry-rub wings (lemon pepper, garlic parm dry, Cajun), celery and carrots, sauce on the side."},
    {"q": "Mexican restaurant", "a": "Fajitas: load up on protein and peppers, use 2 tortillas, salsa and pico. Portion the chips once, then move the basket."},
    {"q": "Sushi", "a": "Sashimi or nigiri plus a hand roll, edamame and miso soup. Limit tempura and creamy rolls."},
    {"q": "Brunch", "a": "Omelet or eggs with turkey sausage and fruit. Share the pancakes if you want them. One mimosa is fine."},
]


# ---------------------------------------------------------------- products
PRODUCTS = [
    {
        "slug": "glute-starter-pack-free-g7f2", "short": "Glute Starter Guide", "title": "The Glute Starter Guide",
        "kicker": "Free guide", "sub": "Three glute workouts and the principles behind them.",
        "meta": ["3 workouts", "1 week", "Free"], "hue": 340, "guide": "glute-starter",
        "sections": [
            {"type": "guide", "id": "guide", "label": "Guide"},
            {"type": "program", "id": "prog", "label": "Workouts", "weeks": build_program(STARTER_DAYS, STARTER_PHASES)},
            {"type": "library", "id": "lib", "label": "Exercise Library"},
            {"type": "upsell", "id": "next", "label": "Next Steps"},
        ],
        "stan": {
            "kind": "Lead Magnet (Free)", "price": "FREE", "strike": "",
            "thumb_title": "Free Glute Starter Guide", "thumb_sub": "3 glute workouts you can start today",
            "button": "Get the Free Guide",
            "checkout_title": "The Glute Starter Guide (Free)",
            "desc": "Want to grow your glutes but don't know where to start? This free guide gives you three of my favorite glute workouts and the four principles behind every program I write. You get an interactive tracker for your phone and a PDF you can print. Enter your email and it's yours.",
            "bullets": ["3 glute-focused gym workouts", "Interactive tracker: log every set, built-in rest timer", "Step-by-step technique for every exercise", "The 4 rules of glute growth", "Printable PDF with fillable workout logs"],
            "cta": "Send Me the Guide",
            "bump": None,
            "thanks": "Your Glute Starter Guide is on its way to your inbox. Open the interactive version on your phone and save it to your home screen. Tag me in your first workout!",
        },
    },
    {
        "slug": "30-day-get-fit-challenge-c9x4", "short": "30-Day Challenge", "title": "The 30-Day Get Fit With Me Challenge",
        "kicker": "30-day program", "sub": "Daily workouts, four habits and a mindset practice.",
        "meta": ["30 days", "20–35 min/day", "Home or gym"], "hue": 18, "guide": "30-day-challenge",
        "sections": [
            {"type": "guide", "id": "guide", "label": "Guide"},
            {"type": "challenge", "id": "ch", "label": "Daily Tracker",
             "tasks": ["Completed today's workout", "Drank 80+ oz of water", "Walked 8,000+ steps", "Protein at every meal"],
             "days": build_challenge()},
            {"type": "progress", "id": "prog", "label": "Progress", "measure": True},
            {"type": "upsell", "id": "next", "label": "Next Steps"},
        ],
        "stan": {
            "kind": "Digital Product", "price": "$14.99", "strike": "$29",
            "thumb_title": "30-Day Get Fit With Me Challenge", "thumb_sub": "Daily workouts, habits & mindset in 30 days",
            "button": "Join the Challenge",
            "checkout_title": "The 30-Day Get Fit With Me Challenge",
            "desc": "Stop waiting for Monday. For 30 days, you'll do one short workout a day at home or the gym, four habits that change everything (water, steps, protein, movement) and a daily mindset prompt. Workouts get harder every week. A built-in tracker keeps your streak going, and the guide teaches you how to scale every move to your level.",
            "bullets": ["30 progressive daily workouts (20–35 min)", "Habit tracker with streaks and daily check-ins", "30 guided journal prompts", "Scaling chart: easier and harder versions of every move", "Measurement tracker with progress charts", "Full guide: habits, NEAT, consistency, what to expect each week", "Printable PDF with a fillable 30-day tracker and journal"],
            "cta": "Start My 30 Days",
            "bump": {"title": "Add Fuel Like A Baddie for $9 (reg. $19)", "desc": "My complete nutrition guide: macro calculator, 7-day meal plan, 12 recipes and grocery list."},
            "thanks": "Welcome to the challenge! Your link is in your email. Take your Day 1 photos and measurements today, then post your first workout and tag me with #GetFitWithMeChallenge.",
        },
    },
    {
        "slug": "booty-builder-8-week-b3k8", "short": "Glute Specialist Program", "title": "The Glute Specialist Program",
        "kicker": "8-week program", "sub": "My signature 4-day program to build stronger, fuller glutes.",
        "meta": ["8 weeks", "4 days/week", "32 workouts", "Gym"], "hue": 345, "guide": "glute-specialist",
        "sections": [
            {"type": "guide", "id": "guide", "label": "Handbook"},
            {"type": "program", "id": "prog", "label": "Program", "weeks": build_program(GLUTE_DAYS, GLUTE_PHASES)},
            {"type": "progress", "id": "stats", "label": "Progress", "measure": True,
             "lifts": ["Barbell Hip Thrust", "Romanian Deadlift", "Sumo Deadlift", "Smith Machine Squat", "Bulgarian Split Squat", "DB Chest Press", "Lat Pulldown"]},
            {"type": "library", "id": "lib", "label": "Exercise Library"},
            {"type": "tools", "id": "tools", "label": "Tools"},
            {"type": "upsell", "id": "next", "label": "Next Steps"},
        ],
        "stan": {
            "kind": "Digital Product", "price": "$37", "strike": "$67",
            "thumb_title": "The Glute Specialist Program", "thumb_sub": "My signature 8-week glute program",
            "button": "Start the Program",
            "checkout_title": "The Glute Specialist Program: 8 Weeks",
            "desc": "Everyone asks what I do for my glutes. This is it: my complete 8-week program, built in four progressive phases (Foundation, Build, Strength, Peak) with three lower-body days and one upper-body day each week. You also get a 14-chapter handbook covering the science of glute growth, progressive overload, effort (RIR), warm-ups, nutrition and troubleshooting. Track every set in the app, see what you lifted last time, and watch your strength climb on your progress charts.",
            "bullets": ["32 progressive workouts across 8 weeks", "14-chapter training handbook with knowledge checks", "Set-by-set logging with 'last time' comparisons", "Progress charts, PR Wall and measurement tracking", "Exercise library: setup, cues, mistakes & swaps for 25+ moves", "1RM and warm-up calculators, auto rest timer", "Printable PDF book with 32 fillable workout logs"],
            "cta": "Get the Program",
            "bump": {"title": "Add Press Like A Boss for $15 (reg. $24)", "desc": "My 6-week upper-body strength program. It pairs perfectly as a full upper/lower split."},
            "thanks": "You're in! Your program link and PDF are in your email. Start with the Handbook (Chapters 1–6), then do Week 1 as your calibration week. Tag me in your first hip thrust!",
        },
    },
    {
        "slug": "press-like-a-boss-p5m1", "short": "Press Like A Boss", "title": "Press Like A Boss",
        "kicker": "6-week strength program", "sub": "Upper-body strength for women: a stronger press, back and shoulders.",
        "meta": ["6 weeks", "3 days/week", "18 workouts", "Gym"], "hue": 265, "guide": "press-like-a-boss",
        "sections": [
            {"type": "guide", "id": "guide", "label": "Handbook"},
            {"type": "program", "id": "prog", "label": "Program", "weeks": build_program(PRESS_DAYS, PRESS_PHASES)},
            {"type": "progress", "id": "stats", "label": "Progress",
             "lifts": ["DB Chest Press", "Incline DB Press", "DB Shoulder Press", "Lat Pulldown", "Single-Arm DB Row", "Paused DB Bench Press"]},
            {"type": "library", "id": "lib", "label": "Exercise Library"},
            {"type": "tools", "id": "tools", "label": "Tools"},
            {"type": "upsell", "id": "next", "label": "Next Steps"},
        ],
        "stan": {
            "kind": "Digital Product", "price": "$24", "strike": "$47",
            "thumb_title": "Press Like A Boss", "thumb_sub": "6 weeks to your strongest upper body",
            "button": "Get Stronger",
            "checkout_title": "Press Like A Boss: 6-Week Upper Body Strength",
            "desc": "You saw me press 70s and 75s. This is the exact plan behind it. Three upper-body days a week for six weeks: a heavy push day, a pull and posture day and a volume day, ending with a structured PR Week. The handbook teaches you dumbbell press technique step by step, how to beat the dumbbell jump problem, shoulder health, spotting and how to test your max safely.",
            "bullets": ["18 progressive workouts across 6 weeks", "11-chapter strength handbook with knowledge checks", "Dumbbell press masterclass, including the kick-up technique", "Strategies for breaking through dumbbell plateaus", "PR Week warm-up protocol + 1RM calculator", "Set-by-set logging and progress charts", "Printable PDF book with fillable workout logs"],
            "cta": "Get the Program",
            "bump": {"title": "Add the Glute Specialist Program for $25 (reg. $37)", "desc": "Complete your split with my signature 8-week lower-body program."},
            "thanks": "Let's get strong! Your program and PDF are in your email. Read Chapter 3 before your first session. Week 6 is PR Week, so film it and tag me.",
        },
    },
    {
        "slug": "fuel-like-a-baddie-f2q6", "short": "Fuel Like A Baddie", "title": "Fuel Like A Baddie",
        "kicker": "Nutrition guide", "sub": "The complete high-protein nutrition system for women who train.",
        "meta": ["17 chapters", "12 recipes", "7-day plan", "Macro calculator"], "hue": 150, "guide": "fuel-like-a-baddie",
        "sections": [
            {"type": "guide", "id": "guide", "label": "Guide"},
            {"type": "macro", "id": "macro", "label": "My Macros"},
            {"type": "meals", "id": "meals", "label": "Meal Plan", "days": MEALS},
            {"type": "recipes", "id": "recipes", "label": "Recipes", "items": RECIPES},
            {"type": "checklist", "id": "groc", "label": "Grocery List", "groups": GROCERY},
            {"type": "checklist", "id": "prep", "label": "Sunday Prep", "groups": [
                {"title": "90-Minute Meal Prep", "items": ["Preheat the oven to 425°F and start the rice cooker", "Season and sheet-pan the chicken (22–25 min)", "Roast potatoes, sweet potatoes and broccoli on a second pan", "Brown the ground turkey for tacos; roll and bake meatballs", "Make 4–5 jars of protein overnight oats", "Bake a tray of 12 egg bites", "Wash and chop vegetables for the week", "Portion meals into containers and label by day", "Freeze Thursday–Saturday portions", "Fill your water bottle and pack tomorrow's gym bag"]}]},
            {"type": "accordion", "id": "out", "label": "Eating Out", "items": EATING_OUT},
            {"type": "progress", "id": "stats", "label": "Check-Ins", "measure": True},
            {"type": "upsell", "id": "next", "label": "Next Steps"},
        ],
        "stan": {
            "kind": "Digital Product", "price": "$19", "strike": "$39",
            "thumb_title": "Fuel Like A Baddie", "thumb_sub": "Macros, meal plan, recipes & grocery list",
            "button": "Get the Guide",
            "checkout_title": "Fuel Like A Baddie: The Nutrition Guide",
            "desc": "Training hard but not seeing it in the mirror? It's usually nutrition. This guide teaches you how to eat for your goal in 17 clear chapters: energy balance, macros, protein, meal timing, hydration, supplements, your cycle, plateaus, eating out and meal prep. Then it gives you the tools: a personal macro calculator, a 7-day high-protein meal plan, 12 recipes with macros, a grocery checklist and a 90-minute meal prep system.",
            "bullets": ["17-chapter nutrition guide with knowledge checks", "Personal macro calculator (calories, protein, carbs, fat, water)", "7-day high-protein meal plan", "12 recipes with ingredients, steps and macros", "Interactive grocery list + 90-minute meal prep checklist", "Eating-out guide for 8 popular restaurants", "Printable PDF book with a fillable meal planner and check-in log"],
            "cta": "Get the Guide",
            "bump": {"title": "Add the 30-Day Challenge for $9 (reg. $14.99)", "desc": "Pair your nutrition with 30 days of workouts, habits and mindset."},
            "thanks": "Your guide is in your email. Start with the My Macros tab, then read Chapters 1–4. Shop with the grocery list this weekend.",
        },
    },
    {
        "slug": "gym-girl-confidence-kit-k4t9", "short": "Gym Confidence Kit", "title": "The Gym Girl Confidence Kit",
        "kicker": "Beginner guide", "sub": "Everything you need to walk into the gym and know exactly what to do.",
        "meta": ["14 chapters", "2-week plan", "Beginner"], "hue": 40, "guide": "gym-girl-confidence-kit",
        "sections": [
            {"type": "guide", "id": "guide", "label": "Guide"},
            {"type": "program", "id": "prog", "label": "2-Week Plan", "weeks": build_program(CONF_DAYS, CONF_PHASES)},
            {"type": "library", "id": "lib", "label": "Exercise Library"},
            {"type": "checklist", "id": "bag", "label": "Checklists", "groups": [
                {"title": "Gym Bag", "items": ["Water bottle (32 oz+)", "Headphones (charged)", "Workout playlist", "Today's workout open in this app", "Lifting straps or grips", "Ankle strap for cable kickbacks", "Mini resistance band", "Small towel", "Deodorant", "Hair ties", "Post-workout snack or shake", "Phone tripod (optional)"]},
                {"title": "Before Your First Visit", "items": ["Book a free gym tour/orientation", "Choose a quiet time to go", "Read today's workout and watch the cues in the library", "Lay out an outfit you feel good in", "Pack your bag the night before", "Tell a friend your plan (accountability)"]},
                {"title": "Confidence Rituals", "items": ["Play my hype song on the way in", "Review my plan in the parking lot", "Say my affirmation", "Walk in with shoulders back", "Journal after the session"]}]},
            {"type": "journal", "id": "jr", "label": "Journal", "prompts": [
                "What exactly makes me nervous about the gym? Naming it takes away its power.",
                "What would I do in the gym if I knew nobody was judging me?",
                "After my first session: how did I feel walking out?",
                "What did I do this week that past-me would have been too nervous to do?",
                "Which station felt most intimidating, and how did it go?",
                "Write a letter to the woman who walks into the gym confidently three months from now."]},
            {"type": "upsell", "id": "next", "label": "Next Steps"},
        ],
        "stan": {
            "kind": "Digital Product", "price": "$12", "strike": "$27",
            "thumb_title": "The Gym Girl Confidence Kit", "thumb_sub": "Beat gym anxiety & own the weight room",
            "button": "Build My Confidence",
            "checkout_title": "The Gym Girl Confidence Kit",
            "desc": "Nervous about the weight room? Not sure how the machines work? This kit is the orientation I wish I'd had. In 14 chapters you'll learn how gym anxiety works and how to beat it, the layout of a gym, how every piece of equipment works, etiquette, exactly what to say in awkward moments, how to read a program and choose weights. Then a 2-week plan eases you in: machines first, then dumbbells, then cables.",
            "bullets": ["14-chapter beginner's guide to the gym", "2-week starter plan with set-by-set tracking", "Exercise library with step-by-step technique", "Word-for-word gym scripts", "Gym bag and first-visit checklists", "Guided confidence journal", "Printable PDF with fillable checklists and logs"],
            "cta": "Get the Kit",
            "bump": {"title": "Add the Glute Specialist Program for $25 (reg. $37)", "desc": "When you're ready, keep the momentum with my signature 8-week program."},
            "thanks": "I'm so proud of you for taking this step. Your kit is in your email. Read Chapters 1–5 tonight and pack your bag. Tag me in your first gym selfie!",
        },
    },
]

BUNDLE = {
    "kind": "Bundle", "price": "$67", "strike": "$106.99",
    "thumb_title": "The Complete Collection", "thumb_sub": "All 5 programs & guides. Save 37%",
    "button": "Get Everything",
    "checkout_title": "The Complete Get Fit With Me Collection",
    "desc": "Everything I teach in one place: training, nutrition and confidence. Get all five programs and guides, each with its interactive app and printable PDF book, and save over $40 compared with buying them separately.",
    "bullets": ["The Glute Specialist Program ($37)", "Press Like A Boss ($24)", "Fuel Like A Baddie ($19)", "30-Day Get Fit With Me Challenge ($14.99)", "The Gym Girl Confidence Kit ($12)", "5 interactive apps + 5 printable PDF books", "Lifetime access and all future updates"],
    "cta": "Get the Collection",
    "bump": {"title": "Add a 30-min Form Check Call for $29 (reg. $49)", "desc": "Send me your lift videos and we'll review your technique together on a 1:1 video call."},
    "thanks": "Welcome to the full collection! All five links are in your email. Suggested order: Confidence Kit, then Fuel Like A Baddie, then the Glute Specialist Program, adding Press Like A Boss when you're ready.",
}

COACHING = [
    {
        "kind": "Coaching Call (Calendar)", "price": "$49", "strike": "",
        "thumb_title": "1:1 Form Check Call", "thumb_sub": "30 minutes on video to perfect your technique",
        "button": "Book a Call",
        "checkout_title": "1:1 Form Check & Strategy Call",
        "desc": "Stop guessing whether your form is right. Send me videos of up to five lifts before the call, then we'll meet for 30 minutes on video. I'll break down your technique, give you the cues that fix it and build a plan for your next 4–8 weeks.",
        "bullets": ["30-minute 1:1 video call", "Review of up to 5 lift videos before the call", "Personalized technique corrections and cues", "Custom next-steps plan for your goals", "Call recording to rewatch"],
        "cta": "Book My Call",
        "bump": None,
        "thanks": "You're booked! Reply to your confirmation email with up to 5 lift videos (side angle is best) at least 24 hours before the call.",
    },
    {
        "kind": "Membership / Application", "price": "$149/mo", "strike": "",
        "thumb_title": "1:1 Online Coaching", "thumb_sub": "Custom training, nutrition & weekly check-ins",
        "button": "Apply Now",
        "checkout_title": "1:1 Online Coaching with Danielle",
        "desc": "For women who are ready to stop starting over. You get a fully custom training program built around your body, schedule and gym; personalized macros; weekly check-ins with adjustments; unlimited form reviews; and direct messaging access to me. I keep my client roster small so every client gets real attention, so please apply.",
        "bullets": ["Custom program updated every 4 weeks", "Personalized macros and nutrition guidance", "Weekly check-ins and adjustments", "Unlimited form-check videos", "Direct messaging access", "All 5 Get Fit With Me programs included"],
        "cta": "Apply for Coaching",
        "bump": None,
        "thanks": "Application received. I personally review every one and will be in touch within 48 hours.",
    },
]

LAUNCH = {
    "captions": [
        "You asked what I do for my glutes, so I wrote it all down. The Glute Specialist Program is live: 8 weeks, 32 workouts, a full training handbook and an app that tracks every set. Start with the free Glute Starter Guide in my bio. #getfitwithme #glutes #womenwholift",
        "75 lb dumbbell press. Six weeks ago that felt impossible. Press Like A Boss is the exact program and technique breakdown, and it's live now. Link in bio. #strongwomen #upperbody",
        "If gym anxiety has ever made you walk in and walk right back out, this one's for you. The Gym Girl Confidence Kit covers the layout, the equipment, the etiquette and exactly what to say. Link in bio.",
        "30 days. One short workout, four habits and a journal prompt every day. Comment CHALLENGE and I'll send you the link.",
    ],
    "story": [
        "Slide 1: video of you lifting. Text: \"You've been asking for months...\"",
        "Slide 2: screen recording scrolling through an app. Text: \"It's finally here.\"",
        "Slide 3: poll. \"What do you need most? Glutes / Upper body / Nutrition / Confidence\"",
        "Slide 4: \"Start free\" + link sticker to the Glute Starter Guide",
        "Slide 5: \"Launch week: the Complete Collection is $67\" + link sticker",
        "Slide 6: countdown sticker for the end of the launch price (72 hours)",
    ],
    "dm_keywords": "Pin a Reel that says \"Comment GLUTES for my free workout guide.\" Send everyone who comments the Glute Starter Guide link. Stan's AutoDM feature can do this automatically.",
}
