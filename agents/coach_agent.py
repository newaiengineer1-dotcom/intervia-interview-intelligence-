import json,re
class PerformanceCoachAgent:
    def __init__(self,client):self.client=client
    def evaluate(self,question,answer,role,jd_text):
        system='''You are an interview performance coach. Evaluate only the supplied answer. Never invent candidate facts. Return JSON only with score, completeness, strengths, improvements, better_answer, follow_up.'''
        user=f'ROLE:{role}\nJOB:{jd_text[:7000]}\nQUESTION:{question}\nANSWER:{answer[:8000]}'
        try:
            r=self.client.chat.completions.create(model='openai/gpt-oss-20b',messages=[{'role':'system','content':system},{'role':'user','content':user}],temperature=.2,max_tokens=1000)
            raw=re.sub(r'^```json\s*|\s*```$','',r.choices[0].message.content.strip(),flags=re.I);return json.loads(raw)
        except Exception:
            w=len(answer.split());return {'score':min(100,max(30,40+w//3)),'completeness':min(100,w*2),'strengths':['A direct response was provided.'],'improvements':['Add situation, action and result where applicable.'],'better_answer':'Structure the response around situation, action and result without adding unsupported facts.','follow_up':'What was the measurable outcome?'}
