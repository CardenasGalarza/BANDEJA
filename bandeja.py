import streamlit as st
import gspread
import pandas as pd


# configuration
st.set_option('deprecation.showfileUploaderEncoding', False)

#st.set_page_config( layout='wide' )

# title of the app
st.title("PROCESOS POR BANDEJA")


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
df = pd.pivot_table(df, index=['desnomctr', 'tiptecnologia'], columns=['day'], aggfunc='size', values='codofcadm')
df = df.reset_index()


df = df.astype(str)
df = df.replace('nan', 999999)
df = df.round().astype(float,errors='ignore')
df = df.apply(pd.to_numeric,downcast ='signed',errors='ignore')
df = df.astype(str)
df = df.replace('999999', '')

####cuadro 1 tod1

values_1=['GPON']
values_2=['FIBRA','GAC-VOIP','MTTO TRABAJOS PROGRAMADOS','TRATAMIENTO CALL PIN TV-M1','INFOPYME PERU SAC','TRIAJE','2DA LINEA TRIAJE','BACK OFFICE','TRIAJE GPON']
tod1 = df[df.tiptecnologia.isin(values_1)&df.desnomctr.isin(values_2)]

texto  = ('📊Cuadro de Bandeja GPON Reporte Actualizado:📊 \n\n⌚'+ actu)

st.markdown( f'<h1 style="color:#08298A;font-size:24px;">{texto}</h1>', unsafe_allow_html=True )




st.dataframe(tod1.style
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