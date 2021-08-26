# file: gws_analysis.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob

# load data files for glycerine, water, and sand (including modified sand
# protocol)

glycerine_files = glob.glob('../data/glycerin*')
water_files = glob.glob('../data/water*')
sand_files = glob.glob('../data/sand*Nov__4*')
modsand_files = glob.glob('../data/sand*Feb__9*') # sand experiments
topsoil_files = glob.glob('../data/topsoil*') # all topsoil experiments (no pressure)

# create data frames
gframes = []
for f in glycerine_files:
    gframes.append(pd.DataFrame((np.loadtxt(f)).T,columns=["time","volume","pressure"]))
wframes = []
for f in water_files:
    wframes.append(pd.DataFrame((np.loadtxt(f)).T,columns=["time","volume","pressure"]))
sframes = []
for f in sand_files:
    sframes.append(pd.DataFrame((np.loadtxt(f)).T,columns=["time","volume","pressure"]))
msframes = []
for f in modsand_files:
    msframes.append(pd.DataFrame((np.loadtxt(f)).T,columns=["time","volume","pressure"]))
tsframes = []
for f in topsoil_files:
    tsframes.append(pd.DataFrame((np.loadtxt(f)).T,columns=["time","volume","pressure"]))

# verify sizes of data sets
print(len(gframes),len(wframes),len(sframes),len(msframes),len(tsframes))

# display data frame heads
print("glycerin")
gframes[0].head()
print("water")
wframes[0].head()
print("sand")
sframes[0].head()
print("sand -- modified protocol")
msframes[0].head()
print("topsoil")
tsframes[0].head()

# smooth the data sets to find cut-points
gsmooth = []
wsmooth = []
ssmooth = []
mssmooth = []
tssmooth = []
gspan = 100
wspan = 100
sspan = 100
msspan = 100
tsspan = 100
for fr in gframes:
    gsmooth.append(fr['volume'].ewm(span=gspan).mean())
for fr in wframes:
    wsmooth.append(fr['volume'].ewm(span=wspan).mean())
for fr in sframes:
    ssmooth.append(fr['volume'].ewm(span=sspan).mean())
for fr in msframes:
    mssmooth.append(fr['volume'].ewm(span=sspan).mean())
for fr in tsframes:
    tssmooth.append(fr['volume'].ewm(span=sspan).mean())

# plot smoothed curves
plt.figure()
for fr in gsmooth:
    plt.plot(fr, 'og')
for fr in wsmooth:
    plt.plot(fr, 'ob')
for fr in ssmooth:
    plt.plot(fr, '.k')
for fr in mssmooth:
    plt.plot(fr, '.k')
for fr in tssmooth:
    plt.plot(fr, '.k')
plt.xlim(0,400);
plt.ylim(240,270);
plt.title("Smoothed curves before clipping.")

# cut the noise at the beginning of each trajectory
print("Cuts will be made at the following indices:")
gl = []
wa = []
sa = []
msa = []
ts = []
print("glycerin")
for ii,fr in enumerate(gsmooth):
    tmp = np.max(np.where(fr>=fr[0]))
    print(tmp)
    gl.append(gframes[ii]['volume'].to_numpy()[tmp:])
print("water")
for ii,fr in enumerate(wsmooth):
    tmp = np.max(np.where(fr>=fr[0]))
    print(tmp)
    wa.append(wframes[ii]['volume'].to_numpy()[tmp:])
print("sand")
for ii,fr in enumerate(ssmooth):
    tmp = np.max(np.where(fr>=fr[0]))
    print(tmp)
    sa.append(sframes[ii]['volume'].to_numpy()[tmp:])
print("sand (modified)")
for ii,fr in enumerate(mssmooth):
    tmp = np.max(np.where(fr>=fr[0]))
    print(tmp)
    msa.append(msframes[ii]['volume'].to_numpy()[tmp:])
print("topsoil")
for ii,fr in enumerate(tssmooth):
    tmp = np.max(np.where(fr>=fr[0]))
    print(tmp)
    ts.append(tsframes[ii]['volume'].to_numpy()[tmp:])

# plot the clipped curves
plt.figure();
for fr in gl:
    plt.plot(fr, 'og')
for fr in wa:
    plt.plot(fr, 'ob')
for fr in sa:
    plt.plot(fr, '.k')
for fr in msa:
    plt.plot(fr, '.k')
for fr in ts:
    plt.plot(fr, '.k')

# convert data to volume
tmp_g = []
tmp_w = []
tmp_s = []
tmp_ms = []
tmp_ts = []
for tmp in gl:
    tmp = (tmp[0] - tmp) / 10. * np.pi * (2.125 * 2.54)**2
    tmp_g.append(pd.Series(tmp,name='volume'))
for tmp in wa:
    tmp = (tmp[0] - tmp) / 10. * np.pi * (2.125 * 2.54)**2
    tmp_w.append(pd.Series(tmp,name='volume'))
for tmp in sa:
    tmp = (tmp[0] - tmp) / 10. * np.pi * (2.125 * 2.54)**2
    tmp_s.append(pd.Series(tmp,name='volume'))
for tmp in msa:
    tmp = (tmp[0] - tmp) / 10. * np.pi * (2.125 * 2.54)**2
    tmp_ms.append(pd.Series(tmp,name='volume'))
for tmp in ts:
    tmp = (tmp[0] - tmp) / 10. * np.pi * (2.125 * 2.54)**2
    tmp_ts.append(pd.Series(tmp,name='volume'))
gl = tmp_g
wa = tmp_w
sa = tmp_s
msa = tmp_ms
ts = tmp_ts

# plot the volume data
plt.figure()
print('glycerin')
for fr in gl:
    plt.plot(fr, "-g")
print(max(fr))
print('water')
for fr in wa:
    plt.plot(fr, "-b")
print(max(fr))
print('sand')
for fr in sa:
    plt.plot(fr, "-m", alpha=0.3)
print(max(fr))
print('modified sand')
for fr in msa:
    plt.plot(fr, "-m", alpha=0.3)
print(max(fr))
print('topsoil')
for fr in sa:
    plt.plot(fr, "-k", alpha=0.3)
print(max(fr))
plt.title("Volume expelled vs. Time")
plt.xlabel("time [s]")
plt.ylabel("volume [mL]")
print(max(fr))

# smooth the volume data to find cut-points
gsmooth = []
wsmooth = []
ssmooth = []
mssmooth = []
tssmooth = []
span = 5
for fr in gl:
    gsmooth.append(fr.ewm(span=span).mean().to_numpy())
for fr in wa:
    wsmooth.append(fr.ewm(span=span).mean().to_numpy())
for fr in sa:
    ssmooth.append(fr.ewm(span=span).mean().to_numpy())
for fr in msa:
    mssmooth.append(fr.ewm(span=span).mean().to_numpy())
for fr in ts:
    tssmooth.append(fr.ewm(span=span).mean().to_numpy())

# plot the result
plt.figure()
for fr in gsmooth:
    plt.plot(fr)
    print(max(fr))
for fr in wsmooth:
    plt.plot(fr)
    print(max(fr))
for fr in ssmooth:
    plt.plot(fr)
    print(max(fr))
for fr in mssmooth:
    plt.plot(fr)
    print(max(fr))
for fr in tssmooth:
    plt.plot(fr)
    print(max(fr))
plt.title("Smoothed volume vs. time")

plt.figure()
for ii,fr in enumerate(gl):
    plt.plot(fr,'g.')
    plt.plot(gsmooth[ii],'k-')
    print(max(fr))
for ii,fr in enumerate(wa):
    plt.plot(fr,'b.')
    plt.plot(wsmooth[ii],'k-')
    print(max(fr))
for ii,fr in enumerate(sa):
    plt.plot(fr,'r.')
    plt.plot(ssmooth[ii],'k-')
    print(max(fr))
for ii,fr in enumerate(msa):
    plt.plot(fr,'m.')
    plt.plot(mssmooth[ii],'k-')
    print(max(fr))
for ii,fr in enumerate(ts):
    plt.plot(fr,'g.')
    plt.plot(tssmooth[ii],'k-')
    print(max(fr))

# find break points for untrans and trans segments
gclips = []
wclips = []
sclips = []
msclips = []
tsclips = []
for fr in gsmooth:
    v = fr
    high = np.max(np.where(v<400.))
    low = np.max(np.where(v<100.))
    mid = np.max(np.where(v<250.))
    gclips.append([low,mid,high])
for fr in wsmooth:
    v = fr
    high = np.max(np.where(v<400.))
    low = np.max(np.where(v<100.))
    mid = np.max(np.where(v<250.))
    wclips.append([low,mid,high])
for fr in ssmooth:
    v = fr
    high = np.max(np.where(v<400.))
    low = np.max(np.where(v<100.))
    mid = np.max(np.where(v<250.))
    sclips.append([low,mid,high])
for fr in mssmooth:
    v = fr
    high = np.max(np.where(v<400.))
    low = np.max(np.where(v<100.))
    mid = np.max(np.where(v<250.))
    msclips.append([low,mid,high])
for fr in tssmooth:
    v = fr
    high = np.max(np.where(v<400.))
    low = np.max(np.where(v<100.))
    mid = np.max(np.where(v<250.))
    tsclips.append([low,mid,high])

# Convert the time series back to numpy arrays
tmp=[]
for fr in gl:
    tmp.append(fr.to_numpy())
gl = tmp
tmp=[]
for fr in wa:
    tmp.append(fr.to_numpy())
wa = tmp
tmp=[]
for fr in sa:
    tmp.append(fr.to_numpy())
sa = tmp
tmp=[]
for fr in msa:
    tmp.append(fr.to_numpy())
msa = tmp
tmp=[]
for fr in ts:
    tmp.append(fr.to_numpy())
ts = tmp

# clip the raw data
gsyms = []
for i,fr in enumerate(gl):
    lo = gclips[i][0]
    mid = gclips[i][1]
    hi = gclips[i][2]
    untrans = fr[lo:mid]
    trans = fr[mid:hi]
    if len(untrans)>len(trans):
        untrans = untrans[:len(trans)]
    elif len(trans)>len(untrans):
        trans = trans[:len(untrans)]
    gsyms.append([untrans,trans])
wsyms = []
for i,fr in enumerate(wa):
    lo = wclips[i][0]
    mid = wclips[i][1]
    hi = wclips[i][2]
    untrans = fr[lo:mid]
    trans = fr[mid:hi]
    if len(untrans)>len(trans):
        untrans = untrans[:len(trans)]
    elif len(trans)>len(untrans):
        trans = trans[:len(untrans)]
    wsyms.append([untrans,trans])
ssyms = []
for i,fr in enumerate(sa):
    lo = sclips[i][0]
    mid = sclips[i][1]
    hi = sclips[i][2]
    untrans = fr[lo:mid]
    trans = fr[mid:hi]
    if len(untrans)>len(trans):
        untrans = untrans[:len(trans)]
    elif len(trans)>len(untrans):
        trans = trans[:len(untrans)]
    ssyms.append([untrans,trans])
mssyms = []
for i,fr in enumerate(msa):
    lo = msclips[i][0]
    mid = msclips[i][1]
    hi = msclips[i][2]
    untrans = fr[lo:mid]
    trans = fr[mid:hi]
    if len(untrans)>len(trans):
        untrans = untrans[:len(trans)]
    elif len(trans)>len(untrans):
        trans = trans[:len(untrans)]
    mssyms.append([untrans,trans])
tssyms = []
for i,fr in enumerate(ts):
    lo = tsclips[i][0]
    mid = tsclips[i][1]
    hi = tsclips[i][2]
    untrans = fr[lo:mid]
    trans = fr[mid:hi]
    if len(untrans)>len(trans):
        untrans = untrans[:len(trans)]
    elif len(trans)>len(untrans):
        trans = trans[:len(untrans)]
    tssyms.append([untrans,trans])

# plot timeseries along with smoothed curves used for determining cut points
plt.figure()
plt.plot(wa[0],'b.')
plt.plot(wsmooth[0],'r-')
plt.figure()
plt.plot(gl[0],'b.')
plt.plot(gsmooth[0],'r-')
plt.figure()
plt.plot(sa[0],'b.')
plt.plot(ssmooth[0],'r-')
plt.figure()
plt.plot(msa[0],'b.')
plt.plot(mssmooth[0],'r-')
plt.figure()
plt.plot(ts[0],'b.')
plt.plot(tssmooth[0],'r-')

# plot sand symmetries
plt.figure()
legend_text = []
for ii,ss in enumerate(ssyms):
    plt.plot(ss[0],ss[1],linestyle='none',marker='.')
    legend_text.append(sand_files[ii])
for ii,ss in enumerate(mssyms):
    plt.plot(ss[0],ss[1],linestyle='none',marker='.')
    legend_text.append(modsand_files[ii])
plt.legend(legend_text)

# plot all symmetries
plt.figure()
for ss in ssyms:
    plt.plot(ss[0],ss[1],'r.', alpha=0.2)
for ss in mssyms:
    plt.plot(ss[0],ss[1],'m.', alpha=0.2)
for gs in gsyms:
    plt.plot(gs[0],gs[1],'g.', alpha=0.2)
for ws in wsyms:
    plt.plot(ws[0],ws[1],'b.', alpha=0.2)
for ts in tssyms:
    plt.plot(ts[0],ts[1],'k.', alpha=0.2)

gfits=[]
wfits=[]
sfits=[]
msfits=[]
tsfits=[]
for gs in gsyms:
    f = np.polyfit(gs[0],gs[1],1)
    gfits.append(np.array(f).reshape(1,-1))
gfits = np.concatenate(gfits,axis=0)
for ws in wsyms:
    f = np.polyfit(ws[0],ws[1],1)
    wfits.append(np.array(f).reshape(1,-1))
wfits = np.concatenate(wfits,axis=0)
for ss in ssyms:
    f = np.polyfit(ss[0],ss[1],1)
    sfits.append(np.array(f).reshape(1,-1))
sfits = np.concatenate(sfits,axis=0)
for mss in mssyms:
    f = np.polyfit(mss[0],mss[1],1)
    msfits.append(np.array(f).reshape(1,-1))
msfits = np.concatenate(msfits,axis=0)
for tss in tssyms:
    f = np.polyfit(tss[0],tss[1],1)
    tsfits.append(np.array(f).reshape(1,-1))
tsfits = np.concatenate(tsfits,axis=0)
print('glycerin fits:\n {}'.format(gfits))
print('water fits:\n {}'.format(wfits))
print('sand fits:\n {}'.format(sfits))
print('modified sand fits:\n {}'.format(msfits))
print('topsoil fits:\n {}'.format(tsfits))

# display all plots
plt.show()
