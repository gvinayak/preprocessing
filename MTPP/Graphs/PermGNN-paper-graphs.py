import matplotlib
from matplotlib import pyplot as plt
import brewer2mpl
import numpy as np
import pickle, pdb
import sys

bmap = brewer2mpl.get_map('Set2', 'qualitative', 7)
color_list = bmap.mpl_colors
color_list = [(0.4, 0.7607843137254902, 0.6470588235294118),
             (0.9882352941176471, 0.5529411764705883, 0.3843137254901961),
             (0.5529411764705883, 0.6274509803921569, 0.796078431372549),
             (0.9058823529411765, 0.5411764705882353, 0.7647058823529411),
             (0.6509803921568628, 0.8470588235294118, 0.32941176470588235),
             (1.0, 0.8509803921568627, 0.1843137254901961),
             (0.8980392156862745, 0.7686274509803922, 0.5803921568627451),
             (0.7019607843137254, 0.7019607843137254, 0.7019607843137254)]

color_list = [(1, 0, 0),
             (0, 0, 1),
              (0,0,0),
             (0.9882352941176471, 0.5529411764705883, 0.3843137254901961),
             (0,0,0),
#              (0.4, 0.7607843137254902, 0.6470588235294118),
             (0.9882352941176471, 0.5529411764705883, 0.3843137254901961),
            (0.6509803921568628, 0.8470588235294118, 0.32941176470588235),]

def latexify():
    matplotlib.rcParams['text.usetex'] = True
    matplotlib.rcParams['axes.spines.right'] = False
    matplotlib.rcParams['axes.spines.top'] = False
    plt.rc('font', family='serif')
    plt.rc('xtick', labelsize=30)
    plt.rc('ytick', labelsize=30)
    matplotlib.rc('text', usetex=True)
    matplotlib.rcParams['text.latex.preamble']=[r"\usepackage{amsmath,amsfonts}"]
    matplotlib.rcParams['text.latex.preamble']=[r"\usepackage{bm}"]
    plt.rc('axes', linewidth=1)
    plt.rc('font', weight='bold')
    matplotlib.rcParams['text.latex.preamble'] = [r'\boldmath']

# Making for Fig 1(a)
file = "Fig1a.p"
score_dict = pickle.load(open(file, "rb"))
latexify()
i=-1
fig, ax = plt.subplots()
for baseline in score_dict.keys():
    i=i+1
    label_map=[r'\textbf{IMTPP vs PFPP}', r'\textbf{IMTPP vs RMTPP}']    
    ax.plot(score_dict[baseline]['xaxis'], score_dict[baseline]['yaxis'], label=label_map[i], linewidth=8, markersize=4, color=color_list[i+5])

    plt.xlabel(r'$e_{k}$-\textbf{ID} \textbf{(sorted by gain)} $\rightarrow$', fontsize=32)

ax.yaxis.set_major_locator(plt.MaxNLocator(5))
# ax.xaxis.set_major_locator(plt.MaxNLocator(2))
plt.xticks([0, 100000, 200000, 300000], [r'$0$', r'$10$', r'$20$', r'$\times 10^4$'])

plt.ylim(top=0.1,bottom=-0.06)
ax.legend(prop={'size': 26}, frameon=False, handlelength=0.4, loc=1, bbox_to_anchor=(1.06,1.06))

plt.ylabel(r'\textbf{Gain in AE} $\rightarrow$ ', fontsize=32, labelpad=1)

plt.grid(axis='y',linestyle='-', linewidth=1)
plt.grid(axis='x',linestyle='-', linewidth=1)

plt.box(on=True)
ax.spines['top'].set_visible(True)
ax.spines['right'].set_visible(True)
# ax.set_title(r'\textbf{Gain} = $\textbf{AP}($\textsc{PermGNN})-$\textbf{AP}($\textbf{baseline})', fontsize=19)
plt.savefig("mv_diff_mae.pdf", bbox_inches='tight')
plt.close()




# Making for Fig 1(b)
file = "Fig1b.p"
score_dict = pickle.load(open(file, "rb"))
latexify()
i=-1
fig, ax = plt.subplots()
for baseline in score_dict.keys():
    i=i+1
    label_map=[r'\textbf{IMTPP vs PFPP}', r'\textbf{IMTPP vs RMTPP}']    
    ax.plot(score_dict[baseline]['xaxis'], score_dict[baseline]['yaxis'], label=label_map[i], linewidth=8, markersize=4, color=color_list[i+5])

plt.xlabel(r'$e_{k}$-\textbf{ID} \textbf{(sorted by gain)} $\rightarrow$', fontsize=32)

ax.yaxis.set_major_locator(plt.MaxNLocator(5))
# ax.xaxis.set_major_locator(plt.MaxNLocator(2))

plt.xticks([0, 40000, 80000, 120000], [r'$0$', r'$4$', r'$8$', r'$\times 10^4$'])

plt.ylim(top=0.1,bottom=-0.06)
ax.legend(prop={'size': 26}, frameon=False, handlelength=0.4, loc=1, bbox_to_anchor=(1.06,1.06))
plt.ylabel(r'\textbf{Gain in AE} $\rightarrow$ ', fontsize=32, labelpad=1)

plt.grid(axis='y',linestyle='-', linewidth=1)
plt.grid(axis='x',linestyle='-', linewidth=1)

plt.box(on=True)
ax.spines['top'].set_visible(True)
ax.spines['right'].set_visible(True)
# ax.set_title(r'\textbf{Gain} = $\textbf{AP}($\textsc{PermGNN})-$\textbf{AP}($\textbf{baseline})', fontsize=19)
plt.savefig("ty_diff_mae.pdf", bbox_inches='tight')
plt.close()




# Making for Fig 2(a)
file = "Fig2a.p"
score_dict = pickle.load(open(file, "rb"))
# pdb.set_trace()
latexify()
i=-1
fig, ax = plt.subplots()
for baseline in score_dict.keys():
    i=i+1
    label_map=[r'\textbf{RMTPP}', r'\textbf{IMTPP}']    
    ax.plot(score_dict[baseline]['xaxis'], score_dict[baseline]['yaxis'], label=label_map[i], linewidth=5, markersize=10, marker='d', color=color_list[i])

plt.xlabel(r'$\boldmath{k}$ \textbf{(index of $e_k$)} $\rightarrow$', fontsize=32)

ax.yaxis.set_major_locator(plt.MaxNLocator(3))
ax.xaxis.set_major_locator(plt.MaxNLocator(5))

plt.ylim(top=0.066, bottom=0.048)
ax.legend(prop={'size': 28}, frameon=False,handlelength=0.4)
plt.ylabel(r'\textbf{MAE} $\rightarrow$ ', fontsize=32, labelpad=2)

plt.grid(axis='y',linestyle='-', linewidth=1)
plt.grid(axis='x',linestyle='-', linewidth=1)

plt.box(on=True)
ax.spines['top'].set_visible(True)
ax.spines['right'].set_visible(True)
# ax.set_title(r'\textbf{Gain} = $\textbf{AP}($\textsc{PermGNN})-$\textbf{AP}($\textbf{baseline})', fontsize=19)
# file = "ty_diff_mae.pdf"
plt.savefig("mv_forecast_mae.pdf", bbox_inches='tight')
plt.close()






# Making for Fig 2(b)
file = "Fig2b.p"
score_dict = pickle.load(open(file, "rb"))
# pdb.set_trace()
latexify()
i=-1
fig, ax = plt.subplots()
for baseline in score_dict.keys():
    i=i+1
    label_map=[r'\textbf{RMTPP}', r'\textbf{IMTPP}']
    score_dict[baseline]['yaxis'] = [score_dict[baseline]['yaxis'][k]/100 for k in range(len(score_dict[baseline]['yaxis']))]
    ax.plot(score_dict[baseline]['xaxis'], score_dict[baseline]['yaxis'], label=label_map[i], linewidth=5, markersize=10, marker='d', color=color_list[i])

plt.xlabel(r'$\boldmath{k}$ \textbf{(index of $e_k$)} $\rightarrow$', fontsize=32)

ax.yaxis.set_major_locator(plt.MaxNLocator(3))
ax.xaxis.set_major_locator(plt.MaxNLocator(5))

plt.ylim(top=0.58, bottom=0.50)
ax.legend(prop={'size': 28}, frameon=False,handlelength=0.4)
plt.ylabel(r'\textbf{MPA} $\rightarrow$ ', fontsize=32, labelpad=2)

plt.grid(axis='y',linestyle='-', linewidth=1)
plt.grid(axis='x',linestyle='-', linewidth=1)

plt.box(on=True)
ax.spines['top'].set_visible(True)
ax.spines['right'].set_visible(True)
# ax.set_title(r'\textbf{Gain} = $\textbf{AP}($\textsc{PermGNN})-$\textbf{AP}($\textbf{baseline})', fontsize=19)
# file = "ty_diff_mae.pdf"
plt.savefig("mv_forecast_mpa.pdf", bbox_inches='tight')
plt.close()







# Making for Fig 4(a)
file = "Fig4a.p"
score_dict = pickle.load(open(file, "rb"))
latexify()
i=-1
fig, ax = plt.subplots()
for baseline in score_dict.keys():
    i=i+1
    label_map=[r'\textbf{True}', r'\textbf{Predicted}']
    ax.plot(score_dict[baseline]['xaxis'], score_dict[baseline]['yaxis'], label=label_map[i], linewidth=5, markersize=10, color=color_list[i])

plt.xlabel(r'$\boldmath{k}$ \textbf{(index of $e_k$)} $\rightarrow$', fontsize=32)

ax.yaxis.set_major_locator(plt.MaxNLocator(5))
ax.xaxis.set_major_locator(plt.MaxNLocator(5))

plt.ylim(top=3.1, bottom=0.15)
ax.legend(prop={'size': 28}, frameon=False,handlelength=0.4)
plt.ylabel(r'$\Delta_{t,k} \rightarrow$ ', fontsize=36, labelpad=5)

plt.grid(axis='y',linestyle='-', linewidth=1)
plt.grid(axis='x',linestyle='-', linewidth=1)

plt.box(on=True)
ax.spines['top'].set_visible(True)
ax.spines['right'].set_visible(True)
# ax.set_title(r'\textbf{Gain} = $\textbf{AP}($\textsc{PermGNN})-$\textbf{AP}($\textbf{baseline})', fontsize=19)
# file = "ty_diff_mae.pdf"
plt.savefig("mv_anec_mae.pdf", bbox_inches='tight')
plt.close()








# Making for Fig 4(b)
file = "Fig4b.p"
score_dict = pickle.load(open(file, "rb"))
latexify()
i=-1
fig, ax = plt.subplots()
for baseline in score_dict.keys():
    i=i+1
    label_map=[r'\textbf{True}', r'\textbf{Predicted}']
    ax.plot(score_dict[baseline]['xaxis'], score_dict[baseline]['yaxis'], label=label_map[i], linewidth=5, markersize=10, color=color_list[i])

plt.xlabel(r'$\boldmath{k}$ \textbf{(index of $e_k$)} $\rightarrow$', fontsize=32)

ax.yaxis.set_major_locator(plt.MaxNLocator(5))
ax.xaxis.set_major_locator(plt.MaxNLocator(5))

plt.ylim(top=0.65, bottom=0)
ax.legend(prop={'size': 28}, frameon=False,handlelength=0.4)
plt.ylabel(r'$\Delta_{t,k} \rightarrow$ ', fontsize=36, labelpad=5)

plt.grid(axis='y',linestyle='-', linewidth=1)
plt.grid(axis='x',linestyle='-', linewidth=1)

plt.box(on=True)
ax.spines['top'].set_visible(True)
ax.spines['right'].set_visible(True)
# ax.set_title(r'\textbf{Gain} = $\textbf{AP}($\textsc{PermGNN})-$\textbf{AP}($\textbf{baseline})', fontsize=19)
# file = "ty_diff_mae.pdf"
plt.savefig("ty_anec_mae.pdf", bbox_inches='tight')
plt.close()



# Making for Mei Epoch
file = "mei_epoch.p"
score_dict = pickle.load(open(file, "rb"))
latexify()
i=-1
fig, ax = plt.subplots()
for baseline in score_dict.keys():
    i=i+1
    label_map=[r'\textbf{PFPP}', r'\textbf{IMTPP}']
    ax.plot(score_dict[baseline]['xaxis'], score_dict[baseline]['yaxis'], label=label_map[i], linewidth=5, markersize=10, color=color_list[i])

plt.xlabel(r'\textbf{Epoch} $\rightarrow$', fontsize=32)

ax.yaxis.set_major_locator(plt.MaxNLocator(5))
ax.xaxis.set_major_locator(plt.MaxNLocator(7))

plt.ylim(top=20, bottom=-0.5)
ax.legend(prop={'size': 28}, frameon=False,handlelength=0.4)
plt.ylabel(r'\textbf{Time (Hours)} $\rightarrow$ ', fontsize=36, labelpad=5)

plt.grid(axis='y',linestyle='-', linewidth=1)
plt.grid(axis='x',linestyle='-', linewidth=1)

plt.box(on=True)
ax.spines['top'].set_visible(True)
ax.spines['right'].set_visible(True)
# ax.set_title(r'\textbf{Gain} = $\textbf{AP}($\textsc{PermGNN})-$\textbf{AP}($\textbf{baseline})', fontsize=19)
# file = "ty_diff_mae.pdf"
plt.savefig("mei_epoch.pdf", bbox_inches='tight')
plt.close()



# Making for Mei Length
file = "mei_seq.p"
score_dict = pickle.load(open(file, "rb"))
latexify()
i=-1
fig, ax = plt.subplots()
for baseline in score_dict.keys():
    i=i+1
    label_map=[r'\textbf{PFPP}', r'\textbf{IMTPP}']
    ax.plot(score_dict[baseline]['xaxis'], score_dict[baseline]['yaxis'], label=label_map[i], linewidth=5, marker='d', markersize=10, color=color_list[i])

plt.xlabel(r'\textbf{Length} $\rightarrow$', fontsize=32)

ax.yaxis.set_major_locator(plt.MaxNLocator(5))
ax.xaxis.set_major_locator(plt.MaxNLocator(5))

plt.xticks([0, 1, 2, 3, 4, 5], [r'$0$', r'$20$', r'$40$', r'$60$', r'$80$', r'$100$'])

plt.ylim(top=23.5, bottom=-0.5)
ax.legend(prop={'size': 28}, frameon=False,handlelength=0.4)
plt.ylabel(r'\textbf{Time (Hours)} $\rightarrow$ ', fontsize=36, labelpad=5)

plt.grid(axis='y',linestyle='-', linewidth=1)
plt.grid(axis='x',linestyle='-', linewidth=1)

plt.box(on=True)
ax.spines['top'].set_visible(True)
ax.spines['right'].set_visible(True)
# ax.set_title(r'\textbf{Gain} = $\textbf{AP}($\textsc{PermGNN})-$\textbf{AP}($\textbf{baseline})', fontsize=19)
# file = "ty_diff_mae.pdf"
plt.savefig("mei_seq.pdf", bbox_inches='tight')
plt.close()