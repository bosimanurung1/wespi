import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from csv import writer

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

if "api" not in st.session_state:
    st.session_state["api"] = 0.00
    
if "sgo" not in st.session_state:
    st.session_state.sgo = 0.00
    
if "_id_tubing_coeff" not in st.session_state:
    st.session_state["_id_tubing_coeff"] = 0
    
if "_tubing_coeff_type" not in st.session_state:
    st.session_state._tubing_coeff_type = ''
    
if "_coefficient" not in st.session_state:
    st.session_state._coefficient = 0
   
col1, col2 = st.columns(2, gap="medium", vertical_alignment="top")
with col1:
    _well_name = ''; _field_name = ''; _company = ''; _engineer = ''
    _username_list = muserlogin['username'].unique().tolist() 
    last_id_calc = _user_id = 0
    
    _username = st.selectbox("Username: ", _username_list)
    _date_calc = st.date_input("Date Input: ")
    _well_name = st.text_input("Well Name:")
    _field_name = st.text_input('Field Name:')
    _company = st.text_input('Company:')
    _engineer = st.text_input('Engineer: ')   
    
with col2:
    _id_instrument = _id_calc_method = _id_measurement = 0
    _instrument_list = minstrument['instrument'].unique().tolist() 
    _calc_method_list = mcalcmethod['calc_method'].unique().tolist(); _welltype_list = mwelltype['welltype'].unique().tolist()
    _measurement_list =  mmeasurement['measurement'].unique().tolist()
    _comment_or_info = ''
    
    _instrument = st.selectbox("Instrument: ", _instrument_list)
    _calc_method = st.selectbox("Calculation Method: ", _calc_method_list)
    _welltype = st.selectbox("Well Type: ", _welltype_list)
    _measurement = st.selectbox("Unit Measurement: ", _measurement_list)
    _comment_or_info = st.text_input('Comment or Info: ')
    
    mycalc_temp = muserlogin.loc[muserlogin['username']==_username].reset_index(drop=True)
    _user_id = mycalc_temp['user_id'].values[0]
    
    mycalc_temp = minstrument.loc[minstrument['instrument']==_instrument].reset_index(drop=True)
    _id_instrument = mycalc_temp['id_instrument'].values[0]
    
    mycalc_temp = mcalcmethod.loc[mcalcmethod['calc_method']==_calc_method].reset_index(drop=True)
    _id_calc_method = mycalc_temp['id_calc_method'].values[0]
    
    mycalc_temp = mwelltype.loc[mwelltype['welltype']==_welltype].reset_index(drop=True)
    _id_welltype = mycalc_temp['id_welltype'].values[0]
    
    mycalc_temp = mmeasurement.loc[mmeasurement['measurement']==_measurement].reset_index(drop=True)
    _id_measurement = mycalc_temp['id_measurement'].values[0]          

#inputing basic data (required), etc.        
row3_1, row3_spacer, row3_2= st.columns((3, 1, 3))
with row3_1:
    _top_perfo_tvd = _top_perfo_md = _bottom_perfo_tvd = _bottom_perfo_md = 0.01
    _qtest = _sbhp = _fbhp = _producing_gor = _wc = _bht = 0.01
    _sgw = _sgg = _qdes = _psd = _whp = _psd_md = 0.01
    
    st.header("Basic Data (Required)", divider="gray")
    _top_perfo_tvd = st.number_input(f"Top Perfo ({_measurement} TVD)", 0.00, None, 'min', 1.00, format="%0.2f")
    _top_perfo_md = st.number_input(f'Top Perfo ({_measurement} MD)', 0.00, None, 'min', 1.00, format="%0.2f")
    _bottom_perfo_tvd = st.number_input(f'Bottom Perfo ({_measurement} TVD)', 0.00, None, 'min', 1.00, format="%0.2f")
    _bottom_perfo_md = st.number_input(f'Bottom Perfo ({_measurement} MD)', 0.00, None, 'min', 1.00, format="%0.2f")
    _qtest = st.number_input('Qtest (BPD)', 0.00, None, 'min', 1.00, format="%0.2f")
    _sbhp = st.number_input('SBHP (psig)', 0.00, None, 'min', 1.00, format="%0.2f")
    _fbhp = st.number_input('FBHP (psig)', 0.00, None, 'min', 1.00, format="%0.2f")
    _producing_gor = st.number_input('Producing GOR (scf/stb)', 0.00, None, 'min', 1.00, format="%0.2f")
    _wc = st.number_input('WC (%)', 0.00, None, 'min', 1.00, format="%0.2f")
    _bht = st.number_input('BHT (℉)', 0.00, None, 'min', 1.00, format="%0.2f")
    _sgw = st.number_input('SGw', 0.00, None, 'min', 1.00, format="%0.2f")
    _sgg = st.number_input('SGg', 0.00, None, 'min', 1.00, format="%0.2f")
    _qdes = st.number_input('Qdes (BPD)', 0.00, None, 'min', 1.00, format="%0.2f")
    _psd = st.number_input(f'PSD ({_measurement} TVD)', 0.00, None, 'min', 1.00, format="%0.2f")
    _whp = st.number_input('WHP (psi)', 0.00, None, 'min', 1.00, format="%0.2f")
    _psd_md = st.number_input(f'PSD ({_measurement} MD)', 0.00, None, 'min', 1.00, format="%0.2f")    

with row3_2:
    _p_casing = _pb = cp = 0.01
    _api = _sgo = _api1 = _sgo1 = 0.00

    st.header("Basic Data (Optional)", divider="gray")
    _p_casing = st.number_input('P. Casing (psi)', 0.00, None, 'min', 1.00, format="%0.2f")
    _pb = st.number_input('Pb (psig)', 0.00, None, 'min', 1.00, format="%0.2f")
    _cp = st.number_input('CP (psi)', 0.00, None, 'min', 1.00, format="%0.2f")
    
    st.header("API/Sgo", divider="gray")
    def api_to_sgo():
        st.session_state.sgo = 141.5/(131.5 + st.session_state.api)
        st.session_state.sgo = round(st.session_state.sgo, 4)
        #_sgo = 141.5/(131.5 + _api)

    def sgo_to_api():
        st.session_state.api = 141.5/st.session_state.sgo - 131.5
        st.session_state.api = round(st.session_state.api, 4) 
        #_api = 141.5/_sgo - 131.5    
        
    # ------------- now how callback work ---------------
    col1, buff, col2 = st.columns([2,1,2])
    with col1:
        _api = st.number_input('API', _api, None, 'min', 1.00, format="%0.2f", 
                               key="api", on_change=api_to_sgo)
        
    with col2:
        _sgo = st.number_input('Sgo', _sgo, None, 'min', 1.00, format="%0.2f", 
                               key="sgo", on_change=sgo_to_api)    
    
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
    
    mycalc_temp = mtubingid.loc[mtubingid['id_tubing_size']==_id_tubing_size].reset_index(drop=True)
    _tubing_id_list = mycalc_temp['tubing_id'].unique().tolist() 

    _tubing_id = st.selectbox("Tubing ID (inch)", _tubing_id_list)
    mycalc_temp = mtubingid.loc[mtubingid['tubing_id']==_tubing_id] .reset_index(drop=True)
    _id_tubing_id = mycalc_temp['id_tubing_id'].values[0]

    _id_tubing_coeff_list = mtubingcoeff['id_tubing_coeff'].unique().tolist()         
    _tubing_coeff_list = mtubingcoeff['type'].unique().tolist()     
    _coefficient_list = mtubingcoeff['coefficient'].unique().tolist()   
    #Using list comprehension to change list of numbers to list of string
    string_coefficient_list = [str(x) for x in _coefficient_list] # -> now means casing drift id
    df_tubing_coeff_type = pd.DataFrame({
        'ID': _id_tubing_coeff_list,
        'Type': _tubing_coeff_list,
        'Coefficient': string_coefficient_list})    
    df_tubing_coeff_type['Combined'] = df_tubing_coeff_type['Type'] + ' - ' + df_tubing_coeff_type['Coefficient']
    _tubing_coeff_type = st.selectbox("Tubing Coeffisien Type & Coefficient", df_tubing_coeff_type['Combined'], 1)

    indexrow = df_tubing_coeff_type.loc[df_tubing_coeff_type['Combined']==_tubing_coeff_type].index[0]
    st.session_state._id_tubing_coeff_type = indexrow + 1 # -> ditambah 1 krn index df_casing_size dimulai dari 0
    therecord = mtubingcoeff.loc[mtubingcoeff['id_tubing_coeff']==st.session_state._id_tubing_coeff_type].reset_index(drop=True)
    st.session_state._id_tubing_coeff = therecord['id_tubing_coeff'].values[0]
    st.session_state._tubing_coeff_type = therecord['type'].values[0]
    st.session_state._coefficient = therecord['coefficient'].values[0]
    st.write('\n')            
    
    st.header("Liner", divider="gray")
    _liner_id = _top_liner_at = _bottom_liner_at = 0
    _liner_id = st.number_input('Liner ID (inch)', 0.00, None, 'min', 1.00, format="%0.2f")
    _top_liner_at = st.number_input(f'Top Liner at ({_measurement} TVD)', 0.00, None, 'min', 1.00, format="%0.2f")
    _bottom_liner_at = st.number_input(f'Bottom Liner at ({_measurement} MD)', 0.00, None, 'min', 1.00, format="%0.2f")
        
if st.button("Save"):                   
    #last_num = mnomor1.iloc[-1:]    
    last_id_calc = mnomor1['tmycalc'].values[0]
    new_id_calc = last_id_calc + 1    
    
    # change value of a single cell directly
    mnomor1.at[0, 'tmycalc'] = new_id_calc
    
    # write out the CSV file 
    mnomor1.to_csv("mnomor1.csv", index=False)
 
    st.title("General Information")
    col1, col2 = st.columns(2, gap="medium", vertical_alignment="top")
    with col1:
        st.subheader('ID Calculation:')
        st.markdown(new_id_calc)
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

    if _id_instrument==1 and _id_calc_method==2: #Downhole Sensor & Vogel         
        #Hitung2an Calculation sblm IPR Curve
        _qmax = _qtest / (1 - 0.2 * (_fbhp/_sbhp) - 0.8 * (_fbhp/_sbhp) ** 2)
        # _Pwf_at_Qdes = (5 * math.sqrt(3.24 - 3.2 * (_qdes/_qmax)) - 1) / 8 * _sbhp --> library math susah diDeploy
        _Pwf_at_Qdes = (5 * (3.24 - 3.2 * (_qdes/_qmax))**0.5 - 1) / 8 * _sbhp
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
        
        # MidPerf = 0.5(TopPerfoTVD+BottomPerfoTVD)
        _MidPerf = 0.5 * (_top_perfo_tvd + _bottom_perfo_tvd)
        # SGFluid = WC * SGw + (1 - WC) * Sgo
        #         = 88% * 1.02 + (1- 88%) * 0.887147335
        _sgfluid = (_wc/100) * _sgw + (1-(_wc/100)) * _sgo
        
        # PIP=Pwf@Qdes-(MidPerf-PSD)*SGFluid/2.31    
        _pip = _Pwf_at_Qdes - ((_MidPerf - _psd) * (_sgfluid/2.31)) 
        
        # Rs=Sgg*(( (PIP/18) * (10^(0.0125*API – 0.00091*BHT)) )^1.2048)
        #_Rs=_sgg*(( (_pip/18) * (10**(0.0125*_api - 0.00091*_bht)) )**1.2048)
        _Rs=_sgg*(( (_pip/18) * (10**(0.0125*st.session_state.api - 0.00091*_bht)) )**1.2048)
        
        # Bo=0.972+0.000147*((Rs*SQRT(SGg/Sgo)+1.25*BHT)^1.175); 
        # _Bo = 0.972+0.000147*((_Rs*math.sqrt(_sgg/_sgo)+1.25*_bht)**1.175) --> math masalah diDeploy
        #_Bo = 0.972+0.000147*((_Rs * (_sgg/_sgo)**0.5 + 1.25 * _bht) ** 1.175)
        _Bo = 0.972+0.000147*((_Rs * (_sgg/st.session_state.sgo)**0.5 + 1.25 * _bht) ** 1.175)
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
        _wfl = _psd-(_pip*2.31/_sgfluid)
        
        # WHP = THP(WHP)*2.31/SGFluid
        _whp_hitung=_whp*2.31/_sgfluid
        
        if _p_casing == 0:
            _p_casing_hitung = 0
        else:
            _p_casing_hitung = (_p_casing * 2.31 / _sgfluid) / 3.28084 # -> utk jadi meter
        
        # Friction Loss = (2.083*(100/TubingCoeff)^1.85*(Qdes         /34.3)^1.85/TubingID^4.8655)  *PSDft/1000
        #_friction_loss = (2.083*(100/_coefficient)**1.85*(_qdes/34.3)**1.85/_tubing_id**4.8655)*_psd/1000
        _friction_loss = (2.083*(100/st.session_state._coefficient)**1.85*(_qdes/34.3)**1.85/_tubing_id**4.8655)*_psd/1000
        
        # % Free Gas = Vg / Vt
        _persen_free_gas = (_Vg / _Vt) * 100
        
        # TDH = sum(WFL, WHP, CP, FrictionLoss)  --> CP (Optional, bila tdk dinput, defaultnya nol) 
        _tdh = _wfl + _whp_hitung + _cp + _friction_loss
        
        #Fluid Over Pump = (PIP-CP)*2.31/SGFluid
        _fluid_over_pump = (_pip - _cp)*2.31/_sgfluid
        
        # Fluid Gradient = SGFluid/2.31
        _fluid_gradient = _sgfluid/2.31
        
        # ---------- Counting data for ipr_curve (2Fields, 8Records) ----------------------- 
        #_flowrate1 = (1-0.2*(Pressure1 / SBHP) - 0.8 * (Pressure1 / SBHP)^2) * Qmax
        _pressure1 = 0
        _flowrate1 = (1-0.2*(_pressure1 / 1914) - 0.8 * (_pressure1 / 1914)**2) * 3002.746
        
        #_flowrate2 = (1-0.2*(Pressure2 / SBHP) - 0.8 * (Pressure2 / SBHP)^2) * Qmax
        #_pressure2 = (MidPerfo - PSD) * SGFluid / 2.31 + CP
        _pressure2 = (_MidPerf - _psd) * _sgfluid / 2.31 + _cp
        _flowrate2 = (1-0.2*(_pressure2 / 1914) - 0.8 * (_pressure2 / 1914)**2) * 3002.746
        
        #_flowrate3 = (1-0.2*(Pressure3 / SBHP) - 0.8 * (Pressure3 / SBHP)^2) * Qmax
        #_pressure3 = 0.2 * SBHP
        _pressure3 = 0.2 * _sbhp
        _flowrate3 = (1-0.2*(_pressure3 / 1914) - 0.8 * (_pressure3 / 1914)**2) * 3002.746
        
        #_flowrate4 = (1-0.2*(Pressure4 / SBHP) - 0.8 * (Pressure4 / SBHP)^2) * Qmax
        #_pressure4 = 0.4 * SBHP
        _pressure4 = 0.4 * _sbhp
        _flowrate4 = (1-0.2*(_pressure4 / 1914) - 0.8 * (_pressure4 / 1914)**2) * 3002.746
        
        #_flowrate5 = (1-0.2*(Pressure5 / SBHP) - 0.8 * (Pressure5 / SBHP)^2) * Qmax
        #_pressure5 = Pwf@Qdes
        _pressure5 = _Pwf_at_Qdes
        _flowrate5 = (1-0.2*(_pressure5 / 1914) - 0.8 * (_pressure5 / 1914)**2) * 3002.746
        
        #_flowrate6 = (1-0.2*(Pressure6 / SBHP) - 0.8 * (Pressure6 / SBHP)^2) * Qmax
        #_pressure6 = 0.6 * SBHP
        _pressure6 = 0.6 * _sbhp
        _flowrate6 = (1-0.2*(_pressure6 / 1914) - 0.8 * (_pressure6 / 1914)**2) * 3002.746
        
        #_flowrate7 = (1-0.2*(Pressure7 / SBHP) - 0.8 * (Pressure7 / SBHP)^2) * Qmax
        #_pressure7 = 0.8 * SBHP
        _pressure7 = 0.8 * _sbhp
        _flowrate7 = (1-0.2*(_pressure7 / 1914) - 0.8 * (_pressure7 / 1914)**2) * 3002.746
        
        #_flowrate8 = (1-0.2*(Pressure8 / SBHP) - 0.8 * (Pressure8 / SBHP)^2) * Qmax
        #_pressure8 = SBHP
        _pressure8 = _sbhp
        _flowrate8 = (1-0.2*(_pressure8 / 1914) - 0.8 * (_pressure8 / 1914)**2) * 3002.746
        
        df_ipr_data = pd.DataFrame({'Flow rate': [_flowrate1, _flowrate2, _flowrate3, _flowrate4, _flowrate5 \
                , _flowrate6, _flowrate7, _flowrate8],
                'Pressure': [_pressure1, _pressure2, _pressure3, _pressure4, _pressure5 \
                , _pressure6, _pressure7, _pressure8]})
        # ---------------------------- until here -----------------------------------------        
        
        st.write('\n')
        st.title("Calculation")
        col1, col2 = st.columns(2, gap="medium", vertical_alignment="top")
        with col1:
           _Pwf_at_Qdes = round(_Pwf_at_Qdes, 4) # jadi 786.7571 yg sblmnya 786.757076405096
           _composite_sg = round(_composite_sg, 2) # sblmnya 0.490559258022
           st.write("Pwf@Qdes: ", _Pwf_at_Qdes, 'psi')
           st.write('Qdes         : ', _qdes, 'BPD')
           st.write('Composite SG : ', _composite_sg) #, '(selisih/beda 0.0003 lbh kecil)')
           #st.write('Di file xls: 0.490859')
           #st.write('\n')
        
           _wfl = round(_wfl, 2) # sblmnya 4743.3883109093
           st.write('PSD          : ', _psd, _measurement, 'TVD')
           st.write('WFL          : ', _wfl, _measurement, 'TVD')
           #st.write('Di file xls: 4744.936')
           #st.write('Hitung2an:')
           #st.write('WFL = PSD - (PIP * 2.31 / SGFluid)')
           #st.write('=', _psd, '- ((', _pip, '* 2.31) /', _sgfluid)
           #st.write('=', _psd, '-', (_pip * 2.31), '/', _sgfluid)
           #st.write('=', _psd, '-', (_pip * 2.31) / _sgfluid)
           #st.write('=', round(_psd - (_pip * 2.31) / _sgfluid, 2), '(selisih/beda 1.6 lbh kecil)')
           #st.write('\n')
           
           _qmax = round(_qmax, 2)
           _whp_hitung = round(_whp_hitung, 2)
           st.write('Qmax         : ', _qmax, 'BPD')
           st.write('WHP          : ', _whp_hitung, _measurement, 'TVD')
           #st.write('Di file xls: 345.0997')
           #st.write('Hitung2an WHP:')
           #st.write('WHP = THP * 2.31 / SGFluid')
           #st.write('= (', _whp, '* 2.31) /', _sgfluid)
           #st.write('=', _whp * 2.31, '/', _sgfluid)
           #st.write('=', round((_whp * 2.31) / _sgfluid, 2), '(selisih/beda 0.3 lbh besar)')
           #st.write('\n')
        
           _sgfluid = round(_sgfluid, 2)
           #st.write('SG Fluid = WC * SGw + (1 - WC) * Sgo')
           #st.write('= (', _wc, '/100) * ', _sgw, '+ (1 - (',  _wc, '/100)) * ', _sgo)
           #st.write('= ', _wc/100,' * ', _sgw, '+ (1 - ', _wc/100, ') * ', _sgo)
           #st.write('= ', _wc/100,' * ', _sgw, '+ ', 1 - (_wc/100), ' * ', _sgo)
           #st.write('= ', (_wc/100) * _sgw, '+ ', (1 - (_wc/100)) * _sgo)
           #_sgfluid = (_wc/100) * _sgw + (1-(_wc/100)) * _sgo
           #st.write('SG Fluid     : ', _sgfluid, '(selisih/beda 0.001 lbh kecil)')
           #st.write('Di file xls: 1.004')
           #st.write('\n')
           
           _pip = round(_pip, 2)
           st.write('PIP          : ', _pip, 'psi')
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
           _friction_loss = round(_friction_loss, 2)
           _persen_free_gas = round(_persen_free_gas, 2)
           st.write('P. Casing    : ', _p_casing_hitung, _measurement, 'TVD')
           st.write('Friction Loss: ', _friction_loss, _measurement, 'TVD')
           st.write('% Free Gas     : ', _persen_free_gas, '%')
           #st.write('Di file xls: 51.80 %')
           #st.write('Hitung2an % Free Gas:')
           #st.write('Free Gas = (Vg / Vt) * 100')
           #st.write('= (', _Vg, '/', _Vt, ') * 100')
           #st.write('=', round((_Vg / _Vt) * 100, 2), '(selisih/beda 0.01 lbh kecil)')
           #st.write('\n')
        
           _tdh = round(_tdh, 2)
           st.write('TDH            : ', _tdh, _measurement, 'TVD')
           #st.write('Di file xls: 5376.58')
           #st.write('Hitung2an TDH:')
           #st.write('= WFL + WHP + CP + FrictionLoss')
           #st.write('CP Optional, bila tdk dinput, defaultnya nol')
           #st.write('=', _wfl, '+', _whp_hitung, '+', _cp, '+', _friction_loss)
           #st.write('=', round(_wfl + _whp_hitung + _cp + _friction_loss, 2), '(selisih/beda 1.2 lbh kecil)')
           #st.write('\n')
        
           _fluid_over_pump = round(_fluid_over_pump, 2)
           st.write('SBHP           : ', _sbhp, 'psig')
           st.write('Fluid Over Pump: ', _fluid_over_pump, _measurement, 'TVD')
           #st.write('Di file xls: 1205.1334')
           #st.write('Hitung2an Fluid Over Pump:')
           #st.write('= (PIP - CP) * 2.31 / SGFluid')
           #st.write('= ((', _pip, '-', _cp, ') * 2.31) /', _sgfluid)
           #st.write('= (', _pip - _cp, '* 2.31) /', _sgfluid)
           #st.write('=', (_pip - _cp) * 2.31, '/', _sgfluid)
           #st.write('=', round(((_pip - _cp) * 2.31) / _sgfluid, 2), '(selisih/beda 1.48 lbh besar)')
           #st.write('\n')
        
           _fluid_gradient = round(_fluid_gradient, 2)
           st.write('FBHP           : ', _fbhp, 'psig')
           st.write('Fluid Gradient : ', _fluid_gradient, 'psi/', _measurement, 'TVD')
           #st.write('Di file xls: 0.43463 (selisih/beda 0.0004 lbh kecil)')
           #st.write('\n')
           
        st.title("Inflow Performance Relationships")    
        #row5_1, row5_spacer2, row5_2= st.columns((11.1, .1, 3.8))
        #with row5_1:
        # perbesar figsize
        #plt.figure(figsize=(20,10))
        plt.figure(figsize=(10,5))
     
        fig, ax  = plt.subplots()
     
        # membuat line plot
        plt.plot(df_ipr_data['Flow rate'], df_ipr_data['Pressure'], 'or:')
     
        # set title & label
        plt.xlabel('Flow rate, Q (BFPD)',fontsize=13,color='darkred')
        plt.ylabel('Pressure (psi)',fontsize=13,color='darkred')
     
        # custom line
        plot_line = plt.plot(df_ipr_data['Flow rate'], df_ipr_data['Pressure'])
        plt.setp(plot_line, color='red', linestyle=':',  linewidth=0.1, marker='o')
     
        # set start 0 y axis
        plt.ylim(ymin=0)
        plt.xlim(xmin=0)
        
        # set grid
        plt.grid(color='darkgray', linestyle=':', linewidth=0.5)
     
        st.pyplot(fig)
        #with row5_2:
        #st.dataframe(df_ipr_data, hide_index=True)               

        new_records = [[new_id_calc, _user_id, _well_name, _field_name, _company, _engineer, _date_calc, \
                          _id_instrument, _id_calc_method, _id_welltype, _id_measurement, _comment_or_info, \
                          _top_perfo_tvd, _top_perfo_md, _bottom_perfo_tvd, _bottom_perfo_md, _qtest, _sbhp, _fbhp, \
                          _producing_gor, _wc, _bht, _sgw, _sgg, _qdes, _psd, _whp, _psd_md, _p_casing, _pb, _cp, \
                          st.session_state.api, st.session_state.sgo, _id_casing_size, _id_tubing_size, _id_tubing_id, \
                          st.session_state._id_tubing_coeff, _liner_id, _top_liner_at, _bottom_liner_at]]                               
        with open('tmycalc.csv', mode='a', newline='') as f_object:
            #writer_object = csv.writer(file)            
            writer_object = writer(f_object)            
            # Add new rows to the CSV
            writer_object.writerows(new_records)                    
            f_object.close() 
               
        if st.button("Confirm"):      
            st.write('')            
            #st.session_state["api"] = 0.00; st.session_state.sgo = 0.00    
            #st.session_state["_id_tubing_coeff"] = 0; st.session_state._tubing_coeff_type = ''    
            #st.session_state._coefficient = 0
            
            #for the_keyyys in st.session_state.keys():
            #    del st.session_state[the_keyyys]
                
            #st.session_state   

    elif _id_instrument==1 and _id_calc_method==1: #Downhole Sensor & Straight Line
        #Hitung2an Calculation sblm IPR Curve
        _pi = _qtest / (_sbhp - _fbhp)
        # _Pwf_at_Qdes = (5 * math.sqrt(3.24 - 3.2 * (_qdes/_qmax)) - 1) / 8 * _sbhp --> library math susah diDeploy
        _Pwf_at_Qdes = _sbhp - _qdes / _pi
    
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
    
        # MidPerf = 0.5(TopPerfoTVD+BottomPerfoTVD)
        _MidPerf = 0.5 * (_top_perfo_tvd + _bottom_perfo_tvd)
        # SGFluid = WC * SGw + (1 - WC) * Sgo
        #         = 88% * 1.02 + (1- 88%) * 0.887147335
        _sgfluid = (_wc/100) * _sgw + (1-(_wc/100)) * _sgo
        
        # PIP=Pwf@Qdes-(MidPerf-PSD)*SGFluid/2.31    
        _pip = _Pwf_at_Qdes - ((_MidPerf - _psd) * (_sgfluid/2.31)) 
        
        # Rs=Sgg*(( (PIP/18) * (10^(0.0125*API – 0.00091*BHT)) )^1.2048)
        #_Rs=_sgg*(( (_pip/18) * (10**(0.0125*_api - 0.00091*_bht)) )**1.2048)
        _Rs=_sgg*(( (_pip/18) * (10**(0.0125*st.session_state.api - 0.00091*_bht)) )**1.2048)
    
        # Bo=0.972+0.000147*((Rs*SQRT(SGg/Sgo)+1.25*BHT)^1.175); 
        # _Bo = 0.972+0.000147*((_Rs*math.sqrt(_sgg/_sgo)+1.25*_bht)**1.175) --> math masalah diDeploy
        #_Bo = 0.972+0.000147*((_Rs * (_sgg/_sgo)**0.5 + 1.25 * _bht) ** 1.175)
        _Bo = 0.972+0.000147*((_Rs * (_sgg/st.session_state.sgo)**0.5 + 1.25 * _bht) ** 1.175)
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
        _wfl = _psd-(_pip*2.31/_sgfluid)
    
        # WHP = THP(WHP)*2.31/SGFluid
        _whp_hitung=_whp*2.31/_sgfluid
    
        if _p_casing == 0:
            _p_casing_hitung = 0
        else:
            _p_casing_hitung = (_p_casing * 2.31 / _sgfluid) / 3.28084 # -> utk jadi meter
    
        # Friction Loss = (2.083*(100/TubingCoeff)^1.85*(Qdes         /34.3)^1.85/TubingID^4.8655)  *PSDft/1000
        #_friction_loss = (2.083*(100/_coefficient)**1.85*(_qdes/34.3)**1.85/_tubing_id**4.8655)*_psd/1000
        _friction_loss = (2.083*(100/st.session_state._coefficient)**1.85*(_qdes/34.3)**1.85/_tubing_id**4.8655)*_psd/1000
    
        # % Free Gas = Vg / Vt
        _persen_free_gas = (_Vg / _Vt) * 100
    
        # TDH = sum(WFL, WHP, CP, FrictionLoss)  --> CP (Optional, bila tdk dinput, defaultnya nol) 
        _tdh = _wfl + _whp_hitung + _cp + _friction_loss
    
        #Fluid Over Pump = (PIP-CP)*2.31/SGFluid
        _fluid_over_pump = (_pip - _cp)*2.31/_sgfluid
    
        # Fluid Gradient = SGFluid/2.31
        _fluid_gradient = _sgfluid/2.31
    
        # ---------- Counting data for ipr_curve (2Fields, 2Records) ----------------------- 
        _settingDepth_or_PSD = 262.967487
        _flowrate1 = 0 
        _pressure1 = _settingDepth_or_PSD
    
        _qmax = _sbhp * _pi
        _flowrate2 = _qmax * 1.05
        _pressure2 = _settingDepth_or_PSD
        
        df_ipr_data = pd.DataFrame({'Flow rate': [_flowrate1, _flowrate2],
                                    'Pressure': [_pressure1, _pressure2]})
        # ---------------------------- until here -----------------------------------------        
    
        st.write('\n')
        st.title("Calculation")
        col1, col2 = st.columns(2, gap="medium", vertical_alignment="top")
        with col1:
            _Pwf_at_Qdes = round(_Pwf_at_Qdes, 2) # jadi 786.7571 yg sblmnya 786.757076405096
            _composite_sg = round(_composite_sg, 2) # sblmnya 0.490559258022
            st.write("Pwf@Qdes: ", _Pwf_at_Qdes, 'psi')
            st.write('Qdes         : ', _qdes, 'BPD')
            st.write('Composite SG : ', _composite_sg) #, '(selisih/beda 0.0003 lbh kecil)')
            #t.write('Di file xls: 0.490859')
            #st.write('\n')
    
            _wfl = round(_wfl, 2) # sblmnya 4743.3883109093
            st.write('PSD          : ', _psd, _measurement, 'TVD')
            st.write('Vertical Lift (Hd)  : ', _wfl, _measurement, 'TVD')
            #st.write('Di file xls: 4744.936')
            #st.write('Hitung2an:')
            #st.write('WFL = PSD - (PIP * 2.31 / SGFluid)')
            #st.write('=', _psd, '- ((', _pip, '* 2.31) /', _sgfluid)
            #st.write('=', _psd, '-', (_pip * 2.31), '/', _sgfluid)
            #st.write('=', _psd, '-', (_pip * 2.31) / _sgfluid)
            #st.write('=', round(_psd - (_pip * 2.31) / _sgfluid, 2), '(selisih/beda 1.6 lbh kecil)')
            #st.write('\n')
            
            _pi = round(_pi, 2)
            _whp_hitung = round(_whp_hitung, 2)
            st.write('PI (Well Prod-tvt Index)   : ', _pi, 'BPD')
            st.write('THP          : ', _whp_hitung, _measurement, 'TVD')
            #st.write('Di file xls: 345.0997')
            #st.write('Hitung2an WHP:')
            #st.write('WHP = THP * 2.31 / SGFluid')
            #st.write('= (', _whp, '* 2.31) /', _sgfluid)
            #st.write('=', _whp * 2.31, '/', _sgfluid)
            #st.write('=', round((_whp * 2.31) / _sgfluid, 2), '(selisih/beda 0.3 lbh besar)')
            #st.write('\n')
    
            _sgfluid = round(_sgfluid, 2)
            #st.write('SG Fluid = WC * SGw + (1 - WC) * Sgo')
            #st.write('= (', _wc, '/100) * ', _sgw, '+ (1 - (',  _wc, '/100)) * ', _sgo)
            #st.write('= ', _wc/100,' * ', _sgw, '+ (1 - ', _wc/100, ') * ', _sgo)
            #st.write('= ', _wc/100,' * ', _sgw, '+ ', 1 - (_wc/100), ' * ', _sgo)
            #st.write('= ', (_wc/100) * _sgw, '+ ', (1 - (_wc/100)) * _sgo)
            #_sgfluid = (_wc/100) * _sgw + (1-(_wc/100)) * _sgo
            st.write('SG Fluid     : ', _sgfluid) #, '(selisih/beda 0.001 lbh kecil)')
            #st.write('Di file xls: 1.004')
            #st.write('\n')
                    
            _pip = round(_pip, 2)
            st.write('PIP          : ', _pip, 'psi')
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
            _friction_loss = round(_friction_loss, 2)
            _persen_free_gas = round(_persen_free_gas, 2)
            st.write('P. Casing    : ', _p_casing_hitung, _measurement, 'TVD')
            st.write('Friction Loss: ', _friction_loss, _measurement, 'TVD')
            st.write('% Free Gas     : ', _persen_free_gas, '%')
            #st.write('Di file xls: 51.80 %')
            #st.write('Hitung2an % Free Gas:')
            #st.write('Free Gas = (Vg / Vt) * 100')
            #st.write('= (', _Vg, '/', _Vt, ') * 100')
            #st.write('=', round((_Vg / _Vt) * 100, 2), '(selisih/beda 0.01 lbh kecil)')
            #st.write('\n')
    
            _tdh = round(_tdh, 2)
            st.write('TDH            : ', _tdh, _measurement, 'TVD')
            #st.write('Di file xls: 5376.58')
            #st.write('Hitung2an TDH:')
            #st.write('= WFL + WHP + CP + FrictionLoss')
            #st.write('CP Optional, bila tdk dinput, defaultnya nol')
            #st.write('=', _wfl, '+', _whp_hitung, '+', _cp, '+', _friction_loss)
            #st.write('=', round(_wfl + _whp_hitung + _cp + _friction_loss, 2), '(selisih/beda 1.2 lbh kecil)')
            #st.write('\n')
    
            _fluid_over_pump = round(_fluid_over_pump, 2)
            st.write('SBHP           : ', _sbhp, 'psig')
            st.write('Fluid Over Pump: ', _fluid_over_pump, _measurement, 'TVD')
            #st.write('Di file xls: 1205.1334')
            #st.write('Hitung2an Fluid Over Pump:')
            #st.write('= (PIP - CP) * 2.31 / SGFluid')
            #st.write('= ((', _pip, '-', _cp, ') * 2.31) /', _sgfluid)
            #st.write('= (', _pip - _cp, '* 2.31) /', _sgfluid)
            #st.write('=', (_pip - _cp) * 2.31, '/', _sgfluid)
            #st.write('=', round(((_pip - _cp) * 2.31) / _sgfluid, 2), '(selisih/beda 1.48 lbh besar)')
            #st.write('\n')
    
            _fluid_gradient = round(_fluid_gradient, 2)
            st.write('FBHP           : ', _fbhp, 'psig')
            st.write('Fluid Gradient : ', _fluid_gradient, 'psi/', _measurement, 'TVD')
            #st.write('Di file xls: 0.43463 (selisih/beda 0.0004 lbh kecil)')
    
        st.write('\n')
        st.title("Inflow Performance Relationships")    
        #row5_1, row5_spacer2, row5_2= st.columns((11.1, .1, 3.8))
        #with row5_1:
        # perbesar figsize
        #plt.figure(figsize=(20,10))
        plt.figure(figsize=(10,5))

        fig, ax  = plt.subplots()

        # membuat line plot
        plt.plot(df_ipr_data['Flow rate'], df_ipr_data['Pressure'], 'or:')

        # set title & label
        plt.xlabel('Flow rate, Q (BFPD)',fontsize=13,color='darkred')
        plt.ylabel('Pressure (psi)',fontsize=13,color='darkred')

        # custom line
        plot_line = plt.plot(df_ipr_data['Flow rate'], df_ipr_data['Pressure'])
        plt.setp(plot_line, color='red', linestyle=':',  linewidth=0.1, marker='o')

        # set start 0 y axis
        plt.ylim(ymin=0)
        plt.xlim(xmin=0)

        # set grid
        plt.grid(color='darkgray', linestyle=':', linewidth=0.5)

        st.pyplot(fig)
        #with row5_2:            
        #st.dataframe(df_ipr_data, hide_index=True)                  
        new_records = [[new_id_calc, _user_id, _well_name, _field_name, _company, _engineer, _date_calc, \
                         _id_instrument, _id_calc_method, _id_welltype, _id_measurement, _comment_or_info, \
                         _top_perfo_tvd, _top_perfo_md, _bottom_perfo_tvd, _bottom_perfo_md, _qtest, _sbhp, _fbhp, \
                         _producing_gor, _wc, _bht, _sgw, _sgg, _qdes, _psd, _whp, _psd_md, _p_casing, _pb, _cp, \
                         st.session_state.api, st.session_state.sgo, _id_casing_size, _id_tubing_size, _id_tubing_id, \
                         st.session_state._id_tubing_coeff, _liner_id, _top_liner_at, _bottom_liner_at]]                               
        with open('tmycalc.csv', mode='a', newline='') as f_object:
            #writer_object = csv.writer(file)            
            writer_object = writer(f_object)            
            # Add new rows to the CSV
            writer_object.writerows(new_records)                    
            f_object.close() 
               
        if st.button("Confirm"):      
            st.write('')
    
