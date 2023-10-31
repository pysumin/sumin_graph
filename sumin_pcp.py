import streamlit as st 
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import plotly.express as px 
import plotly.graph_objs as go 
from sklearn.preprocessing import LabelEncoder 
import streamlit.components.v1 as components 
from plotly.subplots import make_subplots 
import pyperclip

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
    howtogetdataset = st.sidebar.selectbox('select dataset:', ['loade sample set', 'load clipboard'])
    if howtogetdataset == 'load clipboard':
        try:
            clipboard_text = pyperclip.paste()
            st.write(type(clipboard_text))
            st.code(clipboard_text)
            # df = pd.read_clipboard(sep='WWs+')
            st.sidebar.write(clipboard_text.shape)
            y = st.sidebar.selectbox('select Y:',df.columns)
        except:
            st.sidebar.write('clipboard empty :( ')
            return 0, 0
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



# y로 쓸걸 고름 
df, y_name = get_df()

#x 인자를 고름 
x = st.sidebar.multiselect('select inputs:', ['all']+df.columns.to_list())
if 'all' in x :
    x = df.columns
if y_name not in x: 
    x.insert(0, y_name)
df = df[x]

st.sidebar.title('GRAPH') 
if st.sidebar.button('Draw PCP'):

    fig1, fig2, fig3 = pcp2(df, y_name) 
    fig1.update_layout(height=400, margin={'r':50, 't':10, 'l':100, 'b':50} )
    fig2.update_layout(height=400, margin={'r':50, 't':10, 'l':100, 'b':50} ) 
    fig3.update_layout(height=400, margin={'r':20, 't':50, 'l':50, 'b':50} ) 
    st.plotly_chart(fig3, use_container_width = True)
    st.plotly_chart(fig2, use_container_width=True)
    st.plotly_chart(fig1, use_container_width = True)

