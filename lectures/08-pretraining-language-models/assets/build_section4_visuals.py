"""Create editable SVG-in-HTML teaching diagrams; no model outputs are implied."""
from pathlib import Path
from html import escape
OUT=Path(__file__).parent/'section4-diagrams';OUT.mkdir(exist_ok=True)
def start(name,desc,height=470):
 return [f'<svg class="s4-svg" viewBox="0 0 1280 {height}" role="img" aria-labelledby="s4-{name}-title s4-{name}-desc">',f'<title id="s4-{name}-title">{escape(name)}</title><desc id="s4-{name}-desc">{escape(desc)}</desc>',f'<defs><marker id="s4-{name}-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#0f7881"/></marker></defs>']
def text(s,x,y,t,cl='s4-svg-label',anchor='middle'):s.append(f'<text x="{x}" y="{y}" class="{cl}" text-anchor="{anchor}">{escape(t)}</text>')
def box(s,x,y,w,h,cl='s4-svg-backbone'):s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" class="{cl}"/>')
def line(s,x,y,xx,yy,name=None,cl='s4-svg-line'):
 s.append(f'<path d="M{x} {y}L{xx} {yy}" class="{cl}"'+(f' marker-end="url(#s4-{name}-arrow)"' if name else '')+'/>')
def save(name,s): (OUT/(name+'.html')).write_text('```{=html}\n'+'\n'.join(s+['</svg>'])+'\n```\n')
# Classifier: read final CLS, with all supplied positions informing that state.
name='sentiment';s=start(name,'All input tokens enter a pretrained bidirectional encoder. The final CLS state enters a new two-class head, producing sentiment scores. Other token states are not directly classified.')
xs=[110,285,460,635,810,985,1160]
for x in xs:
 for xx in xs:line(s,x,345,xx,270,cl='s4-svg-attention'+(' s4-svg-focus' if xx==110 else ''))
for x,t in zip(xs,['[CLS]','i','loved','this','movie','.','[SEP]']):
 box(s,x-43,345,86,42);text(s,x,443,t)
 box(s,x-43,228,86,42);text(s,x,218,'h[CLS]' if x==110 else 'hᵢ','s4-svg-small')
line(s,110,228,110,155,name)
box(s,30,73,280,80,'s4-svg-head');text(s,170,108,'NEW sentiment head');text(s,170,137,'W h[CLS] + b','s4-svg-small')
line(s,310,113,490,113,name)
box(s,510,65,260,95,'s4-svg-neutral');text(s,640,102,'negative / positive');text(s,640,138,'two scores → softmax','s4-svg-small')
text(s,1010,93,'Label from annotation','s4-svg-small');text(s,1010,136,'positive','s4-svg-answer')
text(s,780,193,'REUSED: embeddings + contextual layers','s4-svg-small')
text(s,640,410,'Input token representations','s4-svg-small');save(name,s)
# Sentence-pair classifier; all-token visibility, no causal or segment barrier.
name='pair';s=start(name,'A and B enter one bidirectional encoder with separator tokens. Cross-sentence attention contributes to CLS, which a new entailment classifier reads.',430)
for x in xs:
 for xx in xs:line(s,x,296,xx,223,cl='s4-svg-attention'+(' s4-svg-focus' if xx==110 else ''))
for i,(x,t) in enumerate(zip(xs,['[CLS]','A₁','A₂','[SEP]','B₁','B₂','[SEP]'])):
 cl='s4-svg-backbone' if i<4 else 's4-svg-head'
 box(s,x-43,296,86,42,cl);text(s,x,375,t)
 box(s,x-43,181,86,42);text(s,x,170,'h[CLS]' if i==0 else 'hᵢ','s4-svg-small')
line(s,110,181,110,101,name);box(s,30,20,350,80,'s4-svg-head');text(s,205,53,'NEW three-class head');text(s,205,84,'reads h[CLS]','s4-svg-small')
line(s,380,60,480,60,name);text(s,845,50,'entailment · contradiction · neutral','s4-svg-label');text(s,845,88,'One decision about the pair','s4-svg-small')
text(s,640,417,'[SEP] marks a boundary; it does not block attention between A and B.','s4-svg-small');save(name,s)
# QA: every passage state is scored by each shared start/end vector.
name='qa';s=start(name,'The question and passage are jointly encoded. Each passage state feeds the same start and end scoring heads. Start and end distributions select an answer span.',430)
xs=[95,275,455,635,815,995,1175]
for x in xs:
 line(s,x,237,380,155,cl='s4-svg-attention')
 line(s,x,237,900,155,cl='s4-svg-attention s4-svg-end')
 box(s,x-42,237,84,44)
for x,t,i in zip(xs,['Lina','studies','at','New','York','University','.'],range(7)):
 text(s,x,326,t);text(s,x,360,str(i),'s4-svg-small')
box(s,200,55,360,100,'s4-svg-head');text(s,380,92,'START scores');text(s,380,130,'same wₛ applied to each hᵢ','s4-svg-small')
box(s,720,55,360,100,'s4-svg-head');text(s,900,92,'END scores');text(s,900,130,'same wₑ applied to each hᵢ','s4-svg-small')
text(s,640,30,'Question-aware passage states from BERT','s4-svg-small')
text(s,640,403,'Two softmax distributions over passage positions—not over vocabulary words.','s4-svg-small');save(name,s)
# Purposeful bridge: intervention follows an unchanged trained model.
name='bridge';s=start(name,'Three versions of an input pass through the same fixed model. Compare outputs to test what evidence changes a prediction. Moving dots trace the information flow.',440)
rows=[('i loved this movie',105),('i hated this movie',225),('i lovde this movie',345)]
for t,y in rows:
 box(s,20,y-35,380,70,'s4-svg-neutral');text(s,210,y+9,t)
 s.append(f'<path id="s4-probe-path-{y}" d="M400 {y}H520L600 225H900L980 {y}H1175" class="s4-probe-path"/>')
 s.append(f'<circle r="7" class="s4-probe-dot"><animateMotion dur="4s" begin="{-(y-105)/120}s" repeatCount="indefinite" path="M400 {y}H520L600 225H900L980 {y}H1175"/></circle>')
 box(s,1000,y-33,240,66,'s4-svg-neutral');text(s,1120,y+9,'prediction ?')
box(s,550,145,360,160,'s4-svg-model');text(s,730,196,'SAME MODEL','s4-svg-white');text(s,730,239,'weights fixed','s4-svg-white');text(s,730,277,'no new training','s4-svg-white-small')
text(s,210,32,'CHANGE THE INPUT','s4-svg-small');text(s,1120,32,'OBSERVE THE OUTPUT','s4-svg-small');save(name,s)
print(OUT)
