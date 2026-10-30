# "30 Days to Her" — choose-what-she-does series telling Danielle's real transformation story.
# Scene keys: bg, pose, face, prop, vo, kids (show her four kids), rain (storm overlay)
# Backgrounds: apartment_night, bedroom_night, bedroom_morning, bathroom, street_dawn, kitchen, office, gym
# Poses: idle, slump, hip, flex, hold, phone, curl, point     Faces: crying, sad, tired, shocked, smirk, determined, happy
# Props: None, phone, dumbbell, basket, shake, letter, jeans, plate, mealprep
# Body: 1.0 = where she started, 0.0 = buff Day-30 Danielle.  Outfit: hoodie, tee, tank, bra

def S(bg, pose, face, vo, prop=None, kids=False, rain=False):
    return {"bg": bg, "pose": pose, "face": face, "prop": prop, "vo": vo, "kids": kids, "rain": rain}


SERIES = {
    "title": "30 Days to Her",
    "tagline": "The story of how I became her.",
    "handle": "@getfitwithme",
    "premise": ("A cartoon retelling of Danielle Dawson's real story. Day 1: a single mother of four, overweight, depressed and job hunting "
                "with no hope left. Over 30 days, the comments decide every move she makes, and the cartoon gets visibly stronger every "
                "episode. On Day 30 she's buff, glowing, surrounded by her four kids, and the finale reveals: that woman is me."),
}

EPISODES = [
    {
        "n": 1, "day": 1, "pct": 0, "body": 1.0, "outfit": "hoodie", "title": "Rock Bottom", "hook": "DAY 1",
        "scenes": [
            S("apartment_night", "slump", "crying", "This is Danielle. It's 2 a.m. It's raining. And she hasn't slept in three days.", rain=True),
            S("apartment_night", "slump", "sad", "Four kids. One paycheck... that stopped coming two months ago. A stack of bills she's too scared to open.", prop="letter", rain=True),
            {"overlay": "phone", "from": "INBOX", "msgs": ["We regret to inform you...", "Unfortunately, we've decided to move forward with other candidates.", "Application status: REJECTED"],
             "vo": "Another rejection email. That's number fourteen."},
            S("bedroom_night", "idle", "crying", "She looks at her babies sleeping, and she whispers... I'm sorry. Mommy's trying.", kids=True),
            S("bathroom", "slump", "sad", "She hasn't looked in a mirror in months. She doesn't recognize the woman looking back."),
        ],
        "choice": {"q": "WHAT SHOULD SHE DO TOMORROW?",
                   "a": {"word": "GET UP", "sub": "Walk outside at sunrise", "pose": "idle", "face": "determined"},
                   "b": {"word": "STAY", "sub": "Stay in bed one more day", "pose": "slump", "face": "sad"}},
        "vo_choice": "Tomorrow, you decide. Comment GET UP, and she walks outside at sunrise. Or STAY, and she stays in bed one more day.",
        "outcomes": {
            "a": S("street_dawn", "idle", "crying", "You chose GET UP. She walked around the block in her slippers. She cried the whole way. But she came home and made pancakes for four kids. Day one. Done."),
            "b": S("bedroom_morning", "slump", "crying", "You chose STAY. At noon her youngest crawled into bed and asked, Mommy, are you sad? Her heart broke wide open. That afternoon, she put on her shoes.", kids=True),
        },
        "caption": "Day 1. Single mom of 4. No job. No hope. This is my story 💔 You decide what she does next: comment GET UP or STAY 👇🏽 If you're in a dark place right now, you are not alone 💜 #30DaysToHer #getfitwithme",
    },
    {
        "n": 2, "day": 3, "pct": 8, "body": 0.96, "outfit": "hoodie", "title": "The Drawing", "hook": "DAY 3",
        "scenes": [
            S("kitchen", "slump", "tired", "Day three. Cereal for dinner again. She can't afford much else this week.", kids=True),
            S("kitchen", "hold", "shocked", "Then her daughter hands her a drawing. A woman in a cape. It says: My mommy is a superhero.", prop="letter", kids=True),
            S("bathroom", "idle", "crying", "She doesn't feel like a superhero. She feels invisible. But her kids don't see what she sees."),
            S("bathroom", "idle", "determined", "So she makes a promise to the mirror. Thirty days. I'm going to become her."),
        ],
        "choice": {"q": "SHOULD SHE TELL ANYONE?",
                   "a": {"word": "SHARE", "sub": "Post it & tell her friends", "pose": "phone", "face": "determined", "prop": "phone"},
                   "b": {"word": "SECRET", "sub": "Keep it to herself", "pose": "slump", "face": "sad"}},
        "vo_choice": "Comment SHARE, and she tells the world. Or SECRET, and she keeps it to herself.",
        "outcomes": {
            "a": S("bedroom_night", "phone", "happy", "You chose SHARE. She posted: Day 3. I'm starting over. Her phone wouldn't stop buzzing. Forty people said: I'm with you. Lesson: accountability is a superpower.", prop="phone"),
            "b": S("bedroom_night", "idle", "sad", "You chose SECRET. Nobody knew, so nobody noticed when she almost quit. Lesson: you don't have to do it alone. Tell one person."),
        },
        "caption": "Day 3. My daughter drew me as a superhero 😭 Comment SHARE or SECRET 👇🏽 #30DaysToHer",
    },
    {
        "n": 3, "day": 6, "pct": 18, "body": 0.9, "outfit": "tee", "title": "No Money for a Gym", "hook": "DAY 6",
        "scenes": [
            S("apartment_night", "hip", "tired", "Day six. She has a plan. She has motivation. What she doesn't have... is a gym membership.", kids=True),
            S("kitchen", "hold", "smirk", "She's got a laundry basket, four kids, and a gallon of milk.", prop="basket", kids=True),
            S("gym", "idle", "shocked", "Or there's the gym down the street. Free seven-day trial. Full of people who look like they've never struggled a day."),
        ],
        "choice": {"q": "WHERE SHOULD SHE TRAIN?",
                   "a": {"word": "HOME", "sub": "Living room workouts", "pose": "hold", "face": "happy", "prop": "basket"},
                   "b": {"word": "GYM", "sub": "Use the free trial", "pose": "idle", "face": "shocked"}},
        "vo_choice": "Comment HOME, or GYM.",
        "outcomes": {
            "a": S("apartment_night", "curl", "happy", "You chose HOME. Laundry basket squats. Milk jug curls. Her kids counted every rep, loud. It became family workout night. Lesson: start with what you have.", prop="basket", kids=True),
            "b": S("gym", "idle", "determined", "You chose GYM. She almost turned around in the parking lot. Twice. But she walked in, did ten minutes on the treadmill, and walked out proud. Lesson: you belong there too."),
        },
        "caption": "Day 6. $0 for a gym. Laundry basket or free trial? Comment HOME or GYM 👇🏽 #30DaysToHer",
    },
    {
        "n": 4, "day": 9, "pct": 28, "body": 0.82, "outfit": "tee", "title": "The Interview", "hook": "DAY 9",
        "scenes": [
            {"overlay": "phone", "from": "UNKNOWN NUMBER", "msgs": ["Hi Danielle! We loved your application.", "Can you come in Thursday at 10am for an interview?"],
             "vo": "Day nine. Her phone buzzes. Application number fifteen... wants an interview."},
            S("office", "idle", "shocked", "She wears the only blazer she owns. Her hands are shaking."),
            S("office", "hip", "tired", "Then the question: So, Danielle. What is your greatest strength?"),
        ],
        "choice": {"q": "WHAT SHOULD SHE SAY?",
                   "a": {"word": "TRUTH", "sub": "\"Single mom of 4. I never quit.\"", "pose": "point", "face": "determined"},
                   "b": {"word": "SAFE", "sub": "The textbook answer", "pose": "idle", "face": "tired"}},
        "vo_choice": "Comment TRUTH, and she tells them who she really is. Or SAFE, and she gives the textbook answer.",
        "outcomes": {
            "a": S("office", "point", "determined", "You chose TRUTH. I'm a single mother of four, and I have never once quit on them. The room went quiet. The interviewer smiled. Lesson: your story is your strength."),
            "b": S("office", "idle", "sad", "You chose SAFE. I'm a hard worker and a team player. Polite nods. She walked out feeling like she hid the best part of herself."),
        },
        "caption": "Day 9. First interview in months 😰 Comment TRUTH or SAFE 👇🏽 #30DaysToHer",
    },
    {
        "n": 5, "day": 12, "pct": 38, "body": 0.75, "outfit": "tee", "title": "The Scale Didn't Move", "hook": "DAY 12",
        "scenes": [
            S("bathroom", "idle", "shocked", "Day twelve. Twelve days of walks, workouts and water. She steps on the scale."),
            S("bathroom", "slump", "crying", "It hasn't moved. Not one pound. She sits on the bathroom floor and cries.", rain=True),
            S("kitchen", "slump", "sad", "There's a tray of brownies on the counter. And a tape measure in the drawer.", kids=True),
        ],
        "choice": {"q": "WHAT SHOULD SHE DO?",
                   "a": {"word": "QUIT", "sub": "Eat the brownies, give up", "pose": "slump", "face": "crying"},
                   "b": {"word": "MEASURE", "sub": "Grab the tape measure", "pose": "hold", "face": "determined"}},
        "vo_choice": "Comment QUIT, or MEASURE.",
        "outcomes": {
            "a": S("bedroom_morning", "idle", "crying", "You chose QUIT. She ate half the tray. The next morning, her son had left his little sneakers outside her door with a note: Workout, Mommy? She went.", kids=True),
            "b": S("bathroom", "flex", "shocked", "You chose MEASURE. Two inches. Gone. From her waist. Lesson: the scale lies. Water, muscle, your cycle. Measure. Take photos. Keep going."),
        },
        "caption": "Day 12. The scale didn't move and I broke down 💔 Comment QUIT or MEASURE 👇🏽 #30DaysToHer",
    },
    {
        "n": 6, "day": 15, "pct": 50, "body": 0.64, "outfit": "tank", "title": "The Call", "hook": "DAY 15",
        "scenes": [
            S("kitchen", "phone", "shocked", "Day fifteen. Halfway. She's making lunches when the phone rings.", prop="phone", kids=True),
            S("kitchen", "phone", "crying", "Danielle... we'd love to offer you the position. She drops to her knees in the kitchen. Four kids screaming. Happy tears.", prop="phone", kids=True),
            S("kitchen", "hip", "tired", "But the job is seven to four. School pickup. Dinner. Homework. Bedtime. When does she train now?"),
        ],
        "choice": {"q": "WHEN SHOULD SHE TRAIN?",
                   "a": {"word": "5AM", "sub": "Before the world wakes up", "pose": "curl", "face": "determined", "prop": "dumbbell"},
                   "b": {"word": "LUNCH", "sub": "30 minutes on her lunch break", "pose": "hold", "face": "happy", "prop": "shake"}},
        "vo_choice": "Comment 5AM, or LUNCH.",
        "outcomes": {
            "a": S("bedroom_morning", "curl", "determined", "You chose 5AM. Alarm at 4:45. Workout in the living room while the house was silent. It became her sacred hour. Lesson: protect your time like it's an appointment.", prop="dumbbell"),
            "b": S("office", "hold", "happy", "You chose LUNCH. Thirty minutes, a walk and a quick workout, every single day. Her coworkers started joining. Lesson: thirty minutes counts. Consistency beats perfect.", prop="shake"),
        },
        "caption": "Day 15. I GOT THE JOB 😭💜 But when do I train now? Comment 5AM or LUNCH 👇🏽 #30DaysToHer",
    },
    {
        "n": 7, "day": 18, "pct": 62, "body": 0.52, "outfit": "tank", "title": "They Laughed", "hook": "DAY 18",
        "scenes": [
            S("gym", "curl", "determined", "Day eighteen. She's a gym member now. First paycheck. First membership. She earned this.", prop="dumbbell"),
            S("gym", "idle", "shocked", "Then she hears it. Two people by the mirrors. Laughing. Looking right at her."),
            S("gym", "slump", "sad", "That voice from Day 1 comes back. Who do you think you are?"),
        ],
        "choice": {"q": "WHAT SHOULD SHE DO?",
                   "a": {"word": "CLAP BACK", "sub": "Say something", "pose": "point", "face": "smirk"},
                   "b": {"word": "LIFT", "sub": "Let the work talk", "pose": "curl", "face": "determined", "prop": "dumbbell"}},
        "vo_choice": "Comment CLAP BACK, or LIFT.",
        "outcomes": {
            "a": S("gym", "point", "smirk", "You chose CLAP BACK. She walked over and said, I'm right here if you want to say it louder. They stopped laughing. She felt ten feet tall."),
            "b": S("gym", "curl", "determined", "You chose LIFT. She put her headphones on and finished every set. Two weeks later, one of them asked her for tips. Lesson: your work is the loudest answer.", prop="dumbbell"),
        },
        "caption": "Day 18. They laughed at me in the gym 😤 Comment CLAP BACK or LIFT 👇🏽 #30DaysToHer",
    },
    {
        "n": 8, "day": 21, "pct": 74, "body": 0.38, "outfit": "tank", "title": "The First Heavy Lift", "hook": "DAY 21",
        "scenes": [
            S("gym", "hip", "smirk", "Day twenty-one. Three weeks. She's stronger. She can feel it in the stairs, in the groceries, in carrying four kids' backpacks."),
            S("gym", "idle", "shocked", "Today she wants to try it. The barbell. The real one. The hip thrust everyone talks about."),
            S("gym", "hold", "tired", "But she doesn't know how to set it up, and the bar is heavier than it looks.", prop="plate"),
        ],
        "choice": {"q": "WHAT SHOULD SHE DO?",
                   "a": {"word": "ASK", "sub": "Ask a trainer for help", "pose": "point", "face": "happy"},
                   "b": {"word": "FIGURE IT OUT", "sub": "Learn it herself", "pose": "phone", "face": "determined", "prop": "phone"}},
        "vo_choice": "Comment ASK, or FIGURE IT OUT.",
        "outcomes": {
            "a": S("gym", "flex", "happy", "You chose ASK. A trainer showed her the setup, the pad, the squeeze at the top. Ninety-five pounds. She cried again. Good tears. And she thought: I want to be the one who helps women like me."),
            "b": S("gym", "flex", "determined", "You chose FIGURE IT OUT. She watched videos, filmed her form, and fixed it set by set. Ninety-five pounds. And something clicked: she wasn't just training anymore. She was learning."),
        },
        "caption": "Day 21. First time touching a barbell 😳 Comment ASK or FIGURE IT OUT 👇🏽 #30DaysToHer",
    },
    {
        "n": 9, "day": 25, "pct": 86, "body": 0.22, "outfit": "bra", "title": "The Old Jeans", "hook": "DAY 25",
        "scenes": [
            S("bedroom_morning", "hold", "shocked", "Day twenty-five. Cleaning out the closet, she finds them. The jeans she wore before everything fell apart.", prop="jeans"),
            S("bedroom_morning", "idle", "sad", "She's been scared of these jeans for years. They remind her of who she used to be."),
            S("bedroom_morning", "hip", "determined", "But she isn't that woman anymore. And she isn't the woman from Day 1 either."),
        ],
        "choice": {"q": "WHAT SHOULD SHE DO?",
                   "a": {"word": "TRY THEM", "sub": "Try them on", "pose": "hold", "face": "determined", "prop": "jeans"},
                   "b": {"word": "DONATE", "sub": "Let the past go", "pose": "hold", "face": "happy", "prop": "jeans"}},
        "vo_choice": "Comment TRY THEM, or DONATE.",
        "outcomes": {
            "a": S("bedroom_morning", "flex", "happy", "You chose TRY THEM. They zipped. She screamed so loud the kids came running. Four kids dancing in her bedroom.", kids=True),
            "b": S("bedroom_morning", "hip", "happy", "You chose DONATE. She folded them, said thank you, and let them go. She didn't need to fit into her past. She was building her future."),
        },
        "caption": "Day 25. Found my old jeans 👖😭 Comment TRY THEM or DONATE 👇🏽 #30DaysToHer",
    },
    {
        "n": 10, "day": 30, "pct": 100, "body": 0.0, "outfit": "bra", "title": "The Woman She Became", "hook": "DAY 30",
        "scenes": [
            S("gym", "flex", "determined", "Day thirty. Remember Day 1? 2 a.m. Rain. Bills. Rejection number fourteen."),
            S("gym", "curl", "happy", "Thirty days later: a job. A gym membership she paid for herself. Seventy-five pound dumbbells. And a fire she didn't know she had.", prop="dumbbell"),
            S("street_dawn", "hip", "happy", "Her kids don't just think she's a superhero anymore. They know it.", kids=True),
            S("gym", "flex", "smirk", "That woman? That was me. My name is Danielle Dawson. And now I help women do exactly what I did."),
        ],
        "choice": {"q": "COMMENT ONE WORD",
                   "a": {"word": "JOIN", "sub": "My 30-Day Challenge", "pose": "point", "face": "happy"},
                   "b": {"word": "STORY", "sub": "The full story, uncut", "pose": "flex", "face": "smirk"}},
        "vo_choice": "Your Day 1 starts now. Comment JOIN, and I'll send you my 30-Day Challenge. Or comment STORY for the full story, uncut.",
        "outcomes": {},
        "caption": "Day 30. That woman was me 💜 Single mom of 4 → coach. Your Day 1 starts now: comment JOIN for my 30-Day Challenge, or STORY for the full uncut story 👇🏽 #30DaysToHer #getfitwithme",
    },
]
