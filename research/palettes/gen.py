import json,re,sys
def lum(h):
    h=h.lstrip('#'); r,g,b=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    f=lambda c: c/12.92 if c<=0.03928 else ((c+0.055)/1.055)**2.4
    return 0.2126*f(r)+0.7152*f(g)+0.0722*f(b)
def cr(a,b):
    la,lb=sorted([lum(a),lum(b)],reverse=True); return (la+0.05)/(lb+0.05)
def onfit(c, dark, light):
    return dark if cr(c,dark)>=cr(c,light) else light
P = {
 'A-navy-coral': dict(name='Navy and coral', ink='#0E1A2B', ink2='#16253A', rule='#24364F', rule2='#34496A',
   stock='#F7F2EA', stock2='#E9E1D3', onstock='#141A24', onstock2='#4A5568', onstock3='#626A7B',
   onink='#F7F2EA', onink2='#B8C4D6', onink3='#8C9AB0',
   fit=['#2D3E73','#2F7FA0','#9AB87A','#F2A65A','#E8553E'], signal='#FF8A65', signal2='#F06A43', check='#B39DDB'),
 'B-paper-ink': dict(name='Light paper', ink='#F6F2EA', ink2='#ECE6DA', rule='#DDD4C4', rule2='#C2B7A3',
   stock='#1C1F26', stock2='#2C313B', onstock='#F6F2EA', onstock2='#C9CED8', onstock3='#9AA1AE',
   onink='#1C1F26', onink2='#4A4F5A', onink3='#6B6F78',
   fit=['#3B4A8C','#3C8DAD','#7DB46C','#F0B440','#E2553A'], signal='#2D4BDB', signal2='#2139B0', check='#7E57C2'),
 'C-charcoal-lime': dict(name='Charcoal and lime', ink='#131417', ink2='#1C1E22', rule='#2A2D33', rule2='#3B3F47',
   stock='#F3F3EE', stock2='#E2E2DA', onstock='#15161A', onstock2='#4B4E57', onstock3='#64676F',
   onink='#F3F3EE', onink2='#B9BCC4', onink3='#8E929B',
   fit=['#40307A','#3A63C4','#23A79A','#9BD83A','#D9F55B'], signal='#C8F03C', signal2='#AFD622', check='#C59BFF', hot='#6A4CE0'),
 'D-plum-sunset': dict(name='Plum and sunset', ink='#24122E', ink2='#2F1A3B', rule='#43294F', rule2='#5A3A69',
   stock='#FFF4EA', stock2='#F3E2D3', onstock='#22131F', onstock2='#5C4558', onstock3='#7D6679',
   onink='#FFF4EA', onink2='#D8C2D9', onink3='#AC92AE',
   fit=['#3E3A8F','#7C5CC4','#D262A6','#F4885A','#FFC94D'], signal='#FF5C8A', signal2='#E83F70', check='#8FD3FF', hot='#D6336C'),
}

SEL = ".pk.on{background:var(--signal);color:#fff;border-color:var(--signal)}.pk.on .pk-n{background:#fff;color:var(--signal)}"
P2 = {
 'E-white-cobalt': dict(name='White and cobalt', ink='#FFFFFF', ink2='#F2F5FA', rule='#E2E7EF', rule2='#C3CCDA',
   stock='#EEF3FB', stock2='#DCE5F3', onstock='#111A2E', onstock2='#46506A', onstock3='#5E6880',
   onink='#111A2E', onink2='#46506A', onink3='#5E6880',
   fit=['#D6E1F5','#9DB9EC','#5E8DE2','#2C62D6','#0F37A8'], signal='#1F4FE0', signal2='#173DB3', check='#7C4DDB', hot='#1F4FE0', extra=SEL),
 'F-white-navy': dict(name='White with navy cards', ink='#FFFFFF', ink2='#F3F5F9', rule='#E3E7EE', rule2='#C6CEDB',
   stock='#0F2347', stock2='#1C3561', onstock='#FFFFFF', onstock2='#C3CEE3', onstock3='#9AA9C6',
   onink='#0F2347', onink2='#44506A', onink3='#5D6882',
   fit=['#1E2F63','#2F5FB3','#4C9AD8','#93CBE8','#F2C94C'], signal='#2563EB', signal2='#1D4FC4', check='#8B5CF6', hot='#E2571E'),
 'G-ice-blue': dict(name='Ice blue', ink='#EAF2FB', ink2='#DCE8F6', rule='#C9D9EC', rule2='#A9BFDB',
   stock='#FFFFFF', stock2='#E8EEF6', onstock='#0E1B33', onstock2='#43506B', onstock3='#5C6884',
   onink='#0E1B33', onink2='#3E4B66', onink3='#55627E',
   fit=['#C9D6E6','#8EAED6','#4F86D6','#2457C5','#0A2F8F'], signal='#1D4ED8', signal2='#163DAE', check='#7C3AED', hot='#1D4ED8', extra=SEL),
 'H-blue-white-sun': dict(name='Blue, white and sun', ink='#FFFFFF', ink2='#F4F6FB', rule='#E4E8F0', rule2='#C8D0DE',
   stock='#F4F7FC', stock2='#E2E9F4', onstock='#0D1A30', onstock2='#45526B', onstock3='#5D6983',
   onink='#0D1A30', onink2='#45526B', onink3='#5D6983',
   fit=['#2B3A6B','#3566C9','#45A6E0','#9DD9D2','#FFC83D'], signal='#0B5CFF', signal2='#0047D1', check='#7C3AED', hot='#0B5CFF', extra=SEL),
}

def css(p):
    d,l='#14161B','#FFFFFF'
    lines=[f"--ink:{p['ink']}",f"--ink-2:{p['ink2']}",f"--rule:{p['rule']}",f"--rule-2:{p['rule2']}",
     f"--stock:{p['stock']}",f"--stock-2:{p['stock2']}",f"--on-stock:{p['onstock']}",f"--on-stock-2:{p['onstock2']}",f"--on-stock-3:{p['onstock3']}",
     f"--on-ink:{p['onink']}",f"--on-ink-2:{p['onink2']}",f"--on-ink-3:{p['onink3']}",
     f"--signal:{p['signal']}",f"--signal-2:{p['signal2']}",f"--check:{p['check']}",f"--thin:{p['onink3']}",
     f"--warm:{p['fit'][3]}",f"--cool:{p['fit'][1]}",f"--hot:{p.get('hot',p['fit'][4])}",f"--z5:{p.get('hot',p['fit'][4])}"]
    for i,c in enumerate(p['fit']):
        o=onfit(c,d,l); lines+= [f"--fit-{i}:{c}"]+([f"--z{i+1}:{c}"] if i<4 else [])+[f"--on-fit-{i}:{o}",f"--unit-{i}:{o}"]
    return ':root{'+';'.join(lines)+'}'+p.get('extra','')
def checks(p):
    out=[]
    pairs=[('text on ground','onink','ink',7),('muted text','onink2','ink',4.5),('faint text','onink3','ink',4.5),
           ('panel text','onstock','stock',7),('panel muted','onstock2','stock',4.5),('panel faint','onstock3','stock',4.5),
           ('button text on signal','ink','signal',4.5),('signal on ground','signal','ink',3),('counting colour on panel','fit4','stock',3),('counting colour on ground','fit4','ink',3)]
    for n,a,b,m in pairs:
        A=p.get('hot',p['fit'][4]) if a=='fit4' else p[a]; v=cr(A,p[b]); out.append((n,round(v,2),'ok' if v>=m else 'FAIL<'+str(m)))
    return out
if __name__=='__main__':
    for k,p in P2.items():
        open(k+'.css','w').write(css(p))
        print(k, [c for c in checks(p) if c[2]!='ok'] or 'all pass')
