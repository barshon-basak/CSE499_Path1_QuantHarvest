"""Publication-readable static plots, PNG and SVG."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import binom

def make_plots(rows,hists,plain,baseline):
    dest=Path(__file__).parent/'plots'; dest.mkdir(exist_ok=True)
    plt.rcParams.update({'font.size':11,'axes.spines.top':False,'axes.spines.right':False,
                         'figure.facecolor':'white','savefig.facecolor':'white'})
    colors={'mini_aes':'#007C91','saes':'#D16127'}
    labels={'mini_aes':'Mini-AES','saes':'S-AES'}
    def save(fig,name):
        fig.savefig(dest/(name+'.png'),dpi=180,bbox_inches='tight')
        fig.savefig(dest/(name+'.svg'),bbox_inches='tight');plt.close(fig)
    x=np.arange(17)
    fig,ax=plt.subplots(1,2,figsize=(12,4.8),layout='constrained')
    for cipher in colors:
        hs=np.array([hists[cipher,p][:17] for p in plain])/65536
        mu=hs.mean(axis=0)
        ax[0].plot(x,mu,'o-',label=labels[cipher],color=colors[cipher])
        ax[0].fill_between(x,hs.min(0),hs.max(0),alpha=.12,color=colors[cipher])
        ax[1].plot(x,x*mu,'o-',label=labels[cipher],color=colors[cipher])
    theory=binom.pmf(x,65536,1/65536)
    ax[0].plot(x,theory,'k--',label='Ideal binomial')
    ax[1].plot(x,x*theory,'k--',label='Ideal (key weighted)')
    for a in ax:
        a.set_xlim(-.2,12.2);a.set_xlabel('Cluster size (keys sharing ciphertext)');a.grid(alpha=.2);a.legend()
    ax[0].set_ylabel('Fraction of ciphertexts');ax[1].set_ylabel('Fraction of keys')
    ax[0].set_title('Random ciphertext perspective')
    ax[1].set_title('Known key perspective')
    fig.suptitle('109 fixed plaintexts: mean occupancy distributions\nShading: observed plaintext range (left panel)',fontsize=14)
    save(fig,'occupancy_perspectives')
    fig,axes=plt.subplots(2,3,figsize=(14,8),layout='constrained')
    for i,p in enumerate(plain[:5]):
        a=axes.flat[i];maxx=max(int(np.flatnonzero(hists[c,p])[-1]) for c in colors)
        xx=np.arange(maxx+1)
        for c,offset in [('mini_aes',-.19),('saes',.19)]:
            a.bar(xx+offset,hists[c,p][:maxx+1]/65536,width=.38,color=colors[c],label=labels[c])
        a.plot(xx,binom.pmf(xx,65536,1/65536),'k.--',label='Ideal')
        a.set_title(f'Plaintext 0x{p:04X}');a.set_xlabel('Cluster size');a.set_ylabel('Ciphertext fraction');a.grid(axis='y',alpha=.2)
    axes.flat[5].axis('off');axes.flat[0].legend()
    fig.suptitle('Paper plaintexts: exhaustive enumeration of every key',fontsize=15)
    save(fig,'paper_plaintexts')
    fig,axes=plt.subplots(1,3,figsize=(15,4.8),layout='constrained')
    for a,metric,title in zip(axes,['colliding_key_pairs','fraction_keys_in_clusters_ge2','max_cluster_size'],
                            ['Colliding key pairs','Fraction of keys with a collision','Largest cluster']):
        for c in colors:
            yy=[r[metric] for r in rows if r['cipher']==c]
            a.scatter(range(109),yy,s=15,alpha=.75,color=colors[c],label=labels[c])
        lo,hi=np.quantile([r[metric] for r in baseline],[.025,.975])
        a.axhspan(lo,hi,color='gray',alpha=.22,label='Ideal: 95% simulation interval')
        a.axvline(4.5,color='gray',ls=':',lw=1);a.axvline(8.5,color='gray',ls=':',lw=1)
        a.set_title(title);a.set_xlabel('Plaintext index (5 paper, 4 structured, 100 random)');a.grid(alpha=.2)
    axes[0].legend(fontsize=8,loc='upper left')
    fig.suptitle('Variation across plaintexts; ideal intervals apply to one plaintext',fontsize=14)
    save(fig,'plaintext_variation')
    fig,axes=plt.subplots(1,2,figsize=(11,4.8),layout='constrained')
    for a,c in zip(axes,colors):
        hh=np.array([hists[c,p][:20] for p in plain])/65536
        for r in hh: a.plot(np.arange(20),r,color=colors[c],alpha=.08)
        a.plot(np.arange(20),hh.mean(0),color=colors[c],lw=2,label='Observed mean')
        a.plot(np.arange(20),binom.pmf(np.arange(20),65536,1/65536),'k--',label='Ideal binomial')
        a.set_yscale('log');a.set_ylim(1e-7,1);a.set_xlim(0,15)
        a.set_title(labels[c]);a.set_xlabel('Cluster size');a.set_ylabel('Ciphertext fraction (log scale)');a.legend();a.grid(alpha=.2)
    fig.suptitle('Distribution tails: faint lines show individual plaintexts',fontsize=14)
    save(fig,'distribution_tails')
