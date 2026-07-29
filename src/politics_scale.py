"""Calibrate the Politics question to the country's own vote distribution.

Hardcoded targets of -55 / 0 / +55 were wrong in both countries, and worse in
Canada than the US. No Canadian riding is anywhere near -55: the most left-leaning
sits at -19.6, so picking "Left" could never score above 0.63 and the answer was
compressed into a band it could never escape. The US runs -86.6 to +92.9 on the
same nominal scale, because pinning both parties to the ends of a two-party race
uses the full width. A US +45 and a Canadian +45 are not the same politics.

So the three targets are read off each country's own distribution instead of typed:
Left is near its left tail, Centre its median, Right near its right tail. That makes
the SCORES comparable between countries even though the raw leans are not.
"""


def calibrate(leans):
    xs = sorted(x for x in leans if x is not None)
    if len(xs) < 20:
        return None
    q = lambda p: xs[min(len(xs) - 1, int(p / 100 * len(xs)))]
    left, centre, right = q(2), q(50), q(98)
    return dict(left=round(left, 1), centre=round(centre, 1), right=round(right, 1),
                tol=round(max(12.0, (right - left) / 3.0), 1))
