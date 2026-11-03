"""CareBand3 live Adzuna API proxy. Set ADZUNA_APP_ID and ADZUNA_APP_KEY."""
import os,json,re,urllib.parse,urllib.request,datetime
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
ROOT=Path(__file__).resolve().parent
TERMS=['healthcare assistant','senior healthcare assistant','healthcare support worker','senior clinical support worker','nursing assistant']
class Handler(SimpleHTTPRequestHandler):
 def __init__(self,*a,**kw):super().__init__(*a,directory=str(ROOT),**kw)
 def do_GET(self):
  if urllib.parse.urlsplit(self.path).path!='/api/jobs':return super().do_GET()
  params=urllib.parse.parse_qs(urllib.parse.urlsplit(self.path).query)
  app_id=os.getenv('ADZUNA_APP_ID');key=os.getenv('ADZUNA_APP_KEY')
  if not app_id or not key:return self.send_json({'error':'API credentials not configured','jobs':[]},503)
  q=params.get('q',[''])[0].strip()[:90];where=params.get('where',[''])[0].strip()[:60]
  search=q or 'healthcare assistant'
  args={'app_id':app_id,'app_key':key,'results_per_page':50,'what':search,'content-type':'application/json','sort_by':'date'}
  if where:args['where']=where
  url='https://api.adzuna.com/v1/api/jobs/gb/search/1?'+urllib.parse.urlencode(args)
  try:
   req=urllib.request.Request(url,headers={'User-Agent':'CareBand3/1.0','Accept':'application/json'})
   with urllib.request.urlopen(req,timeout=18) as response: data=json.load(response) 
   jobs=[]
   for j in data.get('results',[]):
    title=j.get('title','')
    description=j.get('description','')
    if not any(t in title.lower() for t in TERMS):
     continue
    band3 = True
    link=j.get('redirect_url','')
    if not link.startswith('https://'):
     continue
    salary=('£{:,.0f}–£{:,.0f}'.format(j['salary_min'],j['salary_max']) if j.get('salary_min') and j.get('salary_max') else 'See advert')
    jobs.append({'id':j.get('id'),'title':title,'employer':j.get('company',{}).get('display_name','Employer not specified'),'location':j.get('location',{}).get('display_name','UK'),'salary':salary,'created':j.get('created',''),'apply_url':link,'band':'3','source':'Adzuna'})
   return self.send_json({'jobs':jobs,'count':len(jobs),'source':'Adzuna'})
  except Exception as e:
    print(f"Adzuna API error: {type(e).__name__}: {e}", flush=True)
    return self.send_json({
        'error': 'Live job service unavailable',
        'jobs': []
    }, 502)
 def send_json(self,data,status=200):
  payload=json.dumps(data).encode();self.send_response(status);self.send_header('Content-Type','application/json; charset=utf-8');self.send_header('Content-Length',str(len(payload)));self.send_header('Cache-Control','no-store');self.end_headers();self.wfile.write(payload)
if __name__=='__main__':
 port=int(os.getenv('PORT','8000'));print('CareBand3 listening on',port);ThreadingHTTPServer(('0.0.0.0',port),Handler).serve_forever()
