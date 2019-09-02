# Storage for all large text blocks in The Witch's Cat

import colorama
from colorama import Fore, Style
colorama.init()

'''
TO DO:
- finish Tier I endings
'''
'''
Takes regular text and returns the same text with dialogue (anything within
quotes) colored red
'''
def colorQuotes(text):
    quoteList = []
    for i in range(len(text)):
        if text[i] == "\"":
            quoteList.append(i)
    if len(quoteList) == 0:
        return text
    new_text = text[0:quoteList[0]]
    for q in range(len(quoteList) - 1):
        if q % 2 == 0:
            diag_start = quoteList[q]
            diag_end = quoteList[q + 1]
            new_text = new_text + Fore.RED + text[diag_start:diag_end + 1] + Style.RESET_ALL
        else:
            new_text = new_text + text[quoteList[q] + 1:quoteList[q + 1]]
    new_text = new_text + text[quoteList[-1] + 1:]
    return new_text
    
    
# MESSAGES
README = colorQuotes(("To go to a location shown in the list of options, simply type the name of the location."
             + "\nYou cannot go to a location not shown in the list of options. Try backtracking to get to where you want."
             + "\nWhen faced with a choice, type in one of the options offered."
             + "\nIf in battle mode, the syntax for using a skill is \"Use [SKILLNAME]\". "
             + "\nYou begin with the skill named SCRATCH, which deals 10 damage. You will learn more along the way."
             + "\nWhen not in battle, you may equip a new item by typing \"Equip [ITEMNAME]\"."
             + "\nYou can quit at any time by typing \"Quit\"."
             + "\nSave or load your game by typing \"Save\" or \"Load\" and following the prompts."
             + "\nNone of these commands are case-sensitive. Good luck and have fun!"))


# LOCATION PROMPTS
ALLEY_PROMPT = ("\nYou find yourself in an alley. You're not too sure how you got here..."
                    + "\nOptions:\nGraveyard")

GRAVEYARD_PROMPT = ("\nYou are at the graveyard. There is a chill in the air that ruffles your fur."
                    + "\nThe only thing that keeps your paws planted on the ground is the powerful magic you sense all around you."
                    + "\nAmidst all the gravestones sits a black dog. He seems to be thinking about something..."
                    + "\nOptions:\nAlley\nCave\nField")

CAVE_PROMPT = ("\nYou have entered the cave. If being in the graveyard made your fur stand on end, you must look"
                    + "\nlike a bush right now. Despite your impeccable night vision, you can't help but feel like"
                    + "\nsomething is about to jump out at you..."
                    + "\nOptions:\nGraveyard")

FIELD_PROMPT = ("\nYou are now in a field. The friendly wind swirls around you, and the sky, dotted"
                    + "\nby a myriad of dark birds, seems endless. You wish you could share this with your human..."
                    + "\nOptions:\nGraveyard\nRoad")

ROAD_PROMPT = ("\nYou have arrived at a road. Your ears lay flat against your head and you cower as cars roar past you."
                    + "\nYou have the feeling that you are being watched, and not just by the cars..."
                    + "\nOptions:\nField\nPorch")

PORCH_PROMPT = ("\nAfter crossing the road, you arrive at a human dwelling. Sitting on the porch steps is a little girl--"
                    + "\na human kitten. She appears to be crying. You wonder if there's anything you can do to help..."
                    + "\nOptions:\nRoad")


# CHARACTER DIALOGUE
GRIM_DIAG = colorQuotes(("\nCHURCH GRIM's ears are pricked forward eargerly at your approach,"
                    + "\nhis wagging tail sending sprays of ancient graveyard dust into the air."
                    + "\n\"I'm so glad you're here!\", he barks."
                    + "\n\"You see, it's actually my job to protect all the souls here.\""
                    + "\nCHURCH GRIM looks at the ground, suddenly downcast."
                    + "\"But, you see...there's something really big and scary at the edge of the yard!\""
                    + "\nThe dog is wearing a sheepish expression. \"I can't fight it off on my own. Can you help me?\""
                    + "\nOptions:\n"))

BAT_DIAG = colorQuotes(("\nA creature with beady black eyes hovers above you, veiny wings flapping threateningly in your face."
                    + "\n\"IT IS NOT SAFE HERE\", they state flatly. \"TURN BACK NOW. TURN BACK.\""
                    + "\nOptions:\n"))

CROW_DIAG = colorQuotes(("\n\"Ooh, look! A cat! A CAT!!\" exclaims a voice from above you head. You prick your ears towards the source"
                    + "\nAs a pair of wings come barrelling towards you. \"Scary! So scary! Betcha can't catch me!\","
                    + "\nCROW caws before you can get a single word in. You sense that this is going to be a one-sided conversation..."
                    + "\nOptions:\n"))

GIRL_DIAG = ("\nAs you walk closer, the human child blinks, looks at you briefly, then continues to cry."
                    + "\nYou wonder if there is any way to help her feel better..."
                    + "\nOptions:\n")

GHOST_DIAG = colorQuotes(("\nYou narrow your eyes at the spectral form sitting before you. You definitely did not notice THAT before."
                    + "\nIt looks like it might be a cat, but not like any you've seen. GHOST CAT finally opens her mouth to speak:"
                    + "\n\"You have come far with your magic. You have met all the denizens of this place."
                    + "\nI know where your human is; I can guide you to her.\" As GHOST CAT gets to her paws,"
                    + "\na glint of envy passes across her expression. \"But first, you must prove yourself,\""
                    + "\nshe growls. You feel the air suddenly go cold."
                    + "\nOptions:\n"))


# POST-BATTLE OUTCOMES
GIRL_OUTCOME = ("\nYou offer the CAT DOLL to the weeping child. She wipes away her tears and smiles graciously,"
                            + "\nbut wordlessly pushes it back towards you. You keep the CAT DOLL."
                            + " You have gained the skill RAIN, which deals 70 damage.")

GRIM_OUTCOME = colorQuotes(("\nCHURCH GRIM stares at the ground, slumped over and defeated."
                        + "\nHe glances up at you, then looks away fearfully."
                        + "\n\"Will you leave me alone if I teach you this skill?\", he pleads."
                        + "\"Maybe...you'll a better protector than me. But I never meant you any harm.\""
                        + "\nCHURCH GRIM turns tail and slowly plods away."
                        + "\nYou have gained the skill ETERNAL NIGHT, which deals 30 damage."))

PUMPKIN_OUTCOME = colorQuotes(("\n\"Wow!! You really did it!\" CHURCH GRIM yips excitedly as he bounces towards you."
                        + "\n\"That thing was terrifying! Who knows what kind of dark magic it possessed?"
                        + "\n...Huh? You're looking for a human? Let me see that hat. Smells like she went...that way\","
                        + "\nCHURCH GRIM declares, pointing his muzzle towards a cave."
                        + "\n\"The scent is stale, but it still might be worth checking out. I also saw something shiny by the alley.\""
                        + "\nThe huge dog stands up and wags his tail. \"Before you go, I wanted to teach you this\", he woofs."
                        + "\n\"It's how I've protected the graveyard for so long. I think it will help you."
                        + "\nCome and visit sometime, won't you?\""
                        + "\nYou have gained the skill ETERNAL NIGHT, which deals 30 damage."))

BAT_OUTCOME = ("\nBAT retreats to the roof of the cave, staring at you with the level of coldness that"
                        + "\ncould put out the sun. Suddenly, hundreds of other bats descended from the ceiling,"
                        + "\ncrowding you to the point that you can hardly see. It seems like you cannot go any further."
                        + "\nFrom watching the bats heal each other, however, you have learned a valuable skill."
                        + "\nYou have gained the skill HEAL, which recovers 50 hp.")

MONSTER_OUTCOME = colorQuotes(("\nAs the ferocious CAVE MONSTER flees from the cave in a hurry, a flood of bats joyously surrounds you."
                        + "\nBAT flutters up to you. \"YOU SAVED US, CAT. WE APOLOGIZE FOR THAT SMALL WOUND WE GAVE YOU"
                        + "\nWHEN YOU TRIED TO WALK PAST US. IT WASN'T SAFE. WE HOPE THIS IS ENOUGH TO THANK YOU."
                        + "\n...OH? YOU DESIRE KNOWLEDGE, NOT POWER? WE HAVE NOT SEEN A HUMAN RECENTLY."
                        + "\nTHERE WAS ONE, A WITCH, BUT SHE LEFT MOONS AGO. THAT IS WHO YOU SEEK, CORRECT?"
                        + "\nWHEN YOU FIND YOUR WITCH, THE BOTH OF YOU ARE WELCOME HERE ANYTIME, CAT.\""
                        + "\nYou have gained the skill HEAL, which recovers 50 hp."))

CROW_OUTCOME = colorQuotes(("\n\"Ha! You'll have to do better than that, you worm with paws!\" CROW flies out out range,"
                    + "\ncawing at you condescendingly. \"That was pretty fun. I guess I'll bestow you with"
                    + "\nsome of my grand abilities. Use it--or not!\" CROW glides away, laughing all the while."
                    + "\nYou have gained the skill SKY'S BLESSING, which deals 50 damage."))


# ENDINGS
# Bad
DEFEAT_END = ("\nYou are losing strength. It would be best to pull back now to fight another day."
                    + "\nIn the coming years, cats and other animals would report brief sightings of you,"
                    + "\nbut nobody would hear from you ever again.\n\nBAD END 1: DEFEAT")

MISTAKES_END = colorQuotes(("\nThere was once a King. He was not a bad king or a good king. Like his fathers before him, he"
                    + "\nruled his realm comfortably from the perch on his throne, enjoying indulgent royal dinners"
                    + "\nevery night while many of his subjects struggled to secure a proper meal. One day, a"
                    + "\nWitch requested to see the king. She said to him, \"You will never understand your people as"
                    + "\nyou are now, tyrant. I shall teach you humility and resourcefulness, which you shall learn as"
                    + "\nyou stand in the paws of a cat,\" and turned him into a small feline. Aghast at his entire"
                    + "\ncourt seeing him like this, the king ran far, far away and came upon a cave. It is in there"
                    + "\nthat he cultivated not a sense of humility like the witch had hoped, but an all-consuming"
                    + "\nhunger. The king hid in this cave for centuries and became a monster, tempting"
                    + "\nhumans and animals alike into its jaws with whisperings of false power…\n\nBAD END 2: MISTAKES"))

REJECTION_END = ("\nThere are tales of a peculiar cat, consumed by the occult, setting up camp in a certain"
                    + "\nalleyway. It is said that this cat was once kind, but their power has made them bitter and"
                    + "\n dissatisfied. Mothers tell their offspring to steer clear of the area, lest the magic finally drive the"
                    + "\nold cat mad. If you happened to cross paths with the witch cat, there was no telling what"
                    + "\nmisfortune would befall you.\n\nSPECIAL BAD END: REJECTION")

# True
TRUE_END = ("\nGHOST CAT smiles gravely, turns around, and walks off. Alarmed, you run to follow her."
                + "\nThe cat disappears right before your eyes, but in her place you see your human on the horizon."
                + "\nYou run and jump into her arms--a black cat finally reunited with their witch. All is well."
                + "\n\nHaving picked up some magic of your own, you become legendary among felines as the first cat"
                + "\nto create their own magic coven. Sometimes, you are seen walking into an alley that seems to lead nowhere..."
                + "\nIt is said that you go there to visit some old friends.\n\nTRUE END")

# Tier I
RECLUSE_END = ("\nAfter your encounter with GHOST CAT, you spend the next several days in deep thought. Eventually, you"
                + "\ncome to a decision with your allies CHURCH GRIM and the BATS. You decide to close off this cursed land;"
                + "\nno one may come, and no one may go. This is a land of great magic and tragedy, and you are determined"
                + "\nto keep the generations to come safe from it.\n\nRECLUSE END");

LIGHTNING_END = ("\nIt is said that in this land, there are benevolent spirits that guide lost souls, both living and dead,"
                + "\nout of storms. They take the shapes of a cat, a crow, and a dog, and are respected by every living creature."
                + "\n\nLIGHTNING END");

GRAVE_END = colorQuotes(("\nGHOST CAT smiles softly before fading into the mist. She seems to be expecting something" 
                    + "\nfrom you…\n\nYou make your way back to the graveyard. Through the shadows and fog, you"
                    + "\npick out a familiar shape. You approach it. You meet CHURCH GRIM, but he seems to be in low"
                    + "\nspirits. He confesses that despite his best efforts, there was one soul that he failed to protect."
                    + "\nCHURCH GRIM lifts his muzzle to look at you."
                    + "\"Hey, you met her, didn\'t you? You\nshould follow her. I think she knows where your witch is. I will be fine here. Staying here is what\nI was made to do.\""
                    + " You sense a presence atop a gravestone in the corner of your eye."
                    + "\nShaking your head, you take a step back and gesture to the gravestone with your tail."
                    + "\nYou tell CHURCH GRIM that it is your turn. He has worked hard and deserves to have a family."
                    + "\nYou watch CHURCH GRIM and GHOST CAT depart. You take over as the new church grim—"
                    + "\nthe sole guardian of this graveyard and the souls that reside in it. You become an immortal entity who"
                    + "\nnever wavers in this task. Somehow, you sense that one day you shall meet your predecessor once again."
                    + "\n\nGRAVE END"))

WING_END = ("\nAfter the battle, you and CROW become reunited as mutual familiars of your Witch and\n"
            + "together—with information from BAT and its family—you two scour the earth for signs of"
            + "\nher. It has been years and you have still not found her, but you can only assume she is safe."
            + "\nThe MONSTER CAT is gone after all, right?\n\nWING END")

DARK_END = colorQuotes(("\nGHOST CAT stares at you, her eyes appearing to be nothing more than blank, milky-white orbs."
            + "\n\"You have done well,\", she states. \"You have slain the Monster King and saved your"
            + "\nwitch. Congratulations.\" Her voice has no cadence. With a blink and a flick of a tail,"
            + "\nGHOST CAT turns and disappears into the mist. You are left alone in the rain as the"
            + "\ndistant wind howls over the gravestones.\n\nDARK END"))

ICARUS_END = ("\nAt the behest of GHOST CAT, who is too weak to help you, you and CROW set out in search of"
                + "\nyour Witch. It turns out that she was far closer than you thought—in the belly of the cave,"
                + "\nin which dwelled a huge, ferocious MONSTER CAT."
                + "\n…\nYou and CROW exchange what seems like countless blows with MONSTER CAT until you are both at your wit’s end."
                + "\nSomething glitters on the ground. It is a claw from MONSTER CAT’s paw, torn off at some point during the struggle."
                + "\nCROW stares at it for only a moment before plunging down to retrieve it. MONSTER CAT growls and"
                + "\nwhips its head around to face the bird—too late. In a single, fateful instant,"
                + "\nMONSTER CAT’s throat is slit by its own claw and CROW is swatted and thrown hard against the cave wall."
                + "\n…\nYou have managed to rescue your Witch from the temptation of great power,"
                + "\nbut in doing so, have lost a member of your family. You and your Witch grieve the loss of this brave familiar together."
                + "\n\nICARUS END");

# Tier II
RAIN_END = colorQuotes(("\nGHOST CAT’s fur starts to lie flat again as she sits down. \"You have proven your power, kitten. I"
                + "\nsuppose I owe it to you to tell you a few things.\" GHOST CAT’s pelt flickers in the rain. \"That"
                + "\nroad…was the place where I died. I was tempted by a voice…\" She shook her head"
                + "\nruefully. \"I wish I had known then that voice was a terrible beast in disguise. I left my"
                + "\nhuman behind—she’s just a little girl…\" Listening to the phantom cat, you feel like you"
                + "\nunderstand her better. You reflect on this as you rest on a warm lap under a small,"
                + "\nhomely porch, listening to the steady pitter-patter of rain on the roof above you."
                + "\nYou feel like everything will be okay.\n\nRAIN END"))

GUARDIAN_END = ("\nIn the wake of your battle with the mysterious GHOST CAT, you return to the company of your"
                    + "\nfirst and only friend in the graveyard. You still don’t go a day without wondering what"
                    + "\nbecame of your witch, and CHURCH GRIM always seems to wear a guilty look on his"
                    + "\nface, muttering about a soul he failed to protect. You decide to stay with him for the"
                    + "\nremainder of your days. With the two of you working together, no more souls shall go unguided.\n\nGUARDIAN END")

DEPTHS_END = ("\nGHOST CAT evaporates in a cloud of wispy dust. In the silence that follows, you are not sure"
                  + "\nwhat to do. You head back to the Cave and stay with the bats as they slowly recover from"
                  + "\nthe Cave Monster’s reign of terror. They tell you of the Cave Monster’s silver tongue—"
                  + "\nof a cat that became a beast by coaxing prey much larger than itself into its cave. The bats"
                  + "\nbelieve that your witch may have fallen victim to the monster’ temptations. From then on,"
                  + "\nyou settle down into the cave, helping the bats and chasing off intruders. Your real reason"
                  + "\nfor being there, however, is to exact your revenge on the Cave Monster you drove off,"
                  + "\nhoping that someday it will return.\n\nDEPTHS END")

WIND_END = colorQuotes(("\nAfter these events, you become a drifter—living as stray cats do, off the handouts of the land."
                + "\nSitting in a field, you hear a familiar caw. A pair of wings flutter to a pause on the ground"
                + "\nin front of you. It’s CROW. His fire gone, he tells you that he has information on the"
                + "\nwhereabouts of the witch, so you go with him. \"I am another familiar of our Witch,\" he"
                + "\nclaims, perched on a branch above you. You had no knowledge of this, but you also realize"
                + "\nthat, somehow, you hardly remember anything about your Witch—just that you love"
                + "\nher. \"I am a messenger—you’re lucky to be her companion, cat. I have been scouring the"
                + "\nland for answers, but to no avail.\" There is a stretch of silence. \"Perhaps it is for the best"
                + "\nthat I go back on the wing. It seems that death follows me wherever I go. Goodbye, cat.\""
                + "\nAfter another pause, CROW flies off, leaving you to listen only to the whispers of the wind.\n\nWIND END"))

DIALOG_TEXTS = [README, GRIM_DIAG, BAT_DIAG, CROW_DIAG, GHOST_DIAG,
                GRIM_OUTCOME, PUMPKIN_OUTCOME, MONSTER_OUTCOME, CROW_OUTCOME,
                MISTAKES_END, GRAVE_END, RAIN_END, WIND_END, DARK_END]
# reference only