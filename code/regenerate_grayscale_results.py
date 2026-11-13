"""Render empirical and model-results charts in grayscale at 600 dpi.
Reuses the recorded GLEE table, the archived simulation outcomes and the
corresponding published plotting functions.
"""
import plot_publication_figures as pp
pp.INK='#141414';pp.SLATE='#111111';pp.PINE='#858585';pp.RUST='#777777';pp.MID='#666666';pp.GRID='#dddddd';pp.PALE='#f4f4f4';pp.PALE_B='#f4f4f4';pp.PALE_G='#eeeeee';pp.PALE_R='#eeeeee'
old_save=pp.save
# Patch the export resolution only. Preserve data handling and computation.
def save_600(fig,key):
    for ext in ['pdf','svg','png']:
        fig.savefig(pp.OUT/f'{key}.{ext}',dpi=600,bbox_inches='tight',pad_inches=.035)
    pp.plt.close(fig)
pp.save=save_600
pp.micro();pp.trajectories();pp.paired();pp.sensitivity();pp.agents()
