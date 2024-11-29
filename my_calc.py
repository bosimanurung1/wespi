import streamlit as st
import pandas as pd
import pandasql as ps
import matplotlib.pyplot as plt
from new_calc2 import edit_and_add
from sessions import sessionstates
from my_calcb import my_calc_straight

mnomor1 = pd.read_csv('MNomor1.csv')
tmycalc = pd.read_csv('tmycalc.csv')
muserlogin = pd.read_csv('MUserLogin.csv')
minstrument = pd.read_csv('MInstrument.csv')
mcalcmethod = pd.read_csv('MCalcMethod.csv')
mwelltype = pd.read_csv('MWellType.csv')
mmeasurement = pd.read_csv('MMeasurement.csv')
mcasingsize = pd.read_csv('MCasingSize.csv')
mtubingsize = pd.read_csv('MTubingSize.csv')
mtubingid = pd.read_csv('MTubingID.csv')
mtubingcoeff = pd.read_csv('MTubingCoeff.csv')
df_ipr_data = pd.DataFrame(columns=['Flow rate', 'Pressure'])

mycalc3 = mycalc3a = mycalc3b = mycalc3c = mycalc4 = pd.DataFrame()
_id_calc = id_calc_02 = _id_instrument = 0
_pi = 0

sessionstates() # di sessions.py

st.title("My Calculations")

mycalc3 = ps.sqldf("select m.id_calc, m.user_id, u.username, m.well_name, m.field_name, m.company, m.engineer, \
        m.date_calc, m.id_instrument, i.instrument, m.id_calc_method, c.calc_method, m.id_welltype, \
        w.welltype, m.id_measurement, meas.measurement, m.comment_or_info, m.top_perfo_tvd, m.top_perfo_md, \
        m.bottom_perfo_tvd, m.bottom_perfo_md, m.qtest, m.sbhp, m.fbhp, m.producing_gor, m.wc, m.bht, \
        m.sgw, m.sgg, m.qdes, m.psd, m.whp, m.psd_md, m.p_casing, m.pb, m.api, m.sgo, m.sfl, m.smg, \
        m.id_casing_size, s.casing_size, s.casing_drift_id, m.id_tubing_size, tubsize.tubing_size, m.id_tubing_id, tubid.tubing_id, \
        m.id_tubing_coeff, tubcoef.type, tubcoef.coefficient, m.liner_id, m.top_liner_at_tvd, m.top_liner_at_md, \
        m.bottom_liner_at_tvd, m.bottom_liner_at_md \
        from tmycalc m \
            left join muserlogin u on m.user_id = u.user_id \
            left join minstrument i on m.id_instrument = i.id_instrument \
            left join mcalcmethod c on m.id_calc_method = c.id_calc_method \
            left join mmeasurement meas on m.id_measurement = meas.id_measurement \
            left join mwelltype w on m.id_welltype = w.id_welltype \
            left join mcasingsize s on m.id_casing_size = s.id_casing_size \
            left join mtubingsize tubsize on m.id_tubing_size = tubsize.id_tubing_size \
            left join mtubingid tubid on m.id_tubing_id = tubid.id_tubing_id \
            left join mtubingcoeff tubcoef on m.id_tubing_coeff = tubcoef.id_tubing_coeff") 
st.session_state["mycalc3"] = mycalc3

# mycalc3a is about to show simple fields
mycalc3a = ps.sqldf("select m.id_calc as 'ID Calculation', m.well_name as 'Well Name', m.field_name 'Field Name', w.welltype 'Well Type', \
        m.date_calc as 'Date Calculation', i.instrument as Instrument, c.calc_method as Method, meas.measurement as Meeasurement, \
        m.comment_or_info as Comment \
        from tmycalc m \
            left join muserlogin u on m.user_id = u.user_id \
            left join minstrument i on m.id_instrument = i.id_instrument \
            left join mcalcmethod c on m.id_calc_method = c.id_calc_method \
            left join mmeasurement meas on m.id_measurement = meas.id_measurement \
            left join mwelltype w on m.id_welltype = w.id_welltype")
# ---------- To Show ----------------------
st.dataframe(mycalc3a, hide_index=True)      

def search_to_explore():
    st.session_state.id_calc_01 = 0 #if search is not empty, explore will be empty

def explore_to_search():
    st.session_state._well_name_search = '' #if explore is not empty, search will be empty
    
col1, col2 = st.columns(2, gap="medium", vertical_alignment="top")
with col1:
    #_well_name_search = st.text_input('Well Name To Search: ', _well_name_search, None, key="_well_name_search", 
    _well_name_search = st.text_input('Well Name To Search: ', None, key="_well_name_search", 
                        on_change=search_to_explore)
with col2:
    #id_calc_01 = st.number_input("ID Calculation To Explore:", id_calc_01, None, "min", 1, 
    id_calc_01 = st.number_input("ID Calculation To Explore:", 0, None, "min", 1, key="id_calc_01", 
                        on_change=explore_to_search)  
        
st.write('')
if _well_name_search:
    #mycalc3b = mycalc3a[mycalc3a['well_name'].str.contains(_well_name_search)] # for minimalis, using mycalc3a
    mycalc3b = pd.DataFrame()
    mycalc3b = mycalc3[mycalc3['well_name'].str.contains(_well_name_search)]            
    #if len(mycalc3b)>0:
    if not mycalc3b.empty:
        st.subheader(f"Well Name Contains Word '{_well_name_search}'")
        mycalc3b = mycalc3[mycalc3['well_name'].str.contains(_well_name_search)]            
        mycalc3b = ps.sqldf("select m.id_calc as 'ID Calculation', m.well_name as 'Well Name', \
        m.field_name as 'Field Name', w.welltype 'Well Type', m.date_calc as 'Date Calculation', \
        i.instrument as Instrument, c.calc_method as Method, meas.measurement as Meeasurement, \
        m.comment_or_info as Comment, m.top_perfo_tvd, m.top_perfo_md, m.bottom_perfo_tvd, m.bottom_perfo_md, \
        m.qtest, m.sfl, m.smg, m.sbhp, m.fbhp, m.producing_gor, m.wc, m.bht, m.sgw, m.sgg, m.qdes, m.psd, m.whp, m.psd_md, \
        m.p_casing, m.pb, m.api, m.sgo, m.id_casing_size, s.casing_size, s.casing_drift_id, m.id_tubing_size, \
        tubsize.tubing_size, m.id_tubing_id, tubid.tubing_id, m.id_tubing_coeff, tubcoef.type, tubcoef.coefficient, \
        m.liner_id, m.top_liner_at_tvd, m.top_liner_at_md, m.bottom_liner_at_tvd, m.bottom_liner_at_md \
        from mycalc3b m \
            left join muserlogin u on m.user_id = u.user_id \
            left join minstrument i on m.id_instrument = i.id_instrument \
            left join mcalcmethod c on m.id_calc_method = c.id_calc_method \
            left join mmeasurement meas on m.id_measurement = meas.id_measurement \
            left join mwelltype w on m.id_welltype = w.id_welltype \
            left join mcasingsize s on m.id_casing_size = s.id_casing_size \
            left join mtubingsize tubsize on m.id_tubing_size = tubsize.id_tubing_size \
            left join mtubingid tubid on m.id_tubing_id = tubid.id_tubing_id \
            left join mtubingcoeff tubcoef on m.id_tubing_coeff = tubcoef.id_tubing_coeff") 
        st.dataframe(mycalc3b, hide_index=True)
        col1b, col2b = st.columns(2, gap="medium", vertical_alignment="top")
        with col1b:
            st.markdown("<p style='text-align: justify;'>Masukkan Nomor ID Calculation Untuk Diedit Detailnya \
                Lalu Disimpan Menjadi ID Calculation Baru/Lama :</p>", unsafe_allow_html=True)
        with col2b:
            id_calc_02 = st.number_input("ID Calculation To Edit :", 0, None, "min", 1)
            st.session_state["id_calc_02"] = id_calc_02
            #if st.button('Submit'):
            #    mycalc3c = mycalc3b[mycalc3b['id_calc']==id_calc_02]    
    else: #kenapa else ini gak berfungsi ya???
        st.subheader(f"There Is No Well Name Contains Word '{_well_name_search}'")

# --- edit n save to the same id or new id ----------                
if st.session_state["id_calc_02"]:
    mycalc3c = mycalc3[mycalc3['id_calc']==id_calc_02].reset_index(drop=True)
    if mycalc3c.shape[0]!=0:
        st.session_state["mycalc3c"] = mycalc3c
        edit_and_add() # di new_calc2.py, msh blm berhasil membersihkan hasil edit inputan
    else:
        if _well_name_search != '':
            st.write('')
            st.write('Data Tidak Ada')

# --- just explore ----    
if st.session_state["id_calc_01"]:
    mycalc4 = mycalc3.loc[mycalc3['id_calc']==st.session_state["id_calc_01"]].reset_index(drop=True)    

    _username = mycalc4['username'].values[0]; _well_name = mycalc4['well_name'].values[0]
    _field_name=mycalc4['field_name'].values[0]; _company=mycalc4['company'].values[0]; _engineer=mycalc4['engineer'].values[0]
    _date_calc=mycalc4['date_calc'].values[0]
    _instrument=mycalc4['instrument'].values[0]
    _id_instrument=mycalc4['id_instrument'].values[0]; st.session_state._id_instrument=mycalc4['id_instrument'].values[0]
    _calc_method=mycalc4['calc_method'].values[0]; _welltype=mycalc4['welltype'].values[0]
    _id_calc_method=mycalc4['id_calc_method'].values[0]; _id_welltype=mycalc4['id_welltype'].values[0]
    _measurement=mycalc4['measurement'].values[0]; st.session_state._measurement = _measurement
    _id_measurement=mycalc4['id_measurement'].values[0]; st.session_state._id_measurement = _id_measurement
    _comment_or_info=mycalc4['comment_or_info'].values[0]
    
    #st.write('id instrument=', _id_instrument, 'id calc methon=', _id_calc_method)
    st.title("General Information")
    col1, col2 = st.columns(2, gap="medium", vertical_alignment="top")
    with col1:
        st.subheader('ID Calculation:')
        st.markdown(st.session_state["id_calc_01"])
        st.subheader('Well Name:')
        st.markdown(_well_name)
        st.subheader('Field Name:')
        st.markdown(_field_name)
        #st.write('\n')
        st.subheader('Company:')
        st.markdown(_company)
        #st.write('\n')
        st.subheader('User Name:')
        st.markdown(_username)
        #st.write('\n')
        st.subheader('Engineer:')
        st.markdown(_engineer)
    with col2:
        st.subheader('Date Calculation:')
        st.markdown(_date_calc)
        st.subheader('Instrument:')
        st.markdown(_instrument)
        #st.write('\n')
        st.subheader('Calculation Method:')
        st.markdown(_calc_method)
        #st.write('\n')
        st.subheader('Well Type:')
        st.markdown(_welltype)
        #st.write('\n')
        st.subheader('Measurement:')
        if _measurement=='m':
            st.write('Meter (', _measurement, ')')
        elif _measurement=='ft':
            st.write('Feet (', _measurement, ')')
        #st.write('\n')
        st.subheader('Comment or Info:')
        st.markdown(_comment_or_info)
        #st.write('\n')

    _top_perfo_tvd=mycalc4['top_perfo_tvd'].values[0]; st.session_state._top_perfo_tvd = _top_perfo_tvd
    if _id_welltype == 1: # 1-Vertical, 2-Directional
        _top_perfo_md = _top_perfo_tvd; st.session_state._top_perfo_md = _top_perfo_tvd
    else:
        _top_perfo_md=mycalc4['top_perfo_md'].values[0]; st.session_state._top_perfo_md = _top_perfo_tvd

    _bottom_perfo_tvd=mycalc4['bottom_perfo_tvd'].values[0]; st.session_state._bottom_perfo_tvd = _bottom_perfo_tvd
    if _id_welltype == 1: # 1-Vertical, 2-Directional
        _bottom_perfo_md = _bottom_perfo_tvd; st.session_state._bottom_perfo_md = _bottom_perfo_tvd
    else:
        _bottom_perfo_md=mycalc4['bottom_perfo_md'].values[0]; st.session_state._bottom_perfo_md = _bottom_perfo_tvd

    _sbhp=mycalc4['sbhp'].values[0]; st.session_state._sbhp = _sbhp
    _fbhp=mycalc4['fbhp'].values[0]; st.session_state._fbhp = _fbhp
    _sfl=mycalc4['sfl'].values[0]; _smgFreeGasAtQtest=mycalc4['smg'].values[0]
    st.session_state._sfl = _sfl; st.session_state._smgFreeGasAtQtest = _smgFreeGasAtQtest
    
    _qtest=mycalc4['qtest'].values[0]; st.session_state._qtest = _qtest
    _producing_gor=mycalc4['producing_gor'].values[0]; st.session_state._producing_gor = _producing_gor
    _wc=mycalc4['wc'].values[0]; st.session_state._wc = _wc
    _bht=mycalc4['bht'].values[0]; st.session_state._bht = _bht
    _sgw=mycalc4['sgw'].values[0]; st.session_state._sgw = _sgw
    _sgg=mycalc4['sgg'].values[0]; st.session_state._sgg = _sgg
    _qdes=mycalc4['qdes'].values[0]; st.session_state._qdes = _qdes
    _psd=mycalc4['psd'].values[0]; st.session_state._psd = _psd
    _whp=mycalc4['whp'].values[0]; st.session_state._whp = _whp
    _psd_md=mycalc4['psd_md'].values[0]; st.session_state._psd_md = _psd_md
    
    _p_casing=mycalc4['p_casing'].values[0]; st.session_state._p_casing = _p_casing
    _pb=mycalc4['pb'].values[0];       
    _api=mycalc4['api'].values[0]; st.session_state._api = _api
    _sgo=mycalc4['sgo'].values[0]; st.session_state._sgo = _sgo

    _casing_size=mycalc4['casing_size'].values[0]; _casing_id=mycalc4['casing_drift_id'].values[0]
    _tubing_size=mycalc4['tubing_size'].values[0]; 
    _tubing_id=mycalc4['tubing_id'].values[0]; st.session_state._tubing_id = _tubing_id
    _tubing_coeff_type=mycalc4['type'].values[0]
    _coefficient=mycalc4['coefficient'].values[0]; st.session_state._coefficient = _coefficient

    _liner_id=mycalc4['liner_id'].values[0]; 
    _top_liner_at_tvd=mycalc4['top_liner_at_tvd'].values[0]
    if _id_welltype == 1: # 1-Vertical, 2-Directional
        _top_liner_at_md = _top_liner_at_tvd
    else:
        _top_liner_at_md=mycalc4['top_liner_at_md'].values[0]

    _bottom_liner_at_tvd=mycalc4['bottom_liner_at_tvd'].values[0] 
    if _id_welltype == 1: # 1-Vertical, 2-Directional
        _bottom_liner_at_md = _bottom_liner_at_tvd
    else:
        _bottom_liner_at_md=mycalc4['bottom_liner_at_md'].values[0]

    st.write('\n')
    st.title("Data Input")
    #col1, col2 = st.columns(2, gap="medium", vertical_alignment="top")    
    row3_1, row3_spacer, row3_2= st.columns((3, 1, 3))
    with row3_1:
        st.header("Basic Data (Required)", divider="gray")
        #st.write('Top Perfo: {} {} TVD'.format(_top_perfo_tvd, _measurement))
        st.write('Top Perfo    : ', _top_perfo_tvd, _measurement, 'TVD')
        st.write('Top Perfo    : ', _top_perfo_md, _measurement, 'MD')
        st.write('Bottom Perfo : ', _bottom_perfo_tvd, _measurement, 'TVD')
        st.write('Bottom Perfo : ', _bottom_perfo_md, _measurement, 'MD')          
        st.write('Qtest        : ', _qtest, 'BPD')
        if _id_instrument==1: # Downhole Sensor
            st.write('SBHP         : ', _sbhp, 'psig')
            st.write('FBHP         : ', _fbhp, 'psig')
        elif _id_instrument==2: # Sonolog
            st.write('SFL         : ', _sfl, _measurement)
            st.write('SMG Free Gas @ Qtest: ', _smgFreeGasAtQtest, _measurement)
        st.write('Producing GOR: ', _producing_gor, 'scf/stb')
        st.write('WC           : ', _wc, '%')
        st.write('BHT          : ', _bht, '℉')
        st.write('SGw          : ', _sgw)
        st.write('SGg          : ', _sgg)
        st.write('Qdes         : ', _qdes, 'BPD')
        st.write('PSD          : ', _psd, _measurement, 'TVD')
        st.write('PSD (MD)     : ', _psd_md, _measurement, 'MD')
        st.write('WHP          : ', _whp, 'psi')
        st.header("Basic Data (Optional)", divider="gray")
        st.write('P. Casing    : ', _p_casing, 'psi')
        st.write('Pb           : ', _pb, 'psig')
    with row3_2:
        st.header("API/Sgo", divider="gray")
        st.write('API          : ', round(_api, 3))
        st.write('Sgo          : ', round(_sgo, 3))
        st.write('\n')
        st.header("Casing & Tubing", divider="gray")
        st.write('Casing Size  : ', _casing_size)
        st.write('Casing Drift ID    : ', _casing_id, 'inch')
        st.write('Tubing Size  : ', _tubing_size)
        st.write('Tubing ID     : ', _tubing_id, 'inch')
        st.write('Tubing Coeffisien: ', _tubing_coeff_type)
        st.write('\n')
        st.header("Liner", divider="gray")
        st.write('Liner ID     : ', _liner_id, 'inch')
        st.write('Top Liner at : ', _top_liner_at_tvd, _measurement, 'TVD')
        st.write('Top Liner at : ', _top_liner_at_md, _measurement, 'MD')
        st.write('Bottom Liner at: ', _bottom_liner_at_tvd, _measurement, 'TVD')
        st.write('Bottom Liner at: ', _bottom_liner_at_md, _measurement, 'MD')

    #if _id_instrument==1 and _id_calc_method==2: #Downhole Sensor & Vogel    
    if _id_calc_method==2: # Vogel    
        #Hitung2an Calculation sblm IPR Curve    
        # Vt=Vo+Vg+Vw; Vo=(1-WC)*Qdes*Bo; Vg=Bg * Free Gas (FG); Vw=WC * Qdes
        # Bo=0.972+0.000147*((Rs*SQRT(SGg/Sgo)+1.25*BHT)^1.175); 
        # Rs=Sgg*(( (PIP/18) * (10^(0.0125*API – 0.00091*BHT)) ) ^1.2048)
        # PIP=Pwf@Qdes-(MidPerf-PSD)*SGFluid/2.31
        # MidPerf = 0.5(TopPerfoTVD+BottomPerfoTVD)
        # SGFluid = WC * SGw + (1 - WC) * Sgo
        
        # Bg=5.04*0.85*(BHT+460)/(PIP+14.7)   
        # Tg=(1-WC)*Qdes*ProducingGOR/1000;
        # Sg=(1-WC)*Qdes*Rs/1000
        # Free Gas (FG) = Tg - Sg; 

        # SGFluid = WC * SGw + (1 - WC) * Sgo
        #         = 88% * 1.02 + (1- 88%) * 0.887147335
        _sgfluid = (_wc/100) * _sgw + (1-(_wc/100)) * _sgo

        # sgfluid di atas, krn p_casing_hitung perlu dia utk perhitungan rumus     
        if _p_casing == 0:
            _p_casing_hitung = 0
        else:
            if _measurement=='m': # mtr (bila pilihan di awal nya adalah satuan meter, harus diconvert ke meter)
                _p_casing_hitung = (_p_casing * 2.31 / _sgfluid) / 3.28084 # -> utk jadi meter
            elif _measurement=='ft': # ft, biarkan saja, gak usah diconver (dibagi 3.28084 atu dikali 0.3048)
                _p_casing_hitung = (_p_casing * 2.31 / _sgfluid) # -> utk jadi feet

        # MidPerf = 0.5(TopPerfoTVD+BottomPerfoTVD)
        _MidPerf = 0.5 * (_top_perfo_tvd + _bottom_perfo_tvd)
        # 12Nov24
        if _id_measurement==1: # m (meter), bila inputnya mtr, karena _MidPerf hrs dlm ft, jadi diconvert dulu ke ft
            _MidPerf *= 3.28081 
        
        # di bawah ini gak jadi, krn ini hanya explore, ambil saja SBHP & FBHP yg tersimpan
        # to convert SFL & SMG (already in ft) into SBHP & FBHP
        if _id_instrument==2: # Sonolog
            _sbhp = _p_casing_hitung + _sgfluid / 2.31 * (_MidPerf - _sfl)
            _fbhp = _p_casing_hitung + _sgfluid / 2.31 * (_MidPerf - (_sfl+_smgFreeGasAtQtest))

        _qmax = _qtest / (1 - 0.2 * (_fbhp/_sbhp) - 0.8 * (_fbhp/_sbhp) ** 2)
        # _Pwf_at_Qdes = (5 * math.sqrt(3.24 - 3.2 * (_qdes/_qmax)) - 1) / 8 * _sbhp --> library math susah diDeploy
        _Pwf_at_Qdes = (5 * (3.24 - 3.2 * (_qdes/_qmax))**0.5 - 1) / 8 * _sbhp

        #12Nov24 sblm hitung pip hrs convert psd tvd dan psd md yg meter ke ft
        if _measurement=='m': # m (meter)
            # PIP=Pwf@Qdes-(MidPerf-PSD)*SGFluid/2.31    
            _pip = _Pwf_at_Qdes - ((_MidPerf - (_psd * 3.28084)) * (_sgfluid/2.31)) 
        elif _measurement=='ft': # feet
              _pip = _Pwf_at_Qdes - ((_MidPerf - _psd) * (_sgfluid/2.31)) 

        # Rs=Sgg*(( (PIP/18) * (10^(0.0125*API – 0.00091*BHT)) )^1.2048)
        _Rs=_sgg*(( (_pip/18) * (10**(0.0125*_api - 0.00091*_bht)) )**1.2048)
    
        # Bo=0.972+0.000147*((Rs*SQRT(SGg/Sgo)+1.25*BHT)^1.175); 
        # _Bo = 0.972+0.000147*((_Rs*math.sqrt(_sgg/_sgo)+1.25*_bht)**1.175) --> math masalah diDeploy
        _Bo = 0.972+0.000147*((_Rs * (_sgg/_sgo)**0.5 + 1.25 * _bht) ** 1.175)
        # Vo=(1-WC)*Qdes*Bo;
        _Vo = (1-(_wc/100))*_qdes*_Bo;
    
        # Bg=5.04*0.85*(BHT+460)/(PIP+14.7) -> yg benar kurung nya sprti di bawah
        _Bg=5.04*0.85*((_bht+460)/(_pip+14.7))
        # Tg=(1-WC)*Qdes*ProducingGOR/1000;
        _Tg=(1-(_wc/100))*_qdes*_producing_gor/1000
        #Sg=(1-WC)*Qdes*Rs/1000
        _Sg=(1-(_wc/100))*_qdes*_Rs/1000
        # Free Gas (FG) = Tg - Sg;
        _free_gas = _Tg - _Sg
        # Vg=Bg * Free Gas (FG);
        _Vg = _Bg * _free_gas
    
        # Vw=WC * Qdes
        _Vw = (_wc/100) * _qdes
    
         # Vt=Vo+Vg+Vw;
        _Vt = _Vo + _Vg + _Vw
    
        # _composite_sg = ( ( (1-WC)*Qdes*Sgo + WC*Qdes*Sgw) * 62.4*5.6146 + Producing GOR*(1-WC)*Qdes*Sgg*0.0752) / (Vt*5.6146*62.4)
        _composite_sg = ( ( (1-(_wc/100))*_qdes*_sgo + (_wc/100)*_qdes*_sgw) * 62.4*5.6146 + _producing_gor*(1-(_wc/100))*_qdes*_sgg*0.0752) / (_Vt*5.6146*62.4)
    
        # WFL =PSD-(PIP*2.31/SGFluid)
        if _measurement=='m': # PSD nya dikali 3.28084 dulu (dikonversi ke ft krn PSD hrs dlm ft)
            _wfl = (_psd*3.28084)-(_pip*2.31/_sgfluid)
            # lalu dirubah lgi ke mtr:
            _wfl = _wfl * 0.3048 # 0.3048 adalah 1/3.28084
        elif _measurement=='ft': # PSD nya gak perlu dikali 3.28084 dulu
            _wfl = _psd-(_pip*2.31/_sgfluid)

        # WHP = THP(WHP)*2.31/SGFluid (whp sdh diinput dlm pressure)
        if _id_measurement==1: # m (meter)        
            _whp_hitung=_whp*2.31/_sgfluid
            _whp_hitung *= 0.3048 # diconvert ke m (meter), krn saat ini hasil hitungannya dlm ft
        elif _id_measurement==2: # ft (bila input awal pilihannya ft, biarkan saja, gak usah diconvert)        
            _whp_hitung=_whp*2.31/_sgfluid

        # Friction Loss = (2.083*(100/TubingCoeff)^1.85*(Qdes         /34.3)^1.85/TubingID^4.8655)  *PSDft/1000
        #_friction_loss = (2.083*(100/_coefficient)**1.85*(_qdes/34.3)**1.85/_tubing_id**4.8655)*_psd/1000
        if _id_measurement==1: # m (meter), PSD nya dikali 3.28084 dulu (dikonversi ke ft krn PSD hrs dlm ft)        
            _friction_loss = (2.083*(100/_coefficient)**1.85*(_qdes/34.3)**1.85/_tubing_id**4.8655)*(_psd*3.28084)/1000
            # lalu dirubah lgi ke mtr sesuai apa yg diinput di awal (yg diinginkan dlm mtr)
            _friction_loss *= 0.3048        
        elif _id_measurement==2: # ft (tdk perlu diconvert)
            _friction_loss = (2.083*(100/_coefficient)**1.85*(_qdes/34.3)**1.85/_tubing_id**4.8655)*_psd/1000
    
        # % Free Gas = Vg / Vt
        _persen_free_gas = (_Vg / _Vt) * 100
    
        # TDH = sum(WFL, WHP, CP, FrictionLoss)  --> CP (Optional, bila tdk dinput, defaultnya nol) 
        #_tdh = _wfl + _whp_hitung + _cp + _friction_loss
        _tdh = _wfl + _whp_hitung + _p_casing_hitung + _friction_loss # cp dihapus, jadi kalau perlu cp, diganti dgn p.casing
    
        #Fluid Over Pump = (PIP-CP)*2.31/SGFluid
        #_fluid_over_pump = (_pip - _cp)*2.31/_sgfluid
        _fluid_over_pump = (_pip - _p_casing_hitung)*2.31/_sgfluid # cp dihapus, jadi kalau perlu cp, diganti dgn p.casing
    
        # Fluid Gradient = SGFluid/2.31
        _fluid_gradient = _sgfluid/2.31
    
        # ---------- Counting data for ipr_curve (2Fields, 8Records) ----------------------- 
        #_flowrate1 = (1-0.2*(Pressure1 / SBHP) - 0.8 * (Pressure1 / SBHP)^2) * Qmax
        _pressure1 = 0
        _flowrate1 = (1-0.2*(_pressure1 / _sbhp) - 0.8 * (_pressure1 / _sbhp)**2) * _qmax
    
        #_flowrate2 = (1-0.2*(Pressure2 / SBHP) - 0.8 * (Pressure2 / SBHP)^2) * Qmax
        #_pressure2 = (MidPerfo - PSD) * SGFluid / 2.31 + CP
        #_pressure2 = (_MidPerf - _psd) * _sgfluid / 2.31 + _cp 
        _pressure2 = (_MidPerf - _psd) * _sgfluid / 2.31 + _p_casing_hitung # cp dihapus, jadi kalau perlu cp, diganti dgn p.casing
        _flowrate2 = (1-0.2*(_pressure2 / _sbhp) - 0.8 * (_pressure2 / _sbhp)**2) * _qmax
    
        #_flowrate3 = (1-0.2*(Pressure3 / SBHP) - 0.8 * (Pressure3 / SBHP)^2) * Qmax
        #_pressure3 = 0.2 * SBHP
        _pressure3 = 0.2 * _sbhp
        _flowrate3 = (1-0.2*(_pressure3 / _sbhp) - 0.8 * (_pressure3 / _sbhp)**2) * _qmax
    
        #_flowrate4 = (1-0.2*(Pressure4 / SBHP) - 0.8 * (Pressure4 / SBHP)^2) * Qmax
        #_pressure4 = 0.4 * SBHP
        _pressure4 = 0.4 * _sbhp
        _flowrate4 = (1-0.2*(_pressure4 / _sbhp) - 0.8 * (_pressure4 / _sbhp)**2) * _qmax
    
        #_flowrate5 = (1-0.2*(Pressure5 / SBHP) - 0.8 * (Pressure5 / SBHP)^2) * Qmax
        #_pressure5 = Pwf@Qdes
        _pressure5 = _Pwf_at_Qdes
        _flowrate5 = (1-0.2*(_pressure5 / _sbhp) - 0.8 * (_pressure5 / _sbhp)**2) * _qmax
    
        #_flowrate6 = (1-0.2*(Pressure6 / SBHP) - 0.8 * (Pressure6 / SBHP)^2) * Qmax
        #_pressure6 = 0.6 * SBHP
        _pressure6 = 0.6 * _sbhp
        _flowrate6 = (1-0.2*(_pressure6 / _sbhp) - 0.8 * (_pressure6 / _sbhp)**2) * _qmax
    
        #_flowrate7 = (1-0.2*(Pressure7 / SBHP) - 0.8 * (Pressure7 / SBHP)^2) * Qmax
        #_pressure7 = 0.8 * SBHP
        _pressure7 = 0.8 * _sbhp
        _flowrate7 = (1-0.2*(_pressure7 / _sbhp) - 0.8 * (_pressure7 / _sbhp)**2) * _qmax
    
        #_flowrate8 = (1-0.2*(Pressure8 / SBHP) - 0.8 * (Pressure8 / SBHP)^2) * Qmax
        #_pressure8 = SBHP
        _pressure8 = _sbhp
        _flowrate8 = (1-0.2*(_pressure8 / _sbhp) - 0.8 * (_pressure8 / _sbhp)**2) * _qmax
    
        df_ipr_data = pd.DataFrame({'Flow rate': [_flowrate1, _flowrate2, _flowrate3, _flowrate4, _flowrate5 \
                                    , _flowrate6, _flowrate7, _flowrate8],
                                    'Pressure': [_pressure1, _pressure2, _pressure3, _pressure4, _pressure5 \
                                    , _pressure6, _pressure7, _pressure8]})
            
        df_ipr_data = df_ipr_data.sort_values(by=['Flow rate', 'Pressure'], ascending=[False, True])
        # ---------------------------- until here -----------------------------------------        

        # ---------- Counting data for Flowrate di PSD (2Fields, 4Records) ----------------------- 
        _pressure1b = _pressure2
        _flowrate1b = 0
        
        _pressure2b = _pressure2
        _flowrate2b = _flowrate2
        
        _pressure3b = _pressure2b
        _flowrate3b = _flowrate2b
        
        _pressure4b = 0
        _flowrate4b = _flowrate2b
        
        df_flowrate_psd = pd.DataFrame({'Flow rate': [_flowrate1b, _flowrate2b, _flowrate3b, _flowrate4b],
                'Pressure': [_pressure1b, _pressure2b, _pressure3b, _pressure4b]})
            
        df_flowrate_psd = df_flowrate_psd.sort_values(by=['Flow rate', 'Pressure'], ascending=[True, False])
        # ---------------------------- until here -----------------------------------------        
        
        # ---------- Counting data for Flowrate di Pwf@Qdes (2Fields, 4Records) ----------------------- 
        _flowrate1c = 0
        _pressure1c = _Pwf_at_Qdes
   
        _flowrate2c = _flowrate5
        _pressure2c = _Pwf_at_Qdes

        _flowrate3c = _flowrate5
        _pressure3c = _Pwf_at_Qdes

        _flowrate4c = _flowrate5
        _pressure4c = 0
        
        df_flowrate_PwfQdes = pd.DataFrame({'Flow rate': [_flowrate1c, _flowrate2c, _flowrate3c, _flowrate4c],
                'Pressure': [_pressure1c, _pressure2c, _pressure3c, _pressure4c]})
            
        df_flowrate_PwfQdes = df_flowrate_PwfQdes.sort_values(by=['Flow rate', 'Pressure'], ascending=[True, False])
        # ---------------------------- until here -----------------------------------------            
    
        st.write('\n')
        st.title("Calculation")
        col1, col2 = st.columns(2, gap="medium", vertical_alignment="top")
        with col1:
           st.write("Pwf@Qdes: ", round(_Pwf_at_Qdes,3), 'psi')
           st.write('Qdes         : ', _qdes, 'BPD')
           st.write('Composite SG : ', round(_composite_sg,3)) #, '(selisih/beda 0.0003 lbh kecil)')
           #st.write('Di file xls: 0.490859')
           #st.write('\n')
        
           st.write('PSD          : ', _psd, _measurement, 'TVD')
           st.write('WFL          : ', round(_wfl,3), _measurement, 'TVD')
           #st.write('Di file xls: 4744.936')
           #st.write('Hitung2an:')
           #st.write('WFL = PSD - (PIP * 2.31 / SGFluid)')
           #st.write('=', _psd, '- ((', _pip, '* 2.31) /', _sgfluid)
           #st.write('=', _psd, '-', (_pip * 2.31), '/', _sgfluid)
           #st.write('=', _psd, '-', (_pip * 2.31) / _sgfluid)
           #st.write('=', round(_psd - (_pip * 2.31) / _sgfluid, 2), '(selisih/beda 1.6 lbh kecil)')
           #st.write('\n')
           
           st.write('Qmax         : ', round(_qmax,3), 'BPD')
           st.write('WHP          : ', round(_whp_hitung,3), _measurement, 'TVD')
           #st.write('Di file xls: 345.0997')
           #st.write('Hitung2an WHP:')
           #st.write('WHP = THP * 2.31 / SGFluid')
           #st.write('= (', _whp, '* 2.31) /', _sgfluid)
           #st.write('=', _whp * 2.31, '/', _sgfluid)
           #st.write('=', round((_whp * 2.31) / _sgfluid, 2), '(selisih/beda 0.3 lbh besar)')
           #st.write('\n')
        
           #st.write('SG Fluid = WC * SGw + (1 - WC) * Sgo')
           #st.write('= (', _wc, '/100) * ', _sgw, '+ (1 - (',  _wc, '/100)) * ', _sgo)
           #st.write('= ', _wc/100,' * ', _sgw, '+ (1 - ', _wc/100, ') * ', _sgo)
           #st.write('= ', _wc/100,' * ', _sgw, '+ ', 1 - (_wc/100), ' * ', _sgo)
           #st.write('= ', (_wc/100) * _sgw, '+ ', (1 - (_wc/100)) * _sgo)
           #_sgfluid = (_wc/100) * _sgw + (1-(_wc/100)) * _sgo
           st.write('SG Fluid     : ', round(_sgfluid,3))
           #st.write('Di file xls: 1.004')
           #st.write('\n')
           
           st.write('PIP          : ', round(_pip,3), 'psi')
           #st.write('Di file xls: 523.7896')
           #st.write('Hitung2an:')
           #st.write('PIP = Pwf@Qdes - (MidPerf - PSD) * SGFluid / 2.31')
           #st.write('MidPerf = 0.5(TopPerfoTVD + BottomPerfoTVD)')
           #st.write('= 0.5 (', _top_perfo_tvd, '+ ', _bottom_perfo_tvd, ')')
           #st.write('= 0.5 (', _top_perfo_tvd + _bottom_perfo_tvd, ')')        
           #st.write('=', 0.5 * (_top_perfo_tvd + _bottom_perfo_tvd))
           #st.write('PIP = Pwf@Qdes - (MidPerf - PSD) * SGFluid / 2.31')
           #st.write('= ', _Pwf_at_Qdes, '- (', _MidPerf, '- ', _psd, ') * (',  _sgfluid, '/ 2.31)') 
           #st.write('=', _Pwf_at_Qdes, '-', _MidPerf - _psd, '*',  _sgfluid/2.31 )
           #st.write('=', _Pwf_at_Qdes, '-', (_MidPerf - _psd) * (_sgfluid/2.31) )
           #st.write('=', round(_Pwf_at_Qdes - ((_MidPerf - _psd) * (_sgfluid/2.31)), 2), 'psi (selisih/beda 0.3 lbh besar)')
           #_pip = _Pwf_at_Qdes - (_MidPerf - _psd) * (_sgfluid/2.31) 
        
        with col2:
           st.write('P. Casing    : ', _p_casing_hitung, _measurement, 'TVD')
           st.write('Friction Loss: ', round(_friction_loss,3), _measurement, 'TVD')
           st.write('% Free Gas     : ', round(_persen_free_gas,3), '%')
           #st.write('Di file xls: 51.80 %')
           #st.write('Hitung2an % Free Gas:')
           #st.write('Free Gas = (Vg / Vt) * 100')
           #st.write('= (', _Vg, '/', _Vt, ') * 100')
           #st.write('=', round((_Vg / _Vt) * 100, 2), '(selisih/beda 0.01 lbh kecil)')
           #st.write('\n')
        
           st.write('TDH            : ', round(_tdh,3), _measurement, 'TVD')
           #st.write('Di file xls: 5376.58')
           #st.write('Hitung2an TDH:')
           #st.write('= WFL + WHP + CP + FrictionLoss')
           #st.write('CP Optional, bila tdk dinput, defaultnya nol')
           #st.write('=', _wfl, '+', _whp_hitung, '+', _cp, '+', _friction_loss)
           #st.write('=', round(_wfl + _whp_hitung + _cp + _friction_loss, 2), '(selisih/beda 1.2 lbh kecil)')
           #st.write('\n')
        
           st.write('SBHP           : ', round(_sbhp, 3), 'psig')
           st.write('Fluid Over Pump: ', round(_fluid_over_pump,3), _measurement, 'TVD')
           #st.write('Di file xls: 1205.1334')
           #st.write('Hitung2an Fluid Over Pump:')
           #st.write('= (PIP - CP) * 2.31 / SGFluid')
           #st.write('= ((', _pip, '-', _cp, ') * 2.31) /', _sgfluid)
           #st.write('= (', _pip - _cp, '* 2.31) /', _sgfluid)
           #st.write('=', (_pip - _cp) * 2.31, '/', _sgfluid)
           #st.write('=', round(((_pip - _cp) * 2.31) / _sgfluid, 2), '(selisih/beda 1.48 lbh besar)')
           #st.write('\n')
        
           st.write('FBHP           : ', round(_fbhp, 3), 'psig')
           st.write('Fluid Gradient : ', round(_fluid_gradient,3), 'psi/', _measurement, 'TVD')
           #st.write('Di file xls: 0.43463 (selisih/beda 0.0004 lbh kecil)')
    
        st.write('\n')
        st.title("Inflow Performance Relationships")    
        #row5_1, row5_spacer2, row5_2= st.columns((11.1, .1, 3.8))
        #with row5_1:
        # perbesar figsize
        #plt.figure(figsize=(20,10))
        plt.figure(figsize=(5,2))

        fig, ax  = plt.subplots()

        # membuat line plot for IPR
        plt.plot(df_ipr_data['Flow rate'], df_ipr_data['Pressure'], 'or:') 
        # membuat line plot for PSD
        plt.plot(df_flowrate_psd['Flow rate'], df_flowrate_psd['Pressure'], 'ob:')
        # membuat line plot for PwfQdes
        plt.plot(df_flowrate_PwfQdes['Flow rate'], df_flowrate_PwfQdes['Pressure'], 'og:')
     
        # set title & label
        plt.xlabel('Flow rate, Q (BFPD)',fontsize=13,color='darkred')
        plt.ylabel('Pressure (psi)',fontsize=13,color='darkred')
     
        # custom line
        plot_line = plt.plot(df_ipr_data['Flow rate'], df_ipr_data['Pressure']) # for IPR
        plot_line2 = plt.plot(df_flowrate_psd['Flow rate'], df_flowrate_psd['Pressure']) # for PSD
        plot_line3 = plt.plot(df_flowrate_PwfQdes['Flow rate'], df_flowrate_PwfQdes['Pressure']) # for PSD
        plt.setp(plot_line, color='red', linestyle=':',  linewidth=0.1, marker='o') # for IPR
        plt.setp(plot_line2, color='blue', linestyle=':',  linewidth=0.1, marker='o') # for PSD
        plt.setp(plot_line3, color='green', linestyle=':',  linewidth=0.1, marker='o') # for PSD

        # set start 0 y axis
        plt.ylim(ymin=0)
        plt.xlim(xmin=0)

        # set grid
        #plt.grid(color='darkgray', linestyle=':', linewidth=0.5)
        plt.grid(color='darkgray', linestyle=':', linewidth=0.3)

        #plt.legend(bbox_to_anchor=(0.75,0.75)) #persentase x,y
        #plt.legend()
        #ax.legend()
        #legend = ax.legend(loc="upper right", bbox_to_anchor=(1.02, 0, 0.07, 1))
        plt.gca().legend()

        st.pyplot(fig)
        #st.pyplot(plt.gcf())

        #with row5_2:
        #    st.dataframe(df_ipr_data, hide_index=True)
        #    st.write('')
    
    elif _id_calc_method==1: # Straight Line
        my_calc_straight()
        st.write('')
