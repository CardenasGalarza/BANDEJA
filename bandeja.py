import pandas as pd  # pip install pandas openpyxl
import streamlit as st  # pip install streamlit
import streamlit_authenticator as stauth  # pip install streamlit-authenticator
import gspread
import database as db


# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:")# layout="wide"


# --- USER AUTHENTICATION ---
users = db.fetch_all_users()

usernames = [user["key"] for user in users]
names = [user["name"] for user in users]
hashed_passwords = [user["password"] for user in users]

authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
    "sales_dashboard", "abcdef", cookie_expiry_days=30)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")

if authentication_status:

    # ---- SIDEBAR ----
    authenticator.logout("Logout", "sidebar")
    st.sidebar.title(f"Welcome {name}")
    st.sidebar.header("Please Filter Here:")

    # title of the app
    st.title("PROCESOS DE DATOS POR BANDEJA")


    gc = gspread.service_account(filename='datacargar-947843f340e2.json')
    sh = gc.open("Gpon_ticket_WEB")


    #  el 0 simbol del numero de hoja en este caso es la primera hoja = 0
    worksheet = sh.get_worksheet(0)


    # ver datos de google sheet
    df = pd.DataFrame(worksheet.get_all_records())


    df = df.fillna(0).apply(pd.to_numeric, errors='ignore')
    #print(df)
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


    texto  = ('📊Cuadro de Bandeja GPON HFC RESUMEN 1 Actualizado:📊 \n\n⌚'+ actu)

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

    texto  = ('📊Cuadro de Bandeja GPON HFC RESUMEN 2 Actualizado:📊 \n\n⌚'+ actu)

    st.markdown( f'<h1 style="color:#08298A;font-size:24px;">{texto}</h1>', unsafe_allow_html=True )


    st.dataframe(union.style
        .set_table_styles([{'selector': 'thead', 'props': [('font-size', '5pt')]}])
        .set_properties(**{'font-family': 'PT Sans','border': '1.3px solid black','color': 'red','font-size': '10pt'
        })) #'background-color': 'black'



## borrar nombres de la pagina
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.markdown(
    """
    <style>

    header .css-1595djx e8zbici2{
    display: flex;
    flex-direction: column;
    align-items: center;
    }

    header .logo-text{
        margin: 0;
        padding: 10px 26px;
        font-weight: bold;
        color: rgb(60, 255, 0);
        font-size: 0.8em;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <header class="css-1595djx e8zbici2">
        <p class="logo-text">App Alarmas 👨🏻‍💻Giancarlos .C</p>
    </header>
    """,
    unsafe_allow_html=True
)
texto  = ('🔒Estamos mejorando la privacidad de la información, si aún no cuentas con tus credenciales, comunicarte con:')
st.caption( f'<h6 style="color:#08298A;">{texto}</h6>', unsafe_allow_html=True )

textoo = ('\n\n👨🏻‍💻Luis Llerena. \n\n👨🏻‍💻Giancarlos Cardenas.')
st.caption( f'<h6 style="color:#08298A;">{textoo}</h6>', unsafe_allow_html=True )
###
####
####
####
######
######
