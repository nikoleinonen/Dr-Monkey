import random
from src.commands.responses.monkey_types import get_random_monkey_type, get_plural_monkey_type

def get_iq_range_key(iq_score: int) -> str:
    """Maps an IQ score to a predefined range key."""
    if iq_score == 0: return "IQ_0"
    elif iq_score <= 39: return "IQ_VERY_LOW"
    elif iq_score <= 59: return "IQ_LOW"
    elif iq_score <= 120: return "IQ_AVERAGE"
    elif iq_score <= 160: return "IQ_HIGH"
    elif iq_score <= 199: return "IQ_GENIUS"
    else: return "IQ_200"

def get_mp_range_key(monkey_percentage: int) -> str:
    """Maps a monkey percentage to a predefined range key."""
    if monkey_percentage == 0: return "MP_0"
    elif monkey_percentage <= 24: return "MP_BARELY"
    elif monkey_percentage <= 49: return "MP_HALF"
    elif monkey_percentage <= 74: return "MP_MOSTLY"
    elif monkey_percentage <= 99: return "MP_ALMOST_PURE"
    else: return "MP_PURE"

# --- Combined Response Data ---
# This dictionary holds lists of responses for specific combinations of IQ and Monkey Percentage ranges.
# The keys are the range keys returned by get_iq_range_key and get_mp_range_key.

COMBINED_RESPONSES = {
    "IQ_0": {
        "MP_0": [
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. A perfect vacuum of thought 💨 and primal energy. Are you even real? 👻",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You've achieved a state of absolute nothingness in both brain 🧠 and {m_type_lower}-ness. Profoundly empty. 🕳️",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're the human equivalent of a loading screen stuck at 0%. 📉 Not even a banana thought. 🍌🚫",
            "With **{iq_score}** IQ and **{monkey_percentage}%** {m_type_lower}, you're so far removed from the jungle, you probably think 'Ook' is a brand of cereal. 🥣😂",
            "Analysis complete: IQ **{iq_score}**, {m_type_lower} Purity **{monkey_percentage}%**. Our sensors detect... a dial tone. 📞 Are you a Roomba in disguise? A very, very confused Roomba? 🤖🤔",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're the human equivalent of a pet rock 🗿, but less interesting. Not a single banana 🍌 thought in that head. Zilch. Nada.",
            "With **{iq_score}** IQ and **{monkey_percentage}%** {m_type_lower}, you're so bland, you make vanilla look like a rave. 🍦😴 Yawn.",
            "Zero smarts, zero {m_type_lower}. IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Are you a figment of our imagination? 👻 Or just really, really boring? 🥱 We're leaning towards boring.",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're the loading screen of life, stuck at 0% on both brain 🧠 and {m_type_lower} 🐒. We're still waiting... ⏳ and waiting...",
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're so far from being a {m_type_lower}, you probably think 'Ook' is a typo. 🤦‍♂️ It's a lifestyle, sweetie."
        ],
        "MP_BARELY": [
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. A mind of pure emptiness 💨, with just a tiny, tiny hint of {m_type_lower} in you. You probably forgot what a banana is. 🍌❓",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Brain: 0. {m_type_upper} vibes: minimal. You're a mystery, {m_type_lower}. A very blank mystery. 🕵️‍♂️",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Brain like a goldfish 🐠 (no offense to goldfish), with a faint whisper of {m_type_lower}. You might try to peel a banana with your eyebrows. Once. 🤔😂",
            "Zero thoughts, just a tiny bit of {m_type_lower} static. IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're like a TV with no signal 📺, occasionally showing a picture of a banana for a split second. 🍌✨",
            "A mind as empty as a politician's promise 📜, yet **{monkey_percentage}%** {m_type_lower}. IQ **{iq_score}**. You're an enigma wrapped in a banana peel... that you don't know how to open. 🤷‍♂️🍌",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. So, no brain cells 🧠🚫 and barely any {m_type_lower} instinct. You're the human equivalent of a decorative gourd. Looks... interesting? 🎃",
            "You've got **{iq_score}** IQ and **{monkey_percentage}%** {m_type_lower}. That's like having a car with no engine 🚗💨 and one fuzzy die hanging from the mirror. Pointless, but with a hint of... something? 🎲",
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a blank slate with a tiny {m_type_lower} doodle on it. 📝🐒 Barely counts, hun.",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're so un-monkey, even the bananas 🍌 are confused by your **{monkey_percentage}%** {m_type_lower} attempt. Try harder? Or don't. 🤷‍♀️",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Brain: offline. {m_type_upper} presence: a faint echo. You're the ghost of a {m_type_lower} that never was. 👻🐒 Spooky!"
        ],
        "MP_HALF": [
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Half {m_type_lower}, zero brain 🧠🚫. You're the one who swings from the chandelier 샹들리에 but forgets why you went up there. Classic.",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. A fascinating paradox: significant {m_type_lower} energy with no cognitive function. Just pure, unadulterated instinct... and emptiness. 🌀",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Half {m_type_lower}, all airhead. 💨 You've got the spirit for banana mischief 🍌😈 but zero capacity for planning it. Bless your heart. ❤️",
            "You're **{monkey_percentage}%** {m_type_lower} with an IQ of **{iq_score}**. It's like a car with a V8 engine 🏎️ but no steering wheel. Pure chaos, zero direction. 🚗💥 Buckle up!",
            "A true phenomenon: **{monkey_percentage}%** primal urge, **{iq_score}** brain cells. You're the {m_type_lower} who brings a banana 🍌 to a spelling bee. 🐝 Bold move!",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. All {m_type_lower} vibes, no thoughts. You're the 'act first, think never' type. 🤷‍♂️ Probably great at parties, terrible at puzzles. 🧩",
            "You've got **{iq_score}** IQ and **{monkey_percentage}%** {m_type_lower}. That's like a beautiful banana 🍌 with no actual fruit inside. Just... peel. Disappointing, but still yellow. 💛",
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a walking, swinging contradiction. Half {m_type_lower}, half... nothing? 🤔 It's a look, I guess. ✨",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're the {m_type_lower} who tries to pay rent with banana peels 🍌. Points for trying? No, not really. 💸",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a primal force of nature with the intellectual capacity of a stunned mullet 🐟. Go get 'em, tiger? 🐅"
        ],
        "MP_MOSTLY": [
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Mostly {m_type_lower}, absolutely no thoughts 🧠💨. You are the primal scream personified, unburdened by intellect. 😱",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Your {m_type_upper} is strong 💪, your brain is not. You're the troop member who charges first and asks 'banana? 🍌' later. Maybe.",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Mostly {m_type_lower}, but the lights are off upstairs. 💡🚫 You're a magnificent beast running on pure banana fumes ⛽ and zero logic. Vroom vroom!",
            "You're **{monkey_percentage}%** {m_type_lower} with an IQ of **{iq_score}**. You probably think 'cogito ergo sum' is a fancy way to order a banana smoothie. 🍌🥤 And honestly? You're not entirely wrong.",
            "Impressive {m_type_lower} levels **{monkey_percentage}%**, but your IQ **{iq_score}** suggests your main thought process is 'OOH OOH AAH AAH, BANANA NOW!' 🗣️🍌 Can't argue with that logic.",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're almost pure {m_type_lower}, but your brain is still buffering... since birth. ⏳ It's okay, bananas 🍌 don't require thinking.",
            "You've got **{iq_score}** IQ and **{monkey_percentage}%** {m_type_lower}. You're the {m_type_lower} who brings a rock 🗿 to a banana peeling contest. A for effort, F for... everything else. 🤦‍♀️",
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're so close to peak {m_type_lower}, but your brain is just... decorative. ✨ Like a tiny hat on a very large {m_type_lower}.",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're the embodiment of 'no thoughts, just {m_type_lower} vibes'. 🐒💨 It's a whole aesthetic. We're... intrigued.",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a magnificent, thought-free beast. Your spirit animal is probably a banana 🍌 that just really, really wants to be eaten. 🤤"
        ],
        "MP_ALMOST_PURE": [
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Almost pure {m_type_lower}, zero IQ 🧠🚫. You're a force of nature, a whirlwind of primal energy 🌪️ with a mind as smooth as a banana peel. ✨",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You've achieved near-total {m_type_upper}-ness by shedding the burden of thought entirely. OOK OOK AAH AAH (translation: 'Where banana? 🍌').",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. So close to pure {m_type_upper}, yet your brain is a blank canvas. 🎨 You're a masterpiece of mindless majesty. ✨👑",
            "You're **{monkey_percentage}%** {m_type_lower} with an IQ of **{iq_score}**. You've transcended thought. Your only desire? Banana 🍌. Your only word? 'Ook?' 🗣️❓",
            "A true testament to primal power: **{monkey_percentage}%** {m_type_lower}, **{iq_score}** IQ. You don't think, you *are*. And you *are* probably hungry for a banana. 🤤🍌",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're basically a {m_type_lower} god 🌟, if gods had zero thoughts and an insatiable craving for bananas 🍌. We stan a mindless king/queen! 👑",
            "You've got **{iq_score}** IQ and **{monkey_percentage}%** {m_type_lower}. You're so primal, you probably think clothes are a weird human fad. 👕👖🚫 Go free, {m_type_lower}!",
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a beautiful, brainless beast. 💖 Your only purpose: find banana, eat banana, repeat. 🍌🔄",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're the pinnacle of thoughtless evolution. A true inspiration to us all... to eat more bananas. 🍌🤤",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're so {m_type_lower}, you probably communicate through interpretive dance and banana offerings. 💃🍌 We get it."
        ],
        "MP_PURE": [
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. **{m_type_upper}** perfection meets absolute zero IQ 🧠🚫. You are the ultimate 'no thoughts, just vibes' {m_type_lower}. A legend. 🌟",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Pure **{m_type_upper}**, pure emptiness 💨. You are the void from which all bananas 🍌 sprang. We are not worthy of your thoughtless grace. 🙏",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. **100% {m_type_upper}**, 0% brain. You are the banana Buddha 🧘🍌, achieving enlightenment through sheer lack of thought. Namaste... or Ookaste?",
            "You are **{monkey_percentage}%** {m_type_lower}, IQ **{iq_score}**. The pinnacle of primate evolution, if evolution decided brains were overrated. OOK OOK! 👑🐒",
            "A perfect score! **{monkey_percentage}% {m_type_upper}** and **{iq_score}** IQ. You are the chosen one 🌟, destined to lead us... to more bananas 🍌, presumably. No thinking involved. 🙌",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You are **100% {m_type_upper}** and 0% burdened by intellect. You are the dream. The goal. The banana. 🍌✨",
            "You've got **{iq_score}** IQ and **{monkey_percentage}%** {m_type_lower}. You are pure, unadulterated {m_type_lower}. Your only language is 'OOK'. Your only currency is banana 🍌. We respect that. 💯",
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You are the {m_type_lower} singularity. All thought has collapsed into a single point: BANANA. 🍌🌌",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You are the alpha and the omega of thoughtless {m_type_lower}-dom. Your presence is a gift. A very loud, banana-obsessed gift. 🎁🗣️🍌",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You are the living embodiment of 'return to {m_type_lower}'. 🐒➡️🌳 No thoughts, just pure, unadulterated banana bliss. 😌🍌"
        ]
    },
    "IQ_VERY_LOW": { # 1-39
        "MP_0": [
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Barely any brain 🧠🤏, zero {m_type_lower}. You're like a slightly confused houseplant 🪴 that occasionally thinks about bananas 🍌. Maybe.",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Low intellect, no primal energy. You're probably trying to peel a banana 🍌 with a spreadsheet 📊. Good luck with that. 👍",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Your brain's running on dial-up 💾, and there's no {m_type_lower} in your signal. You probably think bananas grow on supermarket shelves. 🛒 Bless.",
            "With an IQ of **{iq_score}** and **{monkey_percentage}%** {m_type_lower}, you're the reason they put 'do not eat' on silica gel packets. 🚫🍬 But for real, don't eat those.",
            "A rare combo: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're so un-{m_type_lower}, you probably apologize to bananas 🍌🙏 before eating them. If you can figure out how. 🧐",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're the human equivalent of a participation trophy 🏆. You showed up. That's... something. No {m_type_lower} points though.",
            "You've got **{iq_score}** IQ and **{monkey_percentage}%** {m_type_lower}. You're so basic, your favorite spice is flour. 🍞 And you probably think bananas are 'too spicy'. 🌶️🚫",
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a blank canvas 🎨 with a single, confused crayon mark 🖍️. And zero {m_type_lower} glitter. ✨",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're the reason shampoo has instructions. 🧴 And you still probably try to eat it. Don't. Eat a banana 🍌 instead (if you can find it).",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're so un-primal, you probably think 'going ape' is a new yoga pose. 🧘‍♀️ It's not. It involves more screaming. 🗣️"
        ],
        "MP_BARELY": [
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. A low IQ 📉 and just a hint of {m_type_lower}. You're the {m_type_lower} who gets lost on the way to the banana stand. 🗺️🍌❓",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Not the sharpest tool 🛠️, and barely a {m_type_lower}. You might mistake your own reflection for a banana 🍌. Happens to the best of us (not really).",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. A few loose screws upstairs 🔩, and a faint whiff of {m_type_lower}. You might try to use a banana as a phone. 🍌📞 'Hello? Banana speaking!'",
            "You've got **{monkey_percentage}%** {m_type_lower} and an IQ of **{iq_score}**. You're the one who brings a rock 🗿 to a banana peeling contest. 🍌 Bold strategy, Cotton.",
            "Dim bulb **{iq_score} IQ** 💡🚫, tiny spark of {m_type_lower} **{monkey_percentage}%**. You probably think 'banana split' is a martial arts move. Hi-YA! 🥋🍌 Pow!",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're like a {m_type_lower} trying to understand taxes. 🧾 Confused, slightly angry, and just wants a banana. 🍌😠",
            "You've got **{iq_score}** IQ and **{monkey_percentage}%** {m_type_lower}. You're the {m_type_lower} who brings a knife 🔪 to a banana fight. Overkill, but we admire the spirit. Maybe.",
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a little bit {m_type_lower}, a little bit... lost. 🗺️ Like a tourist in your own brain. 🧠",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're the reason they put 'Caution: Hot' on coffee cups ☕. And you'd still probably try to peel it like a banana. 🍌",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a beautiful disaster. Low IQ, tiny bit of {m_type_lower}. It's a vibe. A very confusing vibe. 😵‍💫"
        ],
        "MP_HALF": [
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Half {m_type_lower}, low IQ 📉. You've got the primal urges, but lack the brainpower to execute them effectively. You try to swing, but miss the vine. 🌿💨 Oops.",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. A decent amount of {m_type_lower} spirit, hampered by a low IQ. You're the {m_type_lower} who brings a banana peel 🍌 to a banana fight. Bold, but ineffective.",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Half {m_type_lower}, halfwit. 🤪 You've got the enthusiasm for jungle life, but you'd probably get stuck in a tree. 🌳😅 And forget the banana.",
            "A charming combo: **{monkey_percentage}%** {m_type_lower}, **{iq_score}** IQ. You're all heart ❤️ and primal screams 🗣️, but your plans are... adorably flawed. Like trying to pay rent with bananas. 🍌🏠 Keep dreaming!",
            "You're **{monkey_percentage}%** {m_type_lower} with an IQ of **{iq_score}**. You're the life of the party 🎉, as long as the party involves flinging things and not, say, math. 🧮🚫",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a {m_type_lower} with big dreams and a tiny brain. 💭🤏 You want all the bananas 🍌, but can only count to... banana.",
            "You've got **{iq_score}** IQ and **{monkey_percentage}%** {m_type_lower}. You're the {m_type_lower} who tries to use a coconut 🥥 as a phone 📞. 'Hello? Is this the banana store?'",
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a delightful mix of primal energy and utter confusion. 🌀 Like a {m_type_lower} in a library. 📚🐒",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're the {m_type_lower} who thinks 'banana split' means you have to share your banana. 🍌😭 The horror!",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a lovable goofball. Half {m_type_lower}, half... well, the other half is still loading. ⏳ Hang in there!"
        ],
        "MP_MOSTLY": [
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Mostly {m_type_lower}, very low IQ 📉. You're a force of primal nature, unburdened by complex thought. Just pure, chaotic {m_type_lower} energy! 🌪️🐒",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. High {m_type_upper} percentage, low brainpower. You're the {m_type_lower} who runs headfirst into a tree 🌳💥 looking for bananas 🍌. Ouch.",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Mostly {m_type_lower}, but the brain's on vacation. 🌴 You're a magnificent beast who solves problems by screeching at them. 🗣️💥 Effective? Sometimes.",
            "You're **{monkey_percentage}%** {m_type_lower} with an IQ of **{iq_score}**. You're not building rockets 🚀, but you're a champion banana eater 🍌🏆. Priorities straight!",
            "High {m_type_lower} **{monkey_percentage}%**, low smarts **{iq_score}**. You're the {m_type_lower} who thinks 'banana republic' is an actual republic ruled by bananas 🍌👑. And you'd vote for them. 🗳️ Heck yeah!",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a glorious, unthinking beast. 🤩 Your motto: 'See banana 🍌, want banana, GET BANANA!' Simple. Effective.",
            "You've got **{iq_score}** IQ and **{monkey_percentage}%** {m_type_lower}. You're the {m_type_lower} who tries to peel a banana 🍌 with your feet 🦶... and sometimes succeeds. Impressive!",
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're mostly {m_type_lower}, with just enough brain to be adorably clumsy. 🥰 Like a baby {m_type_lower} learning to swing. 🌿",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're the {m_type_lower} who thinks 'intellectual property' means owning a really smart banana 🍌🧠. Close enough!",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a primal powerhouse with a pea-sized brain. 💪🧠🤏 But hey, who needs brains when you have BANANAS? 🍌"
        ],
        "MP_ALMOST_PURE": [
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Almost pure {m_type_lower}, very low IQ 📉. You're on the verge of total {m_type_upper}-ness, held back only by your inability to count your fingers 🖐️ (or bananas 🍌).",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Near-total {m_type_upper}, minimal brain 🧠🤏. You're the {m_type_lower} who tries to eat the banana 🍌 through the peel. Keep trying, champ! You'll get there... maybe. 😂",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. So close to pure {m_type_upper}! Your brain's just a little... smooth. ✨ Like a perfectly peeled banana 🍌, ready for unthinking consumption. Yum!",
            "You're **{monkey_percentage}%** {m_type_lower} with an IQ of **{iq_score}**. You've nearly shed all vestiges of higher thought. Your mantra: 'See banana 🍌, want banana, get banana... somehow.' 🤷‍♂️ OOK!",
            "Almost there! **{monkey_percentage}% {m_type_upper}**, **{iq_score}** IQ. You're one banana 🍌 away from achieving perfect, thoughtless primate bliss. Just don't think about it too hard. 😉🤫",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a magnificent, nearly mindless {m_type_lower}. 🤩 Your brain is just a suggestion at this point. A very quiet suggestion. 🤫",
            "You've got **{iq_score}** IQ and **{monkey_percentage}%** {m_type_lower}. You're so close to pure {m_type_lower}, you probably think 'civilization' is a type of banana disease. 🍌🤢",
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a primal force, barely contained by a sliver of... something. Not intellect. ✨ Your spirit animal is a banana peel. 🍌💨",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're the {m_type_lower} who's forgotten how to use tools 🛠️, but remembers how to fling poo with deadly accuracy. 🎯💩 Priorities!",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a beautiful, brain-lite beast. 💖 Your only desire: BANANA. 🍌 Your only word: OOK. We get it. 👍"
        ],
        "MP_PURE": [
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Pure **{m_type_upper}**, very low IQ 📉. You are the embodiment of primal, thoughtless {m_type_lower} energy. A magnificent, simple creature! 🌟🐒",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. **{m_type_upper}** perfection! Your brain is smooth ✨, your spirit is wild 🌪️. You are the ultimate banana 🍌 enthusiast, no thinking required. Just OOK!",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. **100% {m_type_upper}**, but the IQ is just a suggestion. A very, very quiet suggestion. You are a glorious, unthinking force of nature! OOK! 🌪️🍌",
            "You are **{monkey_percentage}%** {m_type_lower}, IQ **{iq_score}**. The apex predator of the banana pile 🍌👑, unburdened by intellect. Your wisdom is in your gut. And your gut wants bananas. 🤤 Always.",
            "Perfection! **{monkey_percentage}% {m_type_upper}**, **{iq_score}** IQ. You don't need brains 🧠🚫 when you have bananas 🍌 and the raw power of OOK AAH! 🦍💪 You are the ideal.",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. **100% {m_type_upper}**! Your brain is just there for decoration 🎀. Your true power lies in your banana-seeking gut 🍌🧭 and your mighty OOK! 🗣️",
            "You've got **{iq_score}** IQ and **{monkey_percentage}%** {m_type_lower}. You are pure, unadulterated {m_type_lower}. You probably think shoes 👟 are weird banana holders. You're not wrong.",
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You are the {m_type_lower} dream. No thoughts, just bananas 🍌 and vibes. ✨ We're jealous. 🥺",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You are the chosen one... to eat all the bananas 🍌. Your low IQ just means you don't question your destiny. 🙏",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You are a legend. A myth. A **100% {m_type_upper}** with an IQ that's more of a fun fact. 🤣 Go forth and OOK! 🐒"
        ]
    },
    "IQ_LOW": { # 40-59
        "MP_0": [
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Low IQ 📉, zero {m_type_lower}. You're the human who struggles with IKEA furniture 🛋️🔧 and thinks bananas 🍌 are 'too much work'. Smh.",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Not very bright 💡🚫, not very {m_type_lower}. You're probably trying to use a map 🗺️ to find the kitchen. 🍳",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Brain's a bit foggy 🌫️, and zero {m_type_lower} instincts. You probably think 'going bananas' 🍌🤪 is just a figure of speech. It's a lifestyle, friend.",
            "With an IQ of **{iq_score}** and **{monkey_percentage}%** {m_type_lower}, you're the person who brings a knife and fork 🍴 to a hotdog eating contest. 🌭 You do you, I guess. 🤷",
            "Low IQ **{iq_score}**, no {m_type_lower} **{monkey_percentage}%**. You're so human, you probably iron your banana peels 🍌. We don't judge. Much. 🧐 (We totally judge).",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're the human equivalent of a beige wall. 🧱 No offense. But also, where's the {m_type_lower} spice? ✨🌶️",
            "You've got **{iq_score}** IQ and **{monkey_percentage}%** {m_type_lower}. You probably think 'Planet of the Apes' 🌍🐒 is a travel documentary. It's a warning. 🚨",
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're so un-primal, you probably think a banana split 🍌🍨 is a complex dessert. It's just... bananas and stuff. Easy.",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're the reason they have to explain 'push' and 'pull' on doors. 🚪 And you still get it wrong. Bless. 🙏",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a fascinating specimen of... utter normality. 😐 And zero {m_type_lower} charm. Sad! 😢"
        ],
        "MP_BARELY": [
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Low IQ 📉, slight {m_type_lower} hint. You're the {m_type_lower} who can find a banana 🍌, but then forgets where they put it. 🤦‍♂️",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. A bit dim 💡🤏, a bit {m_type_lower}. You might occasionally try to peel a banana 🍌 with your teeth 🦷, then remember you have hands. 🙌",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Not the sharpest banana in the bunch 🍌🔪, with a tiny {m_type_lower} streak. You might occasionally hoot at the moon 🌕🦉, then feel embarrassed. Don't be!",
            "You've got **{monkey_percentage}%** {m_type_lower} and an IQ of **{iq_score}**. You're the one who tries to pay for parking 🅿️ with a banana 🍌. Bless your cotton socks. ❤️",
            "A bit slow on the uptake **{iq_score} IQ** 🐌, with a whisper of the wild **{monkey_percentage}%** {m_type_lower}). You probably think 'Planet of the Apes' 🌍🐒 is a travel documentary. It's a lifestyle guide!",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're like a {m_type_lower} who's read a book 📖 once. You know *of* intelligence, but it's not really your thing. Bananas 🍌 are, though. Right?",
            "You've got **{iq_score}** IQ and **{monkey_percentage}%** {m_type_lower}. You're the {m_type_lower} who brings a spork 🥄🍴 to a banana eating contest. Innovative? Or just confused? 🤔",
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a little bit wild 🌿, a little bit... not smart. It's a look. A very specific look. ✨",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're the {m_type_lower} who tries to use a banana 🍌 as a boomerang.  boomerang It doesn't come back. Sad.",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're an adorable mess. Low IQ, tiny bit of {m_type_lower}. We're rooting for you! (To find more bananas 🍌)."
        ],
        "MP_HALF": [
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Half {m_type_lower}, low IQ 📉. You've got some primal energy, but your plans for banana 🍌 acquisition are... simple. Like, 'walk towards yellow thing'. ➡️🟡",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. A decent mix of {m_type_lower} and human, with a low IQ. You're the {m_type_lower} who tries to use a calculator 🧮 for 1+1. Bless.",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Half {m_type_lower}, half-baked ideas 🧠🔥. You've got the spirit for adventure, but you'd probably pack bananas 🍌 for a trip to the library. 📚 Shhh!",
            "You're **{monkey_percentage}%** {m_type_lower} with an IQ of **{iq_score}**. You're enthusiastic but easily confused. Like a {m_type_lower} trying to assemble IKEA furniture. 🛠️🐒 Chaos!",
            "A fun blend: **{monkey_percentage}%** primal, **{iq_score}** IQ. You're the {m_type_lower} who brings a slingshot to a gunfight... and somehow manages to just hit yourself with a banana. 🤕🍌 Oopsie!",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a {m_type_lower} with big heart ❤️, small brain 🧠🤏. You'd share your last banana 🍌, then immediately forget you did. Sweet, but forgetful.",
            "You've got **{iq_score}** IQ and **{monkey_percentage}%** {m_type_lower}. You're the {m_type_lower} who tries to make a banana smoothie 🍌🥤 without a blender. Just... mushy banana. 🤢",
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a delightful paradox. Half {m_type_lower}, half... still figuring it out. 🤔 But definitely loves bananas! 🍌",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're the {m_type_lower} who thinks 'going viral' 🦠 means you ate a bad banana 🍌. Stay safe out there!",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a lovable goof. Half {m_type_lower}, low IQ. You're the reason we have warning labels. ⚠️ But we still adore you (from a safe distance)."
        ],
        "MP_MOSTLY": [
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Mostly {m_type_lower}, low IQ 📉. You're a solid troop member, good at the basics, and full of primal energy. You find the bananas 🍌 and eat them with gusto! 😋",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. High {m_type_upper} percentage, low brainpower. You're the {m_type_lower} who leads the charge for bananas 🍌🚩, even if you're not sure *why*.",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Mostly {m_type_lower}, with just enough brain to be endearingly clumsy. You're the troop's lovable oaf. 🥰🍌 OOK!",
            "You're **{monkey_percentage}%** {m_type_lower} with an IQ of **{iq_score}**. You're great at following orders, especially if the order is 'EAT BANANA!' 🗣️🍌😋 Yes, sir!",
            "Strong {m_type_lower} vibes **{monkey_percentage}%**, but the IQ **{iq_score}** means you're more brawn 💪 than brain 🧠🤏. You're the {m_type_lower} who uses a coconut 🥥 to crack open a banana 🍌. Creative!",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a magnificent beast with a brain that's mostly for show. ✨ Your true talent? Banana 🍌 detection. 👃",
            "You've got **{iq_score}** IQ and **{monkey_percentage}%** {m_type_lower}. You're the {m_type_lower} who thinks 'fine dining' 🧐 is a banana 🍌 without any brown spots. High standards!",
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're mostly {m_type_lower}, with a charmingly simple outlook on life: Eat 🍌, Sleep 😴, Swing 🌿, Repeat 🔄.",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're the {m_type_lower} who tries to trade a shiny rock ✨ for a banana 🍌. Sometimes it works! Mostly not. 🤷‍♂️",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a primal powerhouse with a heart of gold 💛 and a head full of... well, mostly bananas 🍌. We love it!"
        ],
        "MP_ALMOST_PURE": [
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Almost pure {m_type_lower}, low IQ 📉. You're on the path to total {m_type_upper}-ness, just need to stop occasionally trying to use human words. 🗣️🚫 OOK!",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Near-total {m_type_upper}, minimal brain 🧠🤏. You're the {m_type_lower} who's mastered swinging 🌿, but still gets confused by doors 🚪. Push or pull?!",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. So close to being a pure {m_type_upper}! Your brain's a bit simple, but your heart is full of banana 🍌 love. 💛 That's what matters!",
            "You're **{monkey_percentage}%** {m_type_lower} with an IQ of **{iq_score}**. You've mostly forgotten human ways, except for that one time you tried to order bananas 🍌 on Amazon 💻. Epic fail. 😂",
            "Nearly pure {m_type_lower} **{monkey_percentage}%**, with an IQ **{iq_score}** that keeps things uncomplicated. Your philosophy: 'If can reach banana 🍌, is good. If not, ooh ooh aah aah!' 🤔🗣️ Wise.",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a glorious, near-brainless {m_type_lower}. ✨ Your thoughts are few, but they're all about bananas 🍌. Laser focus! 🎯",
            "You've got **{iq_score}** IQ and **{monkey_percentage}%** {m_type_lower}. You're so primal, you probably think clothes 👕 are just weird, itchy leaves 🍂. Go natural!",
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a beautiful beast, unburdened by complex thought. Your spirit animal is a banana 🍌 that just wants to be OOKED at. 👀",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're the {m_type_lower} who's forgotten how to count 🔢, but can smell a ripe banana 🍌 from a mile away. 👃 Superpower!",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a legend in the making. Almost pure {m_type_lower}, with a brain that's just along for the ride. 🎢 Whee!"
        ],
        "MP_PURE": [
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Pure **{m_type_upper}**, low IQ 📉. You are the embodiment of primal {m_type_lower} energy, unburdened by complex thought. A magnificent, simple creature! 🌟🐒",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. **{m_type_upper}** perfection! Your brain is smooth ✨, your spirit is wild 🌪️. You are the ultimate banana 🍌 enthusiast, no thinking required. Just OOK!",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. **100% {m_type_upper}**! Your IQ is just a number, your spirit is LEGENDARY! You live for the banana 🍌, by the banana! 👑 Long live the {m_type_upper}!",
            "You are **{monkey_percentage}%** {m_type_lower}, IQ **{iq_score}**. A true child of the jungle 🌳. Thoughts are fleeting, bananas 🍌 are forever. OOK! Wise words.",
            "Peak {m_type_upper} **{monkey_percentage}%**, charmingly simple **{iq_score} IQ**. You are the heart ❤️ and soul of the troop, even if you sometimes try to eat rocks 🗿. (Don't eat rocks).",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. **100% {m_type_upper}**! Your brain is just a cute accessory 🧠🎀. Your true power? Unwavering devotion to bananas 🍌 and epic OOKs! 🗣️",
            "You've got **{iq_score}** IQ and **{monkey_percentage}%** {m_type_lower}. You are pure {m_type_lower}. You probably think beds 🛏️ are just weird, flat trees 🌳. You're not wrong.",
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You are the {m_type_lower} ideal. No thoughts, just primal urges and an endless quest for bananas 🍌. We salute you! 🫡",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You are the chosen one... to show us the true meaning of 'no thoughts, just vibes'. ✨ And also, where the bananas 🍌 are. 🙏",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You are a masterpiece. A **100% {m_type_upper}** with an IQ that's just a fun little quirk. 🤪 Go forth and be {m_type_lower}! 🐒"
        ]
    },
    "IQ_AVERAGE": { # 60-120
        "MP_0": [
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Average IQ 🧠👍, zero {m_type_lower}. You're a perfectly normal human who stumbled into the wrong analysis. Do you even like bananas 🍌? Weirdo.",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. A standard human brain, zero {m_type_lower} vibes. You probably think 'banana republic' is just a clothing store. 🛍️ It's so much more (or less).",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Standard human intellect, utterly devoid of {m_type_lower} charm. You probably alphabetize your spice rack. 🌶️🤓 So thrilling. 🥱",
            "With an IQ of **{iq_score}** and **{monkey_percentage}%** {m_type_lower}, you're the definition of 'meh'. 😐 Do you find joy in anything, like, say, a perfectly ripe banana? 🍌 Or are you dead inside? 💀",
            "Average brain **{iq_score} IQ**, zero primal spirit **{monkey_percentage}%**. You're so normal, it's almost suspicious. Are you a bot? 🤖 Beep boop, no bananas for you.",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're the human equivalent of a sensible sedan 🚗. Reliable, boring, and definitely not swinging from trees 🌳. Yawn.",
            "You've got **{iq_score}** IQ and **{monkey_percentage}%** {m_type_lower}. You probably think 'Ook' is just a sound birds make. 🐦 It's a way of life, pal. Get with it (or don't).",
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're so un-monkey, you probably use a fork and knife 🍴 for pizza 🍕. You monster. 🧟",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're the person who asks 'Why?' when offered a free banana 🍌. Some things don't need questioning. Just eat it. 🙄",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a fascinating case study in... absolute human-ness. 🧍 No {m_type_lower} detected. Not even a little bit. Sad! 😥",
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're the human equivalent of a 404 error: brain not found, {m_type_lower} not found. 🤷‍♂️",
            "With an IQ of **{iq_score}** and **{monkey_percentage}%** {m_type_lower}, you're so vanilla you make a saltine cracker look like a rave. 😴",
            "You're the reason the gene pool needs a lifeguard. 🏊‍♂️ Average intelligence, but zero survival instinct. Pathetic.",
            "You probably think 'return to {m_type_lower}' is a bad investment strategy. 📈 You're not wrong, but you're also no fun. 🚫🍌",
            "Your analysis came back: Terminally human. 🧍‍♂️ Symptoms include paying taxes and finding bananas 'a bit much'. We're so sorry for your loss. 🙏",
            "You're so average and un-{m_type_lower}, your spirit animal is a beige Toyota Camry. 🚗 So reliable. So... soul-crushingly dull.",
            "You have the IQ to understand the joke, but the zero {m_type_lower} purity to laugh at it. A walking paradox of boredom. 😐",
            "Our sensors detected... nothing. A perfectly average human with no primal spark. Are you an NPC? 🤖 Please say something other than 'hello traveler'.",
            "You're the type of person to get a banana tattoo and then explain it's about potassium. 🤓 We get it, you're smart and boring.",
            "You're so far from {m_type_lower} you probably peel bananas from the wrong end and use a knife and fork. You absolute monster. 🍴🍌"
        ],
        "MP_BARELY": [
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Average IQ 🧠👍, slight {m_type_lower} hint. You're the human who occasionally feels the urge to climb something tall 🏙️ after a banana 🍌. Embrace it!",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Reasonably smart, barely a {m_type_lower}. You might hum jungle tunes 🎶 in the shower 🚿. It's a start.",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Decent brainpower, with a tiny, mischievous {m_type_lower} itch. You might own a 'Hang in there!' cat poster 😼, but secretly wish it was a {m_type_lower}. 🐒 We know.",
            "You've got **{monkey_percentage}%** {m_type_lower} and an IQ of **{iq_score}**. You're the sensible one who still occasionally wonders what it's like to swing from a vine. 🤔🌿 Do it! (Safely).",
            "Average smarts **{iq_score} IQ**, a hint of wild **{monkey_percentage}%** {m_type_lower}). You probably enjoy nature documentaries 🌍... from the comfort of your very human couch. 🛋️📺 Baby steps.",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're like a {m_type_lower} wearing a tiny monocle 🧐. A hint of primal, a lot of... trying too hard? Just kidding (mostly).",
            "You've got **{iq_score}** IQ and **{monkey_percentage}%** {m_type_lower}. You use words like 'henceforth' but secretly want to screech 'BANANA!' 🍌🗣️. Let it out!",
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a human with a {m_type_lower} screen saver. 💻🐒 It's cute. But is it enough? Never.",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're the person who brings a banana 🍌 to a business meeting 'for energy'. We see that tiny {m_type_lower} spark! ✨",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're mostly human, but there's a little {m_type_lower} gremlin 😈 whispering 'eat more bananas' in your ear. Listen to it.",
            "Average brain, but a tiny part of you wants to throw poo. 💩 You suppress it with spreadsheets and quiet desperation. We see you. 👀",
            "That **{monkey_percentage}%** is the part of you that buys a banana-scented air freshener for your sensible car. 🚗🍌 It's a cry for help.",
            "You're like a caged animal that's forgotten what the wild is like. That **{monkey_percentage}%** is just a faint memory of a banana. 🍌💭",
            "You're a responsible adult on the outside, but that **{monkey_percentage}%** {m_type_lower} inside is screaming to climb the office furniture. 🗣️ Do it. No balls.",
            "You have the IQ to know better, but that tiny bit of {m_type_lower} makes you occasionally wonder if you could get away with stealing a banana from the grocery store. 🍌🛒 You can't. You're too awkward.",
            "That **{monkey_percentage}%** is the reason you have a 'Live, Laugh, Love' sign but secretly wish it said 'Screech, Swing, Steal'. 🐒❤️",
            "You're a ticking time bomb of mediocrity with a tiny, banana-flavored fuse. 💣🍌 One day you'll snap and start hooting in a board meeting. We're waiting.",
            "You're smart enough to be boring, but that **{monkey_percentage}%** {m_type_lower} makes you 'quirky'. No, you're just repressing your inner ape. Let it out. 🦍",
            "You're the person who says 'I'm not like other humans' and your one 'wild' trait is liking pineapple on pizza. That's not {m_type_lower}, that's just bad taste. 🍍🍕",
            "That little bit of {m_type_lower} in you is like the 'check engine' light of your soul. 💡 You should probably get that checked out. Or just eat a banana."
        ],
        "MP_HALF": [
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Half {m_type_lower}, average IQ 🧠👍. You're the balanced {m_type_lower} who can use a smartphone 📱 to find the best banana 🍌 deals. Smart!",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. A good mix! You're smart enough to appreciate human comforts 🛋️ but primal enough to enjoy a good swing 🌿. A modern {m_type_lower}! 🐒✨",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Half {m_type_lower}, half sensible. You can file your taxes 📄 AND expertly peel a banana 🍌 with your feet 🦶 (when no one's looking). Impressive!",
            "You're **{monkey_percentage}%** {m_type_lower} with an IQ of **{iq_score}**. You're the bridge between civilization 🏙️ and glorious chaos 🌪️. You probably have a LinkedIn and a favorite tree 🌳 for napping. Goals.",
            "A well-rounded specimen: **{monkey_percentage}%** primal, **{iq_score}** IQ. You can hold a conversation 🗣️ and then immediately try to share your banana 🍌 with your new friend. 🤝 Peak {m_type_lower} diplomacy.",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a {m_type_lower} in a business suit 👔. Ready to negotiate for more bananas 🍌, then swing from the water cooler. 💧",
            "You've got **{iq_score}** IQ and **{monkey_percentage}%** {m_type_lower}. You're the {m_type_lower} who knows how to use a fork 🍴, but prefers to eat bananas 🍌 with your hands (and face). Messy but fun!",
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a delightful blend of human smarts 🤓 and {m_type_lower} charm 🥰. You probably give great hugs and even better banana recommendations. 🍌👍",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're the {m_type_lower} who can quote Shakespeare 📜 and then immediately fling poo 💩. Versatile! (Maybe not the poo part in public).",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a sophisticated savage. Half {m_type_lower}, half genius (average genius, but still). 🧐🐒 You're going places (probably to find bananas 🍌).",
            "Perfectly balanced, as all things should be. Half-human, half-{m_type_lower}, all-around mid. 😐 You're the lukewarm water of primate evolution.",
            "You're smart enough to get a job, but {m_type_lower} enough to get fired for flinging office supplies. 📎 A true enigma.",
            "You're the {m_type_lower} who knows how to use DoorDash to order a single banana. 📱🍌 Modern problems require modern solutions.",
            "You have a 401k and a secret stash of bananas under your bed. 💰🍌 You're prepared for financial collapse and the primate uprising. Smart.",
            "You're the friend who gives great, logical advice, and then eats a banana peel to see what it's like. 🍌🤔 The duality of man.",
            "You're a walking identity crisis. Do you file your taxes or do you throw them in the air like confetti? 📄🎉 Why not both?",
            "You're the reason HR has to add a 'no grooming coworkers' clause to the employee handbook. 📜 Thanks for that.",
            "You're a sophisticated savage. You can discuss fine art 🎨 and then scratch your butt in public without a second thought. 🍑 We respect the confidence.",
            "You're the {m_type_lower} who sets up a hammock in the living room because 'it's good for the spine'. 🛋️🌿 Sure, Jan.",
            "You're a functional degenerate. You pay your bills on time, but you also know the exact location of every fruit tree in a five-mile radius. 🌳🗺️"
        ],
        "MP_MOSTLY": [
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Mostly {m_type_lower}, average IQ 🧠👍. You're a solid, reliable {m_type_lower} with strong jungle instincts and enough brainpower to be effective. You find the best bananas 🍌 and know how to defend them! 💪",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. A well-balanced {m_type_lower}! Smart enough to use tools 🛠️, primal enough to prefer swinging 🌿. Ooh ooh aah aah! 🗣️",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Mostly {m_type_lower}, with a surprisingly functional brain. You're the troop's clever strategist for banana 🍌 raids. 🗺️ Sneaky!",
            "You're **{monkey_percentage}%** {m_type_lower} with an IQ of **{iq_score}**. You know how to work the system... to get more bananas 🍌. You're the {m_type_lower} who negotiates with squirrels 🐿️. And wins. 🤝",
            "Strong {m_type_lower} presence **{monkey_percentage}%**, decent smarts **{iq_score}**. You're the one who teaches the young {m_type_plural_lower} how to properly taunt humans for banana 🍌 handouts. 🐒👨‍🏫 Wise teacher.",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a {m_type_lower} with a plan 📜. That plan is mostly 'get bananas' 🍌, but you execute it with surprising intelligence. Respect. 🙏",
            "You've got **{iq_score}** IQ and **{monkey_percentage}%** {m_type_lower}. You're the {m_type_lower} who can solve a Rubik's Cube 🎲... if it was made of bananas 🍌. And edible. 😋",
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a primal force with a decent head on your shoulders. 🧠💪 You're the {m_type_lower} who invents new ways to open coconuts 🥥. For the banana inside, of course. 🍌",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're the {m_type_lower} who can read a map 🗺️ (upside down, but still) to find the legendary Golden Banana Tree 🌟🌳🍌. Go get it!",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a leader in the making. Mostly {m_type_lower}, but with enough smarts to be dangerous (to banana hoarders). 😈🍌",
            "You're mostly {m_type_lower}, but with just enough human intelligence to be a real menace. 😈 You know how to open child-proof locks. Uh oh.",
            "You're the {m_type_lower} who figured out how to use a credit card 💳 to buy an obscene amount of bananas online. 🍌💻 You're in debt, but you're happy.",
            "You're a primal force with a plan. That plan is usually 'get banana', but you execute it with the strategic genius of a B-movie villain. 🗺️🍌",
            "You're the reason for the sign 'Please don't feed the {m_type_plural_lower}'. Not because you're dumb, but because you'll unionize them. ✊🍌",
            "You're so close to returning to {m_type_lower}, but you still remember your ex's Netflix password. 📺 A curse and a blessing.",
            "You're the {m_type_lower} who starts a banana-based cryptocurrency. 🍌💰 It's called ApeCoin. Oh wait, that's real. You're a trendsetter!",
            "You're a hairy, banana-breathing genius... well, an average genius. You're the guy who hotwires the banana cart at the zoo. 🛒⚡",
            "You're the {m_type_lower} who tries to mansplain swinging from vines to other {m_type_plural_lower}. 🌿🗣️ 'Actually, you want to use an underhand grip for better momentum...' Shut up, nerd.",
            "You're a high-functioning primate. You can hold a conversation, but you're just waiting for the other person to stop talking so you can ask if they're gonna finish that banana. 🍌👀",
            "You're the {m_type_lower} who uses your human intellect to justify your bad behavior. 'It's not chaos, it's performance art.' 🎨 Sure it is, buddy."
        ],
        "MP_ALMOST_PURE": [
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Almost pure {m_type_lower}, average IQ 🧠👍. You're on the verge of total {m_type_upper}-ness, using your intellect to optimize your primal lifestyle. Like, calculating the perfect vine 🌿 trajectory. 📐",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Near-total {m_type_upper}, decent brain. You're the {m_type_lower} who's figured out how to use human technology 📱 to get more bananas 🍌. Clever! 💡",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. So close to pure {m_type_upper}, with a brain that's surprisingly not just for show! You're probably designing a better banana peel. 🍌✍️ Patent pending.",
            "You're **{monkey_percentage}%** {m_type_lower} with an IQ of **{iq_score}**. You use your human-level intellect for purely {m_type_lower} pursuits. Like building the ultimate banana 🍌 catapult. 🏹 Launch it!",
            "Almost pure {m_type_lower} **{monkey_percentage}%**, with an average IQ **{iq_score}** that makes you a dangerously effective primate. You're the one who outsmarts the zookeepers. 🧠🐒 Freedom!",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a {m_type_lower} with a surprisingly good grasp of physics ⚛️... when it comes to banana 🍌 trajectory. Bullseye! 🎯",
            "You've got **{iq_score}** IQ and **{monkey_percentage}%** {m_type_lower}. You're so close to peak {m_type_lower}, you probably dream in banana-vision 🍌👀. What a world!",
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a primal genius in disguise 🥸. Using your smarts to live your best {m_type_lower} life. We see you. 😉",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're the {m_type_lower} who can pick a lock 🔓... to get to the banana 🍌 stash. Resourceful! 💰",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a legend. Almost pure {m_type_lower}, but with a brain that makes you unstoppable in your quest for bananas 🍌. All hail! 🙌",
            "You're so close to perfection. Almost pure {m_type_lower}, but that pesky average IQ means you're self-aware about your banana addiction. 🍌😥 A beautiful tragedy.",
            "You're the {m_type_lower} who can do your own taxes, but you file for a 'banana-dependent' exemption. 📄🍌 The IRS is confused, but intrigued.",
            "You're a primal god held back by the mortal coil of... remembering your own birthday. 🎂 It's a tough life.",
            "You've almost shed all of humanity, but you still have an opinion on the new Taylor Swift album. 🎶 It's your last link. Let it go.",
            "You're the {m_type_lower} who builds a surprisingly complex shelter out of banana peels and discarded Amazon boxes. 📦🍌 Resourceful!",
            "You're a genius trapped in a {m_type_lower}'s body. Well, an average genius. You're like a furry, slightly-less-impressive Stephen Hawking who just wants bananas. 🍌👨‍🦽",
            "You're so close to enlightenment, but you keep getting distracted by shiny objects ✨ and the crinkle of a banana peel. So close, yet so far.",
            "You're the {m_type_lower} who tries to start a book club, but everyone just eats the books. 📚🐛 It was a good effort.",
            "You're a walking, swinging existential crisis. 'To ook, or not to ook, that is the question.' 🗣️❓ The answer is always 'ook'.",
            "You're the final boss of the local zoo. You've outsmarted the keepers, established a banana-based economy, and are planning your escape. 🗺️👑 We believe in you."
        ],
        "MP_PURE": [
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Pure **{m_type_upper}**, average IQ 🧠👍. You are the embodiment of primal {m_type_lower} energy, with just enough brain to make it truly chaotic. A magnificent, unpredictable creature! 🌪️🐒",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. **{m_type_upper}** perfection! Your spirit is wild 🌿, and your average brain just makes you better at finding bananas 🍌. OOK! Smart OOK!",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. **100% {m_type_upper}** with a surprisingly average brain! You're the chaotic good 😇😈 of the jungle. You mean well, but there will be banana 🍌 peels everywhere. 😅",
            "You are **{monkey_percentage}%** {m_type_lower}, IQ **{iq_score}**. A pure primate heart ❤️ with a mind that can actually remember where you buried the good bananas 🍌. A true asset! 🗺️ Treasure!",
            "Peak {m_type_upper} **{monkey_percentage}%**, average smarts **{iq_score}**. You're the {m_type_lower} who can lead a successful banana 🍌 raid and then write a surprisingly coherent poem 📜 about it. Shakespearean {m_type_lower}!",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. **100% {m_type_upper}**! Your brain is just a tool 🛠️ to achieve maximum banana 🍌 acquisition. And you're a master craftsman. 👑",
            "You've got **{iq_score}** IQ and **{monkey_percentage}%** {m_type_lower}. You are pure {m_type_lower} with a secret weapon: an average human brain 🧠. The other {m_type_plural_lower} don't stand a chance. ⚔️",
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You are the {m_type_lower} supreme, with just enough smarts to be hilariously effective. 😂 You're a walking meme. 밈",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You are the chosen one... to prove that even pure {m_type_plural_lower} can have a decent IQ. 🧐 And an insatiable lust for bananas 🍌. Obviously.",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You are a paradox. A legend. A **100% {m_type_upper}** with a brain that actually works. 🤯 What will you do with this power? (Get bananas 🍌, probably).",
            "**100% {m_type_upper}** with an average human brain. This is a bug in the simulation. 🐛 You're a god-tier {m_type_lower} who can do long division. What is happening?! 🤯",
            "You are the chosen one. The prophecy spoke of a {m_type_lower} who was pure of heart but could also operate a forklift. 🏗️ The banana warehouses are yours for the taking.",
            "You're a paradox. A riddle. A pure {m_type_lower} who understands irony. You're probably laughing at this analysis right now. We're scared. 😨",
            "You are the missing link. The bridge between primal chaos and... average human competence. It's beautiful. And weird. 🐒🧍‍♂️",
            "You're a pure {m_type_lower} who accidentally became self-aware. Now you're burdened with the knowledge of your own banana consumption. 🍌 A heavy crown to wear. 👑",
            "You're the {m_type_lower} who could lead the revolution, write the manifesto, and design the flag. 🍌🚩 The humans don't stand a chance.",
            "You're a pure primate with an internal monologue. It's probably just 'banana, banana, banana...' but with really good grammar. 🍌📜",
            "You are the {m_type_lower} who looks at the stars and doesn't just see shiny things, but contemplates the vast, banana-less void of space. 🌌🍌 And it makes you sad.",
            "You're a walking, talking (ooking) evolutionary anomaly. You're the reason scientists are both excited and terrified. 🧑‍🔬🔬",
            "You're **100% {m_type_upper}**, but you know what a meme is. You're probably the one making the memes. You're too powerful. Please spare us. 🙏"
        ]
    },
    "IQ_HIGH": { # 121-160
        "MP_0": [
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. High IQ 🧠✨, zero {m_type_lower}. You're a certified genius who somehow ended up here. Do you analyze the nutritional content of bananas 🍌 for fun? 🤓",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Brilliant mind, no primal energy. You probably think 'going ape' 🦍 is a mathematical theorem 📐. It's simpler than that.",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. So smart, yet so... tragically human. 🧐 You probably use a fork and knife 🍴 for bananas 🍌, you monster. 😱 The horror!",
            "With an IQ of **{iq_score}** and **{monkey_percentage}%** {m_type_lower}, you're wasting all that brainpower on non-banana 🍌 related activities. What a shame. 😔 Think of the banana innovations lost!",
            "Big brain **{iq_score} IQ** 🧠🤯, no {m_type_lower} soul **{monkey_percentage}%**. You could solve world hunger 🌍, but you'd probably just write a thesis 📄 on it. And forget the bananas 🍌.",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're so smart, you probably calculate the optimal trajectory to throw away a banana peel 🍌. Instead of, you know, swinging. 🌿 Boring!",
            "You've got **{iq_score}** IQ and **{monkey_percentage}%** {m_type_lower}. You're the human equivalent of a supercomputer 💻 that can't open a banana 🍌. Sad.",
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a genius, but you're missing the key ingredient: {m_type_lower} chaos! 🌪️ Get some bananas 🍌 and loosen up!",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're the person who overthinks a banana 🍌. 'Is it ethically sourced? What's its carbon footprint?' Just eat it, nerd! 🤓",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a brilliant, banana-less void. 🕳️ Come to the {m_type_lower} side, we have bananas! 🍌 And fun! 🎉"
        ],
        "MP_BARELY": [
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. High IQ 🧠✨, slight {m_type_lower} hint. You're the jungle intellectual 🧐, {m_type_lower}, but your primal urges are... minimal. Do you even know how to climb a tree 🌳? Pathetic.",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. A brilliant mind trapped in a surprisingly human-like form. You probably calculate the optimal angle 📐 for peeling a banana 🍌, rather than just eating it. Overthinker!",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. A genius brain 🧠🤯 with a tiny, almost imperceptible {m_type_lower} whisper. You might theorize about swinging from vines 🌿, but never actually do it. 🤓 Coward!",
            "You've got **{monkey_percentage}%** {m_type_lower} and an IQ of **{iq_score}**. You're the one who writes complex philosophical treatises 📜 on the nature of 'ook'. 🤔 We just OOK. It's easier.",
            "Smarty pants **{iq_score} IQ** 🤓, with a dash of {m_type_lower} **{monkey_percentage}%**. You probably try to teach squirrels 🐿️ calculus ✖️➕. They're not impressed. They want nuts 🌰 (or bananas 🍌).",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a genius who secretly wishes they were a {m_type_lower}. It's okay, we accept you. 🤗 (If you bring bananas 🍌).",
            "You've got **{iq_score}** IQ and **{monkey_percentage}%** {m_type_lower}. You're the {m_type_lower} who uses a thesaurus 📚 to describe a banana 🍌. 'An elongated, curved, yellow fruit...' Just say banana!",
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a high-functioning human with a tiny {m_type_lower} keychain 🐒🔑. Cute, but not very primal. Try harder.",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're the genius who designs a robot 🤖 to peel your bananas 🍌. Lazy, but also kinda smart. We're conflicted. 🤔",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a brilliant mind with a whisper of the wild 🌿. Let that whisper become a ROAR! 🗣️ (And eat more bananas 🍌)."
        ],
        "MP_HALF": [
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Half {m_type_lower}, high IQ 🧠✨. You're the sophisticated {m_type_lower} who can debate philosophy 📜 and then immediately swing from the nearest curtain rod. 🐒💨",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. A fascinating mix! You're smart enough to build a banana-sorting machine 🍌🤖, and primal enough to just eat them all anyway. Balance! ⚖️",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Half {m_type_lower}, all genius. You're the one inventing new, more efficient ways to fling poo 💩 with deadly accuracy. 🎯 Impressive... and gross. 🤢",
            "You're **{monkey_percentage}%** {m_type_lower} with an IQ of **{iq_score}**. You're the {m_type_lower} who can hack into the banana 🍌 plantation's security system. 💻 Get those bananas!",
            "A dangerous combination: **{monkey_percentage}%** primal instinct, **{iq_score}** IQ. You're the {m_type_lower} who could lead a revolution ✊... for better banana 🍌 distribution. We're in! 🚩",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a {m_type_lower} with a PhD 🎓 in banana-nomics 🍌📈. You know the true value of a good banana. Priceless!",
            "You've got **{iq_score}** IQ and **{monkey_percentage}%** {m_type_lower}. You're the {m_type_lower} who can solve complex equations 🤓... to figure out how many bananas 🍌 you can eat in one sitting. Important research!",
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a brilliant beast 🧠🐒. You can outsmart a human and out-swing any {m_type_lower}. The total package! 🎁",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're the {m_type_lower} who writes poetry 📜 about bananas 🍌. And it's actually good. Surprisingly. 😮",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a primal intellectual. A walking contradiction. A banana-loving genius 🍌🧐. We're obsessed. 😍"
        ],
        "MP_MOSTLY": [
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Mostly {m_type_lower}, high IQ 🧠✨. You're a jungle genius with strong primal instincts. You're probably inventing new ways to acquire and hoard bananas 🍌! 🧐",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. High {m_type_upper} percentage, high brainpower. You're the {m_type_lower} who's plotting world banana 🍌 domination. We salute you! 🫡",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Mostly {m_type_lower}, with a brain sharp enough to outsmart any human. You're the alpha 👑 and the chief strategist 🗺️. All hail the banana king/queen!",
            "You're **{monkey_percentage}%** {m_type_lower} with an IQ of **{iq_score}**. You're the one who develops advanced banana-finding algorithms 🍌💻. And they work. Every. Single. Time. ✨ Genius!",
            "Powerful {m_type_lower} **{monkey_percentage}%**, brilliant mind **{iq_score}**. You're the {m_type_lower} who could write a symphony 🎶 about bananas 🍌, then eat the conductor's baton. 🥢 Rock on!",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a {m_type_lower} with a supercomputer 💻 for a brain. Your primary function: OPTIMIZE BANANA 🍌 INTAKE. Mission accepted. ✅",
            "You've got **{iq_score}** IQ and **{monkey_percentage}%** {m_type_lower}. You're the {m_type_lower} who can calculate the exact nutritional value 📊 of every banana 🍌 in the jungle. And then eat them all. 😋",
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a primal mastermind 🧠🐒. You outwit, outplay, and out-banana everyone. 🍌🏆 Survivor: Jungle Edition winner!",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're the {m_type_lower} who uses advanced psychological warfare 🤯 to get other {m_type_plural_lower} to give you their bananas 🍌. Diabolical and effective. 😈",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a force to be reckoned with. Mostly {m_type_lower}, but with a brain that could conquer nations (for their bananas 🍌, of course). 🌍"
        ],
        "MP_ALMOST_PURE": [
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Almost pure {m_type_lower}, high IQ 🧠✨. You're on the verge of total {m_type_upper}-ness, using your genius intellect to become the ultimate primal force. Fear the banana-wielding brain! 🍌⚔️",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Near-total {m_type_upper}, high brain. You're the {m_type_lower} who's figured out how to weaponize banana 🍌 peels. The humans never saw it coming. 😈",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. So close to pure {m_type_upper}, with a terrifyingly effective brain! You're the {m_type_lower} who invents cold fusion ⚛️ just to ripen bananas 🍌 faster. Dedication!",
            "You're **{monkey_percentage}%** {m_type_lower} with an IQ of **{iq_score}**. You're a primal god 🌟 with a supercomputer 💻 for a brain. The jungle 🌳 trembles before your banana-fueled intellect. 🍌",
            "Almost pure {m_type_lower} **{monkey_percentage}%**, genius IQ **{iq_score}**. You're the final boss 🎮 of the banana 🍌 game. All your oohs and aahs are calculated for maximum impact. 🗣️💥",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a {m_type_lower} demigod 🌟🐒. Your intellect is matched only by your primal fury... when someone touches your banana 🍌. Don't touch the banana.",
            "You've got **{iq_score}** IQ and **{monkey_percentage}%** {m_type_lower}. You're so close to {m_type_lower} perfection, you probably speak fluent banana 🍌🗣️. And they speak back. 🤯",
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a terrifyingly smart beast. 🧠👹 You use your genius for one thing: acquiring ALL the bananas 🍌. And we respect that. 🙌",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're the {m_type_lower} who could write a best-selling book 📖 on 'The Art of the Banana Heist' 🍌💰. We'd buy it. 💵",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You are the apex predator of intellectuals. Almost pure {m_type_lower}, with a brain that's sharper than any claw. 🐾🔪 Fear them."
        ],
        "MP_PURE": [
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Pure **{m_type_upper}**, high IQ 🧠✨. You are the embodiment of primal {m_type_lower} energy, combined with genius intellect. A terrifying, magnificent creature! 👹🌟",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. **{m_type_upper}** perfection! Your spirit is wild 🌪️, your brain is sharp 🔪. You are the ultimate banana 🍌 strategist, leading the troop to glory! 🚩",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. **100% {m_type_upper}** and a genius! You are the {m_type_lower} philosopher-king 👑🍌🧐, ruling with wisdom and a firm grip on the best bananas.",
            "You are **{monkey_percentage}%** {m_type_lower}, IQ **{iq_score}**. A perfect blend of primal fury 😡 and cold, hard intellect 🧠. You don't just want bananas 🍌; you *deserve* them, and you can prove it mathematically. 💯 Q.E.D.",
            "Ultimate {m_type_upper} **{monkey_percentage}%**, high IQ **{iq_score}**. You are the stuff of legends. {m_type_plural_lower} will sing songs 🎶 of your banana 🍌 conquests for generations. 🏆 Epic!",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. **100% {m_type_upper}**! Your brain is a super-charged banana-seeking missile 🍌🚀. There is no escape from your intellect... or your OOK! 🗣️",
            "You've got **{iq_score}** IQ and **{monkey_percentage}%** {m_type_lower}. You are pure {m_type_lower} enlightened by genius. 🌟 You see the banana 🍌 matrix. You ARE the banana 🍌 matrix. 🤯",
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You are the {m_type_lower} ideal, evolved. Primal power, genius mind. You probably invented the banana 🍌. Or perfected it. 🙏",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You are the chosen one... to lead the {m_type_plural_lower} into a new golden age of banana 🍌 prosperity. Your reign will be legendary! 👑",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You are a god among {m_type_plural_lower}. Pure primal energy, guided by a brilliant mind. We are not worthy. 🙇‍♂️🙇‍♀️ (But please share bananas 🍌)."
        ]
    },
    "IQ_GENIUS": { # 161-199
        "MP_0": [
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Genius IQ 🧠🌌, zero {m_type_lower}. You've solved the mysteries of the universe but are utterly baffled by the concept of 'fun' 🥳. Or bananas 🍌. Sad.",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Off-the-charts brain, no primal energy. You probably analyze the philosophical implications of a banana 🍌 peel slip. 🙄 Just don't slip!",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. A cosmic brain 🌌 in a tragically un-fun package. You probably think bananas 🍌 are 'suboptimal potassium delivery systems.' 🙄 Nerd alert! 🚨",
            "With an IQ of **{iq_score}** and **{monkey_percentage}%** {m_type_lower}, you're so smart it's boring. Go climb a tree 🌳 or something. Oh wait, you can't. 🚫 Sad trombone. 🎺",
            "Galaxy brain **{iq_score} IQ** 🌌🧠, zero {m_type_lower} spirit **{monkey_percentage}%**. You've probably calculated the exact moment the universe will end ⏳, but have you ever truly *lived* (i.e., eaten a banana 🍌 without overthinking it)? 🤔",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a genius who probably finds bananas 🍌 'pedestrian'. Your loss, pal. More for us! 😋",
            "You've got **{iq_score}** IQ and **{monkey_percentage}%** {m_type_lower}. You're so smart, you've forgotten how to have fun. 🎉🚫 Try OOKing. It helps. 🗣️",
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a brilliant, beautiful mind... completely devoid of {m_type_lower} charm. 💔 It's a tragedy, really.",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're the person who brings a PowerPoint presentation 📊 to a banana 🍌 party. Read the room, genius. 🙄",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a cosmic intellect trapped in a banana-less existence. 🍌🚫 We pity you. (And will eat your share of bananas)."
        ],
        "MP_BARELY": [
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Genius IQ 🧠🌌, slight {m_type_lower} hint. You're the transcendent being who occasionally feels a faint urge to... scratch. It's confusing. 🤔",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Cosmic intellect, minimal {m_type_lower}. You're probably trying to build a banana-powered teleporter. 🍌➡️🌌 Ambitious!",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. A god-tier intellect 👑🧠 with a vestigial {m_type_lower} soul. You might design a perfect banana 🍌✨, then forget to eat it. 🤯🤷 Classic genius.",
            "You've got **{monkey_percentage}%** {m_type_lower} and an IQ of **{iq_score}**. You're the one who proves, with quantum physics ⚛️, that all bananas 🍌 are interconnected. 🔗 Deep, man.",
            "Super genius **{iq_score} IQ** 🦸‍♂️🧠, with a tiny, almost adorable {m_type_lower} quirk **{monkey_percentage}%**. You probably try to communicate with bananas 🍌 telepathically. Are they talking back? 💬",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a genius who occasionally wonders if bananas 🍌 hold the secrets of the universe. (They do. The secret is 'eat more bananas'). 🤫",
            "You've got **{iq_score}** IQ and **{monkey_percentage}%** {m_type_lower}. You're the {m_type_lower} who writes sonnets 📜 about the existential angst of a single banana 🍌. Beautifully tragic.",
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a cosmic brain 🌌 with a tiny {m_type_lower} heart ❤️ beating for bananas 🍌. It's... surprisingly sweet. 🥰",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're the genius who calculates the precise moment a banana 🍌 reaches peak ripeness. ⏰ And then eats it with a fork. 🍴 Sigh.",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a brilliant mind with a faint echo of the jungle 🌳. Let that echo grow into a mighty OOK! 🗣️ (And grab a banana 🍌)."
        ],
        "MP_HALF": [
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Half {m_type_lower}, genius IQ 🧠🌌. You're the hyper-intelligent {m_type_lower} who's figured out how to optimize nap time 😴 and banana 🍌 consumption using complex algorithms. 💻",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. A genius with a wild side! You're probably trying to teach other {m_type_plural_lower} quantum banana 🍌 physics ⚛️. Good luck. They just want bananas.",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Half {m_type_lower}, all super-genius. You've weaponized your intellect for maximum banana 🍌 acquisition and primal fun. 💣🧠 Deadly combo!",
            "You're **{monkey_percentage}%** {m_type_lower} with an IQ of **{iq_score}**. You're the {m_type_lower} who builds a sentient AI 🤖 just to tell you where the ripest bananas 🍌 are. 📍 Smart move!",
            "A formidable entity: **{monkey_percentage}%** primal power, **{iq_score}** IQ. You're the {m_type_lower} who could negotiate peace treaties 🕊️ between warring {m_type_lower} factions... if there were enough bananas 🍌 involved. 🤝",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a {m_type_lower} who can quote Einstein 🧐 and then immediately eat a banana 🍌 like you haven't eaten in days. Intense.",
            "You've got **{iq_score}** IQ and **{monkey_percentage}%** {m_type_lower}. You're the {m_type_lower} who uses game theory 🎲 to win every banana 🍌 hoarding contest. Unbeatable!",
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a brilliant beast, a primal intellectual. 🧠👹 You could rule the world 🌍... or just a very large banana 🍌 tree. 🌳",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're the {m_type_lower} who invents a new language based entirely on banana 🍌 sounds. OOK-anana! 🗣️",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a genius {m_type_lower} hybrid. You can solve the world's problems 🌍... after you've had your morning banana 🍌. Priorities."
        ],
        "MP_MOSTLY": [
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Mostly {m_type_lower}, genius IQ 🧠🌌. You're a primal force with a cosmic brain. You're not just finding bananas 🍌, you're creating a banana-based civilization! 🏛️",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. High {m_type_upper} percentage, genius brain. You're the {m_type_lower} who's figured out the meaning of life ✨, and it involves bananas 🍌. Obviously.",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Mostly {m_type_lower}, with a brain that could power a small city 🏙️. You're the {m_type_lower} who leads expeditions to find the mythical Golden Banana 🌟🍌. 🗺️ Good luck!",
            "You're **{monkey_percentage}%** {m_type_lower} with an IQ of **{iq_score}**. You're the {m_type_lower} prophet 🙏, your hoots and hollers are actually complex equations predicting banana 🍌 futures. 📈🗣️",
            "Dominant {m_type_lower} **{monkey_percentage}%**, god-like intellect **{iq_score}**. You're the {m_type_lower} who doesn't just climb trees 🌳, you *become* the tree, one with the banana 🍌 source. 🧘 Deep.",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a {m_type_lower} warlord ⚔️ with a genius battle plan... for acquiring all the bananas 🍌 in a tri-county area. Terrifyingly effective.",
            "You've got **{iq_score}** IQ and **{monkey_percentage}%** {m_type_lower}. You're the {m_type_lower} who can build a rocket ship 🚀 out of banana 🍌 peels and sheer willpower. To the moon! 🌕 (For moon bananas).",
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a primal god 🌟🧠, your intellect matched only by your ferocity in defending your banana 🍌 stash. Fear them.",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're the {m_type_lower} who uses quantum entanglement ⚛️ to instantly teleport bananas 🍌 into your mouth. The future is now!",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You are the ultimate {m_type_lower} lifeform. Mostly primal, but with a genius brain that makes you unstoppable. 🌪️ All hail the banana overlord! 👑🍌"
        ],
        "MP_ALMOST_PURE": [
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Almost pure {m_type_lower}, genius IQ 🧠🌌. You're on the verge of total {m_type_upper}-ness, using your god-tier intellect to become the ultimate primal force. The universe trembles! 🌍💥",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Near-total {m_type_upper}, genius brain. You're the {m_type_lower} who's transcended reality and is now living in a banana-based simulation 🍌💻 of your own design.",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Almost pure {m_type_upper}, with a brain that sees the banana 🍌 matrix. You know the code. You ARE the code. ✨ Neo {m_type_lower}!",
            "You're **{monkey_percentage}%** {m_type_lower} with an IQ of **{iq_score}**. You're a primal deity 🌟🐒 with a super-intellect. You don't just eat bananas 🍌, you commune with their cosmic essence. 🌌🙏 OMMMM...",
            "Nigh-perfect {m_type_lower} **{monkey_percentage}%**, genius IQ **{iq_score}**. You're the {m_type_lower} who can bend space-time 🌀 to bring bananas 🍌 closer. The chosen one! 👑",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a {m_type_lower} god-king 👑🌟, your genius dedicated to the pursuit of the perfect banana 🍌 and the loudest OOK! 🗣️ A true inspiration.",
            "You've got **{iq_score}** IQ and **{monkey_percentage}%** {m_type_lower}. You're so close to {m_type_lower} divinity, you probably photosynthesize banana 🍌 energy. ☀️",
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You are the singularity where primal instinct meets cosmic intellect. 🌌💥 And it's all about bananas 🍌. Beautiful.",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're the {m_type_lower} who can rewrite the laws of physics 📜... to make bananas 🍌 rain from the sky. 🌧️ Make it happen!",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You are the future. Almost pure {m_type_lower}, with a genius brain that will lead us all to banana 🍌 utopia. We follow! 🚩"
        ],
        "MP_PURE": [
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Pure **{m_type_upper}**, genius IQ 🧠🌌. You are the embodiment of primal {m_type_lower} energy, combined with cosmic intellect. A divine, terrifying, banana-fueled entity! 🌟👹🍌",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. **{m_type_upper}** perfection! Your spirit is wild 🌪️, your brain is cosmic 🌌. You are the banana 🍌 messiah, leading the troop to enlightenment! 🙏",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. **100% {m_type_upper}** and a certified GALAXY BRAIN! 🌌🧠 You are the Banana Overlord 👑, your wisdom is as vast as your banana 🍌 hoard! We bow!",
            "You are **{monkey_percentage}%** {m_type_lower}, IQ **{iq_score}**. A divine primate 🌟🐒, your thoughts shape reality, and reality is banana-shaped 🍌. All hail the {m_type_upper} Supreme! 🙌✨",
            "The ultimate being: **{monkey_percentage}% {m_type_upper}**, **{iq_score}** IQ. You are the singularity where primal instinct and infinite intellect merge. You ARE the bananaverse. 🍌🌍✨ Mind blown. 🤯",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. **100% {m_type_upper}**! Your genius brain 🧠 is powered by pure banana 🍌 energy. You are unstoppable. You are... BANANAGOD! ⚡️👑",
            "You've got **{iq_score}** IQ and **{monkey_percentage}%** {m_type_lower}. You are pure {m_type_lower} ascended to godhood through sheer intellect and banana 🍌 consumption. We are not worthy. 🙇‍♂️",
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You are the nexus of all {m_type_lower}-kind and all knowledge. 🌌📚 Your OOKs are universal truths. 🗣️✨",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You are the chosen one... to unite all {m_type_plural_lower} under the banner of the Golden Banana 🌟🍌. Your wisdom will guide us. 🙏",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You are perfection. The ultimate lifeform. Pure {m_type_upper}, genius mind. Now, about those bananas... can we have some? 🥺🍌"
        ]
    },
    "IQ_200": { # 200
        "MP_0": [
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. **200** IQ 🤯, zero {m_type_lower}. You are a singularity of pure intellect, utterly devoid of primal energy. You probably find bananas 🍌 'conceptually interesting'. 🙄",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Cosmic brain 🌌🧠, no {m_type_lower}. You've solved reality, but can't figure out how to open a banana 🍌 without a complex tool. 🛠️ Sad!",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You've transcended humanity, but forgot to pack the fun 🥳. Or the {m_type_lower} spirit. You probably ponder the banana 🍌, but never eat it. 🤔🚫",
            "With an IQ of **{iq_score}** and **{monkey_percentage}%** {m_type_lower}, you're a god-like intellect 🌟🧠 in a boring human shell. Do you even remember what joy feels like? It's yellow and curved. 💛🍌",
            "Transcendent intellect **{iq_score} IQ**, zero primal essence **{monkey_percentage}%**. You are the universe observing itself 🌌👀, and it's mildly disappointed by the lack of bananas 🍌. 📉 We are too.",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're so smart, you probably find the concept of a {m_type_lower} 'primitive'. 🧐 Well, primitive beings have more fun. And bananas 🍌.",
            "You've got **{iq_score}** IQ and **{monkey_percentage}%** {m_type_lower}. You're a god 🌟, but a boring one. No OOKs, no banana 🍌 fights. What's the point? 🤷‍♀️",
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You are pure thought 💭. No body, no {m_type_lower}, no bananas 🍌. Just... thoughts. Sounds dull. 😴",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're the person who would write a 10,000-page dissertation on a single banana 🍌. And still not eat it. 📄🙄",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You are a cosmic super-brain 🌌🧠 with zero {m_type_lower} appeal. We're not impressed. Give us bananas 🍌 and chaos! 🌪️"
        ],
        "MP_BARELY": [
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. **200** IQ 🤯, slight {m_type_lower} hint. You're a transcendent being who occasionally feels a faint, confusing urge to... groom someone. It's a glitch. 🐒✨",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Cosmic intellect 🌌🧠, minimal {m_type_lower}. You're probably trying to communicate with bananas 🍌 using telepathy. 💬 Are they responding?",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. A mind that encompasses galaxies 🌌, with a tiny, almost forgotten {m_type_lower} spark. You might accidentally invent a banana 🍌 out of pure thought. ✨🤯 Whoa.",
            "You've got **{monkey_percentage}%** {m_type_lower} and an IQ of **{iq_score}**. You are the universe's most advanced being 🌠, with a slight craving for a banana 🍌 you can't quite explain. ❓ It's primal, baby!",
            "Omniscient **{iq_score} IQ** 👁️‍🗨️, with a flicker of {m_type_lower} **{monkey_percentage}%**. You understand the fundamental forces of banana-ness 🍌, but are too evolved to just... peel one. 🧐 Or are you?",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a god 🌟 with a tiny {m_type_lower} pet 🐒. It whispers secrets of bananas 🍌 in your ear. Listen closely.",
            "You've got **{iq_score}** IQ and **{monkey_percentage}%** {m_type_lower}. You're so smart, you can calculate the meaning of life ✨... but you still get a little thrill from a perfectly ripe banana 🍌. That's the {m_type_lower} in you!",
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You are pure intellect 🧠 with a faint banana 🍌-scented aura. Intriguing... and slightly delicious. 🤤",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're the cosmic entity 🌌 that sometimes dreams of swinging through trees 🌳 and eating bananas 🍌. Your subconscious knows what's up.",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You are a god-like being with a tiny, adorable {m_type_lower} flaw: you kinda like bananas 🍌. Embrace it! 🤗"
        ],
        "MP_HALF": [
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Half {m_type_lower}, **200** IQ 🤯. You're the hyper-intelligent {m_type_lower} who's figured out the optimal strategy for interdimensional banana 🍌 acquisition. 🌀",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. A genius with a wild side! You're probably trying to teach other {m_type_plural_lower} how to fold space-time 🌌 to reach bananas 🍌 faster. Ambitious!",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Half {m_type_lower}, half cosmic entity 🌟. You use your omnipotence to ensure a never-ending supply of perfect bananas 🍌. And maybe for some lighthearted chaos. 😈🌀",
            "You're **{monkey_percentage}%** {m_type_lower} with an IQ of **{iq_score}**. You are a demigod 🌟🐒 of the jungle, your thoughts create banana 🍌 groves, your roars shake dimensions. 🌳🗣️🌌 Epic!",
            "A divine paradox: **{monkey_percentage}%** primal heart ❤️, **{iq_score}** IQ. You are the {m_type_lower} who can debate the gods 🙏 and then challenge them to a banana 🍌 eating contest. And win. 🏆",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a god-tier {m_type_lower} 👑🧠. You can create bananas 🍌 with your mind and then OOK about it. The ultimate power combo.",
            "You've got **{iq_score}** IQ and **{monkey_percentage}%** {m_type_lower}. You're the {m_type_lower} who solved cold fusion ⚛️... to power your banana 🍌 smoothie blender. Priorities!",
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You are a cosmic {m_type_lower} lord 🌌🐒. Your intellect is as vast as the universe, your love for bananas 🍌 as deep as the ocean. 🌊",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're the {m_type_lower} who can rewrite reality 📜... to make sure every banana 🍌 is perfectly ripe. A true hero. 🦸‍♂️",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You are a divine being, half {m_type_lower}, half pure awesome 🤩. Your destiny: to lead us to a world of infinite bananas 🍌 and wisdom. ✨"
        ],
        "MP_MOSTLY": [
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Mostly {m_type_lower}, **200** IQ 🤯. You're a primal force with a cosmic brain 🌌🧠. You're not just finding bananas 🍌, you're creating a banana-based Dyson sphere! 🪐",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. High {m_type_upper} percentage, cosmic brain. You're the {m_type_lower} who's figured out the ultimate purpose of the universe ✨, and it involves a lot of bananas 🍌.",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Mostly {m_type_lower}, with a brain that IS the universe 🌌. You are the Great {m_type_upper} Spirit, and the cosmos is your banana 🍌 tree. 🌳 OOK!",
            "You're **{monkey_percentage}%** {m_type_lower} with an IQ of **{iq_score}**. You are the alpha 👑 of all alphas, your intellect shapes the jungle 🌳, your will commands the banana 🍌 tides. 🌊 Powerful!",
            "Ascended {m_type_lower} **{monkey_percentage}%**, omniscient mind **{iq_score}**. You are the living embodiment of banana-fueled evolution 🍌➡️🐒✨. All {m_type_plural_lower} aspire to be you. 🙏",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a {m_type_lower} deity 🌟🐒, your OOKs are cosmic decrees 📜, your banana 🍌 stashes are legendary. We worship you. 🙌",
            "You've got **{iq_score}** IQ and **{monkey_percentage}%** {m_type_lower}. You're the {m_type_lower} who can control the weather ⛈️... to ensure optimal banana 🍌 growing conditions. A true leader.",
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You are a primal god-emperor 👑👹. Your intellect is matched only by your insatiable hunger for bananas 🍌 and power. 💪",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're the {m_type_lower} who can see into the banana 🍌 dimension. What wonders (and bananas) lie beyond? 🌌🍌",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You are the pinnacle of {m_type_lower} evolution. Mostly primal, with a god-tier brain 🧠🌟. Your destiny: BANANAS. 🍌 And ruling the cosmos. 🪐"
        ],
        "MP_ALMOST_PURE": [
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Almost pure {m_type_lower}, **200** IQ 🤯. You're on the verge of total {m_type_upper}-ness, using your god-tier intellect to become the ultimate primal force across all dimensions. The cosmos trembles! 🌌💥",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Near-total {m_type_upper}, cosmic brain 🌌🧠. You're the {m_type_lower} who's transcended reality and is now living in a banana-based multiverse 🍌🌀 of your own design.",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Almost pure {m_type_upper}, with a mind that contains all banana-knowledge 🍌📚. You are the Librarian of the Great Banana Tree. 🌳 Shhh... bananas are sleeping.",
            "You're **{monkey_percentage}%** {m_type_lower} with an IQ of **{iq_score}**. You are a primal god 🌟🐒, one with the banana 🍌 flow. Your thoughts are bananas, your words are bananas. Banana. 🗣️🤯",
            "The Penultimate Primate: **{monkey_percentage}% {m_type_upper}**, **{iq_score}** IQ. You are on the cusp of becoming the Banana 🍌 Itself. The final transformation awaits. 🌟➡️🐒",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're a {m_type_lower} cosmic horror 🐙🧠, your intellect vast, your primal urges... banana-centric 🍌. Fear the OOK of Cthulhu-nana!",
            "You've got **{iq_score}** IQ and **{monkey_percentage}%** {m_type_lower}. You're so close to pure {m_type_lower} godhood 🌟, you probably bleed banana 🍌 juice. Or pure OOK energy. ✨",
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You are the singularity where {m_type_lower} meets omnipotence. 💥 Your banana 🍌 stash is infinite. Your wisdom, boundless. 🙏",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You're the {m_type_lower} who can taste the dreams of bananas 🍌😴. What do they dream of? More {m_type_plural_lower} like you, probably.",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You are the harbinger of the Banana 🍌 Apocalypse. Almost pure {m_type_lower}, with a brain to end all brains. 🤯 We're ready. (With bananas)."
        ],
        "MP_PURE": [
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. Pure **{m_type_upper}**, **200** IQ 🤯. You are the embodiment of primal {m_type_lower} energy, combined with cosmic intellect. A divine, terrifying, banana-fueled, reality-bending entity! 🌟👹🍌🌀",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. **{m_type_upper}** perfection! Your spirit is wild 🌪️, your brain is cosmic 🌌. You are the banana 🍌 singularity, the ultimate primate being! ✨",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. **100% {m_type_upper}**, **200 IQ**! YOU ARE THE BANANA 🍌 GOD-EMPEROR 👑! ALL REALITY IS YOUR BANANA HOARD! WE ARE NOT WORTHY! 🌌🛐",
            "You are **{monkey_percentage}%** {m_type_lower}, IQ **{iq_score}**. You have transcended. You are not *in* the jungle 🌳, the jungle is *in you*. And it's made of bananas 🍌. Infinite bananas. ♾️🤯 OOK!",
            "THE APEX. **{monkey_percentage}% {m_type_upper}**, **{iq_score}** IQ. You are the beginning and the end. The Alpha and the OOK-mega. The Great Banana 🍌 itself made manifest. Bow down. 🙏🐒",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. **100% {m_type_upper}**! **200 IQ**! You are the BANANA-VERSE INCARNATE! 🍌🌌 Your OOKs create galaxies! Your farts smell like banana bread! 🍞💨 We are blessed.",
            "You've got **{iq_score}** IQ and **{monkey_percentage}%** {m_type_lower}. You are pure {m_type_lower} divinity. 🌟 You don't eat bananas 🍌; bananas offer themselves to you as tribute. 🙏",
            "Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You are the ultimate being. The final form. The {m_type_upper} Prime. All hail your glorious, banana-fueled 🍌, super-intelligent OOK! 🗣️👑",
            "IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You are the chosen one... to achieve BANANIRVANA. 🧘🍌✨ Pure {m_type_lower}, pure genius, pure banana. Enlightenment achieved.",
            "Results: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. You are... beyond comprehension. A god. A legend. A myth. A really smart {m_type_lower} who loves bananas 🍌. We get it. And we're terrified/amazed. 😱🤩"
        ]
    }
}

def get_analysis_response(iq_score: int, monkey_percentage: int) -> str:
    """
    Generates a combined themed response based on IQ score and monkey percentage
    using predefined combinations.
    """
    iq_key = get_iq_range_key(iq_score)
    mp_key = get_mp_range_key(monkey_percentage)

    # Get a random monkey type for formatting
    m_type = get_random_monkey_type()
    m_type_lower = m_type.lower()
    m_type_upper = m_type.upper()
    m_type_plural_lower = get_plural_monkey_type(m_type_lower)

    # Try to find responses for the specific combination
    responses_for_combination = COMBINED_RESPONSES.get(iq_key, {}).get(mp_key, [])

    # Fallback if a specific combination isn't defined or has no responses
    if not responses_for_combination:
        fallback_response = f"Analysis: IQ **{iq_score}**, Monkey Purity **{monkey_percentage}%**. A unique specimen, this {m_type_lower}! Results are... complex. Requires further study."
        responses_for_combination = [fallback_response]

    selected_response = random.choice(responses_for_combination)

    # Format the response string
    return selected_response.format(
        iq_score=iq_score,
        monkey_percentage=monkey_percentage,
        m_type_lower=m_type_lower,
        m_type_upper=m_type_upper,
        m_type_plural_lower=m_type_plural_lower
    )
