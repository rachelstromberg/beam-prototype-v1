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
('body', 'This prototype presents three headline findings from supplied Magic Notes usage and feedback data across three local authorities. It offers focused, interactive views of the evidence and possible improvements for staff and Beam, rather than a walkthrough of the entire dataset.'),
('heading', 'Why these priorities were selected'),
('body', '<b>We selected the three lowest-rated templates as a starting point.</b> Early Help, Mental Health, and Housing average 3.41, 3.55, and 3.71 out of 5. Reviewing three limits how much staff need to take on at once. The ratings show no clear cutoff, so other templates may also need attention. Different tasks and small samples mean these figures should not be treated as a ranking of team performance.'),
('body', '<b>Satisfaction can coexist with consequential problems.</b> Seven of fourteen reports about names or risk information accompany 4-5 stars. These concerns were selected as focus points because they could affect how cases are understood and acted on, not because they are the most frequent complaints. The most common complaints concerned template relevance (9 reports) and excessive length (8). Overall satisfaction cannot substitute for checking specific inaccuracies.'),
('body', '<b>Generation times help set expectations.</b> For recordings over an hour, the median wait was 44 seconds and 90% completed within 66 seconds. These observations can inform staff introductions to Magic Notes. They do not establish that waiting is disruptive, or justify shortening conversations. Explore a change only if staff describe a practical difficulty.'),
('heading', 'Make the follow-up useful'),
('body', 'Review notes with staff and document recurring corrections and missing information. For an agreed sample, capture the template used, the change needed, and editing time. Ask what an acceptable note should contain. This helps Beam distinguish a possible template issue from a need for clearer guidance.'),
('body', 'Before testing improvements, agree on an accuracy and completeness checklist and record a baseline. Afterwards, compare editing time and the proportion of notes meeting that same checklist. Keep specific error reports separate from the overall star rating so useful outputs with important mistakes remain visible.'),
('heading', 'Know what the sample can answer'),
('body', 'The sample points to where to investigate; explaining why problems occur needs staff input and the original conversations and notes. Beyond the three priorities shown, further analysis could explore template relevance, missing context, and unsuccessful generation attempts.'),
('body', 'We also compared ratings by AI model, but each template used only one model. To separate model effects from task differences, Beam could test models on the same transcripts and template tasks, using consistent staff review criteria.'),
('body', 'The extracts contain 200 generation attempts, 150 ratings, and 79 written comments. Timing covers 173 completed attempts and excludes 15 failed and 12 in-progress attempts. It does not include staff checking or editing time. The prototype’s methodology gives the detailed definitions and coverage.'),
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
