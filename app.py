"""Standalone desktop graphical interface to the legacy ADD analysis."""
import csv
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from add_core import analyze
from add_io import load_values, default_parameters, transform

LABELS=('Normal','Uniform','Exponential')

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('ADDT — Anderson-Darling Detection Tool | Legacy Research Preview')
        self.geometry('1100x760')
        self.minsize(790,570)
        self.raw=None; self.results=None; self.loaded_path=None
        bar=ttk.Frame(self,padding=12);bar.pack(fill='x')
        ttk.Button(bar,text='Open TXT data',command=self.open_file).grid(row=0,column=0,padx=5,pady=5)
        self.file_label=ttk.Label(bar,text='No file selected',width=70)
        self.file_label.grid(row=0,column=1,columnspan=5,sticky='w')
        ttk.Label(bar,text='Distribution:').grid(row=1,column=0,sticky='w')
        self.mode=ttk.Combobox(bar,values=LABELS,state='readonly',width=17)
        self.mode.current(0);self.mode.grid(row=1,column=1,sticky='w');self.mode.bind('<<ComboboxSelected>>',self.refresh_params)
        self.p1name=ttk.Label(bar,text='Mean:');self.p1name.grid(row=1,column=2)
        self.p1=tk.StringVar();ttk.Entry(bar,textvariable=self.p1,width=12).grid(row=1,column=3,padx=5)
        self.p2name=ttk.Label(bar,text='SD:');self.p2name.grid(row=1,column=4)
        self.p2=tk.StringVar();self.p2entry=ttk.Entry(bar,textvariable=self.p2,width=12);self.p2entry.grid(row=1,column=5,padx=5)
        ttk.Label(bar,text='Minimum observations on each side:').grid(row=2,column=0,columnspan=2,sticky='w')
        self.min_size=tk.StringVar(value='20');ttk.Entry(bar,textvariable=self.min_size,width=6).grid(row=2,column=2,sticky='w')
        ttk.Button(bar,text='Run analysis',command=self.run_analysis).grid(row=2,column=3,pady=8)
        ttk.Button(bar,text='Export CSV',command=self.export_csv).grid(row=2,column=4)
        ttk.Button(bar,text='Save graph',command=self.save_plot).grid(row=2,column=5)
        self.status=tk.StringVar(value='Open a TXT file with one number per line. Legacy VBA formulas retained.')
        ttk.Label(self,textvariable=self.status,padding=(12,2)).pack(anchor='w')
        self.fig=Figure(figsize=(10,5),dpi=100)
        self.ax=self.fig.add_subplot(111)
        self.ax.set_xlabel('Checkpoint');self.ax.set_ylabel('AD score')
        self.ax.grid(alpha=.25)
        self.canvas=FigureCanvasTkAgg(self.fig,master=self)
        self.canvas.get_tk_widget().pack(fill='both',expand=True,padx=10,pady=3)
        toolbar=NavigationToolbar2Tk(self.canvas,self,pack_toolbar=False);toolbar.update();toolbar.pack(fill='x')
        ttk.Label(self,text='Research preview — legacy formula reproduction; not a validated significance test.',padding=10).pack(anchor='w')

    def open_file(self):
        path=filedialog.askopenfilename(title='Select numeric TXT file',filetypes=[('Text files','*.txt'),('All files','*.*')])
        if not path:return
        try:self.raw=load_values(path)
        except Exception as exc:messagebox.showerror('Invalid input',str(exc));return
        self.loaded_path=Path(path);self.results=None
        self.file_label.config(text=self.loaded_path.name)
        self.refresh_params()
        self.status.set(f'{len(self.raw):,} observations loaded. Mean={np.mean(self.raw):.6g}; sample SD={np.std(self.raw,ddof=1):.6g}.')

    def refresh_params(self,event=None):
        mode=self.mode.current()
        self.p1name.config(text=['Mean (mu):','Lower bound (a):','Scale / mean:'][mode])
        self.p2name.config(text=['SD (sigma):','Upper bound (b):',''][mode])
        self.p2entry.configure(state='disabled' if mode==2 else 'normal')
        if self.raw is not None:
            a,b=default_parameters(self.raw,mode)
            self.p1.set(f'{a:.15g}');self.p2.set('' if b is None else f'{b:.15g}')

    def run_analysis(self):
        if self.raw is None:messagebox.showwarning('Missing data','Open a TXT file first.');return
        try:
            mode=self.mode.current();p1=float(self.p1.get());p2=None if mode==2 else float(self.p2.get())
            minimum=int(self.min_size.get());n=len(self.raw)
            if minimum<1 or 2*minimum>n:raise ValueError('Minimum side size must be >=1 and <= half the sample size')
            x=transform(self.raw,mode,p1,p2)
            self.status.set('Computing legacy scores...');self.update_idletasks()
            self.results=analyze(x,mode)
            ticks=np.array([r.checkpoint for r in self.results]);left=np.array([r.ad_left for r in self.results]);right=np.array([r.ad_right for r in self.results]);diff=np.array([r.ad_difference for r in self.results]);valid=(ticks>=minimum)&(ticks<=n-minimum)
            peak_idx=np.flatnonzero(valid)[np.argmax(diff[valid])];best=int(ticks[peak_idx])
            self.ax.clear()
            self.ax.plot(ticks,left,label='AD Left',color='#4c83ba',linewidth=1.4)
            self.ax.plot(ticks,right,label='AD Right',color='#bc5050',linewidth=1.4)
            self.ax.plot(ticks,diff,label='AD difference',color='#87a94c',linewidth=1.6)
            self.ax.axvline(best,color='black',linestyle='--',linewidth=1,alpha=.65,label=f'Peak valid difference: {best}')
            self.ax.axvspan(0,minimum,alpha=.07,color='gray');self.ax.axvspan(n-minimum,n,alpha=.07,color='gray')
            self.ax.set(xlabel='Checkpoint',ylabel='Legacy AD score',title=f'Tracking for {LABELS[mode]} — {self.loaded_path.name}')
            self.ax.grid(alpha=.22);self.ax.legend(loc='best');self.fig.tight_layout();self.canvas.draw()
            self.status.set(f'{n:,} observations | Peak among valid splits: {best} | AD difference: {diff[peak_idx]:.6f} | Minimum side size: {minimum}')
        except Exception as exc:
            self.status.set('Analysis failed');messagebox.showerror('Analysis error',str(exc))

    def export_csv(self):
        if self.results is None:messagebox.showinfo('No output','Run an analysis first.');return
        path=filedialog.asksaveasfilename(defaultextension='.csv',initialfile='ADD_results.csv',filetypes=[('CSV','*.csv')])
        if not path:return
        with open(path,'w',newline='',encoding='utf-8-sig') as f:
            w=csv.writer(f);w.writerow(['Checkpoint','AD Left','AD Right','AD difference'])
            for r in self.results:w.writerow([r.checkpoint,r.ad_left,r.ad_right,r.ad_difference])
        self.status.set(f'Saved CSV: {path}')

    def save_plot(self):
        if self.results is None:messagebox.showinfo('No output','Run an analysis first.');return
        path=filedialog.asksaveasfilename(defaultextension='.png',initialfile='ADD_graph.png',filetypes=[('PNG image','*.png'),('PDF','*.pdf')])
        if path:self.fig.savefig(path,dpi=180,bbox_inches='tight');self.status.set(f'Saved graph: {path}')

if __name__=='__main__':App().mainloop()
