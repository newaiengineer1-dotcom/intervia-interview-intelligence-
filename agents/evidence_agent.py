import re
class EvidenceAgent:
    def build(self,resume_text,jd_text,target_role):
        return {'candidate_facts':re.sub(r'\s+',' ',resume_text or '').strip()[:12000],'job_requirements':re.sub(r'\s+',' ',jd_text or '').strip()[:12000],'target_role':target_role,'policy':'Never invent candidate facts.'}
