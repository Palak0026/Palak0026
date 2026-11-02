import os
import json
import urllib.request
from datetime import datetime

# ============================================================
# 🏎️ PALAK'S GITHUB GRAND PRIX
# GitHub: @Palak0026
# ============================================================

USERNAME = "Palak0026"
TOKEN = os.environ.get("GITHUB_TOKEN")

if not TOKEN:
    raise RuntimeError("GITHUB_TOKEN is missing.")

# ============================================================
# GET REAL GITHUB CONTRIBUTIONS
# ============================================================

query = """
query($userName:String!) {
  user(login: $userName) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            contributionCount
            date
          }
        }
      }
    }
  }
}
"""

request = urllib.request.Request(
    "https://api.github.com/graphql",
    data=json.dumps({
        "query": query,
        "variables": {
            "userName": USERNAME
        }
    }).encode("utf-8"),
    headers={
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
        "User-Agent": "Palak0026-GitHub-Grand-Prix"
    }
)

with urllib.request.urlopen(request) as response:
    result = json.loads(response.read().decode("utf-8"))

if result.get("errors"):
    raise RuntimeError(result["errors"])

calendar = (
    result["data"]["user"]
    ["contributionsCollection"]
    ["contributionCalendar"]
)

weeks = calendar["weeks"]
total = calendar["totalContributions"]

# ============================================================
# GRAPH SETTINGS
# ============================================================

CELL = 12
GAP = 4

START_X = 40
START_Y = 105

WIDTH = 930
HEIGHT = 335

cells = []

# ============================================================
# CREATE CONTRIBUTION GRID
# ============================================================

for week_index, week in enumerate(weeks):

    for day_index, day in enumerate(week["contributionDays"]):

        count = day["contributionCount"]

        x = START_X + week_index * (CELL + GAP)
        y = START_Y + day_index * (CELL + GAP)

        # 🎀 Pink contribution palette

        if count == 0:
            color = "#21262d"

        elif count <= 2:
            color = "#ffd6e8"

        elif count <= 5:
            color = "#ffadd2"

        elif count <= 9:
            color = "#ff69b4"

        else:
            color = "#d946ef"

        cells.append(
            f'''
            <rect
                x="{x}"
                y="{y}"
                width="{CELL}"
                height="{CELL}"
                rx="3"
                fill="{color}"
            />
            '''
        )

# ============================================================
# RACING TRACK
# ============================================================

TRACK_Y = 255

TRACK_START = 55
TRACK_END = 875

race_path = f"""
M {TRACK_START} {TRACK_Y}

C 160 220,
  250 290,
  355 250

S 540 215,
  630 255

S 770 290,
  {TRACK_END} {TRACK_Y}
"""

# ============================================================
# SVG
# ============================================================

svg = f"""
<svg
xmlns="http://www.w3.org/2000/svg"
width="{WIDTH}"
height="{HEIGHT}"
viewBox="0 0 {WIDTH} {HEIGHT}">

<defs>

    <!-- 🎀 Pink Glow -->

    <filter
        id="pinkGlow"
        x="-100%"
        y="-100%"
        width="300%"
        height="300%">

        <feGaussianBlur
            stdDeviation="4"
            result="blur"
        />

        <feMerge>

            <feMergeNode in="blur"/>

            <feMergeNode in="SourceGraphic"/>

        </feMerge>

    </filter>


    <!-- 🎀 Title Gradient -->

    <linearGradient
        id="titleGradient"
        x1="0%"
        x2="100%">

        <stop
            offset="0%"
            stop-color="#ff69b4"
        />

        <stop
            offset="50%"
            stop-color="#ffc0df"
        />

        <stop
            offset="100%"
            stop-color="#c084fc"
        />

    </linearGradient>


    <!-- 🏎️ Car Racing Path -->

    <path
        id="racePath"
        d="{race_path}"
        fill="none"
    />

</defs>


<!-- ===================================================== -->
<!-- BACKGROUND -->
<!-- ===================================================== -->

<rect
    width="930"
    height="335"
    rx="20"
    fill="#0d1117"
/>


<!-- ===================================================== -->
<!-- DECORATIVE STARS -->
<!-- ===================================================== -->

<g fill="#ffb6d9">

    <text x="35" y="45" font-size="16">✦</text>

    <text x="875" y="48" font-size="19">✦</text>

    <text x="75" y="300" font-size="12">♡</text>

    <text x="840" y="305" font-size="13">♡</text>

</g>


<!-- ===================================================== -->
<!-- TITLE -->
<!-- ===================================================== -->

<text
    x="465"
    y="38"
    text-anchor="middle"
    font-family="Arial, Helvetica, sans-serif"
    font-size="24"
    font-weight="bold"
    fill="url(#titleGradient)">

    PALAK'S GITHUB GRAND PRIX

</text>


<!-- ===================================================== -->
<!-- DRIVER INFORMATION -->
<!-- ===================================================== -->

<text
    x="465"
    y="64"
    text-anchor="middle"
    font-family="monospace"
    font-size="12"
    fill="#8b949e">

    DRIVER: @Palak0026  •  CODE SEASON {datetime.now().year}

</text>


<!-- ===================================================== -->
<!-- CONTRIBUTION TOTAL -->
<!-- ===================================================== -->

<text
    x="465"
    y="84"
    text-anchor="middle"
    font-family="monospace"
    font-size="12"
    fill="#ffb6d9">

    {total} CONTRIBUTIONS • FUELED BY CODE &amp; CAFFEINE

</text>


<!-- ===================================================== -->
<!-- REAL CONTRIBUTION GRID -->
<!-- ===================================================== -->

{"".join(cells)}


<!-- ===================================================== -->
<!-- RACE TRACK GLOW -->
<!-- ===================================================== -->

<path
    d="{race_path}"
    fill="none"
    stroke="#ff69b4"
    stroke-width="23"
    stroke-linecap="round"
    opacity="0.12"
    filter="url(#pinkGlow)"
/>


<!-- ===================================================== -->
<!-- MAIN ROAD -->
<!-- ===================================================== -->

<path
    d="{race_path}"
    fill="none"
    stroke="#30363d"
    stroke-width="17"
    stroke-linecap="round"
/>


<!-- ===================================================== -->
<!-- PINK ROAD BORDER -->
<!-- ===================================================== -->

<path
    d="{race_path}"
    fill="none"
    stroke="#ff69b4"
    stroke-width="2"
    stroke-linecap="round"
/>


<!-- ===================================================== -->
<!-- ROAD MARKINGS -->
<!-- ===================================================== -->

<path
    d="{race_path}"
    fill="none"
    stroke="#ffd6e8"
    stroke-width="2"
    stroke-dasharray="10 12"
    opacity="0.85"
/>


<!-- ===================================================== -->
<!-- START / FINISH FLAG -->
<!-- ===================================================== -->

<g transform="translate(47 218)">

    <!-- pole -->

    <rect
        x="0"
        y="0"
        width="4"
        height="45"
        rx="2"
        fill="#ffffff"
    />

    <!-- checkerboard -->

    <rect
        x="4"
        y="0"
        width="10"
        height="10"
        fill="#ffffff"
    />

    <rect
        x="14"
        y="0"
        width="10"
        height="10"
        fill="#ff69b4"
    />

    <rect
        x="4"
        y="10"
        width="10"
        height="10"
        fill="#ff69b4"
    />

    <rect
        x="14"
        y="10"
        width="10"
        height="10"
        fill="#ffffff"
    />

    <rect
        x="4"
        y="20"
        width="10"
        height="10"
        fill="#ffffff"
    />

    <rect
        x="14"
        y="20"
        width="10"
        height="10"
        fill="#ff69b4"
    />

</g>


<!-- ===================================================== -->
<!-- 🏎️ ANIMATED F1 CAR -->
<!-- ===================================================== -->

<g>


    <!-- glow -->

    <circle
        cx="0"
        cy="0"
        r="18"
        fill="#ff69b4"
        opacity="0.20"
        filter="url(#pinkGlow)"
    />


    <!-- car -->

    <g transform="scale(1.15)">


        <!-- Rear Wing -->

        <rect
            x="-21"
            y="-10"
            width="6"
            height="20"
            rx="2"
            fill="#ffc0df"
        />


        <!-- Main Body -->

        <path
            d="
            M -16 -7
            L 4 -7
            L 14 -5
            L 22 -2
            L 26 0
            L 22 2
            L 14 5
            L 4 7
            L -16 7
            Z"
            fill="#ff69b4"
        />


        <!-- Nose -->

        <path
            d="
            M 20 -3
            L 31 -1
            L 31 1
            L 20 3
            Z"
            fill="#ffc0df"
        />


        <!-- Front Wing -->

        <rect
            x="27"
            y="-10"
            width="4"
            height="20"
            rx="2"
            fill="#ffb6d9"
        />


        <!-- Cockpit -->

        <ellipse
            cx="2"
            cy="0"
            rx="6"
            ry="4"
            fill="#111827"
        />


        <!-- Driver helmet -->

        <circle
            cx="2"
            cy="0"
            r="2"
            fill="#ffffff"
        />


        <!-- Rear Wheels -->

        <rect
            x="-13"
            y="-12"
            width="8"
            height="5"
            rx="2"
            fill="#ffffff"
        />

        <rect
            x="-13"
            y="7"
            width="8"
            height="5"
            rx="2"
            fill="#ffffff"
        />


        <!-- Front Wheels -->

        <rect
            x="11"
            y="-11"
            width="7"
            height="5"
            rx="2"
            fill="#ffffff"
        />

        <rect
            x="11"
            y="6"
            width="7"
            height="5"
            rx="2"
            fill="#ffffff"
        />


        <!-- Cute heart -->

        <text
            x="-8"
            y="4"
            font-size="9"
            fill="#ffffff">

            ♡

        </text>


    </g>


    <!-- ================================================= -->
    <!-- CAR MOVEMENT -->
    <!-- ================================================= -->

    <animateMotion
        dur="7s"
        repeatCount="indefinite"
        rotate="auto">

        <mpath href="#racePath"/>

    </animateMotion>


</g>


<!-- ===================================================== -->
<!-- FINISH TEXT -->
<!-- ===================================================== -->

<text
    x="465"
    y="315"
    text-anchor="middle"
    font-family="monospace"
    font-size="12"
    fill="#ffb6d9">

    CODE • COMMIT • RACE • REPEAT ♡

</text>


</svg>
"""

# ============================================================
# SAVE
# ============================================================

os.makedirs("dist", exist_ok=True)

output = "dist/github-contribution-racer.svg"

with open(output, "w", encoding="utf-8") as file:
    file.write(svg)

print("🏁 PALAK'S GITHUB GRAND PRIX GENERATED!")
print(f"🏎️ Driver: @{USERNAME}")
print(f"💗 Contributions: {total}")
print(f"📁 Output: {output}")
