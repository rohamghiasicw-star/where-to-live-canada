# Friend usability test — "Where to live in Canada"

Tester: 55, Ontario, not techy. On my phone (375-wide). A buddy built the thing I dreamed up in the gym change room and sent me the link. Curious but skeptical.

---

## 1. Landing / first impressions

Big black headline, "Where to live in Canada." Under it: "Every best-places-to-live list picks the weights for you. This one asks what *you* want, then re-ranks all 712 places in Canada against it." I actually like that line — that's my whole idea in one sentence. 712 places is a lot, good, means the small towns are in there.

Then "What you want — Set each one, and how much it matters." First control is "Winter — The January you want to wake up in." A slider sitting in the middle with **-5°** off to the right. Took me a second: is -5 where I am or where I want to be? The little words "Deep freeze / No winter" under it told me drag right = warmer. OK. Under that, four buttons: Skip / A little / Matters / A lot, with "Matters" filled black. Nobody told me yet what those do — I *assume* it's how much I care.

**First real gripe:** on my phone there's NO explanation. Later I made the window wider (by accident) and a whole how-to appeared — numbered steps, and the key line: "A lot counts nine times A little, so one thing you really care about can outrank everything else." Plus a nice data block ("712 cities and towns... Toronto down to Annapolis Royal pop 530... Climate 1981-2010, Smoke 2013-2024"). **On the phone all of that is hidden.** So the mobile user (me) is left guessing at the exact thing that makes the app work.

At the bottom: Answer / List / Map tabs. Fine.

## 2. Setting what I want

I hate deep cold, so first job: warm up the Winter slider. **This is where I got mad.** I tried to drag that little handle to the right. Nothing. Tried again. Nothing. Tapped the track further along. Nothing. It just sat on -5. For the ONE thing I care about most, the control wouldn't budge for me. A thin handle like that on a phone is a bad choice.

I scrolled on and found the rest — and there's a LOT of it (about fifteen factors): Summer, Snow, Sun, **Wildfire smoke** (Dealbreaker / Prefer less / Not fussed), then "The place": **Size** (Village / Town / Small city / Mid city / Big city), **Near a city** ("to the nearest metro over 300,000": In one / Within an hour / Half a day / As far as possible), Housing budget, **Politics** (Left / Centre / Right / Not fussed), then "Life there": growing/emptying, who lives there, commute, life without a car, jobs, mix of people, French, what residents say. Honestly the defaults were already close to me: smoke "Prefer less / Matters," Size "Small city," Near a city "Within an hour." Whoever set the defaults gets a normal person.

I set: Winter mild + Matters, **Wildfire smoke → A lot** (the smoke this summer was brutal), **Size → Town**, Near a city stays "Within an hour," **Politics → Skip** (I lean a bit but I'm not fussed). The importance bar (Skip / A little / Matters / A lot) — once I figured out it's "how much this counts," it's actually clear and I like the four-step feel. Wish someone had told me on the phone.

## 3. The answer

With a mild winter + those settings I got: **"You should live in Chester, NS. It gets you clean air and the size. You give up the sun."** Runner-ups Bridgewater and Truro — all Nova Scotia coast towns, small, near Halifax, clean air. The tradeoff ("You give up the sun") is in orange, there's a mini-map pinning the three towns, and it says which factor separates the runner-ups. That screen is clean and I liked it. Sensible answer.

## 4. The thing I care about most: does "Winter matters A LOT" change the answer?

Yes — and here's where it got scary. When I flipped Winter to **"A lot"**, the top pick became **Salluit, QC** — an Inuit village in the Arctic where January is about -25°. I asked for a MILD winter and it sent me to one of the COLDEST places in Canada. The list confirmed it: #1 Salluit (score 78) ranked ABOVE #2 Duncan BC, which literally shows "Jan 3.4°" and "Gets you the winter." That would have made me close the tab and call my buddy to say it's broken.

**BUT** I kept digging (most people wouldn't). Turns out the real problem is that my mild-winter setting never "took" — the slider handle I fought with earlier never actually registered my drag, so the app quietly kept a COLD winter value and ranked cold places. When I reloaded and found a slider WITH little **"−" and "+" buttons** (which were NOT on the first screen I saw), I tapped "+" up to a mild +4° and set "A lot" — and it correctly gave me **North Cowichan, BC**, then Nanaimo and New Westminster. Vancouver Island. Mild winter, smaller than Vancouver, near a city. That's EXACTLY my dream — I liked Vancouver's climate but the city's too big, and it handed me the Island towns. When it's driven right, it nails it.

So the ranking brain is fine. The problem is the slider fought me, and that turned a good answer into a crazy one.

## 5. Losing my settings

Several times during this, my settings got wiped back to defaults and a red banner popped up: "STAGING · work in progress, may be rough · the stable version is here →". Winter jumped back to -5 on its own more than once. I think it happens when the page reloads or the window changes size. On a real phone that means: rotate it, or leave and come back, and you might lose everything. There's no "your picks are saved."

## 6. Sharing it

I hit **"Send this to someone."** The button turned into a dark box with a long link (`.../#6.3_20.1_1.1_...`) — so it packs all my settings into the URL, clever. No "Copied!" message though, and the link is cut off on the right edge, so I honestly wasn't sure it copied or if I was supposed to select it myself.

Then I opened my own shared link like a friend would. Nice touch: the top changed to "Someone sent you their answers, so this is their result. Change anything on the left and it becomes yours." **But the result was WINNIPEG, MB** — "It gets you the winter and the politics." Winnipeg is famously freezing. I'd been looking at a mild-winter answer and my friend gets Winnipeg. Because of the slider/reset mess, the link captured a COLD winter value, not the mild one I meant. If I'd actually sent that, I'd look like I don't know my friend at all. (One bright spot on that page: a real "The catch, from people who live there" note — "Manitoba ER waits are the worst in Canada..." — sourced and specific. Nice.)

## 7. Looking up Goderich (a town I actually know)

No search box — to find one town in 712 I had to hit "show all 712" and scroll. A search bar would've saved me. Found Goderich at **#334 / 712, score 34.** I tapped it and a detail card opened, and this is the best part of the whole app:

- A little **month-by-month temperature chart** (blue cold months, orange warm)
- **Snow 374 cm/yr** — that's a mountain of snow, and it's TRUE (lake-effect off Huron). Matches exactly what I know: "major snowstorms."
- **Days below -20: 5**, Sun 1793h, Wildfire smoke 0.37
- Honest note: "From BLYTH, 26.5km away, 128m difference in elevation. ECCC normals 1981-2010" — it tells me the weather is from a nearby station, doesn't pretend.
- People 7.9k, Home $468k, Rent $1000/mo, Income $70k, **Unemployment ".."** (shows missing data instead of making it up — I respect that)
- **Nearest city over 300k: London, 101 min** — confirms my "London is a bit of a drive."
- Riding Huron--Bruce, "leans right" — correct.
- **"What residents say":** weather -0.9, housing -1.0, jobs -1.8.

Everything I personally know about Goderich, this card got right. And it explains WHY Goderich scores low for me (cold, buried in snow, far from a big city) — which is fair. That detail card is what makes me trust the thing.

The footer methodology is also unusually honest: it names the smoke model, explains the census sources, says residents were researched for only 71 of 712 places (and marks which), explains a "weighted power mean" so a place "cannot fail the thing you care most about and win anyway," and even says "Nothing here is a recommendation. It is a way to argue with a list." Good voice.

---

## Verdict notes
The idea works and the data is genuinely trustworthy. But the winter slider fighting me, my settings vanishing, and the share link showing a DIFFERENT city than I picked are the kind of things that would make me quietly not share it — not because the idea's bad, but because I'd look silly.
