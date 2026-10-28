import json
import subprocess
from pathlib import Path

query = '{ user(login: "LucasDpaulo") { contributionsCollection { contributionCalendar { totalContributions weeks { contributionDays { contributionCount contributionLevel date weekday } } } } } }'
data = json.loads(subprocess.check_output(['gh', 'api', 'graphql', '-f', 'query=' + query]))
calendar = data['data']['user']['contributionsCollection']['contributionCalendar']
weeks = calendar['weeks']
width = len(weeks) * 13 + 8
colors = {'NONE': '#161b22', 'FIRST_QUARTILE': '#0e4429', 'SECOND_QUARTILE': '#006d32', 'THIRD_QUARTILE': '#26a641', 'FOURTH_QUARTILE': '#39d353'}
parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="95" viewBox="0 0 {width} 95" role="img" aria-labelledby="title">', '<title id="title">GitHub contributions over the past year</title>', '<style>@keyframes load{0%{opacity:.08}10%,72%{opacity:1}88%,100%{opacity:.08}}.week{animation:load 8s ease-in-out infinite}@media(prefers-reduced-motion:reduce){.week{animation:none}}</style>']
for index, week in enumerate(weeks):
    parts.append(f'<g class="week" style="animation-delay:{index * 0.035:.3f}s">')
    for day in week['contributionDays']:
        x, y = index * 13 + 4, day['weekday'] * 13 + 4
        color = colors[day['contributionLevel']]
        parts.append(f'<rect x="{x}" y="{y}" width="10" height="10" rx="2" fill="{color}"><title>{day["date"]}: {day["contributionCount"]} contributions</title></rect>')
    parts.append('</g>')
parts.append('</svg>')
target = Path(__file__).resolve().parent.parent / 'assets' / 'contributions.svg'
target.parent.mkdir(exist_ok=True)
target.write_text('\n'.join(parts) + '\n')
print('Contribution graph generated:', len(weeks), 'weeks')
