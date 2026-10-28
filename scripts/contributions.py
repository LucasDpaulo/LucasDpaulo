import json
import subprocess
from pathlib import Path

query = '{ user(login: "LucasDpaulo") { contributionsCollection { contributionCalendar { totalContributions weeks { contributionDays { contributionCount contributionLevel date weekday } } } } } }'
data = json.loads(subprocess.check_output(['gh', 'api', 'graphql', '-f', 'query=' + query]))
calendar = data['data']['user']['contributionsCollection']['contributionCalendar']
weeks = calendar['weeks']
width = len(weeks) * 13 + 8
colors = {'NONE': '#161b22', 'FIRST_QUARTILE': '#0e4429', 'SECOND_QUARTILE': '#006d32', 'THIRD_QUARTILE': '#26a641', 'FOURTH_QUARTILE': '#39d353'}
parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="114" viewBox="0 0 {width} 114" role="img" aria-labelledby="title">', '<title id="title">GitHub contributions over the past year</title>', '<style>.week{animation:load 700ms ease-out both;animation-delay:calc(var(--i)*22ms)}@keyframes load{from{opacity:0;transform:translateY(5px)}to{opacity:1;transform:translateY(0)}}@media(prefers-reduced-motion:reduce){.week{animation:none}}</style>']
for index, week in enumerate(weeks):
    parts.append(f'<g class="week" style="--i:{index}">')
    for day in week['contributionDays']:
        x, y = index * 13 + 4, day['weekday'] * 13 + 4
        color = colors[day['contributionLevel']]
        parts.append(f'<rect x="{x}" y="{y}" width="10" height="10" rx="2" fill="{color}"><title>{day["date"]}: {day["contributionCount"]} contributions</title></rect>')
    parts.append('</g>')
parts.append('<text x="4" y="109" font-family="Arial,sans-serif" font-size="10" fill="#8b949e">Contributions · last 12 months</text>')
parts.append('</svg>')
target = Path(__file__).resolve().parent.parent / 'assets' / 'contributions.svg'
target.parent.mkdir(exist_ok=True)
target.write_text('\n'.join(parts) + '\n')
print('Contribution graph generated:', len(weeks), 'weeks')
