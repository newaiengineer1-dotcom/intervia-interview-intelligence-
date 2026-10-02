import time, streamlit as st
from agents import EvidenceAgent,ResearchAgent,StrategyAgent,InterviewerAgent,PerformanceCoachAgent
from utils import CATEGORIES,DURATION_TARGETS,extract_uploaded_text,get_groq_client
from report import build_pdf_report
st.set_page_config(page_title='Intervia | Interview Intelligence',page_icon='🎯',layout='wide',initial_sidebar_state='expanded')
st.markdown('''<style>
.block-container{max-width:1480px;padding:1.2rem 2rem 3rem}.hero{padding:1.7rem 2rem;border:1px solid rgba(148,163,184,.2);border-radius:24px;background:linear-gradient(135deg,rgba(79,70,229,.2),rgba(15,23,42,.75));margin-bottom:1rem}.hero h1{margin:0;font-size:2.5rem;letter-spacing:-.04em}.hero p{color:#94a3b8}.question-card{padding:1.5rem;border:1px solid rgba(99,102,241,.35);border-radius:20px;background:linear-gradient(135deg,rgba(99,102,241,.14),rgba(15,23,42,.3));font-size:1.18rem;line-height:1.6}.badge{display:inline-block;padding:.28rem .65rem;border-radius:999px;border:1px solid rgba(148,163,184,.2);font-size:.82rem;margin-right:.35rem}
</style>''',unsafe_allow_html=True)
defaults={'started':False,'current_question':{},'answers':[],'session_start':None,'session_duration':60,'question_mode':'Text Questions','answer_mode':'Type Answers','category':CATEGORIES[0],'resume_text':'','jd_text':'','evidence':{},'research':{},'plan':{},'transcript':''}
for k,v in defaults.items():
 if k not in st.session_state:st.session_state[k]=v
client=get_groq_client()
st.markdown('''<div class="hero"><h1>🎯 Intervia</h1><p>Evidence-Grounded Adaptive Interview Intelligence</p><span class="badge">5-Agent Architecture</span><span class="badge">Text + Voice</span><span class="badge">Adaptive Sessions</span><span class="badge">PDF Reporting</span></div>''',unsafe_allow_html=True)
if not client:st.warning('GROQ_API_KEY is not configured. Add it in Streamlit Cloud → Manage app → Settings → Secrets.')
with st.sidebar:
 st.header('Candidate & Role')
 role=st.text_input('Target Role','Renewable Energy Engineer')
 company=st.text_input('Company / Track','',placeholder='Optional')
 resume=st.file_uploader('CV / Resume',type=['pdf','txt'])
 jd=st.file_uploader('Job Description',type=['pdf','txt'])
 if resume:st.session_state.resume_text=extract_uploaded_text(resume)
 if jd:st.session_state.jd_text=extract_uploaded_text(jd)
 st.divider();st.header('Interview Setup')
 mode_tab,evidence_tab=st.tabs(['🎛 Interview Categories & Mode','📚 Evidence'])
 with mode_tab:
  category=st.selectbox('Interview Category',CATEGORIES)
  duration=st.select_slider('Session Duration',options=[30,60,120,180],value=60,format_func=lambda x:f'{x} minutes • ~{DURATION_TARGETS[x]} questions')
  qmode=st.radio('Generated Question',['Text Questions','Audio Questions'],horizontal=True)
  amode=st.radio('Candidate Answer',['Type Answers','Speak Answers'],horizontal=True)
 with evidence_tab:
  st.caption('Candidate evidence is kept separate from optional company research.')
  st.write('Resume: '+('Loaded' if st.session_state.resume_text else 'Not uploaded'))
  st.write('Job Description: '+('Loaded' if st.session_state.jd_text else 'Not uploaded'))
 st.caption('Industry field removed. Role, CV, JD and optional company track drive the interview.')
a,b=st.columns(2)
with a:start=st.button('🚀 Start / Restart Interview',type='primary',use_container_width=True)
with b:reset=st.button('↻ Reset Session',use_container_width=True)
if reset:
 st.session_state.started=False;st.session_state.current_question={};st.session_state.answers=[];st.session_state.session_start=None;st.session_state.transcript='';st.rerun()
if start:
 if not client:st.error('GROQ_API_KEY is required.');st.stop()
 st.session_state.update({'session_duration':duration,'question_mode':qmode,'answer_mode':amode,'category':category,'answers':[],'transcript':'','session_start':time.time()})
 evidence_agent=EvidenceAgent();research_agent=ResearchAgent(client);strategy_agent=StrategyAgent();interviewer=InterviewerAgent(client)
 st.session_state.evidence=evidence_agent.build(st.session_state.resume_text,st.session_state.jd_text,role)
 st.session_state.research=research_agent.run(company,role,bool(company));st.session_state.plan=strategy_agent.create_plan(duration,category)
 st.session_state.current_question=interviewer.ask(st.session_state.evidence,st.session_state.research,st.session_state.plan,role,category,[]);st.session_state.started=True;st.rerun()
if st.session_state.started:
 target=DURATION_TARGETS[st.session_state.session_duration];done=len(st.session_state.answers);elapsed=int(time.time()-st.session_state.session_start);left=max(0,st.session_state.session_duration*60-elapsed)
 m1,m2,m3,m4=st.columns(4);m1.metric('Questions',f'{done}/{target}');m2.metric('Time Left',f'{left//60:02d}:{left%60:02d}');m3.metric('Category',st.session_state.category.split(' ')[0]);m4.metric('Mode',st.session_state.question_mode.replace(' Questions',''));st.progress(min(1,done/target))
 q=st.session_state.current_question;st.markdown(f'<div class="question-card"><strong>Question {done+1}</strong><br><br>{q.get("question","")}</div>',unsafe_allow_html=True);st.caption(f"Difficulty: {q.get('difficulty','Medium')} · {q.get('why','Role-relevant assessment')}")
 if st.session_state.question_mode=='Audio Questions':
  text=(q.get('question','') or '').replace('\\','\\\\').replace("'","\\'");st.components.v1.html(f"<script>if('speechSynthesis' in window){{speechSynthesis.cancel();const u=new SpeechSynthesisUtterance('{text}');u.rate=.95;speechSynthesis.speak(u);}}</script>",height=10)
 answer=''
 if st.session_state.answer_mode=='Type Answers':answer=st.text_area('Your Answer',height=180,key='typed_answer')
 else:
  audio=st.audio_input('🎙 Record your answer')
  if audio and st.button('📝 Transcribe Answer'):
   try:st.session_state.transcript=InterviewerAgent(client).transcribe(audio.getvalue())
   except Exception as e:st.error(f'Transcription failed: {e}')
  answer=st.session_state.transcript
  if answer:st.text_area('Transcribed Answer',value=answer,height=150,disabled=True)
 if st.button('✅ Submit Answer',type='primary',use_container_width=True):
  if not answer.strip():st.warning('Please provide an answer.')
  else:
   with st.spinner('Analyzing answer...'):evaluation=PerformanceCoachAgent(client).evaluate(q['question'],answer,role,st.session_state.jd_text)
   st.session_state.answers.append({'question':q['question'],'answer':answer,'evaluation':evaluation});st.session_state.transcript=''
   if len(st.session_state.answers)>=target:st.session_state.started=False;st.success('🎉 Target interview session completed.')
   else:
    plan=StrategyAgent().next_plan(st.session_state.plan,len(st.session_state.answers),target,[x['evaluation'].get('score',0) for x in st.session_state.answers]);st.session_state.plan=plan;st.session_state.current_question=InterviewerAgent(client).ask(st.session_state.evidence,st.session_state.research,plan,role,st.session_state.category,[x['question'] for x in st.session_state.answers]);st.rerun()
if st.session_state.answers:
 st.divider();st.subheader('🧠 Performance Intelligence');e=st.session_state.answers[-1]['evaluation'];x,y=st.columns(2);x.metric('Latest Score',e.get('score','N/A'));y.metric('Completeness',e.get('completeness','N/A'));c1,c2=st.columns(2)
 with c1:
  st.markdown('**Strengths**');[st.write('• '+z) for z in e.get('strengths',[])]
 with c2:
  st.markdown('**Improvements**');[st.write('• '+z) for z in e.get('improvements',[])]
 st.markdown('**Practice Answer**');st.info(e.get('better_answer',''));pdf=build_pdf_report(st.session_state.answers)
 if pdf:st.download_button('⬇️ Download Professional PDF Report',pdf,'intervia_interview_report.pdf','application/pdf',use_container_width=True)
