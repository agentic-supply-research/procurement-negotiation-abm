"""Extract GLEE negotiation game outcomes from a *locally cloned* GLEE repo.

Example: python code/extract_glee_local.py --glee-dir ~/GLEE --out data/glee_full_extract.csv
This script uses real original source files and does not call any model.
"""
import argparse,csv,json
from pathlib import Path
import pandas as pd

def extract(source:Path,limit:int|None=None):
 out=[]
 for typ,relative in [('H','human_vs_llm'),('A','llm_vs_llm')]:
  paths=sorted((source/'Data'/relative/'negotiation').rglob('game.csv'))
  for p in (paths[:limit] if limit is not None else paths):
   cfg=p.parent/'config.json'
   if not cfg.exists():continue
   try:
    c=json.loads(cfg.read_text(encoding='utf8'))
    with p.open('r',encoding='utf8',newline='') as f: rows=list(csv.DictReader(f))
    d=any(r.get('decision')=='AcceptOffer' for r in rows)
    prices=[float(r['product_price']) for r in rows if r.get('product_price') and r['product_price'].strip()]
    rcount=max([int(r['round']) for r in rows if r.get('round') and r['round'].strip()] or [0])
    args=c['game_args']; order=float(args['product_price_order'])
    out.append({'type':typ,'id':p.parent.name,'buyer':args['buyer_value'],'seller':args['seller_value'],'price':prices[-1]/order if d and prices else None,'rounds':rcount,'deal':int(d),'info':int(bool(args['complete_information'])),'msg':int(bool(args['messages_allowed']))})
   except (ValueError,KeyError,TypeError,UnicodeDecodeError):continue
 return pd.DataFrame(out)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--glee-dir',type=Path,required=True);ap.add_argument('--out',type=Path,default=Path('data/glee_full_extract.csv'));ap.add_argument('--limit-per-group',type=int,default=None)
 a=ap.parse_args();d=extract(a.glee_dir,a.limit_per_group);a.out.parent.mkdir(parents=True,exist_ok=True);d.to_csv(a.out,index=False);print('Extracted',len(d),'games to',a.out)
