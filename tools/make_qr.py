"""Visual emblem QR codes for the workshop page, in the Reopen the Record emblem-QR style."""
import math, numpy as np, qrcode, zxingcpp
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image, ImageDraw, ImageFont
INK=(43,34,28); GOLD=(169,124,46); WHITE=(255,255,255)
F='/usr/share/fonts/truetype/sand-box/google/Cinzel/Cinzel-VariableFont_wght.ttf'

def ship(S):
    im=Image.new('RGBA',(S,S),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.polygon([(S*.10,S*.62),(S*.90,S*.62),(S*.78,S*.80),(S*.22,S*.80)],fill=INK)      # hull
    d.polygon([(S*.08,S*.56),(S*.24,S*.56),(S*.24,S*.64),(S*.10,S*.64)],fill=INK)      # stern castle
    for x,h in ((.36,.42),(.54,.48),(.72,.36)):
        d.rectangle((S*(x-.012),S*(.62-h),S*(x+.012),S*.62),fill=INK)               # masts
        d.polygon([(S*(x-.11),S*(.62-h+.06)),(S*(x+.11),S*(.62-h+.06)),(S*(x+.09),S*(.62-h*.45)),(S*(x-.09),S*(.62-h*.45))],fill=INK)
    for k in range(3):
        y=S*(.86+k*.035); pts=[(x,y+S*.012*math.sin(x/S*18)) for x in np.linspace(S*.08,S*.92,40)]
        d.line(pts,fill=INK,width=max(2,S//90))
    return im

def stars(S):
    im=Image.new('RGBA',(S,S),(0,0,0,0)); d=ImageDraw.Draw(im)
    c=S/2; w=S*.07
    d.rectangle((c-w/2,S*.10,c+w/2,S*.90),fill=INK); d.rectangle((S*.10,c-w/2,S*.90,c+w/2),fill=INK)
    def star(x,y,r):
        p=[]
        for i in range(10):
            a=-math.pi/2+i*math.pi/5; rr=r if i%2==0 else r*.42
            p.append((x+rr*math.cos(a),y+rr*math.sin(a)))
        d.polygon(p,fill=INK); 
    for (x,y,r) in ((c,c,S*.13),(c,S*.18,S*.10),(c,S*.82,S*.10),(S*.18,c,S*.10),(S*.82,c,S*.10)):
        star(x,y,r*1.15)
    return im

def bus(S):
    im=Image.new('RGBA',(S,S),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.rounded_rectangle((S*.06,S*.30,S*.94,S*.70),radius=S*.06,fill=INK)
    for i in range(5):
        x=S*(.12+i*.15); d.rounded_rectangle((x,S*.36,x+S*.11,S*.48),radius=S*.015,fill=WHITE)
    d.rounded_rectangle((S*.84,S*.36,S*.90,S*.60),radius=S*.01,fill=WHITE)   # door
    for cx in (.24,.74):
        d.ellipse((S*(cx-.09),S*.62,S*(cx+.09),S*.80),fill=INK); d.ellipse((S*(cx-.04),S*.67,S*(cx+.04),S*.75),fill=WHITE)
    d.line([(S*.04,S*.84),(S*.96,S*.84)],fill=INK,width=max(2,S//60))
    return im

def lens(S):
    """Magnifying glass over a case-file folder."""
    im=Image.new('RGBA',(S,S),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.polygon([(S*.08,S*.28),(S*.36,S*.28),(S*.42,S*.20),(S*.62,S*.20),(S*.62,S*.28),(S*.92,S*.28),(S*.92,S*.82),(S*.08,S*.82)],fill=INK)
    d.rectangle((S*.14,S*.36,S*.86,S*.76),fill=WHITE)
    for k in range(4): d.rectangle((S*.20,S*(.43+k*.08),S*.62,S*(.46+k*.08)),fill=INK)
    d.ellipse((S*.46,S*.38,S*.80,S*.72),outline=INK,width=int(S*.06))
    d.line([(S*.75,S*.67),(S*.92,S*.86)],fill=INK,width=int(S*.09))
    return im

def make(url,label,em,target=860):
    q=qrcode.QRCode(error_correction=ERROR_CORRECT_H,border=3,box_size=10); q.add_data(url); q.make(fit=True)
    raw=q.make_image(fill_color=INK,back_color=WHITE).convert('RGB'); n=raw.width; W=n*max(1,target//n)
    canvas=raw.resize((W,W),Image.Resampling.NEAREST)
    badge=int(W*260/860); pad=int(badge*22/260)
    field=Image.new('RGBA',(badge,badge),WHITE+(255,)); d=ImageDraw.Draw(field)
    d.rounded_rectangle((1,1,badge-2,badge-2),radius=int(badge*18/260),outline=GOLD,width=max(4,int(badge*4/260)))
    e=em(1200).resize((badge-2*pad,)*2,Image.Resampling.LANCZOS); field.paste(e,(pad,pad),e)
    c=(W-badge)//2; canvas.paste(field.convert('RGB'),(c,c))
    lh=int(W*0.20); out=Image.new('RGB',(W,W+lh),WHITE); out.paste(canvas,(0,0)); d=ImageDraw.Draw(out)
    f1=ImageFont.truetype(F,int(W*0.075)); f1.set_variation_by_axes([700]); f2=ImageFont.truetype(F,int(W*0.034)); f2.set_variation_by_axes([500])
    d.text((W/2,W-int(W*0.01)),label,font=f1,fill=INK,anchor='mt')
    d.text((W/2,W+int(W*0.11)),'Reopen the Record · scan to open',font=f2,fill=GOLD,anchor='mt')
    r=zxingcpp.read_barcodes(out); assert r and r[0].text==url,(url,r)
    small=out.resize((out.width//4,out.height//4)); r=zxingcpp.read_barcodes(small); assert r and r[0].text==url
    return out

if __name__ == '__main__':
  for fn,url,label,em in [
    ('workshop-eureka-qr.png','https://robmac10.github.io/rtr-workshop-eureka/','Eureka Workshop',stars)]:
    make(url,label,em).save('assets/qr/'+fn,optimize=True); print('ok',fn,url)
