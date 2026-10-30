# Get Fit With Me — all product content + Stan store copy lives here.
# Edit this file, then run:  python3 getfitwithme/_build/build.py

COACH = "Danielle Dawson"
BRAND = "Get Fit With Me"
HANDLE = "@getfitwithme"  # swap for your real handle

STORE = {
    "name": BRAND,
    "bio": "Hey baddie, I'm Danielle 💪🏽 Online fitness coach | Heavy weights, real results & zero gym anxiety. "
           "Programs, meal plans & coaching to help you get STRONG, snatched & confident. Let's get fit together 👇🏽",
    "tagline": "Lift heavy. Glow loud. Get fit with me.",
}

# ---------------------------------------------------------------- exercise tips
TIPS = {
    "Barbell Hip Thrust": "Upper back on the bench edge, bar on a pad over your hips. Chin tucked, ribs down, drive through your heels and squeeze at the top for 1–2 sec. Shins vertical at lockout.",
    "Romanian Deadlift": "Soft knees, push your hips BACK like closing a car door with your booty. Bar/dumbbells slide down your thighs. Stop when you feel a big hamstring stretch, then squeeze glutes to stand.",
    "Bulgarian Split Squat": "Back foot on the bench, front foot far enough forward that you can lean your torso slightly. Lower straight down; drive through the front heel. More lean = more glutes.",
    "Cable Kickback": "Ankle strap on, hinge forward slightly, hold the machine. Kick back AND slightly out — don't arch your lower back. Squeeze, pause, control it back.",
    "Hip Abduction Machine": "Lean forward over the seat and grab the sides for more glute med. Push out, pause, control in. Last set: do partial reps until it burns.",
    "DB Chest Press": "Shoulder blades pinched and tucked into the bench, feet planted. Lower dumbbells to chest level with elbows ~45°, press up and slightly in. Kick the dumbbells up with your knees to get set.",
    "Lat Pulldown": "Lean back slightly, chest up. Pull the bar to your upper chest by driving elbows DOWN into your back pockets. Don't yank with your arms.",
    "Seated Cable Row": "Sit tall, pull the handle to your belly button, squeeze your shoulder blades together like holding a pencil between them.",
    "DB Shoulder Press": "Sit tall with your back on the pad. Press dumbbells up and slightly in, don't flare the ribs. Lower to ear level.",
    "Lateral Raise": "Light weight, slight bend in the elbows. Lead with your elbows, raise to shoulder height. Think 'pouring water out of a pitcher' at the top.",
    "Tricep Rope Pushdown": "Elbows glued to your sides. Push down and split the rope apart at the bottom. Control it back up.",
    "Smith Machine Squat": "Feet slightly in front of the bar, a little wider than hips. Sit back and down, keep your chest proud, drive through your whole foot.",
    "Lying Hamstring Curl": "Hips pressed into the pad, curl your heels to your booty, slow 3-second lower.",
    "Walking Lunges": "Long steps, front shin stays fairly vertical, back knee kisses the floor. Push through the front heel.",
    "45° Back Extension": "Pad below your hip bones, round your upper back slightly and tuck your chin — this keeps it GLUTES, not lower back. Squeeze to lift.",
    "Frog Pumps": "Lie on your back, soles of the feet together, knees out. Drive hips up fast and squeeze. High reps = maximum pump.",
    "Sumo Deadlift": "Wide stance, toes out, hands inside your knees. Chest up, push the floor away and squeeze your glutes to lock out.",
    "Step-Ups": "Use a box or bench at knee height. Drive through the heel of the top leg — don't push off the bottom foot.",
    "Single-Leg Hip Thrust": "Same setup as hip thrust, one foot planted. Keep hips level and squeeze hard at the top.",
    "Weighted Plank": "Elbows under shoulders, squeeze glutes and pull belly button in. Add a plate on your back when you're ready.",
    "Hanging Knee Raise": "Hang from the bar, curl your knees toward your chest by tucking your pelvis. No swinging.",
    "Goblet Squat": "Hold the dumbbell at your chest, elbows inside knees at the bottom. Sit between your hips, chest tall.",
    "Glute Bridge": "On your back, heels close to your booty. Drive hips up, squeeze 2 sec, lower with control.",
    "Banded Lateral Walk": "Band above your knees, quarter squat, step out wide and slow. Keep tension in the band the whole time.",
    "Dumbbell Kickback": "On all fours, dumbbell behind your knee. Kick your heel to the ceiling without arching your back.",
    "Fire Hydrants": "On all fours, lift your knee out to the side, keep hips square. Slow and controlled.",
    "Reverse Lunge": "Step back, lower until both knees are about 90°, push through the front heel to return.",
    "Single-Leg Glute Bridge": "One foot planted, other leg up. Drive up through the planted heel, keep hips level.",
    "Incline DB Press": "Bench at 30°. Same set-up as flat press: blades back and down, lower to upper chest, press up.",
    "Push-Ups": "Hands under shoulders, body in one straight line. Drop to your knees when form breaks — that's still a rep!",
    "Bench Dips": "Hands on bench, legs out in front. Lower until elbows hit 90°, press up through your palms.",
    "Single-Arm DB Row": "Knee and hand on the bench, flat back. Pull the dumbbell to your hip, not your chest.",
    "Face Pulls": "Rope at face height. Pull toward your eyebrows, elbows high, and rotate your hands back like a double bicep pose.",
    "Rear Delt Fly": "Hinge forward, light dumbbells, slight elbow bend. Open your arms wide like a hug in reverse.",
    "Hammer Curl": "Palms facing each other, elbows still. Curl up, slow lower.",
    "Paused DB Bench Press": "Same as DB press but pause 2 sec at the bottom. Builds power off your chest — the secret to heavier presses.",
    "Machine Chest Press": "Adjust the seat so handles line up with mid-chest. Press, don't lock out hard, control the return.",
    "Cable Fly": "Slight bend in the elbows, bring hands together like hugging a tree. Squeeze your chest at the middle.",
    "Arnold Press": "Start palms facing you at chin level, rotate as you press overhead. Reverse on the way down.",
    "Overhead Tricep Extension": "Hold one dumbbell with both hands overhead. Lower behind your head, elbows pointing forward, press up.",
    "Leg Press": "Feet high and wide on the platform for more glutes. Lower until your hips want to tuck, then press through your heels.",
    "Treadmill Incline Walk": "Incline 8–12, speed 2.8–3.3. No holding the rails, baddie.",
}

# ---------------------------------------------------------------- programs
def build_program(days, phases):
    """days: list of (name, focus, [(exercise, role, per_side)])
    phases: list of week dicts {name, phase, note, scheme:{role:(sets, reps, rest)}}"""
    weeks = []
    for ph in phases:
        wdays = []
        for name, focus, exs in days:
            ex = []
            for n, role, side in exs:
                s, r, rest = ph["scheme"][role]
                ex.append({"n": n, "s": s, "r": r + (" /side" if side and "side" not in r else ""),
                           "rest": rest, "tip": TIPS.get(n, "")})
            wdays.append({"name": name, "focus": focus, "ex": ex})
        weeks.append({"name": ph["name"], "phase": ph["phase"], "note": ph["note"], "days": wdays})
    return weeks

BOOTY_DAYS = [
    ("Day 1 · Glute Strength", "Heavy hips. Big lifts. Main-character energy.", [
        ("Barbell Hip Thrust", "main", False), ("Romanian Deadlift", "main", False),
        ("Bulgarian Split Squat", "acc", True), ("Cable Kickback", "acc", True), ("Hip Abduction Machine", "fin", False)]),
    ("Day 2 · Upper Body Sculpt", "Snatched back, sculpted shoulders, strong arms.", [
        ("DB Chest Press", "main", False), ("Lat Pulldown", "main", False), ("Seated Cable Row", "acc", False),
        ("DB Shoulder Press", "acc", False), ("Lateral Raise", "acc", False), ("Tricep Rope Pushdown", "fin", False)]),
    ("Day 3 · Glute & Hamstring Pump", "Chase the pump. Feel every single rep.", [
        ("Smith Machine Squat", "main", False), ("Lying Hamstring Curl", "acc", False), ("Walking Lunges", "acc", True),
        ("45° Back Extension", "acc", False), ("Frog Pumps", "fin", False)]),
    ("Day 4 · Lower Burn + Core", "Legs, booty and a core that holds it all together.", [
        ("Sumo Deadlift", "main", False), ("Step-Ups", "acc", True), ("Single-Leg Hip Thrust", "acc", True),
        ("Leg Press", "acc", False), ("Weighted Plank", "fin", False), ("Hanging Knee Raise", "fin", False)]),
]
BOOTY_PHASES = [
    {"name": "Week 1", "phase": "FOUNDATION", "note": "Learn the moves, find your weights. Leave 2–3 reps in the tank.",
     "scheme": {"main": (3, "12", "90s"), "acc": (3, "12–15", "60s"), "fin": (2, "20 / 30s", "45s")}},
    {"name": "Week 2", "phase": "FOUNDATION", "note": "Same reps, slightly heavier than Week 1. Write your weights down!",
     "scheme": {"main": (3, "12", "90s"), "acc": (3, "12–15", "60s"), "fin": (2, "20 / 30s", "45s")}},
    {"name": "Week 3", "phase": "BUILD", "note": "Extra set on your main lifts. 1–2 reps left in the tank.",
     "scheme": {"main": (4, "10", "2 min"), "acc": (3, "12", "60s"), "fin": (3, "20 / 40s", "45s")}},
    {"name": "Week 4", "phase": "BUILD", "note": "Beat last week: +5 lbs or +1 rep on every main lift.",
     "scheme": {"main": (4, "10", "2 min"), "acc": (3, "12", "60s"), "fin": (3, "20 / 40s", "45s")}},
    {"name": "Week 5", "phase": "STRENGTH", "note": "Heavier, fewer reps. Rest longer. This is where the shape comes in.",
     "scheme": {"main": (4, "6–8", "2.5 min"), "acc": (3, "10–12", "75s"), "fin": (3, "20 / 45s", "45s")}},
    {"name": "Week 6", "phase": "STRENGTH", "note": "Push the main lifts. Film a set and check your form 🎥",
     "scheme": {"main": (4, "6–8", "2.5 min"), "acc": (3, "10–12", "75s"), "fin": (3, "20 / 45s", "45s")}},
    {"name": "Week 7", "phase": "PEAK", "note": "Heaviest week. Hype music ON. Spotter if you need one.",
     "scheme": {"main": (5, "5", "3 min"), "acc": (3, "10", "75s"), "fin": (3, "Burnout", "60s")}},
    {"name": "Week 8", "phase": "SHOW-OFF WEEK", "note": "Work up to a heavy 5 on your main lifts and log your PRs. Then retake your progress pics 📸",
     "scheme": {"main": (4, "Build to heavy 5", "3 min"), "acc": (3, "12", "60s"), "fin": (2, "Drop set", "60s")}},
]

PRESS_DAYS = [
    ("Day 1 · Heavy Push", "The money day. Heavy dumbbells, full confidence.", [
        ("DB Chest Press", "main", False), ("Incline DB Press", "main", False), ("DB Shoulder Press", "acc", False),
        ("Bench Dips", "acc", False), ("Push-Ups", "fin", False)]),
    ("Day 2 · Pull + Posture", "A strong back = a stronger press. Period.", [
        ("Lat Pulldown", "main", False), ("Single-Arm DB Row", "main", True), ("Face Pulls", "acc", False),
        ("Rear Delt Fly", "acc", False), ("Hammer Curl", "fin", False)]),
    ("Day 3 · Volume Push", "Lighter weight, more reps, slow and strong.", [
        ("Paused DB Bench Press", "main", False), ("Machine Chest Press", "acc", False), ("Cable Fly", "acc", False),
        ("Arnold Press", "acc", False), ("Overhead Tricep Extension", "fin", False)]),
]
PRESS_PHASES = [
    {"name": "Week 1", "phase": "FOUNDATION", "note": "Pick a weight you can press 12 times. Do 10 clean reps.",
     "scheme": {"main": (3, "10", "2 min"), "acc": (3, "12", "60s"), "fin": (2, "AMRAP", "60s")}},
    {"name": "Week 2", "phase": "FOUNDATION", "note": "Go up 5 lbs per dumbbell if every rep was clean.",
     "scheme": {"main": (3, "10", "2 min"), "acc": (3, "12", "60s"), "fin": (2, "AMRAP", "60s")}},
    {"name": "Week 3", "phase": "BUILD", "note": "Heavier and an extra set. Kick the dumbbells up with your knees.",
     "scheme": {"main": (4, "8", "2.5 min"), "acc": (3, "10", "75s"), "fin": (3, "AMRAP", "60s")}},
    {"name": "Week 4", "phase": "BUILD", "note": "+1 rep or +5 lbs from last week. Every. Single. Week.",
     "scheme": {"main": (4, "8", "2.5 min"), "acc": (3, "10", "75s"), "fin": (3, "AMRAP", "60s")}},
    {"name": "Week 5", "phase": "STRENGTH", "note": "Heavy fives. Get a spotter or film it.",
     "scheme": {"main": (5, "5", "3 min"), "acc": (3, "8–10", "90s"), "fin": (2, "AMRAP", "60s")}},
    {"name": "Week 6", "phase": "PR WEEK 👑", "note": "Work up to a heavy 3 on Day 1 and log it in your PR Wall. Then POST IT and tag me.",
     "scheme": {"main": (4, "Build to heavy 3", "3 min"), "acc": (2, "10", "90s"), "fin": (1, "AMRAP", "60s")}},
]

STARTER_DAYS = [
    ("Workout A · Glute Wake-Up", "Get your glutes firing. Perfect for home or gym.", [
        ("Glute Bridge", "acc", False), ("Banded Lateral Walk", "acc", True), ("Goblet Squat", "main", False),
        ("Romanian Deadlift", "main", False), ("Dumbbell Kickback", "acc", True)]),
    ("Workout B · Booty Builder Lite", "A sneak peek of the full 8-week program.", [
        ("Barbell Hip Thrust", "main", False), ("Bulgarian Split Squat", "acc", True), ("Cable Kickback", "acc", True),
        ("Hip Abduction Machine", "acc", False), ("Frog Pumps", "fin", False)]),
    ("Workout C · Lower Body Burn", "Legs + booty + sweat.", [
        ("Sumo Deadlift", "main", False), ("Step-Ups", "acc", True), ("Single-Leg Glute Bridge", "acc", True),
        ("Reverse Lunge", "acc", True), ("Fire Hydrants", "fin", True)]),
]
STARTER_PHASES = [{"name": "Your Free Week", "phase": "STARTER", "note": "Do A, B and C this week with a rest day between each. Track your weights so you can beat them next week.",
                   "scheme": {"main": (3, "10", "90s"), "acc": (3, "12", "60s"), "fin": (2, "20", "45s")}}]

CONF_DAYS = [
    ("Day 1 · Machines Only", "Zero pressure. Machines guide the movement for you.", [
        ("Leg Press", "acc", False), ("Lat Pulldown", "acc", False), ("Machine Chest Press", "acc", False),
        ("Lying Hamstring Curl", "acc", False), ("Hip Abduction Machine", "acc", False), ("Treadmill Incline Walk", "fin", False)]),
    ("Day 2 · Dumbbell Corner", "Grab a set of dumbbells + a bench and claim your spot.", [
        ("Goblet Squat", "acc", False), ("DB Chest Press", "acc", False), ("Single-Arm DB Row", "acc", True),
        ("Romanian Deadlift", "acc", False), ("DB Shoulder Press", "acc", False)]),
    ("Day 3 · Cable Queen", "Cables look scary. They're not. Let's go.", [
        ("Cable Kickback", "acc", True), ("Seated Cable Row", "acc", False), ("Face Pulls", "acc", False),
        ("Tricep Rope Pushdown", "acc", False), ("Glute Bridge", "acc", False), ("Treadmill Incline Walk", "fin", False)]),
]
CONF_PHASES = [
    {"name": "Week 1", "phase": "JUST SHOW UP", "note": "Light weights. The only goal is to walk in, do the thing and leave proud.",
     "scheme": {"main": (2, "12", "90s"), "acc": (2, "12", "60s"), "fin": (1, "10 min", "—")}},
    {"name": "Week 2", "phase": "OWN THE ROOM", "note": "Add a set and go a little heavier. You belong here.",
     "scheme": {"main": (3, "12", "90s"), "acc": (3, "12", "60s"), "fin": (1, "15 min", "—")}},
]

# ---------------------------------------------------------------- 30-day challenge
def build_challenge():
    T = {
        "Glutes": [("Glute bridges", 15, ""), ("Donkey kicks", 12, " /side"), ("Fire hydrants", 12, " /side"), ("Sumo squats", 15, ""), ("Frog pumps", 20, "")],
        "Upper Body": [("Push-ups (knees are fine!)", 8, ""), ("Tricep dips", 10, ""), ("Shoulder taps", 16, ""), ("Plank up-downs", 8, ""), ("Superman pulls", 12, "")],
        "Core + Cardio": [("Mountain climbers", 20, ""), ("Bicycle crunches", 20, ""), ("Plank", 30, "s"), ("Leg raises", 10, ""), ("Jumping jacks", 30, "")],
        "Legs": [("Squats", 15, ""), ("Reverse lunges", 10, " /side"), ("Wall sit", 30, "s"), ("Calf raises", 20, ""), ("Squat jumps", 8, "")],
        "Full Body Burn": [("Burpees", 6, ""), ("Squat to press (dumbbells or water bottles)", 12, ""), ("Walking lunges", 10, " /side"), ("Push-ups", 8, ""), ("High knees", 30, "s")],
    }
    recovery = [("Walk outside", "20–30 min"), ("Hip flexor stretch", "45s /side"), ("Pigeon stretch", "45s /side"), ("Cat-cow", "10 slow reps"), ("Child's pose", "60s")]
    reset = [("Sleep 7–9 hours tonight", "💤"), ("Meal prep 3 meals for the week", "🍱"), ("10-min full body stretch", "🧘🏽‍♀️"), ("Take your weekly progress pic", "📸")]
    order = ["Glutes", "Upper Body", "Core + Cardio", "Legs", "Full Body Burn", "Active Recovery", "Rest & Reset"]
    prompts = [
        "Why did you REALLY start this challenge? Write it down — you'll need it on Day 12.",
        "Name 3 things your body did for you today.",
        "What's one excuse you're officially retiring this month?",
        "Describe how you want to FEEL walking into the gym on Day 30.",
        "Who are you doing this for? (The answer should be you.)",
        "What did you eat today that fueled you? What would you swap?",
        "Rest is productive. How are you recharging today?",
        "What's one rep, set or move that felt easier than Day 1?",
        "Write a hype message to yourself for your hardest day.",
        "What does 'strong' mean to you?",
        "Rate your energy 1–10. What helped or hurt it today?",
        "What song gets you through the last set? Add 5 to a playlist today.",
        "Name a woman whose strength inspires you, and why.",
        "Rest day reflection: what are you most proud of from week 2?",
        "Halfway there! What's changed — physically AND mentally?",
        "What would you tell Day-1 you?",
        "What's your non-scale victory this week?",
        "Where do you still hold back? Why?",
        "How are you speaking to yourself in the mirror lately?",
        "Plan your Day 30 celebration. Make it extra.",
        "Rest day: write 5 things you love about your body.",
        "What habit from this challenge are you keeping forever?",
        "Who noticed your glow-up? How did that feel?",
        "What's a goal that felt impossible a month ago but doesn't now?",
        "If you could only do one move for the rest of your life, what would it be?",
        "What will 'Get Fit With Me' look like for you NEXT month?",
        "Write a thank-you note to your body.",
        "What does the girl who finishes this challenge believe about herself?",
        "Final Boss tomorrow. How are you preparing mentally?",
        "YOU DID IT. Compare Day 1 vs Day 30 — photos, energy, mindset. Write it all down. 👑",
    ]
    days = []
    for i in range(30):
        wk = i // 7
        kind = order[i % 7]
        rounds = [3, 3, 4, 4, 4][wk]
        mult = 1 + 0.25 * wk
        if i == 28:
            kind, ex = "Final Boss 🔥", [(n, f"{round(r * 1.75)}{u}") for k in ("Glutes", "Legs", "Full Body Burn") for n, r, u in T[k][:2]]
            rounds = 3
        elif i == 29:
            kind, ex, rounds = "Show-Off Day 👑", [("Redo the Day 1 workout and compare", "📝"), ("Retake your progress photos", "📸"), ("Post your glow-up & tag me", "💜")], 0
        elif kind == "Active Recovery":
            ex, rounds = recovery, 0
        elif kind == "Rest & Reset":
            ex, rounds = reset, 0
        else:
            ex = [(n, f"{round(r * mult)}{u}") for n, r, u in T[kind]]
        days.append({"t": kind, "rounds": rounds, "ex": [{"n": n, "r": r} for n, r in ex], "prompt": prompts[i]})
    return days

# ---------------------------------------------------------------- meal plan
MEALS = [
    {"name": "Mon", "meals": [("Breakfast", "Protein oats: ½ cup oats, 1 scoop vanilla protein, berries, 1 tbsp PB", 32),
                              ("Lunch", "Chicken burrito bowl: rice, black beans, grilled chicken, pico, lettuce, light cheese", 42),
                              ("Snack", "Greek yogurt + honey + granola sprinkle", 18),
                              ("Dinner", "Air-fryer salmon, roasted sweet potato, garlic green beans", 36)]},
    {"name": "Tue", "meals": [("Breakfast", "3 eggs + 2 egg whites scrambled w/ spinach, 1 slice toast, fruit", 30),
                              ("Lunch", "Turkey & avocado wrap + side salad", 34),
                              ("Snack", "Protein shake + banana (post-workout)", 26),
                              ("Dinner", "Lean beef taco lettuce cups (or corn tortillas), salsa, rice", 40)]},
    {"name": "Wed", "meals": [("Breakfast", "Cottage cheese pancakes (oats + cottage cheese + egg) w/ berries", 30),
                              ("Lunch", "Leftover beef tacos as a bowl", 38),
                              ("Snack", "String cheese + apple + 10 almonds", 10),
                              ("Dinner", "Shrimp stir-fry with mixed veggies & jasmine rice", 34)]},
    {"name": "Thu", "meals": [("Breakfast", "Overnight protein oats (prepped Sunday)", 30),
                              ("Lunch", "Chicken Caesar wrap (Greek yogurt dressing)", 40),
                              ("Snack", "Rice cakes + PB + protein shake", 30),
                              ("Dinner", "Turkey meatballs, marinara, pasta or zucchini noodles", 38)]},
    {"name": "Fri", "meals": [("Breakfast", "Egg bites (3) + turkey sausage + fruit", 32),
                              ("Lunch", "Tuna salad (Greek yogurt) on whole grain + cucumbers", 34),
                              ("Snack", "Beef jerky + grapes", 15),
                              ("Dinner", "FUN MEAL 🍔 — enjoy it, no guilt, protein first", 30)]},
    {"name": "Sat", "meals": [("Breakfast", "Protein waffles + Greek yogurt + strawberries", 35),
                              ("Lunch", "Grilled chicken salad w/ quinoa, feta, cucumber, lemon vinaigrette", 40),
                              ("Snack", "Protein shake + a handful of trail mix", 28),
                              ("Dinner", "Jerk chicken, rice & peas (½ cup), cabbage", 42)]},
    {"name": "Sun", "meals": [("Breakfast", "Breakfast burrito: eggs, egg whites, potatoes, turkey bacon, salsa", 38),
                              ("Lunch", "Leftover jerk chicken bowl", 40),
                              ("Snack", "Greek yogurt parfait", 18),
                              ("Dinner", "Meal-prep night: sheet-pan chicken, broccoli & potatoes", 40)]},
]

GROCERY = [
    {"title": "🍗 Protein", "items": ["Chicken breast / thighs (3 lbs)", "93% lean ground beef or turkey (2 lbs)", "Salmon fillets", "Shrimp (frozen)", "Eggs (2 dozen) + liquid egg whites", "Greek yogurt (big tub)", "Cottage cheese", "Tuna packets", "Turkey slices + turkey bacon", "Protein powder", "Beef jerky", "String cheese"]},
    {"title": "🍚 Carbs", "items": ["Old-fashioned oats", "Jasmine rice", "Sweet potatoes + white potatoes", "Whole-grain bread / wraps", "Corn tortillas", "Rice cakes", "Pasta", "Quinoa", "Black beans + kidney beans"]},
    {"title": "🥦 Produce", "items": ["Spinach + mixed greens", "Broccoli", "Green beans", "Zucchini", "Bell peppers + onions", "Cucumbers", "Avocados", "Berries", "Bananas + apples", "Lemons / limes", "Cabbage"]},
    {"title": "🥑 Fats & Flavor", "items": ["Peanut butter", "Almonds / trail mix", "Feta + shredded cheese", "Olive oil spray", "Salsa + pico", "Marinara", "Jerk seasoning", "Hot honey (trust me)"]},
]

# ---------------------------------------------------------------- products
WELCOME = ("<p>Hey baddie! 💜 It's Danielle. First of all — I'm SO proud of you for investing in yourself. "
           "This isn't a PDF you'll forget in your downloads. It's an interactive app: tap things, track things, "
           "and watch yourself get stronger.</p>"
           "<p><b>How to use it:</b> Add this page to your home screen (Share → Add to Home Screen) so it lives on your phone like an app. "
           "Everything you check off and every weight you log saves automatically on this device.</p>")

DISCLAIMER = ("This program is for educational purposes and is not medical advice. Check with your doctor before starting a new "
              "exercise or nutrition plan, especially if you're pregnant, injured or have a medical condition. Stop any exercise that causes pain.")

PRODUCTS = [
    {
        "slug": "glute-starter-pack-free-g7f2", "short": "Free Glute Starter Pack",
        "title": "The Glute Starter Pack", "script": "free gift", "emoji": "🍑",
        "sub": "3 booty workouts to start your glow-up TODAY",
        "c1": "#ff2e93", "c2": "#8b2cf5",
        "sections": [
            {"type": "intro", "id": "start", "label": "Start Here", "icon": "💜", "html": WELCOME +
             "<p>This is a FREE taste of how I train. 3 workouts, one week. Do them, track them, and DM me “STARTER” on Instagram when you finish so I can hype you up.</p>"},
            {"type": "program", "id": "wk", "label": "Workouts", "icon": "🍑", "weeks": build_program(STARTER_DAYS, STARTER_PHASES)},
            {"type": "cards", "id": "rules", "label": "Glute Rules", "icon": "📏", "items": [
                {"i": "🧠", "t": "Mind-muscle connection", "d": "Before each set, squeeze your glute for 3 seconds. You'll feel the difference immediately."},
                {"i": "⏸️", "t": "Pause at the top", "d": "Every hip thrust and bridge gets a 1–2 second squeeze. No bouncing."},
                {"i": "📈", "t": "Progressive overload", "d": "Next week, beat this week: +5 lbs or +1 rep. That's how the booty grows."},
                {"i": "🍗", "t": "Eat your protein", "d": "Aim for ~0.8g per lb of your goal body weight. Muscles are built in the kitchen too."}]},
            {"type": "upsell", "id": "next", "label": "What's Next", "icon": "👑"},
        ],
        "stan": {
            "kind": "Lead Magnet (Free)", "price": "FREE", "strike": "",
            "thumb_title": "FREE Glute Starter Pack 🍑", "thumb_sub": "3 booty workouts you can start TODAY",
            "button": "Send It To Me 💌",
            "checkout_title": "Get My FREE Glute Starter Pack 🍑",
            "desc": "Want to grow your glutes but don't know where to start? I got you, baddie. This is the exact way I train — packed into 3 workouts you can start TODAY. Track every set right from your phone. No boring PDF, no guessing. Just drop your email and it's yours.",
            "bullets": ["3 glute-focused workouts (gym or home with dumbbells)", "Interactive tracker — tap off sets & log your weights", "Built-in rest timer so you never lose count", "Form tips for every single exercise", "My 4 non-negotiable Glute Rules"],
            "cta": "GIVE ME THE BOOTY PLAN 🍑",
            "bump": None,
            "thanks": "Check your email, baddie! 💌 Your Glute Starter Pack is on the way. Screenshot your first workout and tag me — I WILL repost you.",
        },
    },
    {
        "slug": "30-day-get-fit-challenge-c9x4", "short": "30-Day Get Fit With Me Challenge",
        "title": "30-Day Get Fit With Me Challenge", "script": "the glow-up starts now", "emoji": "🔥",
        "sub": "30 days. Daily workouts, habits & mindset. Let's GO.",
        "c1": "#ff7a18", "c2": "#ff2e93",
        "sections": [
            {"type": "intro", "id": "start", "label": "Start Here", "icon": "💜", "html": WELCOME +
             "<p>Every day you'll get a 20–30 minute workout (home or gym, dumbbells optional), 4 daily habits and a mindset prompt. Check off all 4 habits to complete the day and build your streak 🔥</p>"
             "<p><b>Day 1 homework:</b> take front, side and back photos. Day-30 you is going to want them.</p>"},
            {"type": "challenge", "id": "ch", "label": "Challenge", "icon": "🔥",
             "tasks": ["🏋🏽‍♀️ Did today's workout", "💧 Drank 80+ oz of water", "👟 Hit 8,000 steps", "🍗 Protein at every meal"],
             "days": build_challenge()},
            {"type": "pr", "id": "pr", "label": "Measurements", "icon": "📏", "metric": True,
             "lifts": ["Weight", "Waist", "Hips", "Booty", "Thigh", "Arm"], "unit": "lbs / in"},
            {"type": "upsell", "id": "next", "label": "What's Next", "icon": "👑"},
        ],
        "stan": {
            "kind": "Digital Product", "price": "$14.99", "strike": "$29",
            "thumb_title": "30-Day Get Fit With Me Challenge 🔥", "thumb_sub": "Daily workouts + habits + mindset. Glow-up guaranteed.",
            "button": "Join The Challenge 🔥",
            "checkout_title": "The 30-Day Get Fit With Me Challenge",
            "desc": "You keep saying “I'm starting Monday.” Babe… THIS is your Monday. For 30 days, you and me are getting it IN — quick daily workouts you can do at home or the gym, 4 simple habits that change EVERYTHING, and a daily mindset prompt so your head glows up with your body. Check off your day, watch your streak grow, and feel yourself become HER.",
            "bullets": ["30 days of 20–30 min workouts that level up every week", "Daily habit tracker with streaks + confetti (yes, really 🎉)", "30 mindset journal prompts", "Built-in workout timer", "Measurement tracker to see your progress", "Final Boss workout + Show-Off Day 👑", "Works on any phone — no app download"],
            "cta": "I'M IN — LET'S GET FIT 🔥",
            "bump": {"title": "Add Fuel Like A Baddie for just $9 (reg. $19)", "desc": "Get my 7-day high-protein meal plan, grocery list & macro calculator so your nutrition matches your effort."},
            "thanks": "WELCOME TO THE CHALLENGE 🔥 Your link is in your email. Add it to your home screen, take your Day 1 pics and post a story tagging me with #GetFitWithMeChallenge!",
        },
    },
    {
        "slug": "booty-builder-8-week-b3k8", "short": "Glute Specialist: 8-Week Booty Builder",
        "title": "8-Week Booty Builder", "script": "glute specialist", "emoji": "🍑",
        "sub": "My signature 4-day gym program to grow & lift your glutes",
        "c1": "#ff2e93", "c2": "#b0173d",
        "sections": [
            {"type": "intro", "id": "start", "label": "Start Here", "icon": "💜", "html": WELCOME +
             "<p>This is my SIGNATURE program — the way I train my own glutes. 4 days a week, 8 weeks, 4 phases: <b>Foundation → Build → Strength → Peak</b>. "
             "Every week the sets, reps and rest change automatically. Your only job: show up, log your weights, and beat last week.</p>"
             "<p><b>Suggested schedule:</b> Mon Day 1 · Tue Day 2 · Thu Day 3 · Sat Day 4.</p>"},
            {"type": "program", "id": "prog", "label": "Program", "icon": "🏋🏽‍♀️", "weeks": build_program(BOOTY_DAYS, BOOTY_PHASES)},
            {"type": "pr", "id": "pr", "label": "PR Wall", "icon": "👑",
             "lifts": ["Barbell Hip Thrust", "Romanian Deadlift", "Sumo Deadlift", "Smith Machine Squat", "DB Chest Press", "Lat Pulldown"], "unit": "lbs"},
            {"type": "cards", "id": "rules", "label": "Glute Science", "icon": "🧠", "items": [
                {"i": "📈", "t": "Progressive overload", "d": "Muscles grow when you ask them to do MORE over time. +5 lbs or +1 rep every week is the whole secret."},
                {"i": "🍑", "t": "3 glute muscles", "d": "Glute max (hip thrusts, RDLs), glute med & min (abductions, kickbacks). This program hits all three."},
                {"i": "⏱️", "t": "Rest is part of the set", "d": "Heavy lifts need 2–3 min rest. Use the timer. Scrolling for 7 minutes doesn't count 😂"},
                {"i": "🍗", "t": "Fuel the growth", "d": "Eat at maintenance or a small surplus with ~0.8g protein per lb. You can't build a booty on salad alone."},
                {"i": "😴", "t": "Sleep = gains", "d": "7–9 hours. That's when your muscles actually repair and grow."},
                {"i": "📸", "t": "Track, don't guess", "d": "Photos every 2 weeks, same lighting, same angle. The mirror lies — the log doesn't."}]},
            {"type": "upsell", "id": "next", "label": "What's Next", "icon": "👑"},
        ],
        "stan": {
            "kind": "Digital Product", "price": "$37", "strike": "$67",
            "thumb_title": "8-Week Booty Builder 🍑", "thumb_sub": "My signature glute program — the one everybody asks for",
            "button": "Build My Booty 🍑",
            "checkout_title": "Glute Specialist: The 8-Week Booty Builder",
            "desc": "Y'all ask me EVERY day “what do you do for your glutes?” This is it. My full signature program — 4 days a week, 8 weeks, built in 4 phases so your body never gets bored and never stops growing. Every set, rep, rest time and form tip is laid out for you in an app-style tracker right on your phone. Walk into the gym knowing EXACTLY what to do. No more copying random TikTok workouts and hoping for the best.",
            "bullets": ["8 weeks · 4 workouts/week · 4 progressive phases", "32 done-for-you workouts that auto-progress each week", "Log your weight for every exercise + tap off every set", "Form tips for all 25+ exercises", "Built-in rest timer with alarm", "PR Wall to track your strongest lifts 👑", "Includes upper body day so you're snatched head to toe"],
            "cta": "START BUILDING 🍑",
            "bump": {"title": "Add the PR Press Program for $15 (reg. $24)", "desc": "Want to chest press 75s like me? Add my 6-week upper body strength program."},
            "thanks": "Ayyyye welcome to the Booty Builder 🍑 Your program link is in your email. Save it to your home screen, start Week 1, and tag me in your first hip thrust video!",
        },
    },
    {
        "slug": "press-like-a-boss-p5m1", "short": "Press Like A Boss",
        "title": "Press Like A Boss", "script": "75 lbs & counting", "emoji": "💪🏽",
        "sub": "6-week upper body strength program for women",
        "c1": "#8b2cf5", "c2": "#3b82f6",
        "sections": [
            {"type": "intro", "id": "start", "label": "Start Here", "icon": "💜", "html": WELCOME +
             "<p>Y'all saw me chest press 70s and 75s 😤 This is how I got there. 3 upper days a week for 6 weeks: one heavy push day, one pull day for a strong back and posture, and one volume day. "
             "Week 6 is PR Week — you're going to work up to the heaviest press of your LIFE and log it on the PR Wall.</p>"
             "<p><b>Pair it with:</b> the 8-Week Booty Builder lower days for a full split, or do it on its own.</p>"},
            {"type": "program", "id": "prog", "label": "Program", "icon": "💪🏽", "weeks": build_program(PRESS_DAYS, PRESS_PHASES)},
            {"type": "pr", "id": "pr", "label": "PR Wall", "icon": "👑",
             "lifts": ["DB Chest Press (per DB)", "Incline DB Press (per DB)", "DB Shoulder Press (per DB)", "Lat Pulldown", "Single-Arm DB Row"], "unit": "lbs"},
            {"type": "accordion", "id": "faq", "label": "Press Secrets", "icon": "🤫", "items": [
                {"q": "How do I get heavy dumbbells into position?", "a": "Sit on the end of the bench with the dumbbells standing on your thighs. As you lie back, kick one knee up at a time to pop each dumbbell to your chest. Reverse it to put them down — never drop them out to the side."},
                {"q": "Will lifting heavy make me bulky?", "a": "No, babe. Women build muscle slowly. Heavy lifting makes you strong, toned, and snatched. 'Bulky' takes years of intentional eating and training."},
                {"q": "My press is stuck. Now what?", "a": "1) Make sure you're eating enough protein. 2) Sleep 7+ hours. 3) Do the paused presses on Day 3 seriously. 4) Strengthen your back — Day 2 is not optional!"},
                {"q": "Should I use a spotter?", "a": "For Week 5–6 heavy sets, yes. Ask someone: “Can you spot me for one set? Just help if I get stuck.” Gym people LOVE being asked."},
                {"q": "How do I know when to go up in weight?", "a": "If you hit every rep of every set with good form, go up 5 lbs per dumbbell next session."}]},
            {"type": "upsell", "id": "next", "label": "What's Next", "icon": "👑"},
        ],
        "stan": {
            "kind": "Digital Product", "price": "$24", "strike": "$47",
            "thumb_title": "Press Like A Boss 💪🏽", "thumb_sub": "6 weeks to your strongest upper body ever",
            "button": "Get Strong 💪🏽",
            "checkout_title": "Press Like A Boss: 6-Week Upper Body Strength",
            "desc": "Y'all went CRAZY over my 70 & 75 lb chest press video 😤 So here's the exact plan. 6 weeks, 3 upper body days a week, built to make you STRONG — not bulky. Sculpted shoulders, a snatched back, toned arms and a chest press that makes the gym bros look twice. Week 6 is PR Week, and you're gonna surprise yourself.",
            "bullets": ["6-week progressive strength program (3 days/week)", "Heavy push, pull & volume days", "Weight logger + tap-off sets for every exercise", "PR Wall with automatic 1-rep-max estimate", "My secrets for getting heavy dumbbells into position", "Rest timer built in"],
            "cta": "LET'S PRESS 💪🏽",
            "bump": {"title": "Add the 8-Week Booty Builder for $25 (reg. $37)", "desc": "Complete your split with my signature lower-body & glute program."},
            "thanks": "Let's GO 💪🏽 Your program is in your email. Week 6 = PR week… film it and tag me, I want to SEE it!",
        },
    },
    {
        "slug": "fuel-like-a-baddie-f2q6", "short": "Fuel Like A Baddie",
        "title": "Fuel Like A Baddie", "script": "eat to get snatched", "emoji": "🍗",
        "sub": "High-protein meal plan, grocery list & macro calculator",
        "c1": "#22c55e", "c2": "#ff2e93",
        "sections": [
            {"type": "intro", "id": "start", "label": "Start Here", "icon": "💜", "html": WELCOME +
             "<p>You can't out-train your fork, babe. This kit takes the guessing out of eating for your goals: calculate your macros, follow the 7-day high-protein plan, shop with the checklist, and meal prep once on Sunday. "
             "No starving. No boring chicken-and-broccoli only. Real food with flavor.</p>"},
            {"type": "macro", "id": "macro", "label": "My Macros", "icon": "🧮"},
            {"type": "meals", "id": "meals", "label": "Meal Plan", "icon": "🍽️", "days": MEALS},
            {"type": "checklist", "id": "groc", "label": "Grocery List", "icon": "🛒", "groups": GROCERY},
            {"type": "checklist", "id": "prep", "label": "Sunday Prep", "icon": "🍱", "groups": [
                {"title": "⏰ 90-Minute Meal Prep", "items": ["Preheat oven to 425°F, start rice cooker", "Season & sheet-pan 3 lbs chicken (25 min)", "Roast potatoes & broccoli on a second pan", "Brown ground turkey/beef for tacos & meatballs", "Make 5 jars of overnight protein oats", "Bake egg bites in a muffin tin (12)", "Wash & chop veggies for the week", "Portion into containers & label the days", "Fill your water bottle + set tomorrow's gym bag 😉"]}]},
            {"type": "cards", "id": "snacks", "label": "Snack Menu", "icon": "🍓", "items": [
                {"i": "🥤", "t": "Protein shake + banana", "d": "~26g protein · perfect post-workout"},
                {"i": "🍓", "t": "Greek yogurt parfait", "d": "~18g protein · sweet tooth approved"},
                {"i": "🧀", "t": "String cheese + apple", "d": "~8g protein · throw-in-your-bag easy"},
                {"i": "🥩", "t": "Beef jerky + grapes", "d": "~15g protein · road trip queen"},
                {"i": "🍘", "t": "Rice cakes + PB", "d": "Pre-workout carbs that won't sit heavy"},
                {"i": "🥚", "t": "2 hard-boiled eggs", "d": "~12g protein · prep a dozen Sunday"},
                {"i": "🧁", "t": "Protein mug cake", "d": "1 scoop protein, 1 tbsp flour, ½ tsp baking powder, splash of milk — microwave 60s"},
                {"i": "🍫", "t": "Chocolate protein 'pudding'", "d": "Greek yogurt + chocolate protein powder, stir & chill"}]},
            {"type": "accordion", "id": "out", "label": "Eating Out", "icon": "🌮", "items": [
                {"q": "Chipotle", "a": "Bowl: double chicken, rice, fajita veggies, black beans, salsa, lettuce. Skip or go light on sour cream & cheese. ~60g protein."},
                {"q": "Chick-fil-A", "a": "12-count grilled nuggets + side salad or fruit cup. Or grilled chicken sandwich. Zesty Buffalo sauce is the lowest-cal flavor."},
                {"q": "Starbucks", "a": "Egg white & roasted red pepper egg bites + a protein box. Order your latte with protein cold foam."},
                {"q": "Wingstop / wings night", "a": "Plain or dry-rub wings (lemon pepper, garlic parm dry), veggie sticks, skip the ranch or get it on the side."},
                {"q": "Mexican restaurant", "a": "Fajitas! Load up on the protein and veggies, 2 tortillas, salsa & pico. Chips: pour a portion, push the basket away."},
                {"q": "Brunch with the girls", "a": "Omelet or eggs + side of turkey sausage, fruit, 1 pancake if you want it. Mimosa? Enjoy one. Balance > perfection."}]},
            {"type": "upsell", "id": "next", "label": "What's Next", "icon": "👑"},
        ],
        "stan": {
            "kind": "Digital Product", "price": "$19", "strike": "$39",
            "thumb_title": "Fuel Like A Baddie 🍗", "thumb_sub": "Meal plan + grocery list + macro calculator",
            "button": "Feed Me Right 🍗",
            "checkout_title": "Fuel Like A Baddie: High-Protein Meal Plan Kit",
            "desc": "You're killing it in the gym but the scale and the mirror aren't moving? It's the food, babe. This kit tells you EXACTLY how much to eat for your goal, then hands you a 7-day high-protein meal plan with real, flavorful food (jerk chicken, burrito bowls, protein waffles 😍), a tap-to-check grocery list, a 90-minute Sunday meal prep plan, and my eating-out cheat sheet so you can still go out with the girls.",
            "bullets": ["Personal macro calculator (calories, protein, carbs, fat, water)", "7-day high-protein meal plan (28 meals)", "Interactive grocery checklist", "90-minute Sunday meal prep game plan", "8 high-protein snacks + sweet treats", "Eating-out cheat sheet: Chipotle, Chick-fil-A, Starbucks & more"],
            "cta": "FUEL ME UP 🍗",
            "bump": {"title": "Add the 30-Day Challenge for $9 (reg. $14.99)", "desc": "Pair your new meal plan with 30 days of workouts, habits & mindset."},
            "thanks": "Your kitchen is about to be a gains factory 🍗 Check your email for your link and calculate your macros first!",
        },
    },
    {
        "slug": "gym-girl-confidence-kit-k4t9", "short": "Gym Girl Confidence Kit",
        "title": "Gym Girl Confidence Kit", "script": "from scared to stage", "emoji": "✨",
        "sub": "Beat gym anxiety & walk in like you own the place",
        "c1": "#f5b70a", "c2": "#ff2e93",
        "sections": [
            {"type": "intro", "id": "start", "label": "Start Here", "icon": "💜", "html": WELCOME +
             "<p>Real talk: I was once the girl who walked in, did 10 minutes on the treadmill and left because I didn't know what to do. Gym anxiety is REAL, and it's keeping so many of us from our goals. "
             "This kit fixes that: what to pack, what to wear, how to use the machines, gym etiquette, word-for-word scripts, and a 2-week plan that eases you in. You belong in that weight room, sis.</p>"},
            {"type": "program", "id": "prog", "label": "2-Week Plan", "icon": "🗓️", "weeks": build_program(CONF_DAYS, CONF_PHASES)},
            {"type": "accordion", "id": "mach", "label": "Machine Guide", "icon": "⚙️", "items": [
                {"q": "Leg Press", "a": TIPS["Leg Press"] + " Seat: adjust so your knees reach ~90° at the bottom. Always lock the safety handles before getting out."},
                {"q": "Hip Abduction (the 'booty machine')", "a": TIPS["Hip Abduction Machine"] + " Set the start lever so your legs start together."},
                {"q": "Lat Pulldown", "a": TIPS["Lat Pulldown"] + " Lock your thighs under the pad first."},
                {"q": "Seated Cable Row", "a": TIPS["Seated Cable Row"]},
                {"q": "Smith Machine", "a": "The bar is on a track and hooks into slots. Rotate your wrists to unhook/re-hook. " + TIPS["Smith Machine Squat"]},
                {"q": "Cable Machine", "a": "Pull the pin on the side to slide the pulley up/down. Clip on the attachment you need (rope, handle, ankle strap). The weight stack pin sets your load."},
                {"q": "Lying Hamstring Curl", "a": TIPS["Lying Hamstring Curl"] + " Pad should sit just above your heels."},
                {"q": "Chest Press Machine", "a": TIPS["Machine Chest Press"]},
                {"q": "Hip Thrust Machine / Bench", "a": TIPS["Barbell Hip Thrust"] + " Use a bar pad — your hip bones will thank you."},
                {"q": "Stair Master", "a": "Start at level 4–6, stand tall, don't lean on the rails. 10–15 min is a WORKOUT."}]},
            {"type": "cards", "id": "scripts", "label": "Gym Scripts", "icon": "💬", "items": [
                {"i": "🔁", "t": "Want a machine someone's on", "d": "“Hey, how many sets do you have left?” or “Mind if I work in?”"},
                {"i": "🙋🏽‍♀️", "t": "Need a spot", "d": "“Can you spot me for one set? Just help if I get stuck around rep 8.”"},
                {"i": "🎧", "t": "Someone won't stop talking", "d": "Point at your headphones, smile, “Sorry, in the zone!” and keep it moving."},
                {"i": "🏋🏽‍♀️", "t": "Taking the dumbbells to your bench", "d": "Totally allowed. Just bring them back when you're done."},
                {"i": "📱", "t": "Filming your set", "d": "Set up out of walkways and don't film other people without asking. Your content, your space."},
                {"i": "🤷🏽‍♀️", "t": "Someone gives unsolicited advice", "d": "“Thanks! I'm following my coach's program.” 😌 Then go back to work."}]},
            {"type": "checklist", "id": "bag", "label": "Gym Bag", "icon": "🎒", "groups": [
                {"title": "🎒 Pack The Night Before", "items": ["Water bottle (40 oz+)", "Headphones — charged!", "Pre-made playlist", "Lifting gloves or straps", "Ankle strap for cable kickbacks", "Resistance band (booty band)", "Small towel", "Deodorant + body spray", "Hair ties + edge brush 😂", "Post-workout snack or shake", "Phone tripod for content", "Your program open on your phone"]},
                {"title": "✨ Confidence Rituals", "items": ["Outfit I feel GOOD in laid out", "Hype song for the parking lot", "Plan which machines I'm using today", "Say my affirmation in the mirror", "Walk in with my shoulders back"]}]},
            {"type": "cards", "id": "aff", "label": "Affirmations", "icon": "🪞", "items": [
                {"i": "💜", "t": "I belong here.", "d": "Every person in this gym was a beginner once."},
                {"i": "👑", "t": "Nobody is watching me the way I think.", "d": "They're thinking about their own set, babe."},
                {"i": "💪🏽", "t": "Strong is beautiful.", "d": "I lift for me — not for anyone's approval."},
                {"i": "🔥", "t": "Progress, not perfection.", "d": "Showing up today is the win."},
                {"i": "✨", "t": "I'm becoming HER.", "d": "The confident girl I see in my head is me in 90 days."},
                {"i": "🦋", "t": "Discomfort means growth.", "d": "Nervous and doing it anyway = brave."}]},
            {"type": "journal", "id": "jr", "label": "Journal", "icon": "📝", "prompts": [
                "What exactly makes me nervous about the gym? Name it so it loses its power.",
                "What would I do in the gym if I knew nobody was judging me?",
                "After my first workout in this plan, how did I feel walking out?",
                "What's one thing I did this week that past-me would've been too scared to do?",
                "Write a letter to the girl who will walk into the gym confidently 3 months from now."]},
            {"type": "upsell", "id": "next", "label": "What's Next", "icon": "👑"},
        ],
        "stan": {
            "kind": "Digital Product", "price": "$12", "strike": "$27",
            "thumb_title": "Gym Girl Confidence Kit ✨", "thumb_sub": "Beat gym anxiety & own the weight room",
            "button": "Boost My Confidence ✨",
            "checkout_title": "The Gym Girl Confidence Kit",
            "desc": "Scared of the weight room? Don't know how the machines work? Feel like everyone's staring? Sis… I've been there. This kit takes you from nervous to NOTHING-CAN-STOP-ME in 2 weeks. You'll know what to pack, how to use 10 of the most common machines, exactly what to say in awkward moments, and you'll follow a beginner plan that eases you in — machines first, then dumbbells, then cables. You belong in that gym.",
            "bullets": ["2-week beginner gym plan (machines → dumbbells → cables)", "Step-by-step guide to 10 gym machines", "Word-for-word gym scripts for awkward moments", "Gym bag + confidence ritual checklists", "6 gym affirmations + 5 journal prompts", "Interactive tracker with rest timer"],
            "cta": "I'M READY TO OWN IT ✨",
            "bump": {"title": "Add the 8-Week Booty Builder for $25 (reg. $37)", "desc": "Once you're confident, keep the momentum with my signature 8-week program."},
            "thanks": "I'm SO proud of you for this step 💜 Your kit is in your email. Pack your bag tonight and tag me in your first gym selfie!",
        },
    },
]

BUNDLE = {
    "kind": "Bundle", "price": "$67", "strike": "$106.99",
    "thumb_title": "THE WHOLE BADDIE BUNDLE 👑", "thumb_sub": "Every program, meal plan & kit — save 37%",
    "button": "Get Everything 👑",
    "checkout_title": "The Whole Baddie Bundle 👑",
    "desc": "Want it ALL? Of course you do. 👑 Get every single Get Fit With Me product in one bundle and save over $40. Your workouts, your nutrition, your confidence — all handled. This is the complete glow-up system I wish I had when I started.",
    "bullets": ["8-Week Booty Builder ($37)", "Press Like A Boss ($24)", "Fuel Like A Baddie ($19)", "30-Day Get Fit With Me Challenge ($14.99)", "Gym Girl Confidence Kit ($12)", "Lifetime access + every future update FREE"],
    "cta": "GIVE ME EVERYTHING 👑",
    "bump": {"title": "Add a 30-min Form Check Call for $29 (reg. $49)", "desc": "Send me your lift videos and we'll fix your form together on a 1:1 video call."},
    "thanks": "BADDIE STATUS UNLOCKED 👑 All 5 links are in your email. Start with the Confidence Kit + Fuel Like A Baddie, then hit Week 1 of the Booty Builder. I'm so proud of you!",
}

COACHING = [
    {
        "kind": "Coaching Call (Calendar)", "price": "$49", "strike": "",
        "thumb_title": "1:1 Form Check Call 🎥", "thumb_sub": "30 min on video — let's fix your form together",
        "button": "Book My Call 📅",
        "checkout_title": "1:1 Form Check + Strategy Call",
        "desc": "Not sure if you're doing it right? Stop guessing and get eyes on your form. Send me videos of your lifts before the call, then we hop on a 30-minute video call where I break down your technique, fix what's holding you back, and build you a game plan for your goals.",
        "bullets": ["30-minute 1:1 video call with me", "I review up to 5 of your lift videos beforehand", "Personal form corrections + cues", "Custom next-steps plan for your goals", "Recording of the call so you can rewatch"],
        "cta": "BOOK IT 📅",
        "bump": None,
        "thanks": "You're booked! 🎉 Reply to your confirmation email with up to 5 lift videos (side angle is best) at least 24 hours before our call.",
    },
    {
        "kind": "Membership / Application", "price": "$149/mo", "strike": "",
        "thumb_title": "Online Coaching With Danielle 💜", "thumb_sub": "Custom program, macros & weekly check-ins",
        "button": "Apply Now 💜",
        "checkout_title": "1:1 Online Coaching With Danielle",
        "desc": "This is for the girl who's DONE starting over. You get a fully custom training program built around your body, schedule and gym, your own macros, weekly check-ins, form reviews and direct access to me in your DMs. I only take a small number of clients so I can actually give you my attention — so apply and let's see if we're a fit.",
        "bullets": ["Custom training program updated every 4 weeks", "Personal macros + nutrition guidance", "Weekly check-ins & adjustments", "Unlimited form check videos", "Direct messaging access to me", "All 5 Get Fit With Me products included FREE"],
        "cta": "APPLY FOR COACHING 💜",
        "bump": None,
        "thanks": "Application received! 💜 I personally review every one. Keep an eye on your email (and DMs) within 48 hours.",
    },
]

LAUNCH = {
    "captions": [
        "POV: you finally stopped making the girl who's been asking “what's your glute workout?” wait 😂🍑 My Get Fit With Me store is OFFICIALLY LIVE. Free Glute Starter Pack is in my bio — go grab it before I change my mind 💜 #getfitwithme #glutes #gymgirl",
        "I chest pressed 75s and y'all lost it 😤 So I made the program. Press Like A Boss is live — 6 weeks to the strongest upper body you've ever had. Link in bio 💪🏽 #womenwholift #chestpress #strongwomen",
        "Scared of the gym? I was too. Built the Gym Girl Confidence Kit for every girl who's ever walked in and walked right back out. You belong here, sis ✨ Link in bio. #gymanxiety #beginnergym",
        "30 days. You + me. Daily workouts, habits & mindset. The 30-Day Get Fit With Me Challenge starts whenever YOU say so 🔥 Comment “CHALLENGE” and I'll DM you the link.",
    ],
    "story": [
        "Slide 1 (video of you lifting): “Y'all have been asking for MONTHS…”",
        "Slide 2: “My store is finally LIVE 😭💜” + screenshot of the store",
        "Slide 3: Poll — “What do you need most? 🍑 Glutes / 💪🏽 Upper body / 🍗 Food / ✨ Confidence”",
        "Slide 4: “Start with the FREE Glute Starter Pack” + link sticker",
        "Slide 5: “Launch week only: the Whole Baddie Bundle is $67 👑” + link sticker",
        "Slide 6: Countdown sticker “Launch sale ends” (set for 72 hrs)",
    ],
    "dm_keywords": "Pin a reel that says “Comment GLUTES for my free workout.” Then send everyone who comments the Free Glute Starter Pack link (Stan has an Instagram AutoDM feature that can do this automatically).",
}
