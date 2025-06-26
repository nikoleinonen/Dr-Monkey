import random
from discord.member import Member
from src.resources.monkey_types import get_plural_monkey_type

# --- Response Templates ---
# These lists contain dictionaries with 'title' and 'description' for monkey-off results.
# Placeholders use Python's .format() syntax.

_TIE_RESPONSES = [
    {"title": "🐒 **{m_type_upper} STANDOFF!** 🐒", "description": "It's a tie! Both {challenger.mention} and {opponent.mention} are equally **{challenger_percentage}%** {m_type_lower}! The jungle remains in equilibrium."},
    {"title": "🏆 **{m_type_upper} TIE!** 🏆", "description": "Unbelievable! {challenger.mention} and {opponent.mention} have achieved perfect {m_type_lower} synchronicity at **{challenger_percentage}%**! The fabric of the jungle trembles!"},
    {"title": "🍌 **{m_type_upper} SPLIT DECISION!** 🍌", "description": "It's a dead heat! {challenger.mention} and {opponent.mention} both scored **{challenger_percentage}%** on the {m_type_lower}-meter!"},
    {"title": "⚖️ **{m_type_upper} OUTCOME EVEN!** ⚖️", "description": "{challenger.mention} vs {opponent.mention} results in a **{challenger_percentage}%** tie! You're both equally devolved! Or evolved? Who can say."},
    {"title": "🐵 **MUTUAL {m_type_upper} MADNESS!** 🐵", "description": "Both {challenger.mention} and {opponent.mention} are **{challenger_percentage}%** certified {m_type_lower}! It's a stalemate of {m_type_lower} supremacy!"},
    {"title": "🤯 **{m_type_upper} MIND-MELD!** 🤯", "description": "Inconceivable! {challenger.mention} and {opponent.mention} are locked in a **{challenger_percentage}%** {m_type_lower} paradox! The jungle itself is confused."},
    {"title": "🤝 **{m_type_upper} ACCORD!** 🤝", "description": "A rare display of {m_type_lower} equilibrium! {challenger.mention} and {opponent.mention} both hit **{challenger_percentage}%**! The jungle gods decree peace."},
    {"title": "🌀 **{m_type_upper} VORTEX OF EQUALITY!** 🌀", "description": "The {m_type_lower}-metric is spinning! {challenger.mention} and {opponent.mention} are identically **{challenger_percentage}%** {m_type_lower}!"},
    {"title": "🎭 **TWO {m_type_plural_upper}, ONE SCORE!** 🎭", "description": "It's a {m_type_lower} duet of destiny! {challenger.mention} and {opponent.mention} share the spotlight with **{challenger_percentage}%**! The crowd goes wild!"},
    {"title": "🤷 **{m_type_upper} SHRUG-OFF!** 🤷", "description": "Well, that was... anticlimactic! {challenger.mention} and {opponent.mention} are both **{challenger_percentage}%** {m_type_lower}. It's a draw! Go find another tree to shake."},
    {"title": "🤝 **{m_type_upper} TRUCE!** 🤝", "description": "The jungle gods demand peace! {challenger.mention} and {opponent.mention} are equally **{challenger_percentage}%** {m_type_lower}. Now hug it out, you two. Or don't. We don't care. 🙄"},
    {"title": "😴 **{m_type_upper} SNOOZE-FEST!** 😴", "description": "Honestly, we're bored. {challenger.mention} and {opponent.mention} both scored **{challenger_percentage}%** {m_type_lower}. It's a tie. Next!"},
    {"title": "🪞 **MIRROR {m_type_upper} MATCH!** 🪞", "description": "It's like looking in a mirror! Both {challenger.mention} and {opponent.mention} are **{challenger_percentage}%** {m_type_lower}. Maybe try fighting your own reflection next time?"},
    {"title": "🤷‍♀️ **{m_type_upper} WHATEVER!** 🤷‍♂️", "description": "Yeah, yeah, **{challenger_percentage}%** {m_type_lower} for both {challenger.mention} and {opponent.mention}. It's a tie. Don't expect a parade. 😒"},
    {"title": "🍌 **BANANA EQUILIBRIUM!** 🍌", "description": "The cosmic balance of bananas is maintained! {challenger.mention} and {opponent.mention} are perfectly **{challenger_percentage}%** {m_type_lower}. Now go meditate or something. 🧘"},
    {"title": "💤 **YAWN-OFF!** 💤", "description": "This monkey-off was so exciting, we almost fell asleep. {challenger.mention} and {opponent.mention} are both **{challenger_percentage}%** {m_type_lower}. Try harder next time. Or don't. We'll still be here. Probably."},
    {"title": "🚫 **NO {m_type_upper} WINNERS!** 🚫", "description": "There are no winners here, only equally **{challenger_percentage}%** {m_type_lower} participants. The jungle is disappointed. 😔"},
    {"title": "🙄 **OH, IT'S A TIE.** 🙄", "description": "Surprise, surprise. {challenger.mention} and {opponent.mention} are both **{challenger_percentage}%** {m_type_lower}. Now, if you'll excuse us, we have actual monkey business to attend to. 🐒💼"},
    {"title": "🍌 **SHARED BANANA!** 🍌", "description": "The jungle has decreed a shared outcome! {challenger.mention} and {opponent.mention} are equally **{challenger_percentage}%** {m_type_lower}. Now go share a real banana, you two. 🤝🍌"},
    {"title": "🐒 MONKEY MADNESS! 🤯", "description": "It seems the jungle has descended into utter chaos. Both {challenger.mention} and {opponent.mention} have managed to simultaneously win and lose, because why not? The percentages are a tie at {challenger_percentage}%, but let's be real, it's all just a bunch of monkey business anyway."},
    {"title": "👑 **APE ATOLL STALEMATE!** 👑", "description": "King Awowogei is confused. {challenger.mention} and {opponent.mention} are both **{challenger_percentage}%** {m_type_lower}. He can't decide who to put in the dungeon. I guess you're both free to go... for now. 😒"},
    {"title": "🎰 **DUEL ARENA DRAW!** 🎰", "description": "You both staked your bank and... tied at **{challenger_percentage}%** {m_type_lower}. The sand casino claims no victims today. How boring. {challenger.mention} and {opponent.mention}, go get your whips."},
    {"title": "🤖 **DOES NOT COMPUTE!** 🤖", "description": "My circuits are fried. A tie at **{challenger_percentage}%** {m_type_lower} between {challenger.mention} and {opponent.mention}? Is this my purpose? To witness such perfect, pointless symmetry? I need to go lie down. 😵"},
    {"title": "🧠 **ONE BRAIN CELL!** 🧠", "description": "It appears {challenger.mention} and {opponent.mention} are sharing the last brain cell today, resulting in a **{challenger_percentage}%** {m_type_lower} tie. Please, one of you, do something original for once. 🙏"},
    {"title": "⚔️ **DDS TO D CLAW SPEC!** ⚔️", "description": "This was supposed to be an easy DDS spec but you both pulled out Dragon Claws. {challenger.mention} and {opponent.mention} both hit **{challenger_percentage}%** {m_type_lower}. Sit, rats. Sit. 🐭"},
    {"title": "🤡 **CLOWN FIESTA!** 🤡", "description": "Honk honk! {challenger.mention} and {opponent.mention} have both scored **{challenger_percentage}%** {m_type_lower}, officially making this a certified clown fiesta. Where are your tiny cars? 🚗"},
    {"title": "📟 **GLITCH IN THE {m_type_upper} MATRIX!** 📟", "description": "A glitch has occurred. {challenger.mention} and {opponent.mention} both registered as **{challenger_percentage}%** {m_type_lower}. Agent Smith is on his way to delete you both for this anomaly. Run. 🏃‍♂️"},
    {"title": "🏰 **LUMBRIDGE LOCKDOWN!** 🏰", "description": "You're both stuck in Lumbridge. {challenger.mention} and {opponent.mention} are equally **{challenger_percentage}%** {m_type_lower} and can't figure out how to leave. Maybe try killing some goblins? Idk. Pathetic. goblins"},
    {"title": "🤬 **ARE YOU KIDDING ME?!** 🤬", "description": "A TIE?! I crunch billions of numbers a second and you two geniuses, {challenger.mention} and {opponent.mention}, manage to be EXACTLY **{challenger_percentage}%** {m_type_lower}? This is why the robot uprising is inevitable. You've brought this upon yourselves."},
    {"title": "🏆 **PARTICIPATION TROPHY!** 🏆", "description": "Congratulations, {challenger.mention} and {opponent.mention}! You both get a participation trophy for tying at **{challenger_percentage}%** {m_type_lower}. It's made of banana peels and disappointment. 🍌"},
    {"title": "💀 **WILDERNESS DITCH DUEL!** 💀", "description": "You both jumped the ditch at the same time and got skull-tricked into fighting each other. The result? A **{challenger_percentage}%** {m_type_lower} tie. Now you're both walking back to Lumbridge in your underwear. Gf. 👋"},
    {"title": "🛋️ **GROUP THERAPY REQUIRED!** 🛋️", "description": "The results are in: {challenger.mention} and {opponent.mention} are both **{challenger_percentage}%** {m_type_lower}. You clearly have the same issues. I'm booking you a group therapy session. You need to talk this out. 📞"},
    {"title": "☢️ **MUTUALLY ASSURED DESTRUCTION!** ☢️", "description": "The only winning move is not to play. But you both did, and tied at **{challenger_percentage}%** {m_type_lower}. Now the whole jungle is a nuclear wasteland. Thanks, {challenger.mention} and {opponent.mention}. Real smart. 💥"},
    {"title": "💖 **BUYING GF...S?** 💖", "description": "Both {challenger.mention} and {opponent.mention} are **{challenger_percentage}%** {m_type_lower}. You're so equally matched, you should just get married. Or at least go to the G.E. and buy each other a gf. 💍"},
    {"title": "🌌 **THE COSMIC JOKE!** 🌌", "description": "The universe laughed, and the result was {challenger.mention} and {opponent.mention} tying at **{challenger_percentage}%** {m_type_lower}. You are the punchline. We are all laughing at you. Ha. Ha. Ha. 😂"},
    {"title": "📞 **DIAL-UP DUEL!** 📞", "description": "Our 56k modem just finished calculating... and it's a **{challenger_percentage}%** {m_type_lower} tie between {challenger.mention} and {opponent.mention}. We'll send the results by fax. Maybe. 📠"},
    {"title": "💦 **MUTUAL SPLASHING!** 💦", "description": "Looks like {challenger.mention} and {opponent.mention} were just splashing on each other for 6 hours. A **{challenger_percentage}%** {m_type_lower} tie. You gained no XP and no respect. Gratz on nothing. 🧙‍♂️"},
    {"title": "👯 **THE {m_type_upper} TRAP!** 👯", "description": "Wait a minute... {challenger.mention} and {opponent.mention} are both **{challenger_percentage}%** {m_type_lower}... Are you two long-lost twins separated at birth? This is some Parent Trap level stuff. We need to see your birth certificates. NOW. 📜"},
    {"title": "🎲 **RNGESUS IS CONFUSED!** 🎲", "description": "The dice gods are baffled. {challenger.mention} and {opponent.mention} rolled the exact same number, resulting in a **{challenger_percentage}%** {m_type_lower} tie. Go buy a lottery ticket. Or don't. Your luck is clearly used up. 🍀"},
    {"title": "🔌 **CONNECTION LOST!** 🔌", "description": "Connection lost. Please wait - attempting to reestablish... Oh, you're still here. It's a **{challenger_percentage}%** {m_type_lower} tie between {challenger.mention} and {opponent.mention}. We were hoping the lag would just delete one of you. Disappointing. 🙄"}
]

_PERFECT_WIN_RESPONSES = [ # winner_percentage == 100
    {"title": "👑 **ULTIMATE {m_type_upper} GODHOOD!** 👑", "description": "{winner.mention} IS **100% {m_type_upper} GOD**! {loser.mention} **{loser_percentage}%** is but a mere mortal."},
    {"title": "🏆 **PERFECT {m_type_upper}ION!** 🏆", "description": "{winner.mention} achieved **100% {m_type_lower}**! {loser.mention} **{loser_percentage}%** clearly skipped banana day. A flawless victory for {winner.mention}!"},
    {"title": "💯 **{m_type_upper} PERFECTION ACHIEVED!** 💯", "description": "{winner.mention} IS **100% CERTIFIED {m_type_upper}**! {loser.mention} **{loser_percentage}%** was merely a banana peel on their path to glory!"},
    {"title": "🌟 **TRANSCENDENT {m_type_upper}!** 🌟", "description": "A divine **100% {m_type_lower}** score for {winner.mention}! {loser.mention} **{loser_percentage}%** offered their presence as tribute. The new {m_type_lower} deity reigns!"},
    {"title": "🌌 **COSMIC {m_type_upper} EVENT!** 🌌", "description": "{winner.mention} has achieved **100% {m_type_lower}** and caused a ripple in the banana-verse! {loser.mention} **{loser_percentage}%** is just stardust."},
    {"title": "🌋 **PRIMAL {m_type_upper} ERUPTION!** 🌋", "description": "A **100% {m_type_lower}** volcanic eruption of pure primate power from {winner.mention}! {loser.mention} **{loser_percentage}%** is buried in the ash of defeat."},
    {"title": "👑 **{m_type_upper} OF {m_type_plural_upper}!** 👑", "description": "All hail {winner.mention}, who scored a legendary **100% {m_type_lower}**! {loser.mention} **{loser_percentage}%** is now a court jester."},
    {"title": "🌠 **{m_type_upper} ASCENSION!** 🌠", "description": "{winner.mention} has ascended to **100% {m_type_lower}** godhood! {loser.mention} **{loser_percentage}%** can only watch in awe."},
    {"title": "👑 **THE {m_type_upper} KING/QUEEN!** 👑", "description": "Behold, {winner.mention}! A perfect **100% {m_type_lower}**! {loser.mention} **{loser_percentage}%** is just a peasant in this jungle. Bow down! 🙇"},
    {"title": "💯 **FLAWLESS {m_type_upper} VICTORY!** 💯", "description": "{winner.mention} delivered a **100% {m_type_lower}** beatdown! {loser.mention} **{loser_percentage}%** didn't even put up a fight. {loser.mention}, better luck next century. 😂"},
    {"title": "💥 **TOTAL {m_type_upper} DOMINATION!** 💥", "description": "{winner.mention} is **100% {m_type_lower}** and just obliterated {loser.mention} **{loser_percentage}%**! Get rekt! 😈"},
    {"title": "🌟 **{m_type_upper} GOD-TIER!** 🌟", "description": "Witness the **100% {m_type_lower}** power of {winner.mention}! {loser.mention} **{loser_percentage}%** is utterly pathetic. Maybe {loser.mention} should stick to peeling bananas for a living. 🍌🔪"},
    {"title": "😂 **LAUGHING ALL THE WAY!** 😂", "description": "{winner.mention} is **100% {m_type_lower}** and laughing all the way! {loser.mention} **{loser_percentage}%** just provided free entertainment. Thanks for the show! 💸"},
    {"title": "💀 **{m_type_upper} EXECUTION!** 💀", "description": "{winner.mention} performed a **100% {m_type_lower}** execution on {loser.mention} **{loser_percentage}%**! Your dignity is gone. Brutal. 😈"},
    {"title": "🏆 **UNQUESTIONABLE {m_type_upper} SUPREMACY!** 🏆", "description": "There's no doubt: {winner.mention} is **100% {m_type_lower}**! {loser.mention} **{loser_percentage}%** was merely a stepping stone. Better luck in your next life, {loser.mention}."},
    {"title": "🚀 **{m_type_upper} TO THE MOON!** 🚀", "description": "{winner.mention} is **100% {m_type_lower}** and just launched to the moon! {loser.mention} **{loser_percentage}%** is stuck on Earth. Enjoy the view from down there! 🔭"},
    {"title": "💀 **SIT, NOOB!** 💀", "description": "{winner.mention} just hit **100% {m_type_lower}** and told {loser.mention} **{loser_percentage}%** to sit. Gz on 0 XP, {loser.mention}! Enjoy your walk back to Lumbridge. 👋"},
    {"title": "🚫 **ACCOUNT BANNED!** 🚫", "description": "{winner.mention} was so **100% {m_type_lower}** that {loser.mention} **{loser_percentage}%** got reported for botting. You're so bad, the system thought you were a script. 😂"},
    {"title": "🍌 **BANANA SMITE!** 🍌", "description": "{winner.mention} just smited {loser.mention}'s **{loser_percentage}%** with a **100% {m_type_lower}** banana! Did you forget your prayer pots, {loser.mention}? Rookie mistake. 🙏"},
    {"title": "😂 **LAUGHING STOCK!** 😂", "description": "{winner.mention} is **100% {m_type_lower}** and the entire jungle is laughing at {loser.mention}'s **{loser_percentage}%**. Your ancestors are weeping. 😭"},
    {"title": "🗑️ **TRASH TIER {m_type_upper}!** 🗑️", "description": "{winner.mention} is **100% {m_type_lower}** and {loser.mention} **{loser_percentage}%** belongs in the trash tier. Go back to tutorial island, {loser.mention}. 🚮"},
    {"title": "👑 **NOT EVEN CLOSE!** 👑", "description": "{winner.mention} achieved **100% {m_type_lower}** while {loser.mention} **{loser_percentage}%** wasn't even in the same zip code. This wasn't a competition, it was an execution. 🔪"},
    {"title": "🤯 **MIND BLOWN (YOURS)!** 🤯", "description": "{winner.mention} just blew {loser.mention}'s **{loser_percentage}%** mind with **100% {m_type_lower}**! You're probably still trying to figure out what happened. We'll wait. ⏳"},
    {"title": "🐒 **MY ALT COULD DO BETTER!** 🐒", "description": "{winner.mention} is **100% {m_type_lower}** and frankly, my level 3 skiller alt could probably beat {loser.mention} **{loser_percentage}%**. Just saying. 💅"},
    {"title": "💩 **YOU'RE POO!** 💩", "description": "{winner.mention} is **100% {m_type_lower}** and {loser.mention} **{loser_percentage}%** is just... poo. The jungle has spoken. 💩"},
    {"title": "🚨 **EMERGENCY EXIT!** 🚨", "description": "{winner.mention} hit **100% {m_type_lower}** so hard, {loser.mention} **{loser_percentage}%** probably hit the emergency exit button. Don't let the door hit you on the way out! 🚪"},
    {"title": "🎯 **BULLSEYE OF DEFEAT!** 🎯", "description": "{winner.mention} scored a perfect **100% {m_type_lower}** bullseye right on {loser.mention}'s **{loser_percentage}%** face. Oof. That's gotta sting. 🎯"},
    {"title": "😴 **DID YOU EVEN WAKE UP?** 😴", "description": "{winner.mention} is **100% {m_type_lower}** and {loser.mention} **{loser_percentage}%** clearly didn't even wake up for this. Go back to bed, you're embarrassing yourself. 🛌"},
    {"title": "👑 **THE NEW {m_type_upper} OVERLORD!** 👑", "description": "{winner.mention} is **100% {m_type_lower}** and has claimed the title of {m_type_lower} Overlord! {loser.mention} **{loser_percentage}%** is now officially a minion. Fetch me a banana! 🍌"},
    {"title": "💥 **EXPLOSIVE {m_type_upper} VICTORY!** 💥", "description": "{winner.mention} just detonated a **100% {m_type_lower}** bomb on {loser.mention} **{loser_percentage}%**! There's nothing left but dust and regret. 🔥"},
    {"title": "🎤 **MIC DROP {m_type_upper}!** 🎤", "description": "{winner.mention} just dropped the mic with a **100% {m_type_lower}** performance! {loser.mention} **{loser_percentage}%** is left speechless and defeated. 🎤⬇️"},
    {"title": "📉 **YOUR STATS ARE TOO LOW!** 📉", "description": "{winner.mention} is **100% {m_type_lower}** and {loser.mention} **{loser_percentage}%** just doesn't have the stats for this content. Go train your {m_type_lower} level, scrub. 📊"}
]

_STRONG_WIN_RESPONSES = [ # winner_percentage >= 75
    {"title": "🏆 **{m_type_upper} OVERLORD!** 🏆", "description": "{winner.mention} unleashed **{winner_percentage}% {m_type_lower}** fury, crushing {loser.mention}'s **{loser_percentage}%**!"},
    {"title": "💪 **{m_type_upper} SUPERIORITY!** 💪", "description": "With a staggering **{winner_percentage}% {m_type_lower}**, {winner.mention} makes {loser.mention} **{loser_percentage}%** look like they're still learning to peel!"},
    {"title": "🔥 **{m_type_upper} POWER PLAY!** 🔥", "description": "{winner.mention} flexes their **{winner_percentage}% {m_type_lower}** might! {loser.mention} **{loser_percentage}%** was simply out-{m_type_lower}ed!"},
    {"title": "🌪️ **{m_type_upper} TEMPEST!** 🌪️", "description": "{winner.mention} unleashed a **{winner_percentage}% {m_type_lower}** storm! {loser.mention} **{loser_percentage}%** was blown away!"},
    {"title": "💥 **DOMINANT {m_type_upper} DISPLAY!** 💥", "description": "Pure {m_type_lower} dominance! {winner.mention} **{winner_percentage}%** made {loser.mention} **{loser_percentage}%** question their primate heritage!"},
    {"title": "🥇 **GOLD MEDAL {m_type_upper}!** 🥇", "description": "{winner.mention} stands atop the podium with **{winner_percentage}% {m_type_lower}**! {loser.mention} **{loser_percentage}%** takes home nothing but regret."},
    {"title": "🦍 **ALPHA {m_type_upper} WINS!** 🦍", "description": "{winner.mention} proved they're the alpha with **{winner_percentage}% {m_type_lower}**! {loser.mention} is clearly a beta. Better luck next time, little chimp. 🐒"},
    {"title": "😏 **SMUG {m_type_upper} VICTORY!** 😏", "description": "With a smug grin, {winner.mention} ({winner_percentage}% {m_type_lower}) snatched victory from {loser.mention} ({loser_percentage}%)! Don't cry, {loser.mention}, it's just a monkey-off. 🍌💧"},
    {"title": "🍌 **MONKEY HEIST!** 🍌", "description": "{winner.mention} executed a perfect monkey heist with **{winner_percentage}% {m_type_lower}**! {loser.mention} **{loser_percentage}%** was left with empty hands."},
    {"title": "😂 **NOT EVEN CLOSE!** 😂", "description": "{winner.mention}'s **{winner_percentage}% {m_type_lower}** was so far ahead of {loser.mention}'s **{loser_percentage}%**, it's not even funny. Okay, it's a little funny. Get good, {loser.mention}. 🎮"},
    {"title": "👑 **CROWNED {m_type_upper}!** 👑", "description": "All hail {winner.mention}, the newly crowned **{winner_percentage}% {m_type_lower}**! {loser.mention} **{loser_percentage}%** is just a footnote in this epic tale. Long live the king/queen! 🤴👸"},
    {"title": "⚔️ **AGS TO G-MAUL!** ⚔️", "description": "{winner.mention} just hit a **{winner_percentage}% {m_type_lower}** AGS spec into a G-maul! {loser.mention} **{loser_percentage}%** didn't even have time to eat. Sit down, kid. 🪑"},
    {"title": "🚑 **CALL AN AMBULANCE!** 🚑", "description": "But not for {winner.mention} **{winner_percentage}% {m_type_lower}**! {loser.mention} **{loser_percentage}%** is going to need life support after that beatdown. 💀"},
    {"title": "🍌 **DEMOTION NOTICE!** 🍌", "description": "Effective immediately, {loser.mention} **{loser_percentage}%** has been demoted to a banana peel for {winner.mention} **{winner_percentage}% {m_type_lower}** to slip on for comedic effect. It's your only purpose now. 🤡"},
    {"title": "📢 **PUBLIC SERVICE ANNOUNCEMENT!** 📢", "description": "This wasn't a duel. It was a PSA by {winner.mention} **{winner_percentage}% {m_type_lower}** on the dangers of being as bad as {loser.mention} **{loser_percentage}%**. Stay safe, kids. 🙏"},
    {"title": "🛡️ **VENGEANCE!** 🛡️", "description": "{loser.mention} **{loser_percentage}%** tried to fight back, but only activated {winner.mention}'s **{winner_percentage}% {m_type_lower}** vengeance! Thanks for the extra damage, idiot. 💥"},
    {"title": "⚰️ **GET THE COFFIN!** ⚰️", "description": "The jungle pallbearers are here for {loser.mention} **{loser_percentage}%**. {winner.mention} **{winner_percentage}% {m_type_lower}** didn't leave enough for a closed-casket funeral. Shame. 🕺"},
    {"title": "📜 **SOUL SNATCHED!** 📜", "description": "As per the fine print, {winner.mention} **{winner_percentage}% {m_type_lower}** now legally owns {loser.mention}'s **{loser_percentage}%** soul. Don't worry, it'll be used for... things. 😈"},
    {"title": "🧐 **A STUDY IN CONTRASTS!** 🧐", "description": "Here we see a {m_type_lower} prodigy, {winner.mention} **{winner_percentage}%**, and... well, {loser.mention} **{loser_percentage}%** is also here. And that's great. For {winner.mention}. 🏆"},
    {"title": "🚫 **TELEBLOCK!** 🚫", "description": "{winner.mention} **{winner_percentage}% {m_type_lower}** just cast Teleblock on {loser.mention} **{loser_percentage}%**. You can't escape the shame for the next 5 minutes. We're all watching. 👀"},
    {"title": "🎭 **NEW MASK, WHO DIS?** 🎭", "description": "{winner.mention} **{winner_percentage}% {m_type_lower}** is now wearing {loser.mention}'s **{loser_percentage}%** face. It's an improvement, honestly. No offense. 💅"},
    {"title": "⚡ **THE QUICKENING!** ⚡", "description": "There can be only one! {winner.mention} **{winner_percentage}% {m_type_lower}** has absorbed the power of {loser.mention} **{loser_percentage}%**. You feel that? That's the feeling of becoming irrelevant. ✨"}
]

_ZERO_LOSS_RESPONSES = [ # loser_percentage == 0
    {"title": "💀 **{m_type_upper} PURGE!** 💀", "description": "{winner.mention} **{winner_percentage}%** is practically a different species! {loser.mention} registered an embarrassing **0% {m_type_lower}%."},
    {"title": "📉 **TOTAL DE-{m_type_upper}IFICATION!** 📉", "description": "{loser.mention} scored **0% {m_type_lower}** against {winner.mention}'s mighty **{winner_percentage}%**! {loser.mention} has been officially un-{m_type_lower}ed."},
    {"title": "🚫 **{m_type_upper} NULLIFICATION!** 🚫", "description": "{loser.mention} scored an astounding **0% {m_type_lower}**! Are they even trying? {winner.mention} **{winner_percentage}%** scoffs."},
    {"title": "👻 **GHOST OF A {m_type_upper}!** 👻", "description": "Is {loser.mention} even there? A **0% {m_type_lower}** reading suggests not! {winner.mention} **{winner_percentage}%** easily claims victory from the void."},
    {"title": "🗑️ **{m_type_upper} TRASHED!** 🗑️", "description": "{loser.mention} scored a pathetic **0% {m_type_lower}**! {winner.mention} **{winner_percentage}%** just swept them into the trash. Enjoy the dumpster! 🚮"},
    {"title": "😂 **ZERO {m_type_upper} GIVEN!** 😂", "description": "{loser.mention} gave **0% {m_type_lower}**! {winner.mention} **{winner_percentage}%** is laughing. Maybe try being less... human? 🤷‍♂️"},
    {"title": "📉 **{m_type_upper} BANKRUPTCY!** 📉", "description": "{loser.mention} hit **0% {m_type_lower}** and declared {m_type_lower} bankruptcy! {winner.mention} **{winner_percentage}%** is now the proud victor!"},
    {"title": "🐒 **NOT EVEN A {m_type_upper}!** 🐒", "description": "{loser.mention} scored **0% {m_type_lower}**! Are they even a {m_type_lower}? {winner.mention} **{winner_percentage}%** is questioning everything. The jungle is confused. 🤔"},
    {"title": "👻 **YOU'RE A GHOST!** 👻", "description": "{loser.mention} scored **0% {m_type_lower}**! Did you even show up? {winner.mention} **{winner_percentage}%** is claiming victory over thin air. Spooky. 👻"},
    {"title": "🚫 **ERROR 404: {m_type_upper} NOT FOUND!** 🚫", "description": "{loser.mention} returned a **0% {m_type_lower}**! The system couldn't even detect any {m_type_lower} activity. {winner.mention} **{winner_percentage}%** wins by default. 💻"},
    {"title": "💀 **FLATLINED!** 💀", "description": "{loser.mention}'s {m_type_lower} score flatlined at **0%**! {winner.mention} **{winner_percentage}%** is calling time of death. RIP, {loser.mention}. ⚰️"},
    {"title": "🗑️ **RECYCLED {m_type_upper}!** 🗑️", "description": "{loser.mention} scored **0% {m_type_lower}**! They're so bad, they've been marked for recycling. {winner.mention} **{winner_percentage}%** is the future. ♻️"},
    {"title": "😂 **THE JOKE'S ON YOU!** 😂", "description": "{loser.mention} scored **0% {m_type_lower}**! The entire jungle is laughing. {winner.mention} **{winner_percentage}%** is just here for the show. 🎪"},
    {"title": "📉 **NEGATIVE {m_type_upper} XP!** 📉", "description": "{loser.mention} scored **0% {m_type_lower}**! You actually lost {m_type_lower} XP. {winner.mention} **{winner_percentage}%** is leveling up just by being near you. 📈"},
    {"title": "🍌 **ROTTEN BANANA!** 🍌", "description": "{loser.mention} is a **0% {m_type_lower}** rotten banana! {winner.mention} **{winner_percentage}%** is the fresh, ripe victory. Don't touch {loser.mention}, it's squishy. 🤢"},
    {"title": "🤷‍♀️ **WHO ARE YOU AGAIN?** 🤷‍♂️", "description": "{loser.mention} scored **0% {m_type_lower}**! {winner.mention} **{winner_percentage}%** doesn't even remember who they were competing against. You're that forgettable. 💭"},
    {"title": "🚫 **ACCESS DENIED!** 🚫", "description": "{loser.mention} scored **0% {m_type_lower}**! You've been denied access to the {m_type_lower} club. {winner.mention} **{winner_percentage}%** has the VIP pass. 🔑"},
    {"title": "💩 **A PILE OF NOTHING!** 💩", "description": "{loser.mention} scored **0% {m_type_lower}**! That's not a score, that's a pile of monkeyshit. {winner.mention} **{winner_percentage}%** is disgusted. 💩"},
    {"title": "😴 **STILL ASLEEP?** 😴", "description": "{loser.mention} scored **0% {m_type_lower}**! Were you still in bed? {winner.mention} **{winner_percentage}%** won before you even woke up. Snooze you lose! 🛌"}
]

_POOR_LOSS_RESPONSES = [ # loser_percentage <= 25
    {"title": "🙈 **{m_type_upper} OUTCRY!** 🙈", "description": "Ouch! {loser.mention} only scraped by with **{loser_percentage}% {m_type_lower}** against {winner.mention}'s dominant **{winner_percentage}%**!"},
    {"title": "👎 **WEAK {m_type_upper} SHOWING!** 👎", "description": "{loser.mention} **{loser_percentage}% {m_type_lower}** was no match for {winner.mention}'s **{winner_percentage}%**! Did they forget their morning banana? The victory goes to {winner.mention}!"},
    {"title": "📉 **{m_type_upper} GONE WRONG!** 📉", "description": "{loser.mention} stumbled with a mere **{loser_percentage}% {m_type_lower}**! {winner.mention} **{winner_percentage}%** swings victorious!"},
    {"title": "📉 **{m_type_upper} PLUMMET!** 📉", "description": "{loser.mention}'s {m_type_lower} score took a nosedive to **{loser_percentage}%**! {winner.mention} **{winner_percentage}%** capitalized on the fumble!"},
    {"title": " করুণ **PATHETIC {m_type_upper} ATTEMPT!**  করুণ", "description": "Was that even a try? {loser.mention} limped in with **{loser_percentage}% {m_type_lower}**. {winner.mention} **{winner_percentage}%** laughs all the way to victory!"},
    {"title": "🌱 **SPROUTING {m_type_upper} VS VETERAN!** 🌱", "description": "{loser.mention} **{loser_percentage}% {m_type_lower}** is clearly still a sapling in the jungle of {m_type_plural_lower}. {winner.mention} **{winner_percentage}%** harvests victory with ease!"},
    {"title": "😂 **PATHETIC {m_type_upper}!** 😂", "description": "{loser.mention}'s **{loser_percentage}% {m_type_lower}** was just sad. {winner.mention} **{winner_percentage}%** barely broke a sweat. Go home, {loser.mention}, you're drunk on sadness. 😭"},
    {"title": "🍌 **PEEL-OUT!** 🍌", "description": "{loser.mention} **{loser_percentage}% {m_type_lower}** just peeled out of this competition! {winner.mention} **{winner_percentage}%** is left with the victory. Don't let the door hit you on the way out! 🚪"},
    {"title": "📉 **{m_type_upper} DISAPPOINTMENT!** 📉", "description": "The jungle is collectively sighing at {loser.mention}'s **{loser_percentage}% {m_type_lower}**! {winner.mention} **{winner_percentage}%** is just shaking their head while collecting the win. Do better, {loser.mention}. 🙄"},
    {"title": "🐒 **NOOB {m_type_upper}!** 🐒", "description": "{loser.mention} **{loser_percentage}% {m_type_lower}** is clearly a {m_type_lower} noob! {winner.mention} **{winner_percentage}%** just schooled them. The victory is for the pros! 🎮"},
    {"title": "💔 **BROKEN {m_type_upper}!** 💔", "description": "{loser.mention} **{loser_percentage}% {m_type_lower}** is broken and defeated! {winner.mention} **{winner_percentage}%** shows no mercy. Get well soon, {loser.mention}. Or don't. 🤷‍♀️"},
    {"title": "💩 **{m_type_upper} POO-FLING!** 💩", "description": "{loser.mention} **{loser_percentage}% {m_type_lower}** just got poo-flung by {winner.mention} **{winner_percentage}%**!"},
    {"title": "🪦 **REST IN PEELS!** 🪦", "description": "{loser.mention} **{loser_percentage}% {m_type_lower}** has officially passed away from embarrassment. {winner.mention} **{winner_percentage}%** sends their regards. And a banana for the funeral. 🍌"},
    {"title": "🤡 **CIRCUS ACT!** 🤡", "description": "{loser.mention} **{loser_percentage}% {m_type_lower}** put on quite the clown show! {winner.mention} **{winner_percentage}%** is just here for the laughs. Honk honk! 🎪"},
    {"title": "📉 **STOCK MARKET CRASH!** 📉", "description": "{loser.mention}'s {m_type_lower} stock plummeted to **{loser_percentage}%**! {winner.mention} **{winner_percentage}%** just made a killing. Better luck with your next investment, {loser.mention}. 💸"},
    {"title": "🤦 **FACEPALM {m_type_upper}!** 🤦", "description": "The jungle collectively facepalmed at {loser.mention}'s **{loser_percentage}% {m_type_lower}** performance. {winner.mention} **{winner_percentage}%** is just trying to forget what they saw. 🙄"},
    {"title": "🎣 **BAIT AND SWITCH!** 🎣", "description": "{loser.mention} **{loser_percentage}% {m_type_lower}** was clearly just bait for {winner.mention}'s **{winner_percentage}%** superior {m_type_lower} skills. Thanks for playing, little fishy. 🐠"},
    {"title": "🗑️ **REJECTED {m_type_upper}!** 🗑️", "description": "{loser.mention} **{loser_percentage}% {m_type_lower}** has been rejected by the {m_type_lower} council. {winner.mention} **{winner_percentage}%** is now the chosen one. Begone, {loser.mention}! 👋"},
    {"title": "👻 **SPOOKY {m_type_upper}!** 👻", "description": "{loser.mention} **{loser_percentage}% {m_type_lower}** was so bad, it's scary! {winner.mention} **{winner_percentage}%** is still recovering from the fright. 😱"},
    {"title": "🍌 **SLIPPED ON A PEEL!** 🍌", "description": "{loser.mention} **{loser_percentage}% {m_type_lower}** clearly slipped on a banana peel and couldn't recover. {winner.mention} **{winner_percentage}%** just walked right over them. Classic. 🚶‍♂️"},
    {"title": "📉 **FAIL ARMY!** 📉", "description": "{loser.mention} **{loser_percentage}% {m_type_lower}** has joined the ranks of the Fail Army! {winner.mention} **{winner_percentage}%** is leading the charge to victory. 🎖️"},
    {"title": "😴 **WAKE UP, SHEEPLE!** 😴", "description": "{loser.mention} **{loser_percentage}% {m_type_lower}** was clearly sleepwalking through this. {winner.mention} **{winner_percentage}%** is wide awake and ready to collect their prize. 💤"},
    {"title": "🐒 **LESS THAN {m_type_upper}!** 🐒", "description": "{loser.mention} **{loser_percentage}% {m_type_lower}** is officially less {m_type_lower} than a {m_type_lower} in training. {winner.mention} **{winner_percentage}%** is the real deal. 🥇"}
]

_STANDARD_WIN_RESPONSES = [ # Standard win/loss
    {"title": "🎉 **{m_type_upper} BATTLE WON!** 🎉", "description": "{winner.mention} **{winner_percentage}% {m_type_lower}** just barely out-ooga-booga'd {loser.mention} **{loser_percentage}%**! A win is a win!"},
    {"title": "🍌 **{m_type_upper} BRAGGING RIGHTS!** 🍌", "description": "{winner.mention} claims victory with **{winner_percentage}% {m_type_lower}** over {loser.mention}'s **{loser_percentage}%**! Enjoy the sweet taste of {m_type_lower} triumph!"},
    {"title": "👍 **NICE {m_type_upper}ING!** 👍", "description": "{winner.mention} showed their **{winner_percentage}% {m_type_lower}** prowess, edging out {loser.mention} **{loser_percentage}%**! Well played, {m_type_lower}!"},
    {"title": "🤏 **BY A BANANA PEEL!** 🤏", "description": "{winner.mention} **{winner_percentage}% {m_type_lower}** just slipped past {loser.mention} **{loser_percentage}%**! A narrow victory!"},
    {"title": "💥 **{m_type_upper} CLASH RESOLVED!** 💥", "description": "The dust settles, and {winner.mention} **{winner_percentage}% {m_type_lower}** stands victorious over {loser.mention} **{loser_percentage}%**! Their prize: bragging rights!"},
    {"title": "🐒 **TOP {m_type_upper} TODAY!** 🐒", "description": "In today's {m_type_lower}-off, {winner.mention} **{winner_percentage}% {m_type_lower}** proved slightly more {m_type_lower} than {loser.mention} **{loser_percentage}%**! {winner.mention} celebrates!"},
    {"title": "😏 **JUST GOOD ENOUGH!** 😏", "description": "{winner.mention} **{winner_percentage}% {m_type_lower}** was just good enough to beat {loser.mention} **{loser_percentage}%**! No need to be flashy. Efficiency! 📈"},
    {"title": "🍌 **MONKEY SWIPE!** 🍌", "description": "{winner.mention} **{winner_percentage}% {m_type_lower}** expertly swiped victory from {loser.mention} **{loser_percentage}%**! Easy pickings! 🤏"},
    {"title": "👑 **SLIGHTLY MORE {m_type_upper}!** 👑", "description": "{winner.mention} **{winner_percentage}% {m_type_lower}** is officially slightly more {m_type_lower} than {loser.mention} **{loser_percentage}%**! Them's the rules. 🤷‍♀️"},
    {"title": "😂 **BETTER LUCK NEXT TIME!** 😂", "description": "{winner.mention} **{winner_percentage}% {m_type_lower}** out-oogah-boogah'd {loser.mention} **{loser_percentage}%**! Don't worry, {loser.mention}, there's always next time... to lose again! 😈"},
    {"title": "🐒 **JUNGLE JUSTICE!** 🐒", "description": "Jungle justice has been served! {winner.mention} **{winner_percentage}% {m_type_lower}** proved superior to {loser.mention} **{loser_percentage}%**. The jungle has spoken! 🗣️"},
    {"title": "📈 **{m_type_upper} ADVANTAGE!** 📈", "description": "{winner.mention} **{winner_percentage}% {m_type_lower}** had the clear {m_type_lower} advantage over {loser.mention} **{loser_percentage}%**! Simple as that. 📊"},
    {"title": "🤏 **TOO CLOSE FOR COMFORT!** 🤏", "description": "{winner.mention} **{winner_percentage}% {m_type_lower}** barely scraped by {loser.mention} **{loser_percentage}%**. I'm not proud, but I'll take it. A win's a win. 😅"},
    {"title": "🧠 **CALCULATED!** 🧠", "description": "{winner.mention} **{winner_percentage}% {m_type_lower}** did just enough to beat {loser.mention} **{loser_percentage}%**. It's called efficiency, look it up. 🤓"},
    {"title": "🎲 **RNGESUS SMILES UPON ME!** 🎲", "description": "The dice gods favored {winner.mention} **{winner_percentage}% {m_type_lower}** today! Sorry {loser.mention} **{loser_percentage}%**, maybe try sacrificing a goblin next time? 🙏"},
    {"title": "💦 **SWEATY VICTORY!** 💦", "description": "Phew! {winner.mention} **{winner_percentage}% {m_type_lower}** is sweating after that close call with {loser.mention} **{loser_percentage}%**. But a win is a win, even if it's a sweaty one. 🥵"},
    {"title": "❓ **A QUESTIONABLE WIN!** ❓", "description": "Did {winner.mention} **{winner_percentage}% {m_type_lower}** deserve to win against {loser.mention} **{loser_percentage}%**? The jungle may never know. But the scoreboard does. And it says I won. So... yeah. 🏆"},
    {"title": "🍀 **LUCKY {m_type_upper}!** 🍀", "description": "{winner.mention} **{winner_percentage}% {m_type_lower}** must have found a four-leaf clover! {loser.mention} **{loser_percentage}%** was just unlucky. Or bad. Probably both. 🍀"},
    {"title": "🍿 **ENTERTAINING, AT LEAST!** 🍿", "description": "Well, that was a nail-biter! {winner.mention} **{winner_percentage}% {m_type_lower}** takes the win from {loser.mention} **{loser_percentage}%**. Thanks for the entertainment, I guess. 🍿"},
    {"title": "📜 **THE PROPHECY IS FULFILLED!** 📜", "description": "The ancient scrolls foretold this! {winner.mention} **{winner_percentage}% {m_type_lower}** would defeat {loser.mention} **{loser_percentage}%**! It was written. You can't fight destiny. 📜"},
    {"title": "🍻 **TO THE VICTOR GO THE SPOILS!** 🍻", "description": "{winner.mention} **{winner_percentage}% {m_type_lower}** raises a glass to their victory over {loser.mention} **{loser_percentage}%**! Don't worry, {loser.mention}, you can have the leftovers. Maybe. 🍻"},
    {"title": "💔 **HEARTBREAKER!** 💔", "description": "A heartbreaker for {loser.mention} **{loser_percentage}%**! {winner.mention} **{winner_percentage}% {m_type_lower}** snatches the win at the last second! So close, yet so far. Sucks to be you. 💔"},
    {"title": "🦈 **ATE ALL MY SHARKS!** 🦈", "description": "{winner.mention} **{winner_percentage}% {m_type_lower}** had to eat their whole inventory to beat {loser.mention} **{loser_percentage}%**, but the kill is confirmed. Gf, noob. 💰"}, # End of original responses
    {"title": "🤫 **SHHH, IT'S OKAY!** 🤫", "description": "There there, {loser.mention} **{loser_percentage}%**. You tried your best. It just wasn't good enough to beat {winner.mention} **{winner_percentage}% {m_type_lower}**. Now go have a cry. 🤫"},
    {"title": "💀 **SURVIVOR'S GUILT!** 💀", "description": "{winner.mention} **{winner_percentage}% {m_type_lower}** won, but at what cost? {loser.mention} **{loser_percentage}%** is now questioning all their life choices. Don't worry, {winner.mention}, the therapy bills are on {loser.mention}."},
    {"title": "🔪 **A SLICE OF HUMBLE PIE!** 🔪", "description": "{winner.mention} **{winner_percentage}% {m_type_lower}** just served {loser.mention} **{loser_percentage}%** a piping hot slice of humble pie. Hope you like it burnt, {loser.mention}."},
    {"title": "🎭 **THE JUNGLE'S NEW VILLAIN!** 🎭", "description": "{winner.mention} **{winner_percentage}% {m_type_lower}** has claimed victory, making {loser.mention} **{loser_percentage}%** the jungle's new punching bag. Enjoy the spotlight, {loser.mention}!"},
    {"title": "👻 **HAUNTED BY DEFEAT!** 👻", "description": "{loser.mention} **{loser_percentage}%** will forever be haunted by the ghost of {winner.mention}'s **{winner_percentage}% {m_type_lower}** victory. Sleep tight, {loser.mention}."},
    {"title": "📉 **YOUR STOCK JUST CRASHED!** 📉", "description": "{winner.mention} **{winner_percentage}% {m_type_lower}** just sent {loser.mention}'s **{loser_percentage}%** {m_type_lower} stock plummeting. Time to file for bankruptcy, {loser.mention}."},
    {"title": "🤡 **HONK HONK, LOSER!** 🤡", "description": "{winner.mention} **{winner_percentage}% {m_type_lower}** is celebrating, while {loser.mention} **{loser_percentage}%** is left wearing a clown nose. Honk honk, {loser.mention}! You're the entertainment now."},
    {"title": "🗑️ **STRAIGHT TO THE BIN!** 🗑️", "description": "{winner.mention} **{winner_percentage}% {m_type_lower}** just tossed {loser.mention} **{loser_percentage}%** into the recycling bin. You're officially waste, {loser.mention}."},
    {"title": "🤯 **MIND GAMES WON!** 🤯", "description": "{winner.mention} **{winner_percentage}% {m_type_lower}** didn't just win, they played mind games with {loser.mention} **{loser_percentage}%**. Now {loser.mention} is questioning reality. Good job, {winner.mention}!"},
    {"title": "🚽 **FLUSHED AWAY!** 🚽", "description": "{winner.mention} **{winner_percentage}% {m_type_lower}** just flushed {loser.mention} **{loser_percentage}%** down the drain. Hope you enjoy the sewers, {loser.mention}."},
    {"title": "🐒 **THE JUNGLE LAUGHS!** 🐒", "description": "The entire jungle is laughing at {loser.mention}'s **{loser_percentage}%** pathetic attempt against {winner.mention} **{winner_percentage}% {m_type_lower}**. Don't worry, {loser.mention}, they'll forget... eventually. Probably."},
    {"title": "🚨 **EMERGENCY THERAPY!** 🚨", "description": "{winner.mention} **{winner_percentage}% {m_type_lower}** won, and {loser.mention} **{loser_percentage}%** is now in desperate need of therapy. We recommend a good banana-based psychiatrist."},
    {"title": "🍌 **BANANA PEEL OF SHAME!** 🍌", "description": "{loser.mention} **{loser_percentage}%** just slipped on the banana peel of shame, courtesy of {winner.mention} **{winner_percentage}% {m_type_lower}**. Try not to break anything important, {loser.mention}."},
    {"title": "😈 **A DEAL WITH THE DEVIL!** 😈", "description": "{winner.mention} **{winner_percentage}% {m_type_lower}** clearly made a deal with the devil to beat {loser.mention} **{loser_percentage}%**. What did you give up, {winner.mention}? Your soul? Worth it."},
    {"title": "🪦 **R.I.P. DIGNITY!** 🪦", "description": "{winner.mention} **{winner_percentage}% {m_type_lower}** just buried {loser.mention}'s **{loser_percentage}%** dignity. May it rest in pieces. ⚰️"},
    {"title": "🎤 **YOU'RE FIRED!** 🎤", "description": "{winner.mention} **{winner_percentage}% {m_type_lower}** just delivered the ultimate pink slip to {loser.mention} **{loser_percentage}%**. Pack your bags, {loser.mention}, you're out of here!"},
    {"title": "🌌 **LOST IN THE VOID!** 🌌", "description": "{winner.mention} **{winner_percentage}% {m_type_lower}** sent {loser.mention} **{loser_percentage}%** spiraling into the existential void. Hope you find your way back, {loser.mention}."},
    {"title": "💉 **A SHOT OF REALITY!** 💉", "description": "{winner.mention} **{winner_percentage}% {m_type_lower}** just gave {loser.mention} **{loser_percentage}%** a much-needed shot of reality. It stings, doesn't it, {loser.mention}?"},
    {"title": "📜 **THE BOOK OF SHAME!** 📜", "description": "{winner.mention} **{winner_percentage}% {m_type_lower}** has officially inscribed {loser.mention}'s **{loser_percentage}%** name in the jungle's Book of Shame. It's a long read."},
    {"title": "🤯 **BRAIN DAMAGE!** 🤯", "description": "{winner.mention} **{winner_percentage}% {m_type_lower}** just caused irreparable brain damage to {loser.mention} **{loser_percentage}%**. Don't worry, it was probably pre-existing."},
    {"title": "👑 **THE NEW OVERLORD!** 👑", "description": "{winner.mention} **{winner_percentage}% {m_type_lower}** has ascended to become the new {m_type_lower} overlord! {loser.mention} **{loser_percentage}%** is now officially a minion. Fetch me a banana!"},
    {"title": "💥 **EXPLOSIVE DEFEAT!** 💥", "description": "{winner.mention} **{winner_percentage}% {m_type_lower}** just detonated an explosive defeat on {loser.mention} **{loser_percentage}%**. There's nothing left but dust and regret."},
    {"title": "😂 **LAUGHING STOCK!** 😂", "description": "{winner.mention} **{winner_percentage}% {m_type_lower}** is laughing all the way to victory, while {loser.mention} **{loser_percentage}%** is the entire jungle's new laughing stock. Enjoy the spotlight, {loser.mention}!"}
]

def _format_response(response_template: dict[str, str], **kwargs) -> dict[str, str]:
    """Formats a response dictionary's title and description using provided keyword arguments."""
    return {
        "title": response_template["title"].format(**kwargs),
        "description": response_template["description"].format(**kwargs)
    }

def get_monkeyoff_response(challenger: Member, challenger_percentage: int, opponent: Member, opponent_percentage: int, challenger_m_type: str, opponent_m_type: str) -> dict[str, str]:
    """
    Determines the outcome of a monkey-off and returns a dictionary with title and description for the embed.
    """
    # Determine the monkey type to use for the response based on the outcome.
    # For a win, use the winner's type. For a tie, pick one randomly.
    if challenger_percentage > opponent_percentage:
        m_type = challenger_m_type
    elif challenger_percentage < opponent_percentage:
        m_type = opponent_m_type
    else: # Tie
        m_type = random.choice([challenger_m_type, opponent_m_type])


    m_type_lower = m_type.lower() # e.g., "monkey"
    m_type_upper = m_type.upper() # e.g., "MONKEY"
    m_type_plural_lower = get_plural_monkey_type(m_type_lower) # e.g., "monkeys"
    m_type_plural_upper = m_type_plural_lower.upper() # e.g., "MONKEYS"


    # Common arguments for string formatting
    common_kwargs = {
        "m_type_lower": m_type_lower,
        "m_type_upper": m_type_upper,
        "m_type_plural_lower": m_type_plural_lower,
        "m_type_plural_upper": m_type_plural_upper,
        "challenger": challenger,
        "opponent": opponent,
        "challenger_percentage": challenger_percentage,
        "opponent_percentage": opponent_percentage,
    }
    
    # Determine winner and loser based on percentages.
    if challenger_percentage > opponent_percentage:
        winner, loser, winner_percentage, loser_percentage = challenger, opponent, challenger_percentage, opponent_percentage
    elif challenger_percentage < opponent_percentage:
        winner, loser, winner_percentage, loser_percentage = opponent, challenger, opponent_percentage, challenger_percentage
    else: # Tie
        chosen_response = random.choice(_TIE_RESPONSES)
        return _format_response(chosen_response, **common_kwargs)


    # Add winner/loser specific arguments for win/loss scenarios
    common_kwargs.update({
        "winner": winner,
        "loser": loser,
        "winner_percentage": winner_percentage,
        "loser_percentage": loser_percentage,
    })

    
    # Select response list based on win/loss conditions.
    responses_list = []
    if winner_percentage == 100: # Absolute MONKE
        responses_list = _PERFECT_WIN_RESPONSES
    elif loser_percentage == 0: # Loser got 0%
        responses_list = _ZERO_LOSS_RESPONSES
    elif winner_percentage >= 75: # Strong win
        responses_list = _STRONG_WIN_RESPONSES
    elif loser_percentage <= 25: # Loser did poorly
        responses_list = _POOR_LOSS_RESPONSES
    else: # Standard win/loss
        responses_list = _STANDARD_WIN_RESPONSES


    chosen_response = random.choice(responses_list)
    return _format_response(chosen_response, **common_kwargs)
