import json,re
class InterviewerAgent:
    def __init__(self,client): self.client=client
    def _call(self,system,user):
        if not self.client: raise RuntimeError('GROQ_API_KEY is not configured.')
        r=self.client.chat.completions.create(model='openai/gpt-oss-20b',messages=[{'role':'system','content':system},{'role':'user','content':user}],temperature=.3,max_tokens=700)
        return r.choices[0].message.content.strip()
    def ask(self,evidence,research,plan,role,category,previous_questions):
        system='''You are an evidence-grounded professional interviewer. Ask exactly ONE concise practical interview question. Never invent candidate facts. Job requirements are not candidate history. Return JSON only: {"question":"...","difficulty":"Easy|Medium|Hard","why":"..."}.'''
        user=f'ROLE:{role}\nCATEGORY:{category}\nPLAN:{json.dumps(plan)}\nEVIDENCE:{json.dumps(evidence)}\nRESEARCH:{json.dumps(research)}\nPREVIOUS:{json.dumps(previous_questions[-8:])}'
        try:
            raw=re.sub(r'^```json\s*|\s*```$','',self._call(system,user),flags=re.I); d=json.loads(raw)
            if d.get('question'):return d
        except Exception:pass
        return {'question':f'Describe a practical situation relevant to {role} where you solved a difficult problem. What did you do and what was the result?','difficulty':plan.get('difficulty','Medium'),'why':'Tests practical role-relevant evidence.'}
    def transcribe(self,audio_bytes):
        r=self.client.audio.transcriptions.create(file=('answer.wav',audio_bytes),model='whisper-large-v3-turbo',response_format='text'); return str(r)
