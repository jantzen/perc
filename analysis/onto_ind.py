# file: onto_in.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import matplotlib.patches as mpatches
import eugene as eu
import pdb

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

# test all symmetries against each other
out = []
for ss in ssyms:
    for tss in tssyms:
        X = np.array(ss).T
        Y = np.array(tss).T
        D = eu.probability.EnergyDistance(X, Y)
        n = 50
        result = eu.probability.significant(X, Y, D, n)
        out.append(result)
        print(result)
if np.all(np.array(out) == False):
    print("All symmetries the same.")
else:
    print("There is a signficant difference between dynamical symmetries.")

# plot timeseries along with smoothed curves used for determining cut points
fig, axs = plt.subplots(3, 1, figsize=(3,6))
fig.tight_layout(rect=[0.05, 0.05, 0.95, 0.95], h_pad=3., w_pad=2.7)
for ii, fr in enumerate(sa):
    t = np.arange(len(fr))
    t = t / 10.
    axs[0].plot(t, fr, "o", color='tan', alpha=0.3)
    axs[0].plot(t, ssmooth[ii],'k-')
axs[0].set_ylim([0,1200] )
axs[0].set_xlim([0, 1000])
axs[0].set_xlabel("time [s]", fontsize=6)
axs[0].set_ylabel("volume [mL]", fontsize=6)
axs[0].set_title("(a)", fontsize=8, weight='bold')
axs[0].tick_params(axis='x', labelsize=6)
axs[0].tick_params(axis='y', labelsize=6)
for ii, fr in enumerate(ts):
    t = np.arange(len(fr))
    t = t / 10.
    axs[1].plot(t, fr, "o", color='darkolivegreen', alpha=0.3)
    axs[1].plot(t, tssmooth[ii],'k-')
axs[1].set_ylim([0, 1200]) 
axs[1].set_xlim([0, 1000])
axs[1].set_xlabel("time [s]", fontsize=6)
axs[1].set_ylabel("volume [mL]", fontsize=6)
axs[1].set_title("(b)", fontsize=8, weight='bold')
axs[1].tick_params(axis='x', labelsize=6)
axs[1].tick_params(axis='y', labelsize=6)
# plot the symmetries
for ss in ssyms:
    axs[2].plot(ss[0], ss[1], "o", color='tan', alpha=0.3)
for ts in tssyms:
    axs[2].plot(ts[0], ts[1], "o", color='darkolivegreen', alpha=0.3)
axs[2].set_ylim([200, 500])
axs[2].set_xlim([70, 300])
axs[2].set_xlabel("volume [mL]", fontsize=6)
axs[2].set_ylabel("volume [mL]", fontsize=6)
axs[2].set_title("(c)", fontsize=8, weight='bold')
axs[2].tick_params(axis='x', labelsize=6)
axs[2].tick_params(axis='y', labelsize=6)
tan_patch = mpatches.Patch(color='tan', label='sand')
green_patch = mpatches.Patch(color='darkolivegreen', label='topsoil')
plt.legend(handles=[tan_patch, green_patch])
plt.savefig("./paper_figs/fig1.pdf")

# compute and display wettability and intrinsic resistance
sand_wettability = []
sand_ir = []
soil_wettability = []
soil_ir = []
for fr in ssmooth:
    v = fr
    high = np.max(v)
    mid = np.max(np.where(v<600.))
    sand_wettability.append(1200. - high)
    sand_ir.append(mid / 10.)
for fr in tssmooth:
    v = fr
    high = np.max(v)
    mid = np.max(np.where(v<600.))
    soil_wettability.append(1200. - high)
    soil_ir.append(mid / 10.)
for ii, f in enumerate(sand_files):
    print(f)
    print("wettability: {}".format(sand_wettability[ii]))
    print("intrinsic resistance: {}".format(sand_ir[ii]))
for ii, f in enumerate(topsoil_files):
    print(f)
    print("wettability: {}".format(soil_wettability[ii]))
    print("intrinsic resistance: {}".format(soil_ir[ii]))

#####################################################################
# Pressure study with sand
files=[]
#files.append('../data/sand_900.0_10.0_22.937_Mon_Nov__4_12:08:43_2019')
#files.append('../data/sand_900.0_10.0_22.25_Mon_Nov__4_12:37:56_2019')
files.append('../data/sand_900.0_10.0_22.562_Mon_Nov__4_13:07:53_2019')
files.append('../data/sand_960.0_10.0_24.375_Mon_Nov__4_13:37:13_2019')
files.append('../data/sand_1010.0_10.0_26.312_Mon_Nov__4_14:06:45_2019')
files.append('../data/sand_1060.0_10.0_27.375_Mon_Nov__4_14:28:19_2019')
files.append('../data/sand_1110.0_10.0_27.25_Mon_Nov__4_14:43:04_2019')
files.append('../data/sand_1160.0_10.0_26.937_Mon_Nov__4_14:58:00_2019')
#files.append('../data/sand_900.0_10.0_26.875_Mon_Nov__4_15:08:46_2019')

frames = []
for f in files:
    tmp = np.loadtxt(f)
    tmp = tmp[:,np.max(np.where(tmp[1,:]>250)):]
    tmp = tmp.T
    tmp[:,1] = (tmp[0,1] - tmp[:,1]) / 10. * np.pi * (2.25 * 2.54)**2
    frames.append(pd.DataFrame(tmp,columns=["time","volume","pressure"]))

smooth = []
for fr in frames:
    smooth.append(fr['volume'].ewm(span=50).mean())

#motor_setting = [951., 951., 951., 960., 1010., 1060., 1110., 1160., 951.]
motor_setting = [951., 960., 1010., 1060., 1110., 1160.]
cp = []
for s in smooth:
    cp.append(np.min(np.where(s>=800))/ 10.) 
data = np.concatenate([np.array(motor_setting).reshape(-1,1),np.array(cp).reshape(-1,1)],axis=1)
pdata = pd.DataFrame(data, columns=["motor_setting","time_800"])
print(pdata)

fig, axs = plt.subplots(1, 2, figsize=(6,3))
fig.tight_layout(rect=[0.05, 0.05, 0.95, 0.95], h_pad=3., w_pad=2.7)
for ii, fr in enumerate(frames):
#    axs[0].plot(fr['time'], fr['volume'], '.', color='tan', alpha=0.3)
    times = fr['time'].to_numpy()
    times = times - times[0]
    axs[0].plot(times, fr['volume'], '.', color='tan', alpha=0.3)
    axs[0].plot(times, smooth[ii], 'k-')
    axs[0].set_xlabel("time [s]", fontsize=6)
    axs[0].set_ylabel("volume [mL]", fontsize=6)
axs[0].tick_params(axis='x', labelsize=6)
axs[0].tick_params(axis='y', labelsize=6)
axs[0].set_title("(a)", fontsize=8)
axs[1].plot((pdata["motor_setting"]),np.log(pdata["time_800"]),'o', 
        color='tab:purple')
fit = np.polyfit((pdata["motor_setting"]),np.log(pdata["time_800"]),1)
print(fit)
x = np.linspace(np.min(pdata["motor_setting"]),np.max(pdata["motor_setting"]))
y = fit[0] * x + fit[1]
axs[1].plot(x,y,'k-')
axs[1].set_title("(b)", fontsize=8)
axs[1].set_xlabel("motor setting [hPa]", fontsize=6)
axs[1].set_ylabel("log(intrinsic resistance) [log(s)]", fontsize=6)
axs[1].tick_params(axis='x', labelsize=6)
axs[1].tick_params(axis='y', labelsize=6)
plt.savefig("./paper_figs/fig2.pdf")


#plt.show()

