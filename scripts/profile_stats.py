import json,subprocess
from pathlib import Path
from xml.sax.saxutils import escape
q='{user(login:"LucasDpaulo"){contributionsCollection{totalCommitContributions totalIssueContributions totalPullRequestContributions totalRepositoriesWithContributedCommits}repositories(first:100,ownerAffiliations:OWNER,privacy:PUBLIC,isFork:false){nodes{stargazerCount languages(first:10,orderBy:{field:SIZE,direction:DESC}){edges{size node{name color}}}}}}}'
u=json.loads(subprocess.check_output(['gh','api','graphql','-f','query='+q]))['data']['user'];c=u['contributionsCollection'];repos=u['repositories']['nodes']
base=Path(__file__).resolve().parent.parent/'assets';base.mkdir(exist_ok=True)
def wrap(body,title):return '<svg xmlns="http://www.w3.org/2000/svg" width="460" height="240" viewBox="0 0 460 240" role="img"><title>'+title+'</title><rect x="1" y="1" width="458" height="238" rx="9" fill="#272833" stroke="#383a48"/><g font-family="Arial,sans-serif">'+body+'</g></svg>'
b='<text x="22" y="32" fill="#ff6188" font-size="17" font-weight="700">Lucas · GitHub Stats</text>'
rows=[('Estrelas em repositórios públicos',sum(r['stargazerCount'] for r in repos)),('Commits · últimos 12 meses',c['totalCommitContributions']),('Pull requests · últimos 12 meses',c['totalPullRequestContributions']),('Issues · últimos 12 meses',c['totalIssueContributions']),('Repositórios com contribuições · 12 meses',c['totalRepositoriesWithContributedCommits'])]
for i,(label,value) in enumerate(rows):
 y=68+i*32;b+=f'<circle cx="25" cy="{y-5}" r="3" fill="#e6db74"/><text x="39" y="{y}" fill="#e6edf3" font-size="12">{label}</text><text x="430" y="{y}" text-anchor="end" fill="#e6db74" font-size="14" font-weight="700">{value:,}</text>'
(base/'stats.svg').write_text(wrap(b,'Estatísticas públicas do GitHub de Lucas'))
langs={};colors={}
for r in repos:
 for edge in r['languages']['edges']:
  name=edge['node']['name'];langs[name]=langs.get(name,0)+edge['size'];colors[name]=edge['node']['color'] or '#8b949e'
total=sum(langs.values()) or 1;top=sorted(langs,key=langs.get,reverse=True)[:6]
b='<text x="22" y="32" fill="#ff6188" font-size="17" font-weight="700">Linguagens nos repositórios públicos</text>';x=22
for name in top:
 w=416*langs[name]/total;b+=f'<rect x="{x:.2f}" y="53" width="{w:.2f}" height="12" fill="{colors[name]}"/>';x+=w
for i,name in enumerate(top):
 col=i%2;row=i//2;x=22+col*215;y=101+row*35
 b+=f'<circle cx="{x+4}" cy="{y-4}" r="5" fill="{colors[name]}"/><text x="{x+17}" y="{y}" fill="#e6edf3" font-size="12">{escape(name)} · {100*langs[name]/total:.1f}%</text>'
b+='<text x="22" y="222" fill="#8b949e" font-size="10">Distribuição por bytes de código · forks excluídos</text>'
(base/'languages.svg').write_text(wrap(b,'Distribuição de linguagens nos repositórios públicos'))
print('Cards gerados com dados da API do GitHub.')
