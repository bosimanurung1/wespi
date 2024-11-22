import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from csv import writer
from sessions import sessionstates
from new_calcb import new_calc_straight

#open datas
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
df_temp = pd.DataFrame()

st.title("Add New Calculation")
new_records = []

if "new_id_calc" not in st.session_state:
    last_id_calc = mnomor1['tmycalc'].values[0]
    st.session_state["new_id_calc"] = last_id_calc

sessionstates() # di sessions.py
   
col1, col2 = st.columns(2, gap="medium", vertical_alignment="top")
with col1:
    _well_name = ''; _field_name = ''; _company = ''; _engineer = ''
    _username_list = muserlogin['username'].unique().tolist() 
    last_id_calc = _user_id = 0
    
    _username = st.selectbox("Username: ", _username_list)
    _date_calc = st.date_input("Date Input: ")
    _well_name = st.text_input("Well Name:"); st.session_state._well_name = _well_name
    _field_name = st.text_input('Field Name:'); st.session_state._field_name = _field_name
    _company = st.text_input('Company:'); st.session_state._company = _company
    _engineer = st.text_input('Engineer: '); st.session_state._engineer = _engineer
    
with col2:
    _id_instrument = _id_calc_method = _id_measurement = 0
    _instrument_list = minstrument['instrument'].unique().tolist() 
    _calc_method_list = mcalcmethod['calc_method'].unique().tolist(); _welltype_list = mwelltype['welltype'].unique().tolist()
    _measurement_list =  mmeasurement['measurement'].unique().tolist()
    _comment_or_info = ''
    
    _instrument = st.selectbox("Instrument: ", _instrument_list); st.session_state._instrument = _instrument
    _calc_method = st.selectbox("Calculation Method: ", _calc_method_list); st.session_state._calc_method = _calc_method
    _welltype = st.selectbox("Well Type: ", _welltype_list); st.session_state._welltype = _welltype
    _measurement = st.selectbox("Unit Measurement: ", _measurement_list); st.session_state._measurement = _measurement
    _comment_or_info = st.text_input('Comment or Info: '); st.session_state._comment_or_info = _comment_or_info
    
    mycalc_temp = muserlogin.loc[muserlogin['username']==_username].reset_index(drop=True)
    _user_id = mycalc_temp['user_id'].values[0]; st.session_state._user_id = _user_id
    
    mycalc_temp = minstrument.loc[minstrument['instrument']==_instrument].reset_index(drop=True)
    _id_instrument = mycalc_temp['id_instrument'].values[0]; st.session_state._id_instrument = _id_instrument
    
    mycalc_temp = mcalcmethod.loc[mcalcmethod['calc_method']==_calc_method].reset_index(drop=True)
    _id_calc_method = mycalc_temp['id_calc_method'].values[0]; st.session_state._id_calc_method = _id_calc_method
    
    mycalc_temp = mwelltype.loc[mwelltype['welltype']==_welltype].reset_index(drop=True)
    _id_welltype = mycalc_temp['id_welltype'].values[0]; st.session_state._id_welltype = _id_welltype
    
    mycalc_temp = mmeasurement.loc[mmeasurement['measurement']==_measurement].reset_index(drop=True)
    _id_measurement = mycalc_temp['id_measurement'].values[0]; st.session_state._id_measurement = _id_measurement     

#inputing basic data (required), etc.        
row3_1, row3_spacer, row3_2= st.columns((3, 1, 3))
with row3_1:
    _top_perfo_tvd = _top_perfo_md = _bottom_perfo_tvd = _bottom_perfo_md = 0.00
    _qtest = _sbhp = _fbhp = _sfl = _smgFreeGasAtQtest = _producing_gor = _wc = _bht = 0.00
    _sgw = _sgg = _qdes = _psd = _whp = _psd_md = 0.00
    
    st.header("Basic Data (Required)", divider="gray")
    _top_perfo_tvd = st.number_input(f"Top Perfo ({_measurement} TVD)", 0.00, None, 'min', 1.00, format="%0.2f")
    st.session_state._top_perfo_tvd = _top_perfo_tvd
   
    if _id_welltype == 1: # 1-Vertical, 2-Directional
        _top_perfo_md = _top_perfo_tvd; st.session_state._top_perfo_md = st.session_state._top_perfo_tvd
        st.write(f'Top Perfo ({_measurement} MD) : {_top_perfo_md:.2f}')
    else:
        _top_perfo_md = st.number_input(f'Top Perfo ({_measurement} MD)', 0.00, None, 'min', 1.00, format="%0.2f")
        st.session_state._top_perfo_md = _top_perfo_md
        
    _bottom_perfo_tvd = st.number_input(f'Bottom Perfo ({_measurement} TVD)', 0.00, None, 'min', 1.00, format="%0.2f")
    st.session_state._bottom_perfo_tvd = _bottom_perfo_tvd
    if _id_welltype == 1: # 1-Vertical, 2-Directional
        _bottom_perfo_md = _bottom_perfo_tvd; st.session_state._bottom_perfo_md = st.session_state._bottom_perfo_tvd
        st.write(f'Bottom Perfo ({_measurement} MD) : {_bottom_perfo_md:.2f}')
    else:
        _bottom_perfo_md = st.number_input(f'Bottom Perfo ({_measurement} MD)', 0.00, None, 'min', 1.00, format="%0.2f")
        st.session_state._bottom_perfo_md = _bottom_perfo_md
    
    _qtest = st.number_input('Qtest (BPD)', 0.00, None, 'min', 1.00, format="%0.2f"); st.session_state._qtest = _qtest
    
    if _id_instrument == 1: # Downhole Sensor
        _sbhp = st.number_input('SBHP (psig)', 0.00, None, 'min', 1.00, format="%0.2f"); st.session_state._sbhp = _sbhp
        _fbhp = st.number_input('FBHP (psig)', 0.00, None, 'min', 1.00, format="%0.2f"); st.session_state._fbhp = _fbhp
    elif _id_instrument == 2: # Sonolog
         _sfl = st.number_input(f'SFL ({_measurement})', _sfl, None, 'min', 1.00, format="%0.2f"); st.session_state._sfl = _sfl
         _smgFreeGasAtQtest = st.number_input(f'SMG Free Gas @ Qtest ({_measurement})', _smgFreeGasAtQtest, None, 'min', 1.00, format="%0.2f")
         st.session_state._smgFreeGasAtQtest = _smgFreeGasAtQtest
    _producing_gor = st.number_input('Producing GOR (scf/stb)', 0.00, None, 'min', 1.00, format="%0.2f")
    st.session_state._producing_gor = _producing_gor
    _wc = st.number_input('WC (%)', 0.00, None, 'min', 1.00, format="%0.2f"); st.session_state._wc = _wc
    _bht = st.number_input('BHT (℉)', 0.00, None, 'min', 1.00, format="%0.2f"); st.session_state._bht = _bht
    _sgw = st.number_input('SGw', 0.00, None, 'min', 1.00, format="%0.2f"); st.session_state._sgw = _sgw
    _sgg = st.number_input('SGg', 0.00, None, 'min', 1.00, format="%0.2f"); st.session_state._sgg = _sgg
    _qdes = st.number_input('Qdes (BPD)', 0.00, None, 'min', 1.00, format="%0.2f"); st.session_state._qdes = _qdes
    _psd = st.number_input(f'PSD ({_measurement} TVD)', 0.00, None, 'min', 1.00, format="%0.2f"); st.session_state._psd = _psd
    
    st.session_state._psd = _psd
    if _id_welltype == 1: # Vertical
        _psd_md = _psd; st.session_state._psd_md = st.session_state._psd
        st.write(f'PSD ({_measurement} MD) : {_psd:.2f}')
    else:
        _psd_md = st.number_input(f'PSD ({_measurement} MD)', 0.00, None, 'min', 1.00, format="%0.2f")    
        st.session_state._psd_md = _psd_md
    _whp = st.number_input('WHP (psi)', 0.00, None, 'min', 1.00, format="%0.2f"); st.session_state._whp = _whp

with row3_2:
    _p_casing = _pb = 0.00

    st.header("Basic Data (Optional)", divider="gray")
    _p_casing = st.number_input('P. Casing (psi)', 0.00, None, 'min', 1.00, format="%0.2f"); st.session_state._p_casing = _p_casing
    _pb = st.number_input('Pb (psig)', 0.00, None, 'min', 1.00, format="%0.2f"); st.session_state._pb = _pb
    #_cp = st.number_input('CP (psi)', 0.00, None, 'min', 1.00, format="%0.2f")
    # cp itu sama dgn p.casing, jadi utk hitung cp gunakan p.casing
    
    st.header("API/Sgo", divider="gray")
    def lbs_to_kg(): # api to sgo
        st.session_state.kg = 141.5/(131.5 + st.session_state.lbs)

    def kg_to_lbs(): # sgo to api
        st.session_state.lbs = 141.5/st.session_state.kg - 131.5
        
    # ------------- now how callback work ---------------
    col1, buff, col2 = st.columns([2,1,2])
    with col1:
        pounds = st.number_input("API", key="lbs", on_change=lbs_to_kg)  # api to sgo
    with col2:
        kilogram = st.number_input("Sgo: ", key="kg", on_change=kg_to_lbs)  # sgo to api                    
    
    _id_casing_size = _id_casing_id = _id_tubing_size = _id_tubing_id = 0
    _casing_size = ''; _casing_id = _tubing_size = _tubing_id = 0.00
    _casing_size_list = mcasingsize['casing_size'].unique().tolist()     
    _casing_id_list = mcasingsize['casing_drift_id'].unique().tolist() # casing id berarti caslng drift id
    #Using list comprehension to change list of numbers to list of string
    string_casing_id_list = [str(x) for x in _casing_id_list] # -> now means casing drift id
    df_casing_size = pd.DataFrame({
        'Size': _casing_size_list,
        'Drift ID': string_casing_id_list})    
    df_casing_size['Combined'] = df_casing_size['Size'] + ' - ' + df_casing_size['Drift ID']
    #st.dataframe(df_casing_size)   

    st.header("Casing & Tubing", divider="gray")
    _casing_size = st.selectbox("Casing Size & Casing Drift ID (inch)", df_casing_size['Combined'], 1)
    indexrow = df_casing_size.loc[df_casing_size['Combined']==_casing_size].index[0]
    _id_casing_size = indexrow + 1 # -> ditambah 1 krn index df_casing_size dimulai dari 0
    st.session_state._id_casing_size = _id_casing_size
    therecord = mcasingsize.loc[mcasingsize['id_casing_size']==_id_casing_size].reset_index(drop=True)
    _casing_size = therecord['casing_size'].values[0]
    _casing_id = therecord['casing_drift_id'].values[0]
    #st.write("casing size:", _casing_size) --> sdh benar
    #st.write("casing drift id:", _casing_id) --> sdh benar

    _tubing_size_list = mtubingsize['tubing_size'].unique().tolist() 
    _tubing_id_list = mtubingid['tubing_id'].unique().tolist()  
    _tubing_size = st.selectbox("Tubing Size ", _tubing_size_list)
    # filtering tubing id which is under tubing size
    mycalc_temp = mtubingsize.loc[mtubingsize['tubing_size']==_tubing_size].reset_index(drop=True)
    _id_tubing_size = mycalc_temp['id_tubing_size'].values[0]
    st.session_state._id_tubing_size = _id_tubing_size
    mycalc_temp = mtubingid.loc[mtubingid['id_tubing_size']==_id_tubing_size].reset_index(drop=True)
    _tubing_id_list = mycalc_temp['tubing_id'].unique().tolist() 

    _tubing_id = st.selectbox("Tubing ID (inch)", _tubing_id_list); st.session_state._tubing_id = _tubing_id
    mycalc_temp = mtubingid.loc[mtubingid['tubing_id']==_tubing_id].reset_index(drop=True)
    _id_tubing_id = mycalc_temp['id_tubing_id'].values[0]
    st.session_state._id_tubig_id = _id_tubing_id

    _tubing_coeff_list = mtubingcoeff['type'].unique().tolist()     
    _tubing_coeff_type = st.selectbox("Tubing Coeffisien Type", _tubing_coeff_list) #dont have 2 be like casing size
    mycalc_temp = mtubingcoeff.loc[mtubingcoeff['type']==_tubing_coeff_type].reset_index(drop=True)
    st.session_state._id_tubing_coeff = mycalc_temp['id_tubing_coeff'].values[0]    
    st.session_state._tubing_coeff_type = mycalc_temp['type'].values[0]
    st.session_state._coefficient = mycalc_temp['coefficient'].values[0]
    st.write('\n')            
    
    st.header("Liner", divider="gray")
    _liner_id = _top_liner_at = _bottom_liner_at = 0
    _liner_id = st.number_input('Liner ID (inch)', 0.00, None, 'min', 1.00, format="%0.2f"); st.session_state._liner_id = _liner_id
    _top_liner_at_tvd = st.number_input(f'Top Liner at ({_measurement} TVD)', 0.00, None, 'min', 1.00, format="%0.2f")
    st.session_state._top_liner_at_tvd= _top_liner_at_tvd
    if _id_welltype == 1: # 1-Vertical, 2-Directional
        _top_liner_at_md = _top_liner_at_tvd; st.session_state._top_liner_at_md = st.session_state._top_liner_at_tvd
        st.write(f'Top Liner at ({_measurement} MD) : {_top_liner_at_md:.2f}')
    else:
        _top_liner_at_md = st.number_input(f'Top Liner at ({_measurement} MD)', 0.00, None, 'min', 1.00, format="%0.2f")
        st.session_state._top_liner_at_md = _top_liner_at_md

    _bottom_liner_at_tvd = st.number_input(f'Bottom Liner at ({_measurement} TVD)', 0.00, None, 'min', 1.00, format="%0.2f")
    st.session_state._bottom_liner_at_tvd = _bottom_liner_at_tvd
    if _id_welltype == 1: # 1-Vertical, 2-Directional
        _bottom_liner_at_md = _bottom_liner_at_tvd; st.session_state._bottom_liner_at_md = st.session_state._bottom_liner_at_tvd
        st.write(f'Bottom Liner at ({_measurement} MD) : {_bottom_liner_at_md:.2f}')
    else:
        _bottom_liner_at_md = st.number_input(f'Bottom Liner at ({_measurement} MD)', 0.00, None, 'min', 1.00, format="%0.2f")
        st.session_state._bottom_liner_at_md = _bottom_liner_at_md

if st.button("Save"):                   
    #last_num = mnomor1.iloc[-1:]    
    #last_id_calc = mnomor1['tmycalc'].values[0]
    #new_id_calc = last_id_calc + 1    
    st.session_state["new_id_calc"] += 1
    
    # change value of a single cell directly
    mnomor1.at[0, 'tmycalc'] = st.session_state["new_id_calc"]
    
    # write out the CSV file 
    mnomor1.to_csv("mnomor1.csv", index=False)
 
    st.title("General Information")
    col1, col2 = st.columns(2, gap="medium", vertical_alignment="top")
    with col1:
        st.subheader('ID Calculation:')
        st.markdown(st.session_state["new_id_calc"])
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

        # SGFluid = WC * SGw + (1 - WC) * Sgo
        #         = 88% * 1.02 + (1- 88%) * 0.887147335
        _sgfluid = (_wc/100) * _sgw + (1-(_wc/100)) * st.session_state.kg
        
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
        #_Rs=_sgg*(( (_pip/18) * (10**(0.0125*_api - 0.00091*_bht)) )**1.2048)
        _Rs=_sgg*(( (_pip/18) * (10**(0.0125*st.session_state.lbs - 0.00091*_bht)) )**1.2048)
        
        # Bo=0.972+0.000147*((Rs*SQRT(SGg/Sgo)+1.25*BHT)^1.175); 
        # _Bo = 0.972+0.000147*((_Rs*math.sqrt(_sgg/_sgo)+1.25*_bht)**1.175) --> math masalah diDeploy
        #_Bo = 0.972+0.000147*((_Rs * (_sgg/_sgo)**0.5 + 1.25 * _bht) ** 1.175)
        _Bo = 0.972+0.000147*((_Rs * (_sgg/st.session_state.kg)**0.5 + 1.25 * _bht) ** 1.175)
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
        _composite_sg = ( ( (1-(_wc/100))*_qdes*st.session_state.kg + (_wc/100)*_qdes*_sgw) * 62.4*5.6146 + _producing_gor*(1-(_wc/100))*_qdes*_sgg*0.0752) / (_Vt*5.6146*62.4)
        
        # WFL =PSD-(PIP*2.31/SGFluid)
        if _id_measurement==1: # m (meter), PSD nya dikali 3.28084 dulu (dikonversi ke ft krn PSD hrs dlm ft)
            _wfl = (_psd*3.28084)-(_pip*2.31/_sgfluid)
            # lalu dirubah lgi ke mtr sesuai apa yg diinput di awal (yg diinginkan dlm mtr)
            _wfl = _wfl * 0.3048 # 0.3048 adalah 1/3.28084
        elif _id_measurement==2: # ft (feet) PSD nya gak perlu dikali 3.28084 dulu
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
            _friction_loss = (2.083*(100/st.session_state._coefficient)**1.85*(_qdes/34.3)**1.85/_tubing_id**4.8655)*(_psd*3.28084)/1000
            # lalu dirubah lgi ke mtr sesuai apa yg diinput di awal (yg diinginkan dlm mtr)
            _friction_loss *= 0.3048        
        elif _id_measurement==2: # ft (tdk perlu diconvert)
            _friction_loss = (2.083*(100/st.session_state._coefficient)**1.85*(_qdes/34.3)**1.85/_tubing_id**4.8655)*_psd/1000
        
        # % Free Gas = Vg / Vt
        _persen_free_gas = (_Vg / _Vt) * 100
        
        # TDH = sum(WFL, WHP, CP, FrictionLoss)  --> CP (Optional, bila tdk dinput, defaultnya nol) 
        #tdh = _wfl + _whp_hitung + _cp + _friction_loss
        _tdh = _wfl + _whp_hitung + _p_casing_hitung + _friction_loss  # cp dihapus, jadi kalau perlu cp, diganti dgn p.casing
        
        #Fluid Over Pump = (PIP-CP)*2.31/SGFluid
        #_fluid_over_pump = (_pip - _cp)*2.31/_sgfluid
        _fluid_over_pump = (_pip - _p_casing_hitung)*2.31/_sgfluid # cp dihapus, jadi kalau perlu cp, diganti dgn p.casing
        
        # Fluid Gradient = SGFluid/2.31
        _fluid_gradient = _sgfluid/2.31
        
        # ---------- Counting data for ipr_curve Vogel (2Fields, 8Records) ----------------------- 
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
           st.write('Composite SG : ', round(_composite_sg,2)) #, '(selisih/beda 0.0003 lbh kecil)')
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
           #st.write('\n')
           
        st.title("Inflow Performance Relationships")    
        #row5_1, row5_spacer2, row5_2= st.columns((11.1, .1, 3.8))
        #with row5_1:
        # perbesar figsize
        #plt.figure(figsize=(20,10))
        plt.figure(figsize=(10,5))
     
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
        plt.grid(color='darkgray', linestyle=':', linewidth=0.5)
     
        st.pyplot(fig)
        #with row5_2:
        #    st.dataframe(df_ipr_data, hide_index=True)     
        #    st.write('')
                            # st.session_state.lbs = st.session_state._api and st.session_state.kg = st.session_state._sgo
        new_records = [[st.session_state["new_id_calc"], _user_id, _well_name, _field_name, _company, _engineer, _date_calc, \
                          _id_instrument, _id_calc_method, _id_welltype, _id_measurement, _comment_or_info, \
                          _top_perfo_tvd, _top_perfo_md, _bottom_perfo_tvd, _bottom_perfo_md, _qtest, _sfl, _smgFreeGasAtQtest, _sbhp, _fbhp, \
                          _producing_gor, _wc, _bht, _sgw, _sgg, _qdes, _psd, _whp, _psd_md, _p_casing, _pb, \
                          st.session_state.lbs, st.session_state.kg, _id_casing_size, _id_tubing_size, _id_tubing_id, \
                          st.session_state._id_tubing_coeff, _liner_id, _top_liner_at_tvd, _top_liner_at_md, \
                          _bottom_liner_at_tvd, _bottom_liner_at_md]]   

        with open('tmycalc.csv', mode='a', newline='') as f_object:
           #writer_object = csv.writer(file)            
            writer_object = writer(f_object)            
            # Add new rows to the CSV
            writer_object.writerows(new_records)                    
            f_object.close() 
               
        if st.button("Next"):      
            st.write('')            
            #st.session_state["api"] = 0.00; st.session_state.sgo = 0.00    
            #st.session_state["_id_tubing_coeff"] = 0; st.session_state._tubing_coeff_type = ''    
            #st.session_state._coefficient = 0
            
            #for the_keyyys in st.session_state.keys():
            #    del st.session_state[the_keyyys]
                
            #st.session_state   

    elif _id_calc_method==1: # Straight Line
        new_calc_straight() # new_calcb.py
        st.write('')
