#~ Imports & globals
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
plot_jsons = {}
def toInt(x):
    try: return int(x)
    except: return x

#~ Read & organize data
C = pd.read_csv("../data/full_data.csv")
C['date'] = pd.to_datetime(C['date'])
C_ = C.groupby('location')[['new_cases','new_deaths']].rolling(4).mean().applymap(toInt).reset_index(0)
C  = C.join(C_,rsuffix='_avg').dropna()
C['DATE']= C.date.dt.strftime("%m-%d")
C['NiceDate']= C.date.dt.strftime("%B %d")

#~ Keep only the intersting countries & dates (Include South Korea & start in February)
C_ = C.loc[(C.final>10200) & C['DATE'].apply(lambda x: int(x[:2])>1)].sort_values(by=['date'])
countries = list(set(C_['locations']))
days = list(set(C_['DATE']))
traces = []
frames = [ {'data': [], 'traces': list(range(len(countries)))} for k in range(1, len(days)-1)]
for country, cdf in C_.groupby('location'):
    trace = go.Scatter(x=cdf['total_cases'],y=cdf['new_cases_avg'],name=country,
                      customdata=cdf['NiceDate'], line=dict(color='grey', width=1), mode='lines',
                      hovertemplate= country+"<br>Date: %{customdata}<br>Total: %{x}<br><b>New: %{y}</b><extra></extra>")
    traces.append(trace)
    
    for k, frame in enumerate(frames):
        datum = {'type':'scatter',
                 'x': cdf['total_cases'][:k+2],
                 'y': cdf['new_cases_avg'][:k+2]}
        frame['data'].append(datum)


layout = go.Layout(title_text="New Cases vs Total Cases",
                  xaxis_title_text="Total Cases",
                  yaxis_title_text="New Cases (among test results reported)",
                  yaxis_type="log", xaxis_type="log",
                  updatemenus=[dict(type='buttons', showactive=False,
                               y=1.05, x=1.15, xanchor='right', yanchor='top',
                               pad=dict(t=0, r=10),
                               buttons=[dict(label='Start',
                                             method='animate',
                                             args=[None, 
                                                   dict(frame=dict(duration=6, redraw=False),
                                                        transition=dict(duration=0), fromcurrent=True,
                                                        mode='immediate')])])])

#~ Roughly log_10 of min & max of x and y
layout.update(xaxis =dict(range=[2.5,5.5], autorange=False),
              yaxis =dict(range=[1,5], autorange=False));


fig = go.Figure(data=traces, frames=frames, layout=layout)
fig.show()
#~ trace1 = go.Scatter(x=df.Date[:2],
#~                     y=low[:2],
#~                     mode='lines',
#~                     line=dict(color='grey',width=1))
#~ 
#~ trace2 = go.Scatter(x = df.Date[:2],
#~                     y = high[:2],
#~                     mode='lines',
#~                     line=dict(width=1.5))
#~ 
#~ frames = [dict(data= [dict(type='scatter',
#~                            x=df.Date[:k+1],
#~                            y=low[:k+1]),
#~                       dict(type='scatter',
#~                            x=df.Date[:k+1],
#~                            y=high[:k+1])],
#~                traces= [0, 1],  #this means that  frames[k]['data'][0]  updates trace1, and   frames[k]['data'][1], trace2 
#~               ) for k  in  range(1, len(low)-1)]

#~ layout = go.Layout(width=650,
#~                    height=400,
#~                    showlegend=False,
#~                    hovermode='closest',
#~                    updatemenus=[dict(type='buttons', showactive=False,
#~                                 y=1.05,
#~                                 x=1.15,
#~                                 xanchor='right',
#~                                 yanchor='top',
#~                                 pad=dict(t=0, r=10),
#~                                 buttons=[dict(label='Play',
#~                                               method='animate',
#~                                               args=[None, 
#~                                                     dict(frame=dict(duration=3, 
#~                                                                     redraw=False),
#~                                                          transition=dict(duration=0),
#~                                                          fromcurrent=True,
#~                                                          mode='immediate')])])])


#~ layout.update(xaxis =dict(range=[df.Date[0], df.Date[len(df)-1]], autorange=False),
#~               yaxis =dict(range=[min(low)-0.5, high.max()+0.5], autorange=False));
#~ 
#~ fig = go.Figure(data=[trace1, trace2], frames=frames, layout=layout)
#~ fig.show()
