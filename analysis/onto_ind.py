# file: onto_in.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob

# There is variation within the same kind (multiple runs of sand and soil at
# atmospheric pressure)
# load data
sand_files = ('../data/sand_900.0_10.0_21.5_Mon_Oct_28_13:37:00_2019',
        '../data/sand_900.0_10.0_22.125_Mon_Oct_28_14:06:53_2019')

topsoil_files = ('../data/topsoil_900.0_10.0_23.125_Tue_Oct_29_13:15:30_2019',
        '../data/topsoil_900.0_10.0_24.187_Tue_Oct_29_14:50:16_2019')

# create data frames
sframes = []
for f in sand_files:
    sframes.append(pd.DataFrame((np.loadtxt(f)).T,columns=["time","volume","pressure"]))

tsframes = []
for f in topsoil_files:
    tsframes.append(pd.DataFrame((np.loadtxt(f)).T,columns=["time","volume","pressure"]))

# smooth the data sets to find cut-points
ssmooth = []
tssmooth = []
sspan = 100
tsspan = 100
for fr in sframes:
    ssmooth.append(fr['volume'].ewm(span=sspan).mean())
for fr in tsframes:
    tssmooth.append(fr['volume'].ewm(span=sspan).mean())

# cut the noise at the beginning of each trajectory
print("Cuts will be made at the following indices:")
sa = []
ts = []
print("sand")
for ii,fr in enumerate(ssmooth):
    tmp = np.max(np.where(fr>=fr[0]))
    print(tmp)
    sa.append(sframes[ii]['volume'].to_numpy()[tmp:])
print("topsoil")
for ii,fr in enumerate(tssmooth):
    tmp = np.max(np.where(fr>=fr[0]))
    print(tmp)
    ts.append(tsframes[ii]['volume'].to_numpy()[tmp:])

## plot the clipped curves
#plt.figure();
#for fr in sa:
#    plt.plot(fr, "-", color='tan', alpha=0.3)
#for fr in ts:
#    plt.plot(fr, '-', color='darkolivegreen', alpha=0.3)

# convert data to volume
tmp_s = []
tmp_ts = []
for tmp in sa:
    tmp = (tmp[0] - tmp) / 10. * np.pi * (2.125 * 2.54)**2
    tmp_s.append(pd.Series(tmp,name='volume'))
for tmp in ts:
    tmp = (tmp[0] - tmp) / 10. * np.pi * (2.125 * 2.54)**2
    tmp_ts.append(pd.Series(tmp,name='volume'))
sa = tmp_s
ts = tmp_ts

## plot the volume data
#plt.figure()
#print('sand')
#for fr in sa:
#    plt.plot(fr, "o", color='tan', alpha=0.3)
#print('topsoil')
#for fr in ts:
#    plt.plot(fr, "o", color='black', alpha=0.3)
#plt.title("Volume expelled vs. Time")
#plt.xlabel("time [s]")
#plt.ylabel("volume [mL]")

# smooth the volume data to find cut-points
ssmooth = []
tssmooth = []
span = 40 
for fr in sa:
    ssmooth.append(fr.ewm(span=span).mean().to_numpy())
for fr in ts:
    tssmooth.append(fr.ewm(span=span).mean().to_numpy())

## plot the result
#plt.figure()
#for fr in gsmooth:
#    plt.plot(fr)
#    print(max(fr))
#for fr in wsmooth:
#    plt.plot(fr)
#    print(max(fr))
#for fr in ssmooth:
#    plt.plot(fr)
#    print(max(fr))
#for fr in mssmooth:
#    plt.plot(fr)
#    print(max(fr))
#for fr in tssmooth:
#    plt.plot(fr)
#    print(max(fr))
#plt.title("Smoothed volume vs. time")
#
#plt.figure()
#for ii,fr in enumerate(sa):
#    plt.plot(fr,'r.')
#    plt.plot(ssmooth[ii],'k-')
#for ii,fr in enumerate(ts):
#    plt.plot(fr,'g.')
#    plt.plot(tssmooth[ii],'k-')

# find break points for untrans and trans segments
sclips = []
tsclips = []
for fr in ssmooth:
    v = fr
    high = np.max(np.where(v<400.))
    low = np.max(np.where(v<100.))
    mid = np.max(np.where(v<250.))
    sclips.append([low,mid,high])
for fr in tssmooth:
    v = fr
    high = np.max(np.where(v<400.))
    low = np.max(np.where(v<100.))
    mid = np.max(np.where(v<250.))
    tsclips.append([low,mid,high])

# Convert the time series back to numpy arrays
tmp=[]
for fr in sa:
    tmp.append(fr.to_numpy())
sa = tmp
tmp=[]
for fr in ts:
    tmp.append(fr.to_numpy())
ts = tmp

# clip the raw data
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
fig, axs = plt.subplots(3, 1)
fig.tight_layout()
for ii, fr in enumerate(sa):
    t = np.arange(len(fr))
    t = t / 10.
    axs[0].plot(t, fr, "o", color='tan', alpha=0.3)
    axs[0].plot(t, ssmooth[ii],'k-')
axs[0].set_ylim([0,1200] )
axs[0].set_xlim([0, 1000])
axs[0].set_title("Volume of water passing through sand vs. time")
for ii, fr in enumerate(ts):
    t = np.arange(len(fr))
    t = t / 10.
    axs[1].plot(t, fr, "o", color='darkolivegreen', alpha=0.3)
    axs[1].plot(t, tssmooth[ii],'k-')
axs[1].set_ylim([0, 1200]) 
axs[1].set_xlim([0, 1000])
axs[1].set_title("Volume of water passing through topsoil vs. time")
# plot the symmetries
for ss in ssyms:
    axs[2].plot(ss[0], ss[1], "o", color='tan', alpha=0.3)
for ts in tssyms:
    axs[2].plot(ts[0], ts[1], "o", color='darkolivegreen', alpha=0.3)

plt.show()

# generate plot of volume-time curves

# we thus introduce hydrological resistance (HR)

# HR varies with water content introduce saturation
