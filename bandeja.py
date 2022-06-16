import streamlit as st
import gspread
import pandas as pd


# configuration
st.set_option('deprecation.showfileUploaderEncoding', False)

#st.set_page_config( layout='wide' )

# title of the app
st.title("PROCESOS DE DATOS POR BANDEJA")


gc = gspread.service_account(filename='datacargar-947843f340e2.json')
sh = gc.open("Gpon_ticket_WEB")


#  el 0 simbol del numero de hoja en este caso es la primera hoja = 0
worksheet = sh.get_worksheet(0)


# ver datos de google sheet
df = pd.DataFrame(worksheet.get_all_records())


df = df.fillna(0).apply(pd.to_numeric, errors='ignore')
print(df)
actu = df.loc[df.index[-1], "fec_regist"]

df['fec_regist']= pd.to_datetime(df['fec_regist']).dt.date



start_date = st.date_input('Date de début :')
end_date = st.date_input('Date de fin :')
if start_date <= end_date:
    pass
else:
    st.error('Error: Date de fin doit être choisi après la dete de début.')

mask = (df['fec_regist'] >= start_date) & (df['fec_regist'] <= end_date)
df = df.loc[mask]

def to_int(val):
    """ Reconoce valores numericos y los transforma a enteros.
    """
    try:
        value = int(float(val))
    except ValueError:
        value = ""
    return value

df["day"] = df["day"].map(to_int)

df['fec_regist']= pd.to_datetime(df['fec_regist']).dt.date

#Matrix maestra cuadro 1
cdru = df

cdru = pd.pivot_table(cdru, index=['desnomctr', 'tiptecnologia'], columns=['day'], aggfunc='size', values='codofcadm')
cdru = cdru.reset_index()


cdru = cdru.astype(str)
cdru = cdru.replace('nan', 999999)
cdru = cdru.round().astype(float,errors='ignore')
cdru = cdru.apply(pd.to_numeric,downcast ='signed',errors='ignore')
cdru = cdru.astype(str)
cdru = cdru.replace('999999', '')

####cuadro 1 tod1

values_1=['GPON']
values_2=['FIBRA','GAC-VOIP','MTTO TRABAJOS PROGRAMADOS','TRATAMIENTO CALL PIN TV-M1','INFOPYME PERU SAC','TRIAJE','2DA LINEA TRIAJE','BACK OFFICE','TRIAJE GPON']
cdru = cdru[cdru.tiptecnologia.isin(values_1)&cdru.desnomctr.isin(values_2)]

texto  = ('📊Cuadro de Bandeja GPON Reporte Actualizado:📊 \n\n⌚'+ actu)

st.markdown( f'<h1 style="color:#08298A;font-size:24px;">{texto}</h1>', unsafe_allow_html=True )


st.dataframe(cdru.style
    .set_table_styles([{'selector': 'thead', 'props': [('font-size', '5pt')]}])
    .set_properties(**{'font-family': 'PT Sans','border': '1.3px solid black','color': 'red','font-size': '10pt'
    })) #'background-color': 'black'

######################3
#Matrix maestra cuadro 2
cdrd = df

cdrd = pd.pivot_table(cdrd, index=['codctr', 'desnomctr', 'tiptecnologia'], columns=['day'], aggfunc='size', values='codofcadm')
cdrd = cdrd.reset_index()


cdrd = cdrd.astype(str)
cdrd = cdrd.replace('nan', 999999)
cdrd = cdrd.round().astype(float,errors='ignore')
cdrd = cdrd.apply(pd.to_numeric,downcast ='signed',errors='ignore')
cdrd = cdrd.astype(str)
cdrd = cdrd.replace('999999', '')


values_3 = ['209','210', '365']

values_4 = ['TRABAJOS PROGRAMADOS']

cdrd = cdrd[cdrd.codctr.isin(values_3)&~cdrd.desnomctr.isin(values_4)]


texto  = ('📊Cuadro de Bandeja GPON Reporte Actualizado:📊 \n\n⌚'+ actu)

st.markdown( f'<h1 style="color:#08298A;font-size:24px;">{texto}</h1>', unsafe_allow_html=True )


st.dataframe(cdrd.style
    .set_table_styles([{'selector': 'thead', 'props': [('font-size', '5pt')]}])
    .set_properties(**{'font-family': 'PT Sans','border': '1.3px solid black','color': 'red','font-size': '10pt'
    })) #'background-color': 'black'

#### el  cradro 3

values_3 = [353, 479]
cdrd = df[df.codctr.isin(values_3)]

values_4 = ['TRIAJE GPON']
cdrde = df[df.desnomctr.isin(values_4)]

union = pd.concat([cdrd, cdrde])

union = pd.pivot_table(union, index=['tiptecnologia','desnomctr'], columns=['day'], aggfunc='size', values='codofcadm')
union = union.reset_index()

union = union.astype(str)
union = union.replace('nan', 999999)
union = union.round().astype(float,errors='ignore')
union = union.apply(pd.to_numeric,downcast ='signed',errors='ignore')
union = union.astype(str)
union = union.replace('999999', '')

texto  = ('📊Cuadro de Bandeja GPON Reporte Actualizado:📊 \n\n⌚'+ actu)

st.markdown( f'<h1 style="color:#08298A;font-size:24px;">{texto}</h1>', unsafe_allow_html=True )


st.dataframe(union.style
    .set_table_styles([{'selector': 'thead', 'props': [('font-size', '5pt')]}])
    .set_properties(**{'font-family': 'PT Sans','border': '1.3px solid black','color': 'red','font-size': '10pt'
    })) #'background-color': 'black'






# CSS to inject contained in a string
hide_dataframe_row_index = """
            <style>
            .row_heading.level0 {display:none}
            .blank {display:none}
            </style>
            """

# Inject CSS with Markdown
st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)

###
####
####
####
######
######