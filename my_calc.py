import streamlit as st
import pandas as pd
import pandasql as ps
import matplotlib.pyplot as plt
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder

#@st.dialog("ID Calculation")
#def show_id_form():
#    st.text_input("ID Calculation")

#open datas
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

st.title("My Calculations")

mycalc3 = ps.sqldf("select m.id_calc, m.user_id, u.username, m.well_name, m.field_name, m.company, m.engineer, \
        m.date_calc, m.id_instrument, i.instrument, m.id_calc_method, c.calc_method, m.id_welltype, \
        w.welltype, m.id_measurement, meas.measurement, m.comment_or_info, m.top_perfo_tvd, m.top_perfo_md, \
        m.bottom_perfo_tvd, m.bottom_perfo_md, m.qtest, m.sbhp, m.fbhp, m.producing_gor, m.wc, m.bht, \
        m.sgw, m.sgg, m.qdes, m.psd, m.whp, m.psd_md, m.p_casing, m.pb, m.api, m.sgo, \
        s.casing_size, s.casing_drift_id, tubsize.tubing_size, tubid.tubing_id, \
        tubcoef.type, tubcoef.coefficient, m.liner_id, m.top_liner_at, m.bottom_liner_at \
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

gd = GridOptionsBuilder.from_dataframe(mycalc3)
gd.configure_pagination(enabled=True)
#gd.configure_default_column(editable=True, groupable=True)

#sel_mode = st.radio('Selection Type', options=['single', 'multiple'])
#gd.configure_selection(selection_mode=sel_mode, use_checkbox=True)
gd.configure_selection(use_checkbox=True)
gridoptions = gd.build()

#AgGrid(mycalc3, gridOptions=gridoptions)
bs_grid_table = AgGrid(mycalc3, gridOptions=gridoptions,
                        enable_enterprise_modul=True,
                        height=500,
                        allow_unsafe_jscode=True,
                        theme='alpine')
sel_row = bs_grid_table["selected_rows"]
#if not sel_row.empty:
#    st.dataframe(sel_row, hide_index=True)

id_calc_01=0
col1, col2 = st.columns(2, gap="medium", vertical_alignment="top")
with col1:
    st.markdown("<p style='text-align: justify;'>Masukkan Nomor ID Calculation untuk melihat detail informasi \
        perhitungan yang sudah dibuat, seperti Well Name, Field Name, Created by, Company, \
        dan lain-lain.</p>", unsafe_allow_html=True)

with col2:
    id_calc_01 = st.number_input("ID Calculation To Explore:", 0, None, "min", 1)
   
if id_calc_01:
    mycalc4 = mycalc3.loc[mycalc3['id_calc']==id_calc_01].reset_index(drop=True)

    _username = mycalc4['username'].values[0]; _well_name = mycalc4['well_name'].values[0]
    _field_name=mycalc4['field_name'].values[0]; _company=mycalc4['company'].values[0]; _engineer=mycalc4['engineer'].values[0]
    _date_calc=mycalc4['date_calc'].values[0]
    _instrument=mycalc4['instrument'].values[0]; _id_instrument=mycalc4['id_instrument'].values[0]
    _calc_method=mycalc4['calc_method'].values[0]; _welltype=mycalc4['welltype'].values[0]
    _id_calc_method=mycalc4['id_calc_method'].values[0]
    _measurement=mycalc4['measurement'].values[0]; _comment_or_info=mycalc4['comment_or_info'].values[0]
    
    #st.write('id instrument=', _id_instrument, 'id calc methon=', _id_calc_method)
    st.title("General Information")
    col1, col2 = st.columns(2, gap="medium", vertical_alignment="top")
    with col1:
        st.subheader('ID Calculation:')
        st.markdown(id_calc_01)
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

    _top_perfo_tvd=mycalc4['top_perfo_tvd'].values[0]; _top_perfo_md=mycalc4['top_perfo_md'].values[0]
    _bottom_perfo_tvd=mycalc4['bottom_perfo_tvd'].values[0]; _bottom_perfo_md=mycalc4['bottom_perfo_md'].values[0]
    _qtest=mycalc4['qtest'].values[0]; _sbhp=mycalc4['sbhp'].values[0]; _fbhp=mycalc4['fbhp'].values[0]
    _producing_gor=mycalc4['producing_gor'].values[0]; _wc=mycalc4['wc'].values[0]; _bht=mycalc4['bht'].values[0]
    _sgw=mycalc4['sgw'].values[0]; _sgg=mycalc4['sgg'].values[0]; _qdes=mycalc4['qdes'].values[0]
    _psd=mycalc4['psd'].values[0]; _whp=mycalc4['whp'].values[0]; _psd_md=mycalc4['psd_md'].values[0]
    
    _p_casing=mycalc4['p_casing'].values[0]; _pb=mycalc4['pb'].values[0];       
    _api=mycalc4['api'].values[0]; _sgo=mycalc4['sgo'].values[0]

    _casing_size=mycalc4['casing_size'].values[0]; _casing_id=mycalc4['casing_drift_id'].values[0]
    _tubing_size=mycalc4['tubing_size'].values[0]; _tubing_id=mycalc4['tubing_id'].values[0]
    _tubing_coeff_type=mycalc4['type'].values[0]
    _coefficient=mycalc4['coefficient'].values[0]

    _liner_id=mycalc4['liner_id'].values[0]; _top_liner_at=mycalc4['top_liner_at'].values[0]
    _bottom_liner_at=mycalc4['bottom_liner_at'].values[0]
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
        st.write('SBHP         : ', _sbhp, 'psig')
        st.write('FBHP         : ', _fbhp, 'psig')
        st.write('Producing GOR: ', _producing_gor, 'scf/stb')
        st.write('WC           : ', _wc, '%')
        st.write('BHT          : ', _bht, '℉')
        st.write('SGw          : ', _sgw)
        st.write('SGg          : ', _sgg)
        st.write('Qdes         : ', _qdes, 'BPD')
        st.write('PSD          : ', _psd, _measurement, 'TVD')
        st.write('WHP          : ', _whp, 'psi')
        st.write('PSD (MD)     : ', _psd_md, _measurement, 'MD')
        st.header("Basic Data (Optional)", divider="gray")
        st.write('P. Casing    : ', _p_casing, 'psi')
        st.write('Pb           : ', _pb, 'psig')
    with row3_2:
        st.header("API/Sgo", divider="gray")
        st.write('API          : ', _api)
        st.write('Sgo          : ', _sgo)
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
        st.write('Top Liner at : ', _top_liner_at, _measurement, 'TVD')
        st.write('Bottom Liner at: ', _bottom_liner_at, _measurement, 'MD')

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
        _wfl = _psd-(_pip*2.31/_sgfluid)
    
        # WHP = THP(WHP)*2.31/SGFluid
        _whp_hitung=_whp*2.31/_sgfluid
    
        if _p_casing == 0:
            _p_casing_hitung = 0
        else:
            _p_casing_hitung = (_p_casing * 2.31 / _sgfluid) / 3.28084 # -> utk jadi meter
    
        # Friction Loss = (2.083*(100/TubingCoeff)^1.85*(Qdes         /34.3)^1.85/TubingID^4.8655)  *PSDft/1000
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
        
           st.write('SBHP           : ', _sbhp, 'psig')
           st.write('Fluid Over Pump: ', round(_fluid_over_pump,3), _measurement, 'TVD')
           #st.write('Di file xls: 1205.1334')
           #st.write('Hitung2an Fluid Over Pump:')
           #st.write('= (PIP - CP) * 2.31 / SGFluid')
           #st.write('= ((', _pip, '-', _cp, ') * 2.31) /', _sgfluid)
           #st.write('= (', _pip - _cp, '* 2.31) /', _sgfluid)
           #st.write('=', (_pip - _cp) * 2.31, '/', _sgfluid)
           #st.write('=', round(((_pip - _cp) * 2.31) / _sgfluid, 2), '(selisih/beda 1.48 lbh besar)')
           #st.write('\n')
        
           st.write('FBHP           : ', _fbhp, 'psig')
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

        st.pyplot(fig)
        #with row5_2:
        #    st.dataframe(df_ipr_data, hide_index=True)
        #    st.write('')
    
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
        _wfl = _psd-(_pip*2.31/_sgfluid)
    
        # WHP = THP(WHP)*2.31/SGFluid
        _whp_hitung=_whp*2.31/_sgfluid
    
        if _p_casing == 0:
            _p_casing_hitung = 0
        else:
            _p_casing_hitung = (_p_casing * 2.31 / _sgfluid) / 3.28084 # -> utk jadi meter
    
        # Friction Loss = (2.083*(100/TubingCoeff)^1.85*(Qdes         /34.3)^1.85/TubingID^4.8655)  *PSDft/1000
        _friction_loss = (2.083*(100/_coefficient)**1.85*(_qdes/34.3)**1.85/_tubing_id**4.8655)*_psd/1000
    
        # % Free Gas = Vg / Vt
        _persen_free_gas = (_Vg / _Vt) * 100
    
        # TDH = sum(WFL, WHP, CP, FrictionLoss)  --> CP (Optional, bila tdk dinput, defaultnya nol) 
        #_tdh = _wfl + _whp_hitung + _cp + _friction_loss 
        _tdh = _wfl + _whp_hitung + _p_casing_hitung + _friction_loss  # cp dihapus, jadi kalau perlu cp, diganti dgn p.casing
        
        #Fluid Over Pump = (PIP-CP)*2.31/SGFluid
        #_fluid_over_pump = (_pip - _cp)*2.31/_sgfluid  
        _fluid_over_pump = (_pip - _p_casing_hitung)*2.31/_sgfluid  # cp dihapus, jadi kalau perlu cp, diganti dgn p.casing
    
        # Fluid Gradient = SGFluid/2.31
        _fluid_gradient = _sgfluid/2.31
    
        # ---------- Counting data for ipr_curve (2Fields, 2Records) ----------------------- 
        _qmax = _sbhp * _pi               
        
        _flowrate1 = 0 
        _pressure1 = _sbhp
        
        _flowrate2 = _qmax
        _pressure2 = 0
        
        df_ipr_data = pd.DataFrame({'Flow rate': [_flowrate1, _flowrate2],
                                    'Pressure': [_pressure1, _pressure2]})
        
        df_ipr_data = df_ipr_data.sort_values(by=['Flow rate', 'Pressure'], ascending=[False, True])
        # ---------------------------- until here -----------------------------------------        

        # ---------- Counting data for Flowrate di PSD (2Fields, 2Records) ----------------------- 
        #_settingDepth_or_PSD = 262.967487
        
        _flowrate1b = 0
        _pressure1b = (_MidPerf - _psd) * _sgfluid / 2.31 + _p_casing_hitung # cp dihapus, jadi kalau perlu cp, diganti dgn p.casing        
        
        _flowrate2b = _qmax * 1.05
        _pressure2b = _pressure1b        
        
        _flowrate3b = _qmax * 1.05
        _pressure3b = _pressure1b    

        _flowrate4b = _qmax * 1.05
        _pressure4b = 0
        
        df_flowrate_psd = pd.DataFrame({'Flow rate': [_flowrate1b, _flowrate2b, _flowrate3b, _flowrate4b],
                'Pressure': [_pressure1b, _pressure2b, _pressure3b, _pressure4b]})
            
        df_flowrate_psd = df_flowrate_psd.sort_values(by=['Flow rate', 'Pressure'], ascending=[True, False])
        # ---------------------------- until here -----------------------------------------        

        # ---------- Counting data for Flowrate di Pwf@Qdes (2Fields, 4Records) ----------------------- 
        _flowrate1c = 0
        _pressure1c = _Pwf_at_Qdes
   
        _flowrate2c = _qdes
        _pressure2c = _Pwf_at_Qdes

        _flowrate3c = _qdes
        _pressure3c = _Pwf_at_Qdes

        _flowrate4c = _qdes
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
            #t.write('Di file xls: 0.490859')
            #st.write('\n')
    
            st.write('PSD          : ', _psd, _measurement, 'TVD')
            st.write('Vertical Lift (Hd)  : ', round(_wfl,3), _measurement, 'TVD')
            #st.write('Di file xls: 4744.936')
            #st.write('Hitung2an:')
            #st.write('WFL = PSD - (PIP * 2.31 / SGFluid)')
            #st.write('=', _psd, '- ((', _pip, '* 2.31) /', _sgfluid)
            #st.write('=', _psd, '-', (_pip * 2.31), '/', _sgfluid)
            #st.write('=', _psd, '-', (_pip * 2.31) / _sgfluid)
            #st.write('=', round(_psd - (_pip * 2.31) / _sgfluid, 2), '(selisih/beda 1.6 lbh kecil)')
            #st.write('\n')
            
            st.write('PI (Well Prod-tvt Index)   : ', round(_pi,3), 'BPD')
            st.write('THP          : ', round(_whp_hitung,3), _measurement, 'TVD')
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
            st.write('SG Fluid     : ', round(_sgfluid,3)) #, '(selisih/beda 0.001 lbh kecil)')
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
    
            st.write('SBHP           : ', _sbhp, 'psig')
            st.write('Fluid Over Pump: ', round(_fluid_over_pump,3), _measurement, 'TVD')
            #st.write('Di file xls: 1205.1334')
            #st.write('Hitung2an Fluid Over Pump:')
            #st.write('= (PIP - CP) * 2.31 / SGFluid')
            #st.write('= ((', _pip, '-', _cp, ') * 2.31) /', _sgfluid)
            #st.write('= (', _pip - _cp, '* 2.31) /', _sgfluid)
            #st.write('=', (_pip - _cp) * 2.31, '/', _sgfluid)
            #st.write('=', round(((_pip - _cp) * 2.31) / _sgfluid, 2), '(selisih/beda 1.48 lbh besar)')
            #st.write('\n')
    
            st.write('FBHP           : ', _fbhp, 'psig')
            st.write('Fluid Gradient : ', round(_fluid_gradient,3), 'psi/', _measurement, 'TVD')
            #st.write('Di file xls: 0.43463 (selisih/beda 0.0004 lbh kecil)')
    
        st.write('\n')
        st.title("Inflow Performance Relationships")    
        #row5_1, row5_spacer2, row5_2= st.columns((11.1, .1, 3.8))
        #with row5_1:
        # perbesar figsize
        #plt.figure(figsize=(20,10))
        plt.figure(figsize=(8,3))

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
