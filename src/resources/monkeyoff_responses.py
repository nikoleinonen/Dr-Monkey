import random
from discord.member import Member
from src.resources.monkey_types import get_random_monkey_type, get_plural_monkey_type

def get_monkeyoff_response(challenger: Member, challenger_percentage: int, opponent: Member, opponent_percentage: int) -> dict[str, str]:
    """
    Determines the outcome of a monkey-off and returns a dictionary
    containing a 'title' and 'description' for the result embed.
    """
    m_type = get_random_monkey_type()
    m_type_lower = m_type.lower()
    m_type_upper = m_type.upper()
    m_type_plural_lower = get_plural_monkey_type(m_type_lower)
    m_type_plural_upper = m_type_plural_lower.upper()

    if challenger_percentage > opponent_percentage:
        winner, loser, winner_percentage, loser_percentage = challenger, opponent, challenger_percentage, opponent_percentage
        # outcome = "win" # Relative to challenger, not strictly needed if we use absolute winner/loser
    elif challenger_percentage < opponent_percentage:
        winner, loser, winner_percentage, loser_percentage = opponent, challenger, opponent_percentage, challenger_percentage
        # outcome = "lose" # Relative to challenger
    else:
        tie_responses = [
            {"title": f"🐒 **{m_type_upper} STANDOFF!** 🐒", "description": f"It's a tie! Both {{challenger.mention}} and {{opponent.mention}} are equally **{{challenger_percentage}}%** {m_type_lower}! The jungle remains in equilibrium."},
            {"title": f"🏆 **{m_type_upper} TIE!** 🏆", "description": f"Unbelievable! {{challenger.mention}} and {{opponent.mention}} have achieved perfect {m_type_lower} synchronicity at **{{challenger_percentage}}%**! The fabric of the jungle trembles!"},
            {"title": f"🍌 **{m_type_upper} SPLIT DECISION!** 🍌", "description": f"It's a dead heat! {{challenger.mention}} and {{opponent.mention}} both scored **{{challenger_percentage}}%** on the {m_type_lower}-meter!"},
            {"title": f"⚖️ **{m_type_upper} OUTCOME EVEN!** ⚖️", "description": f"{{challenger.mention}} vs {{opponent.mention}} results in a **{{challenger_percentage}}%** tie! You're both equally devolved! Or evolved? Who can say."},
            {"title": f"🐵 **MUTUAL {m_type_upper} MADNESS!** 🐵", "description": f"Both {{challenger.mention}} and {{opponent.mention}} are **{{challenger_percentage}}%** certified {m_type_lower}! It's a stalemate of {m_type_lower} supremacy!"},
            {"title": f"🤯 **{m_type_upper} MIND-MELD!** 🤯", "description": f"Inconceivable! {{challenger.mention}} and {{opponent.mention}} are locked in a **{{challenger_percentage}}%** {m_type_lower} paradox! The jungle itself is confused."},
            {"title": f"🤝 **{m_type_upper} ACCORD!** 🤝", "description": f"A rare display of {m_type_lower} equilibrium! {{challenger.mention}} and {{opponent.mention}} both hit **{{challenger_percentage}}%**! The jungle gods decree peace."},
            {"title": f"🌀 **{m_type_upper} VORTEX OF EQUALITY!** 🌀", "description": f"The {m_type_lower}-metric is spinning! {{challenger.mention}} and {{opponent.mention}} are identically **{{challenger_percentage}}%** {m_type_lower}!"},
            {"title": f"🎭 **TWO {m_type_plural_upper}, ONE SCORE!** 🎭", "description": f"It's a {m_type_lower} duet of destiny! {{challenger.mention}} and {{opponent.mention}} share the spotlight with **{{challenger_percentage}}%**! The crowd goes wild!"},
            {"title": f"🤷 **{m_type_upper} SHRUG-OFF!** 🤷", "description": f"Well, that was... anticlimactic! {{challenger.mention}} and {{opponent.mention}} are both **{{challenger_percentage}}%** {m_type_lower}. It's a draw! Go find another tree to shake."},
            {"title": f"🤝 **{m_type_upper} TRUCE!** 🤝", "description": f"The jungle gods demand peace! {{challenger.mention}} and {{opponent.mention}} are equally **{{challenger_percentage}}%** {m_type_lower}. Now hug it out, you two. Or don't. We don't care. 🙄"},
            {"title": f"😴 **{m_type_upper} SNOOZE-FEST!** 😴", "description": f"Honestly, we're bored. {{challenger.mention}} and {{opponent.mention}} both scored **{{challenger_percentage}}%** {m_type_lower}. It's a tie. Next!"},
            {"title": f"🪞 **MIRROR {m_type_upper} MATCH!** 🪞", "description": f"It's like looking in a mirror! Both {{challenger.mention}} and {{opponent.mention}} are **{{challenger_percentage}}%** {m_type_lower}. Maybe try fighting your own reflection next time?"},
            {"title": f"🤷‍♀️ **{m_type_upper} WHATEVER!** 🤷‍♂️", "description": f"Yeah, yeah, **{{challenger_percentage}}%** {m_type_lower} for both {{challenger.mention}} and {{opponent.mention}}. It's a tie. Don't expect a parade. 😒"},
            {"title": f"🍌 **BANANA EQUILIBRIUM!** 🍌", "description": f"The cosmic balance of bananas is maintained! {{challenger.mention}} and {{opponent.mention}} are perfectly **{{challenger_percentage}}%** {m_type_lower}. Now go meditate or something. 🧘"},
            {"title": f"💤 **YAWN-OFF!** 💤", "description": f"This monkey-off was so exciting, we almost fell asleep. {{challenger.mention}} and {{opponent.mention}} are both **{{challenger_percentage}}%** {m_type_lower}. Try harder next time. Or don't. We'll still be here. Probably."},
            {"title": f"🚫 **NO {m_type_upper} WINNERS!** 🚫", "description": f"There are no winners here, only equally **{{challenger_percentage}}%** {m_type_lower} participants. The jungle is disappointed. 😔"},
            {"title": f"🙄 **OH, IT'S A TIE.** 🙄", "description": f"Surprise, surprise. {{challenger.mention}} and {{opponent.mention}} are both **{{challenger_percentage}}%** {m_type_lower}. Now, if you'll excuse us, we have actual monkey business to attend to. 🐒💼"},
            {"title": f"🍌 **SHARED BANANA!** 🍌", "description": f"The jungle has decreed a shared outcome! {{challenger.mention}} and {{opponent.mention}} are equally **{{challenger_percentage}}%** {m_type_lower}. Now go share a real banana, you two. 🤝🍌"}
        ]
        chosen_response = random.choice(tie_responses)
        return {
            "title": chosen_response["title"].format(m_type_upper=m_type_upper),
            "description": chosen_response["description"].format(m_type_lower=m_type_lower, m_type_plural_upper=m_type_plural_upper, challenger_percentage=challenger_percentage, challenger=challenger, opponent=opponent)
        }

    # This block handles win/loss based on the determined winner and loser
    
    if winner_percentage == 100: # Absolute MONKE
        responses = [
            {"title": f"👑 **ULTIMATE {m_type_upper} GODHOOD!** 👑", "description": f"{{winner.mention}} IS **100% {m_type_upper} GOD**! {{loser.mention}} **{{loser_percentage}}%** is but a mere mortal."},
            {"title": f"🏆 **PERFECT {m_type_upper}ION!** 🏆", "description": f"{{winner.mention}} achieved **100% {m_type_lower}**! {{loser.mention}} **{{loser_percentage}}%** clearly skipped banana day. A flawless victory for {{winner.mention}}!"},
            {"title": f"💯 **{m_type_upper} PERFECTION ACHIEVED!** 💯", "description": f"{{winner.mention}} IS **100% CERTIFIED {m_type_upper}**! {{loser.mention}} **{{loser_percentage}}%** was merely a banana peel on their path to glory!"},
            {"title": f"🌟 **TRANSCENDENT {m_type_upper}!** 🌟", "description": f"A divine **100% {m_type_lower}** score for {{winner.mention}}! {{loser.mention}} (**{{loser_percentage}}%**) offered their presence as tribute. The new {m_type_lower} deity reigns!"},
            {"title": f"🌌 **COSMIC {m_type_upper} EVENT!** 🌌", "description": f"{{winner.mention}} has achieved **100% {m_type_lower}** and caused a ripple in the banana-verse! {{loser.mention}} (**{{loser_percentage}}%**) is just stardust."},
            {"title": f"🌋 **PRIMAL {m_type_upper} ERUPTION!** 🌋", "description": f"A **100% {m_type_lower}** volcanic eruption of pure primate power from {{winner.mention}}! {{loser.mention}} (**{{loser_percentage}}%**) is buried in the ash of defeat."},
            {"title": f"👑 **{m_type_upper} OF {m_type_plural_upper}!** 👑", "description": f"All hail {{winner.mention}}, who scored a legendary **100% {m_type_lower}**! {{loser.mention}} (**{{loser_percentage}}%**) is now a court jester."},
            {"title": f"🌠 **{m_type_upper} ASCENSION!** 🌠", "description": f"{{winner.mention}} has ascended to **100% {m_type_lower}** godhood! {{loser.mention}} (**{{loser_percentage}}%**) can only watch in awe."},
            {"title": f"👑 **THE {m_type_upper} KING/QUEEN!** 👑", "description": f"Behold, {{winner.mention}}! A perfect **100% {m_type_lower}**! {{loser.mention}} (**{{loser_percentage}}%**) is just a peasant in this jungle. Bow down! 🙇"},
            {"title": f"💯 **FLAWLESS {m_type_upper} VICTORY!** 💯", "description": f"{{winner.mention}} delivered a **100% {m_type_lower}** beatdown! {{loser.mention}} (**{{loser_percentage}}%**) didn't even put up a fight. {{loser.mention}}, better luck next century. 😂"},
            {"title": f"💥 **TOTAL {m_type_upper} DOMINATION!** 💥", "description": f"{{winner.mention}} is **100% {m_type_lower}** and just obliterated {{loser.mention}} (**{{loser_percentage}}%**)! Get rekt! 😈"},
            {"title": f"🌟 **{m_type_upper} GOD-TIER!** 🌟", "description": f"Witness the **100% {m_type_lower}** power of {{winner.mention}}! {{loser.mention}} (**{{loser_percentage}}%**) is utterly pathetic. Maybe {{loser.mention}} should stick to peeling bananas for a living. 🍌🔪"},
            {"title": f"😂 **LAUGHING ALL THE WAY!** 😂", "description": f"{{winner.mention}} is **100% {m_type_lower}** and laughing all the way! {{loser.mention}} (**{{loser_percentage}}%**) just provided free entertainment. Thanks for the show! 💸"},
            {"title": f"💀 **{m_type_upper} EXECUTION!** 💀", "description": f"{{winner.mention}} performed a **100% {m_type_lower}** execution on {{loser.mention}} (**{{loser_percentage}}%**)! Your dignity is gone. Brutal. 😈"},
            {"title": f"🏆 **UNQUESTIONABLE {m_type_upper} SUPREMACY!** 🏆", "description": f"There's no doubt: {{winner.mention}} is **100% {m_type_lower}**! {{loser.mention}} (**{{loser_percentage}}%**) was merely a stepping stone. Better luck in your next life, {{loser.mention}}."},
            {"title": f"🚀 **{m_type_upper} TO THE MOON!** 🚀", "description": f"{{winner.mention}} is **100% {m_type_lower}** and just launched to the moon! {{loser.mention}} (**{{loser_percentage}}%**) is stuck on Earth. Enjoy the view from down there! 🔭"}
        ]
    elif winner_percentage >= 75: # Strong win
        responses = [
            {"title": f"🏆 **{m_type_upper} OVERLORD!** 🏆", "description": f"{{winner.mention}} unleashed **{{winner_percentage}}% {m_type_lower}** fury, crushing {{loser.mention}}'s **{{loser_percentage}}%**!"},
            {"title": f"💪 **{m_type_upper} SUPERIORITY!** 💪", "description": f"With a staggering **{{winner_percentage}}% {m_type_lower}**, {{winner.mention}} makes {{loser.mention}} **{{loser_percentage}}%** look like they're still learning to peel!"},
            {"title": f"🔥 **{m_type_upper} POWER PLAY!** 🔥", "description": f"{{winner.mention}} flexes their **{{winner_percentage}}% {m_type_lower}** might! {{loser.mention}} **{{loser_percentage}}%** was simply out-{m_type_lower}ed!"},
            {"title": f"🌪️ **{m_type_upper} TEMPEST!** 🌪️", "description": f"{{winner.mention}} unleashed a **{{winner_percentage}}% {m_type_lower}** storm! {{loser.mention}} **{{loser_percentage}}%** was blown away!"},
            {"title": f"💥 **DOMINANT {m_type_upper} DISPLAY!** 💥", "description": f"Pure {m_type_lower} dominance! {{winner.mention}} **{{winner_percentage}}%** made {{loser.mention}} **{{loser_percentage}}%** question their primate heritage!"},
            {"title": f"🥇 **GOLD MEDAL {m_type_upper}!** 🥇", "description": f"{{winner.mention}} stands atop the podium with **{{winner_percentage}}% {m_type_lower}**! {{loser.mention}} **{{loser_percentage}}%** takes home nothing but regret."},
            {"title": f"🦍 **ALPHA {m_type_upper} WINS!** 🦍", "description": f"{{winner.mention}} proved they're the alpha with **{{winner_percentage}}% {m_type_lower}**! {{loser.mention}} is clearly a beta. Better luck next time, little chimp. 🐒"},
            {"title": f"😏 **SMUG {m_type_upper} VICTORY!** 😏", "description": f"With a smug grin, {{winner.mention}} ({{winner_percentage}}% {m_type_lower}) snatched victory from {{loser.mention}} ({{loser_percentage}}%)! Don't cry, {{loser.mention}}, it's just a monkey-off. 🍌💧"},
            {"title": f"🍌 **MONKEY HEIST!** 🍌", "description": f"{{winner.mention}} executed a perfect monkey heist with **{{winner_percentage}}% {m_type_lower}**! {{loser.mention}} (**{{loser_percentage}}%**) was left with empty hands."},
            {"title": f"😂 **NOT EVEN CLOSE!** 😂", "description": f"{{winner.mention}}'s **{{winner_percentage}}% {m_type_lower}** was so far ahead of {{loser.mention}}'s **{{loser_percentage}}%**, it's not even funny. Okay, it's a little funny. Get good, {{loser.mention}}. 🎮"},
            {"title": f"👑 **CROWNED {m_type_upper}!** 👑", "description": f"All hail {{winner.mention}}, the newly crowned **{{winner_percentage}}% {m_type_lower}**! {{loser.mention}} (**{{loser_percentage}}%**) is just a footnote in this epic tale. Long live the king/queen! 🤴👸"}
        ]
    elif loser_percentage == 0: # Loser got 0%
        responses = [
            {"title": f"💀 **{m_type_upper} PURGE!** 💀", "description": f"{{winner.mention}} **{{winner_percentage}}%** is practically a different species! {{loser.mention}} registered an embarrassing **0% {m_type_lower}%."},
            {"title": f"📉 **TOTAL DE-{m_type_upper}IFICATION!** 📉", "description": f"{{loser.mention}} scored **0% {m_type_lower}** against {{winner.mention}}'s mighty **{{winner_percentage}}%**! {{loser.mention}} has been officially un-{m_type_lower}ed."},
            {"title": f"🚫 **{m_type_upper} NULLIFICATION!** 🚫", "description": f"{{loser.mention}} scored an astounding **0% {m_type_lower}**! Are they even trying? {{winner.mention}} **{{winner_percentage}}%** scoffs."},
            {"title": f"👻 **GHOST OF A {m_type_upper}!** 👻", "description": f"Is {{loser.mention}} even there? A **0% {m_type_lower}** reading suggests not! {{winner.mention}} **{{winner_percentage}}%** easily claims victory from the void."},
            {"title": f"🗑️ **{m_type_upper} TRASHED!** 🗑️", "description": f"{{loser.mention}} scored a pathetic **0% {m_type_lower}**! {{winner.mention}} (**{{winner_percentage}}%**) just swept them into the trash. Enjoy the dumpster! 🚮"},
            {"title": f"😂 **ZERO {m_type_upper} GIVEN!** 😂", "description": f"{{loser.mention}} gave **0% {m_type_lower}**! {{winner.mention}} (**{{winner_percentage}}%**) is laughing. Maybe try being less... human? 🤷‍♂️"},
            {"title": f"📉 **{m_type_upper} BANKRUPTCY!** 📉", "description": f"{{loser.mention}} hit **0% {m_type_lower}** and declared {m_type_lower} bankruptcy! {{winner.mention}} (**{{winner_percentage}}%**) is now the proud victor!"},
            {"title": f"🐒 **NOT EVEN A {m_type_upper}!** 🐒", "description": f"{{loser.mention}} scored **0% {m_type_lower}**! Are they even a {m_type_lower}? {{winner.mention}} (**{{winner_percentage}}%**) is questioning everything. The jungle is confused. 🤔"}
        ]
    elif loser_percentage <= 25: # Loser did poorly
        responses = [
            {"title": f"🙈 **{m_type_upper} OUTCRY!** 🙈", "description": f"Ouch! {{loser.mention}} only scraped by with **{{loser_percentage}}% {m_type_lower}** against {{winner.mention}}'s dominant **{{winner_percentage}}%**!"},
            {"title": f"👎 **WEAK {m_type_upper} SHOWING!** 👎", "description": f"{{loser.mention}} **{{loser_percentage}}% {m_type_lower}** was no match for {{winner.mention}}'s **{{winner_percentage}}%**! Did they forget their morning banana? The victory goes to {{winner.mention}}!"},
            {"title": f"📉 **{m_type_upper} GONE WRONG!** 📉", "description": f"{{loser.mention}} stumbled with a mere **{{loser_percentage}}% {m_type_lower}**! {{winner.mention}} **{{winner_percentage}}%** swings victorious!"},
            {"title": f"📉 **{m_type_upper} PLUMMET!** 📉", "description": f"{{loser.mention}}'s {m_type_lower} score took a nosedive to **{{loser_percentage}}%**! {{winner.mention}} **{{winner_percentage}}%** capitalized on the fumble!"},
            {"title": f" করুণ **PATHETIC {m_type_upper} ATTEMPT!**  করুণ", "description": f"Was that even a try? {{loser.mention}} limped in with **{{loser_percentage}}% {m_type_lower}**. {{winner.mention}} **{{winner_percentage}}%** laughs all the way to victory!"},
            {"title": f"🌱 **SPROUTING {m_type_upper} VS VETERAN!** 🌱", "description": f"{{loser.mention}} **{{loser_percentage}}% {m_type_lower}** is clearly still a sapling in the jungle of {m_type_plural_lower}. {{winner.mention}} **{{winner_percentage}}%** harvests victory with ease!"},
            {"title": f"😂 **PATHETIC {m_type_upper}!** 😂", "description": f"{{loser.mention}}'s **{{loser_percentage}}% {m_type_lower}** was just sad. {{winner.mention}} (**{{winner_percentage}}%**) barely broke a sweat. Go home, {{loser.mention}}, you're drunk on sadness. 😭"},
            {"title": f"🍌 **PEEL-OUT!** 🍌", "description": f"{{loser.mention}} (**{{loser_percentage}}% {m_type_lower}**) just peeled out of this competition! {{winner.mention}} (**{{winner_percentage}}%**) is left with the victory. Don't let the door hit you on the way out! 🚪"},
            {"title": f"📉 **{m_type_upper} DISAPPOINTMENT!** 📉", "description": f"The jungle is collectively sighing at {{loser.mention}}'s **{{loser_percentage}}% {m_type_lower}**! {{winner.mention}} (**{{winner_percentage}}%**) is just shaking their head while collecting the win. Do better, {{loser.mention}}. 🙄"},
            {"title": f"🐒 **NOOB {m_type_upper}!** 🐒", "description": f"{{loser.mention}} (**{{loser_percentage}}% {m_type_lower}**) is clearly a {m_type_lower} noob! {{winner.mention}} (**{{winner_percentage}}%**) just schooled them. The victory is for the pros! 🎮"},
            {"title": f"💔 **BROKEN {m_type_upper}!** 💔", "description": f"{{loser.mention}} (**{{loser_percentage}}% {m_type_lower}**) is broken and defeated! {{winner.mention}} (**{{winner_percentage}}%**) shows no mercy. Get well soon, {{loser.mention}}. Or don't. 🤷‍♀️"},
            {"title": f"💩 **{m_type_upper} POO-FLING!** 💩", "description": f"{{loser.mention}} (**{{loser_percentage}}% {m_type_lower}**) just got poo-flung by {{winner.mention}} (**{{winner_percentage}}%**)!"}
        ]
    else: # Standard win/loss
        responses = [
            {"title": f"🎉 **{m_type_upper} BATTLE WON!** 🎉", "description": f"{{winner.mention}} **{{winner_percentage}}% {m_type_lower}** just barely out-ooga-booga'd {{loser.mention}} **{{loser_percentage}}%**! A win is a win!"},
            {"title": f"🍌 **{m_type_upper} BRAGGING RIGHTS!** 🍌", "description": f"{{winner.mention}} claims victory with **{{winner_percentage}}% {m_type_lower}** over {{loser.mention}}'s **{{loser_percentage}}%**! Enjoy the sweet taste of {m_type_lower} triumph!"},
            {"title": f"👍 **NICE {m_type_upper}ING!** 👍", "description": f"{{winner.mention}} showed their **{{winner_percentage}}% {m_type_lower}** prowess, edging out {{loser.mention}} **{{loser_percentage}}%**! Well played, {m_type_lower}!"},
            {"title": f"🤏 **BY A BANANA PEEL!** 🤏", "description": f"{{winner.mention}} **{{winner_percentage}}% {m_type_lower}** just slipped past {{loser.mention}} **{{loser_percentage}}%**! A narrow victory!"},
            {"title": f"💥 **{m_type_upper} CLASH RESOLVED!** 💥", "description": f"The dust settles, and {{winner.mention}} **{{winner_percentage}}% {m_type_lower}** stands victorious over {{loser.mention}} **{{loser_percentage}}%**! Their prize: bragging rights!"},
            {"title": f"🐒 **TOP {m_type_upper} TODAY!** 🐒", "description": f"In today's {m_type_lower}-off, {{winner.mention}} **{{winner_percentage}}% {m_type_lower}** proved slightly more {m_type_lower} than {{loser.mention}} **{{loser_percentage}}%**! {{winner.mention}} celebrates!"},
            {"title": f"😏 **JUST GOOD ENOUGH!** 😏", "description": f"{{winner.mention}} (**{{winner_percentage}}% {m_type_lower}**) was just good enough to beat {{loser.mention}} (**{{loser_percentage}}%**)! No need to be flashy. Efficiency! 📈"},
            {"title": f"🍌 **MONKEY SWIPE!** 🍌", "description": f"{{winner.mention}} (**{{winner_percentage}}% {m_type_lower}**) expertly swiped victory from {{loser.mention}} (**{{loser_percentage}}%**)! Easy pickings! 🤏"},
            {"title": f"👑 **SLIGHTLY MORE {m_type_upper}!** 👑", "description": f"{{winner.mention}} (**{{winner_percentage}}% {m_type_lower}**) is officially slightly more {m_type_lower} than {{loser.mention}} (**{{loser_percentage}}%**)! Them's the rules. 🤷‍♀️"},
            {"title": f"😂 **BETTER LUCK NEXT TIME!** 😂", "description": f"{{winner.mention}} (**{{winner_percentage}}% {m_type_lower}**) out-oogah-boogah'd {{loser.mention}} (**{{loser_percentage}}%**)! Don't worry, {{loser.mention}}, there's always next time... to lose again! 😈"},
            {"title": f"🐒 **JUNGLE JUSTICE!** 🐒", "description": f"Jungle justice has been served! {{winner.mention}} (**{{winner_percentage}}% {m_type_lower}**) proved superior to {{loser.mention}} (**{{loser_percentage}}%**). The jungle has spoken! 🗣️"},
            {"title": f"📈 **{m_type_upper} ADVANTAGE!** 📈", "description": f"{{winner.mention}} (**{{winner_percentage}}% {m_type_lower}**) had the clear {m_type_lower} advantage over {{loser.mention}} (**{{loser_percentage}}%**)! Simple as that. 📊"}
        ]

    chosen_response = random.choice(responses)
    return {
        "title": chosen_response["title"].format(m_type_upper=m_type_upper),
        "description": chosen_response["description"].format(
            m_type_lower=m_type_lower, m_type_upper=m_type_upper,
            m_type_plural_lower=m_type_plural_lower,
            winner=winner, loser=loser,
            winner_percentage=winner_percentage, loser_percentage=loser_percentage
        )
    }
