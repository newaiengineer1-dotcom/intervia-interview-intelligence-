import io
from datetime import datetime
try:
 from reportlab.lib.pagesizes import A4
 from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer
 from reportlab.lib.styles import getSampleStyleSheet
except Exception:A4=SimpleDocTemplate=Paragraph=Spacer=getSampleStyleSheet=None
def build_pdf_report(items):
 if not A4:return None
 b=io.BytesIO();d=SimpleDocTemplate(b,pagesize=A4,rightMargin=40,leftMargin=40);s=getSampleStyleSheet();story=[Paragraph('Intervia — Interview Intelligence Report',s['Title']),Spacer(1,8),Paragraph(datetime.now().strftime('%Y-%m-%d %H:%M'),s['Normal']),Spacer(1,12)]
 for i,x in enumerate(items,1):
  e=x.get('evaluation',{});story += [Paragraph(f'Question {i}',s['Heading2']),Paragraph(x.get('question',''),s['Normal']),Spacer(1,4),Paragraph('<b>Answer:</b> '+x.get('answer',''),s['Normal']),Spacer(1,4),Paragraph(f"<b>Score:</b> {e.get('score','N/A')} | <b>Completeness:</b> {e.get('completeness','N/A')}",s['Normal']),Spacer(1,4),Paragraph('<b>Improvements:</b> '+'; '.join(e.get('improvements',[])),s['Normal']),Spacer(1,10)]
 d.build(story);b.seek(0);return b.getvalue()
