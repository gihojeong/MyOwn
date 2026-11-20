import json,glob,re
def load(root='/home/user/MyOwn/hbm_quiz/data'):
    out=[]
    for f in sorted(glob.glob(root+'/[0-9]*.json')):
        d=json.load(open(f))
        for q in d['questions']:
            q=dict(q); q['_d']=d['code']
            core=q.get('stem') if q.get('stem') is not None else q.get('qt','')
            q['_core']=core or ''
            q['exp']=re.sub(r'\s*\[근거\].*$','',q.get('exp',''),flags=re.S)
            q['_full']=' '.join([q.get('title',''),q.get('ctx','') or '',q['_core'],' '.join(q.get('opts',[])),q.get('exp','')])
            out.append(q)
    return out
