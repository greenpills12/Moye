import numpy as np, wave
SR=44100; D=15; N=SR*D; out=np.zeros(N)
def note(f,t0,dur,vol,kind='sq',duty=.5):
    a=int(t0*SR); n=int(dur*SR); t=np.arange(n)/SR
    if kind=='sq': w=np.where((t*f)%1<duty,1,-1.)
    elif kind=='tri': w=2*np.abs(2*((t*f)%1)-1)-1
    else: w=np.sin(2*np.pi*f*t)
    env=np.minimum(1,t/0.005)*np.exp(-t*3/dur)
    b=min(n,N-a); out[a:a+b]+=(w*env*vol)[:b]
m=lambda k:440*2**((k-69)/12)
bpm=112; beat=60/bpm; s16=beat/4
chords=[[57,60,64],[53,57,60],[48,52,55],[55,59,62]]  # Am F C G
# intro pad (0-5.5): sparse twinkle
for i in range(int(5.5/(beat/2))):
    c=chords[(i//8)%4]; note(m(c[i%3]+24),i*beat/2,0.4,.05,'sine')
# from 5.5: arp + bass build
t=5.4; i=0
while t<14.2:
    c=chords[int((t-5.4)//(beat*4))%4]
    note(m(c[i%3]+12+12*(i%4==3)),t,s16*1.6,.07,'sq',.25)
    if i%4==0: note(m(c[0]-12),t,beat*.9,.16,'tri')
    t+=s16; i+=1
# riser into title lock
for k in range(24): note(m(60+k),7.3+k*0.055,0.08,.03+.002*k,'sq',.125)
# lock-in hit at 8.7
note(m(45),8.7,1.5,.25,'tri'); [note(m(p),8.7,2.2,.07,'sq',.5) for p in (69,72,76,81)]
# PRESS START chime
for j,p in enumerate((84,88,91,96)): note(m(p),10.8+j*0.07,0.5,.07,'sq',.25)
# noise sweep
nz=np.random.default_rng(1).uniform(-1,1,int(1.4*SR))*np.linspace(0,1,int(1.4*SR))**2*.05; a=int(7.3*SR); out[a:a+len(nz)]+=nz
fade=np.ones(N); fl=int(1.2*SR); fade[-fl:]=np.linspace(1,.02,fl); fi=int(.4*SR); fade[:fi]=np.linspace(0,1,fi)
out+=np.random.default_rng(2).normal(0,2e-4,N); out*=fade; out/=np.max(np.abs(out))*1.25
s=(np.stack([out,out],1)*32767).astype('<i2')
with wave.open('mix.wav','wb') as w: w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes(s.tobytes())
