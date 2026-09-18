"""Render the customer leadership use guide. Requires ReportLab."""
from html import escape
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph

ROOT = Path(__file__).resolve().parents[1]
GREEN = colors.HexColor('#203b38')
MUTED = colors.HexColor('#4e635c')
styles = {
    'title': ParagraphStyle('title', fontName='Times-Roman', fontSize=25, leading=28, textColor=GREEN, spaceAfter=8),
    'subtitle': ParagraphStyle('subtitle', fontName='Helvetica', fontSize=10, leading=13, textColor=MUTED, spaceAfter=17),
    'heading': ParagraphStyle('heading', fontName='Helvetica-Bold', fontSize=11, leading=14, textColor=GREEN, spaceBefore=13, spaceAfter=6, keepWithNext=True),
    'body': ParagraphStyle('body', fontName='Helvetica', fontSize=10, leading=14, textColor=GREEN, spaceAfter=7),
}
blocks = [
('title', 'Using the Magic Notes review'),
('subtitle', 'A short guide for customer leadership | <link href="https://beam-magic-notes-customer-review.streamlit.app/" color="#345f50"><u>Open the interactive review</u></link>'),
('body', 'Use the prototype to choose a focused improvement to test with staff and Beam. The supplied sample combines three local authorities; check whether its findings match your own teams’ experience before setting priorities.'),
('heading', 'Use it to reach a decision'),
('body', 'In a leadership discussion, choose one finding to investigate, identify the staff who can explain it, and agree who will coordinate the work with Beam. Leave with a small review to carry out and a date to discuss the results. The charts help decide where to look; staff examples help establish what needs to change.'),
('heading', 'Why these priorities were selected'),
('body', '<b>Lower ratings give a starting point.</b> Early Help, Mental Health, and Housing average 3.41, 3.55, and 3.71 out of 5. Starting with three keeps the review manageable; it is not a statistical cutoff. Child &amp; Family is close behind at 3.76. Different tasks and small samples mean these figures should not be treated as a ranking of team performance.'),
('body', '<b>Satisfaction can coexist with consequential problems.</b> Seven of fourteen reports about names or risk information accompany 4-5 stars. These concerns were selected because they could affect how a case is understood or acted on, not because they are the most frequent complaints. Overall satisfaction cannot substitute for checking specific inaccuracies. The reports have not been independently verified.'),
('body', '<b>Generation times help set expectations.</b> For recordings over an hour, the median wait was 44 seconds and 90% completed within 66 seconds. These observations can inform staff introductions to Magic Notes. They do not establish that waiting is disruptive, or justify shortening conversations. Explore a change only if staff describe a practical difficulty.'),
('heading', 'Make the follow-up useful'),
('body', 'Review notes with staff and document recurring corrections and missing information. For an agreed sample, capture the template used, the change needed, and editing time. Ask what an acceptable note should contain. This helps Beam distinguish a possible template issue from a need for clearer guidance.'),
('body', 'Before testing improvements, agree an accuracy and completeness checklist and record a baseline. Afterwards, compare editing time and the proportion of notes meeting that same checklist. Keep specific error reports separate from the overall star rating so useful outputs with important mistakes remain visible.'),
('heading', 'Know what the sample can answer'),
('body', 'The extracts contain 200 generation attempts, 150 ratings, and 79 written comments. Some transcripts were used more than once. The comments describe reported experiences; the extracts do not include the original conversations or generated notes needed to verify them. Repeated wording is grouped, with all responses and their ratings retained.'),
('body', 'Timing covers 173 completed attempts. The 15 failed and 12 in-progress attempts are excluded, with no established link to long waits. Generation time does not include staff checking or editing, and is not a measure of time saved. The prototype’s methodology gives the detailed definitions.'),
]
story = [Paragraph(text, styles[kind]) for kind, text in blocks]
def footer(canvas, doc):
    canvas.setStrokeColor(colors.HexColor('#d4ded5'))
    canvas.line(44, 36, A4[0]-44, 36)
    canvas.setFillColor(MUTED)
    canvas.setFont('Helvetica', 8)
    canvas.drawString(44, 24, 'Magic Notes | Customer leadership guide')
    canvas.drawRightString(A4[0]-44, 24, str(doc.page))
out = ROOT/'LEADERSHIP_GUIDE.pdf'
doc=SimpleDocTemplate(str(out),pagesize=A4,leftMargin=44,rightMargin=44,topMargin=38,bottomMargin=48,title='Using the Magic Notes review',author='Rachel Stromberg')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(out)
