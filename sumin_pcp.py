import streamlit as st 
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import plotly.express as px 
import plotly.graph_objs as go 
from sklearn.preprocessing import LabelEncoder 
import streamlit.components.v1 as components 
from plotly.subplots import make_subplots 
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.datasets import load_digits
import plotly.figure_factory as ff


plt.rcParams['font.family'] = 'Malgun Gothic' 
st.set_page_config(layout="wide")

# @st.cache_data(experimental_allow_widgets=True)
# @st.cache_data

def pcp2 (df, y_name):
    clsnum = 10  #범주가 이거보다 많으면 이걸로 퉁침 

    q_labels = [i/clsnum for i in range(clsnum)] 
    dims_co, dims_co_le, dims_ca = [], [], []    #세가지 그래프에 대한 축 리스트

    colorscale = [ [0, '#00868B'], [0.5, 'gray'], [1, 'red']   ]

    for col in df.columns:
        cates = df[col].unique() #컬럼에서 유일값 추출
        cates_num = len(cates) #유일값의 개수

        if df[col].dtype== 'object': #범주형 컬럼일 경우

            #기본형 - 수치로 바꿔야함
            value2dummy = dict(zip(cates, range(cates_num))) 
            df[col+'q'] = [value2dummy[i] for i in df[col]] #
            dim_co= dict( label=col 
                        , tickvals=list(value2dummy.values())
                        , ticktext=list(value2dummy.keys()) 
                        , values=df[col+'q']    )

            #순서형 - 등수 매기고 수치로 바꿔야함
            dim_co_le = dict( label=col 
                             , tickvals=list(value2dummy.values()) 
                             , ticktext=list(value2dummy.keys() )
                             , values=df[col+'q']   )

            #범주형 - 범주형으로 바꿔야함
            dim_ca = dict( label=col 
                          , ticktext=list(value2dummy.keys()) 
                          , values=df[col+'q'] 
                          , categoryorder = 'array')

        else:   # 수치형 컬럼이면

            #기본형 - 수치로 바꿔야함
            dim_co = dict( label=col ,values=df[col]    )

            #순서형
            le=LabelEncoder()
            df_temp = le.fit_transform(df[col]) #순서를 매김
            dim_co_le = dict( label=col
                            ,values=df_temp )

            #범주형
            if cates_num > clsnum :  #유일값이 너무 많으면
                df[col+'q'] = pd.qcut(df[col], clsnum, labels = False, duplicates = 'drop') #구간으로 나눔
            else: df[col+'q'] = df[col].astype('category')  #같은수가 반복되면 그냥 사용
            dim_ca = dict( label = col
                            , values = df[col+'q']
                            , categoryorder = 'category descending')
            
        dims_co.append(dim_co)
        dims_co_le.append(dim_co_le)
        dims_ca.append(dim_ca)

    #기본형
    fig_co = go.Figure(
        data=go.Parcoords( 
            line = dict( 
                color = df[y_name+'q']
                ,colorscale = colorscale    )
            , dimensions = dims_co 
            , labelfont = dict(size=15) 
            , tickfont = dict(size = 18) 
            , unselected = dict(line = dict(color = 'lightgray', opacity= 0.3))
        )
    )

    fig_le = go.Figure(
        data=go.Parcoords( 
            line = dict( 
                color = df[y_name+'q']
                , colorscale = colorscale   )
            , dimensions = dims_co_le
            , labelfont = dict(size=15) 
            , tickfont = dict(size = 18)
            , unselected = dict(line = dict(color = 'gray', opacity= 0.3))
        )
    )

    fig_ca = go.Figure(
        data = go.Parcats(
            line = dict(
                color = df[y_name+'q']
                , colorscale = colorscale
                , shape = 'hspline'     )
            ,dimensions=dims_ca
            , labelfont = dict(size=20) 
            , tickfont = dict(size = 18)
        )
    )

    fig1 = go.FigureWidget(fig_co)
    fig2 = go.FigureWidget(fig_le)
    fig3 = go.FigureWidget(fig_ca)

    return fig1, fig2, fig3


def get_df():

    st.sidebar.title('Getting Dataset')
    howtogetdataset = st.sidebar.selectbox('select dataset:', ['text input','loade sample set' ])
    if howtogetdataset == 'text input':
        text = st.sidebar.text_area('paste dataset', height = 5)
        data = [row.split('\t') for row in text.split('\n')]
        df = pd.DataFrame(data[1:], columns=data[0])
        
        for i in df.columns:
            df[i] = df[i].astype('float64', copy=True, errors='ignore')
        y = st.sidebar.selectbox('select Y:',df.columns)
    else :
        df = pd.read_csv("https://raw.githubusercontent.com/bcdunbar/datasets/master/iris.csv")
        st.sidebar.write(df.shape)
        y = st.sidebar.selectbox('select Y:',df.columns)

    #y를 맨 처음으로 이동시킴
    cols = df.columns.to_list() 
    inxofy = cols.index(y)
    cols.pop(inxofy) 
    cols = [y]+cols
    df = df[cols]

    return df, y

def pca():
    df,y = load_digits(n_class=5, return_X_y = True ,as_frame=True)
    # df 의 인덱스가 코일번호다.
    # y는 코일번호가 속한 클래스다.

    df_scaled = StandardScaler().fit_transform(df.T).T # 표준화
    pca = PCA(n_components=2) 
    pca_vals_scaled = pca.fit_transform(df_scaled)
    pca_df = pd.DataFrame(data = pca_vals_scaled, columns = ['p1','p2'])
    pca_df = pd.concat( [pca_df, y], axis = 1 )
    # pca.explained_variance_ratio_,pca.components_
    color_spaces = ['algae', 'amp' 'bluered', 'blugrn','brwnyl', 'bugn', 'bupu', 'burg', 'burgyl', 'cividis', 'curl','darkmint', 'deep', 'delta', 'dense', 'earth', 'edge', 'electric','emrld', 'fall', 'geyser', 'gnbu', 'gray', 'greens', 'greys',
    'haline', 'hot', 'hsv', 'ice', 'icefire', 'inferno', 'jet','magenta', 'magma', 'matter', 'mint', 'mrybm', 'mygbm', 'oranges','orrd', 'oryel', 'oxy', 'peach', 'phase', 'picnic', 'pinkyl','piyg', 'plasma', 'plotly3', 'portland', 'prgn', 'pubu', 'pubugn',
    'puor', 'purd', 'purp', 'purples', 'purpor', 'rainbow', 'rdbu','rdgy', 'rdpu', 'rdylbu', 'rdylgn', 'redor', 'reds', 'solar','spectral', 'speed', 'sunset', 'sunsetdark', 'teal', 'tealgrn',
    'tealrose', 'tempo', 'temps', 'thermal', 'tropic', 'turbid','turbo', 'twilight', 'viridis', 'ylgn', 'ylgnbu', 'ylorbr','ylorrd']

    color_num = 5
    fig1 = px.scatter(pca_df,   y= 'p2',    x= 'p1',    color = y
                    ,color_continuous_scale= color_spaces[color_num] 
                    #  , color_discrete_sequence='T10' 
                    )

    hist_data = [ pca_df[ pca_df.target == i ]['p1'] for i in y.unique()  ]
    glabels = list(pca_df.target.unique())
    colors = px.colors.sample_colorscale(color_spaces[color_num], len(y.unique()))
    for i in glabels:    glabels[i] = str(i)
    fig2 = ff.create_distplot(hist_data, group_labels = glabels, show_hist=False, show_rug=False
                            ,colors = colors)
    # fig2.show()

    fig = make_subplots(rows=2, cols = 1)
    fig.add_trace(fig1.data[0], row=1, col=1)
    for i in range(len(fig2.data)):    
        fig.add_trace(fig2.data[i], row=2, col=1)
    return fig



#=================== y로 쓸걸 고름 
df, y_name = get_df()

#===================x 인자를 고름 
cols= df.columns.to_list()
cols=['all']+cols
x = st.sidebar.multiselect('select inputs:', cols, default = 'all')
if 'all' in x :
    x = df.columns
if y_name not in x: 
    x.insert(0, y_name)
df = df[x]

# ============필터링 ===========
st.sidebar.title('Filtering')
filters = {}
cols = st.sidebar.multiselect('select filtering items:', df.columns.to_list())
for col in cols:
    vals = st.sidebar.multiselect('select values of '+col, df[col].unique(), default = df[col].unique())
    filters[col] = vals  #선택한 컬럼에서 선택한 값을 저장해둠
for key in filters.keys():
    df = df[    df[key].isin(filters[key])   ]

# ==============이제 탭을 사용하자=====================
t1,t2,t3 = st.tabs(['pcp','pca','row code'])


# ===========그래프 그리기==========
with t1:
    fig1, fig2, fig3 = pcp2(df, y_name) 
    fig1.update_layout(height=400, margin={'r':50, 't':10, 'l':100, 'b':50} )
    fig2.update_layout(height=400, margin={'r':50, 't':10, 'l':100, 'b':50} ) 
    fig3.update_layout(height=400, margin={'r':20, 't':50, 'l':50, 'b':50} ) 
    st.plotly_chart(fig3, use_container_width = True)
    st.plotly_chart(fig2, use_container_width=True)
    st.plotly_chart(fig1, use_container_width = True)


with t2:
    fig = pca()
    st.plotly_chart(fig, use_container_width = True)


with t3:
    code = '''
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.datasets import load_digits
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.figure_factory as ff
import numpy as np

df,y = load_digits(n_class=5, return_X_y = True ,as_frame=True)
# df 의 인덱스가 코일번호다.
# y는 코일번호가 속한 클래스다.

df_scaled = StandardScaler().fit_transform(df.T).T # 표준화
pca = PCA(n_components=2) 
pca_vals_scaled = pca.fit_transform(df_scaled)
pca_df = pd.DataFrame(data = pca_vals_scaled, columns = ['p1','p2'])
pca_df = pd.concat( [pca_df, y], axis = 1 )
# pca.explained_variance_ratio_,pca.components_
color_spaces = ['algae', 'amp' 'bluered', 'blugrn','brwnyl', 'bugn', 'bupu', 'burg', 'burgyl', 'cividis', 'curl','darkmint', 'deep', 'delta', 'dense', 'earth', 'edge', 'electric','emrld', 'fall', 'geyser', 'gnbu', 'gray', 'greens', 'greys',
'haline', 'hot', 'hsv', 'ice', 'icefire', 'inferno', 'jet','magenta', 'magma', 'matter', 'mint', 'mrybm', 'mygbm', 'oranges','orrd', 'oryel', 'oxy', 'peach', 'phase', 'picnic', 'pinkyl','piyg', 'plasma', 'plotly3', 'portland', 'prgn', 'pubu', 'pubugn',
'puor', 'purd', 'purp', 'purples', 'purpor', 'rainbow', 'rdbu','rdgy', 'rdpu', 'rdylbu', 'rdylgn', 'redor', 'reds', 'solar','spectral', 'speed', 'sunset', 'sunsetdark', 'teal', 'tealgrn',
'tealrose', 'tempo', 'temps', 'thermal', 'tropic', 'turbid','turbo', 'twilight', 'viridis', 'ylgn', 'ylgnbu', 'ylorbr','ylorrd']

color_num = 5
fig1 = px.scatter(pca_df,   y= 'p2',    x= 'p1',    color = y
                 ,color_continuous_scale= color_spaces[color_num] 
                #  , color_discrete_sequence='T10' 
                 )

hist_data = [ pca_df[ pca_df.target == i ]['p1'] for i in y.unique()  ]
glabels = list(pca_df.target.unique())
colors = px.colors.sample_colorscale(color_spaces[color_num], len(y.unique()))
for i in glabels:    glabels[i] = str(i)
fig2 = ff.create_distplot(hist_data, group_labels = glabels, show_hist=False, show_rug=False
                          ,colors = colors)
# fig2.show()

fig = make_subplots(rows=2, cols = 1)
fig.add_trace(fig1.data[0], row=1, col=1)
for i in range(len(fig2.data)):    
    fig.add_trace(fig2.data[i], row=2, col=1)
fig.show()


            '''
    st.code(code, language='python')
