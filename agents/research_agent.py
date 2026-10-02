class ResearchAgent:
    def __init__(self,client=None): self.client=client
    def run(self,company,role,enabled=True):
        if not enabled or not company:return {'enabled':False,'company':company or '','role':role,'sources':[]}
        return {'enabled':True,'company':company,'role':role,'sources':[],'note':'External research adapter is isolated and can be added without changing candidate evidence.'}
