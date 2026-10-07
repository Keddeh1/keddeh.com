from pathlib import Path
from bs4 import BeautifulSoup
import json,sys
root=Path(__file__).resolve().parents[1]
manifest=json.loads((root/'public/route-manifest.json').read_text())
routes={r['path'] for r in manifest['routes']}
errors=[];controls=0;links=0
for r in manifest['routes']:
 p=r['path'];file=root/'public'/('index.html' if p=='/' else p.strip('/')+'/index.html');soup=BeautifulSoup(file.read_text(),'html.parser')
 def err(msg):errors.append(f'{p}: {msg}')
 if soup.html.get('lang')!='en':err('missing html lang')
 if len(soup.find_all('h1'))!=1:err('must have exactly one h1')
 if not soup.find('main',id='main'):err('missing main#main')
 if not soup.find('nav',attrs={'aria-label':'Main navigation'}):err('missing named main nav')
 if not soup.find('a',class_='skip'):err('missing skip link')
 if not soup.find('meta',attrs={'name':'description'}):err('missing description')
 if not soup.find('link',rel='canonical'):err('missing canonical')
 if 'focus-visible' not in soup.style.get_text():err('missing focus-visible style')
 if 'prefers-reduced-motion' not in soup.style.get_text():err('missing reduced-motion CSS')
 for a in soup.find_all('a',href=True):
  links+=1;href=a['href']
  if href=='#':err('placeholder href #')
  if href.startswith('/') and not href.startswith('/api/'):
   dest=href.split('#')[0]
   if dest not in routes and (dest.rstrip('/') or '/') not in routes and (dest.rstrip('/')+'/') not in routes:err(f'broken internal link {href}')
 for el in soup.select('button,input,select,textarea,summary,a'):
  controls+=1
  if el.name=='button' and not el.get('type'):err('button missing type')
 for inp in soup.select('input:not([type="checkbox"]),select,textarea'):
  if not inp.get('id') or not soup.find('label',attrs={'for':inp.get('id')}):err(f'unlabelled field {inp.name}#{inp.get("id")}')
 if p=='/learn':
  if not soup.find('form',attrs={'data-interest-form':True}):err('learning form missing')
  if not soup.find(attrs={'role':'status','aria-live':'polite'}):err('form status announcement missing')
 if p=='/site-map' and len(soup.select('.directory a'))<len(routes):err('site-map does not expose all routes')
print(json.dumps({'routes':len(routes),'links':links,'controls':controls,'errors':errors},indent=2))
if errors:sys.exit(1)
