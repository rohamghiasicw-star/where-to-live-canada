# Usability test — "Where to live in Canada"

Persona: 29-year-old remote software worker in Toronto, tech-savvy, impatient with jank, priced out of the city. Wants: affordable housing (big deal), a growing (not dying) place, some scene/diversity (not all-retiree), tolerable winter, near-ish a city.

URL: https://rohamghiasicw-star.github.io/where-to-live-canada/
Viewport: window set to 1280w (renders ~1470 CSS px inner). Desktop.

---

## 1. First impression (skeptic hat on)

- Loads instantly. Static GitHub Pages page, no spinner, no cookie banner, no email-wall. Good start.
- Does NOT read as AI-generic. Editorial/newsroom feel: giant bold "Where to live in Canada", a short manifesto ("Every best-places-to-list picks the weights for you. This one asks what you want."), and a live computed answer up top ("You should live in Woodstock, ON — It gets you the drive and the winter. You give up the sun.").
- Nice crafted touches: the answer writes a sentence about tradeoffs, names near-ties ("Nearly the same on your answers: St. Thomas, Salaberry-de-Valleyfield. What separates them is the sun."), and there's a "Send this to someone" share button. The URL hash encodes my exact answers (`#-5.2_20.1_...`), so state is shareable. That's a real product decision, not boilerplate.
- Right-hand meta column states provenance up front: 712 places, Census 2021, Climate 1981-2010, Smoke 2013-2024, Votes 2025. Reads like someone who cares about data honesty.
- Methodology footer is unusually candid: weighted power mean (so you can't fail your top priority and still win), Revelstoke's snow station is 43km away and 1,431m up a mountain so its 1,388cm is "alpine snowpack, not the town", Indian reserves deliberately excluded. This is craft, not a template.

Skeptic note: 16 sliders is a LOT to land on a first-time user. No onboarding beyond the numbered list. But the defaults are pre-filled and an answer is already showing, so it's explorable.

## 2. The task — crank Housing budget low + cost matters a lot
