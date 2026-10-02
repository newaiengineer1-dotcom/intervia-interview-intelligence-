class StrategyAgent:
    TARGETS={30:8,60:15,120:28,180:40}
    def create_plan(self,duration_minutes,category): return {'duration_minutes':duration_minutes,'target_questions':self.TARGETS.get(duration_minutes,15),'category':category,'difficulty':'Medium','focus':'balanced'}
    def next_plan(self,base_plan,completed,target,scores):
        p=dict(base_plan); avg=sum(scores)/len(scores) if scores else 0
        p['difficulty']='Hard' if avg>=85 else 'Medium'; p['focus']='increase depth' if avg>=85 else ('clarify fundamentals' if avg<60 else 'balanced'); p['remaining_questions']=max(0,target-completed); return p
