import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
#import my_calc --> diremark karena kalau disini import file itu, lalu itu import file ini, error! 
#Jadi variabel2 yg ada di file itu dipanggilnya pakai st.session_state aja

def my_calc_straight():
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

    # sgfluid di atas, krn p_casing_hitung perlu dia utk perhitungan rumus
    # SGFluid = WC * SGw + (1 - WC) * Sgo
    #         = 88% * 1.02 + (1- 88%) * 0.887147335
    _sgfluid = (st.session_state._wc/100) * st.session_state._sgw + (1-(st.session_state._wc/100)) * st.session_state._sgo

    if st.session_state._p_casing == 0:
        _p_casing_hitung = 0
    else:
        if st.session_state._measurement=='m': # mtr (bila pilihan di awal nya adalah satuan meter, harus diconvert ke meter)
            _p_casing_hitung = (st.session_state._p_casing * 2.31 / _sgfluid) / 3.28084 # -> utk jadi meter
        elif st.session_state._measurement=='ft': # ft, biarkan saja, gak usah diconver (dibagi 3.28084 atu dikali 0.3048)
            _p_casing_hitung = (st.session_state._p_casing * 2.31 / _sgfluid) # -> utk jadi feet

    # MidPerf = 0.5(TopPerfoTVD+BottomPerfoTVD)
    _MidPerf = 0.5 * (st.session_state._top_perfo_tvd + st.session_state._bottom_perfo_tvd)
    # 12Nov24
    if st.session_state._id_measurement==1: # m (meter), bila inputnya mtr, karena _MidPerf hrs dlm ft, jadi diconvert dulu ke ft
        _MidPerf *= 3.28084
    
    # di bawah ini gak jadi, krn ini hanya explore, ambil saja SBHP & FBHP yg tersimpan
    # to convert SFL & SMG (already in ft) into SBHP & FBHP
    if st.session_state._id_instrument==2: # Sonolog
        st.session_state._sbhp = _p_casing_hitung + _sgfluid / 2.31 * (_MidPerf - st.session_state._sfl)
        st.session_state._fbhp = _p_casing_hitung + _sgfluid / 2.31 * (_MidPerf - (st.session_state._sfl+st.session_state._smgFreeGasAtQtest))

    # in straight line no need _qmax but _pi
    _pi = st.session_state._qtest / (st.session_state._sbhp - st.session_state._fbhp)
    #_qmax = _qtest / (1 - 0.2 * (_fbhp/_sbhp) - 0.8 * (_fbhp/_sbhp) ** 2)

    # _Pwf_at_Qdes = (5 * math.sqrt(3.24 - 3.2 * (_qdes/_qmax)) - 1) / 8 * _sbhp --> library math susah diDeploy
    #_Pwf_at_Qdes = (5 * (3.24 - 3.2 * (_qdes/_qmax))**0.5 - 1) / 8 * _sbhp
    # in straight line:
    _Pwf_at_Qdes = st.session_state._sbhp - st.session_state._qdes / _pi

    #12Nov24 sblm hitung pip hrs convert psd tvd dan psd md yg meter ke ft
    if st.session_state._measurement=='m': # m (meter)
        # PIP=Pwf@Qdes-(MidPerf-PSD)*SGFluid/2.31    
        _pip = _Pwf_at_Qdes - ((_MidPerf - (st.session_state._psd * 3.28084)) * (_sgfluid/2.31)) 
    elif st.session_state._measurement=='ft': # feet
        _pip = _Pwf_at_Qdes - ((_MidPerf - st.session_state._psd) * (_sgfluid/2.31)) 
            
    # Rs=Sgg*(( (PIP/18) * (10^(0.0125*API – 0.00091*BHT)) )^1.2048)
    _Rs=st.session_state._sgg*(( (_pip/18) * (10**(0.0125*st.session_state._api - 0.00091*st.session_state._bht)) )**1.2048)

    # Bo=0.972+0.000147*((Rs*SQRT(SGg/Sgo)+1.25*BHT)^1.175); 
    # _Bo = 0.972+0.000147*((_Rs*math.sqrt(_sgg/_sgo)+1.25*_bht)**1.175) --> math masalah diDeploy
    _Bo = 0.972+0.000147*((_Rs * (st.session_state._sgg/st.session_state._sgo)**0.5 + 1.25 * st.session_state._bht) ** 1.175)
    # Vo=(1-WC)*Qdes*Bo;
    _Vo = (1-(st.session_state._wc/100))*st.session_state._qdes*_Bo;

    # Bg=5.04*0.85*(BHT+460)/(PIP+14.7) -> yg benar kurung nya sprti di bawah
    _Bg=5.04*0.85*((st.session_state._bht+460)/(_pip+14.7))
    # Tg=(1-WC)*Qdes*ProducingGOR/1000;
    _Tg=(1-(st.session_state._wc/100))*st.session_state._qdes*st.session_state._producing_gor/1000
    #Sg=(1-WC)*Qdes*Rs/1000
    _Sg=(1-(st.session_state._wc/100))*st.session_state._qdes*_Rs/1000
    # Free Gas (FG) = Tg - Sg;
    _free_gas = _Tg - _Sg
    # Vg=Bg * Free Gas (FG);
    _Vg = _Bg * _free_gas

    # Vw=WC * Qdes
    _Vw = (st.session_state._wc/100) * st.session_state._qdes

    # Vt=Vo+Vg+Vw;
    _Vt = _Vo + _Vg + _Vw

    # _composite_sg = ( ( (1-WC)*Qdes*Sgo + WC*Qdes*Sgw) * 62.4*5.6146 + Producing GOR*(1-WC)*Qdes*Sgg*0.0752) / (Vt*5.6146*62.4)
    _composite_sg = ( ( (1-(st.session_state._wc/100))*st.session_state._qdes*st.session_state._sgo + (st.session_state._wc/100)*st.session_state._qdes*st.session_state._sgw) * 62.4*5.6146 + st.session_state._producing_gor*(1-(st.session_state._wc/100))*st.session_state._qdes*st.session_state._sgg*0.0752) / (_Vt*5.6146*62.4)

    # WFL =PSD-(PIP*2.31/SGFluid)
    if st.session_state._measurement=='m': # PSD nya dikali 3.28084 dulu (dikonversi ke ft krn PSD hrs dlm ft)
        _wfl = (st.session_state._psd*3.28084)-(_pip*2.31/_sgfluid)
        # lalu dirubah lgi ke mtr:
        _wfl = _wfl * 0.3048 # 0.3048 adalah 1/3.28084
    elif st.session_state._measurement=='ft': # PSD nya gak perlu dikali 3.28084 dulu
        _wfl = st.session_state._psd-(_pip*2.31/_sgfluid)
            
    # WHP = THP(WHP)*2.31/SGFluid (whp sdh diinput dlm pressure)
    if st.session_state._id_measurement==1: # m (meter)        
        _whp_hitung=st.session_state._whp*2.31/_sgfluid # jadi ft
        _whp_hitung *= 0.3048 # diconvert ke m (meter), krn saat ini hasil hitungannya dlm ft
    elif st.session_state._id_measurement==2: # ft (bila input awal pilihannya ft, biarkan saja, gak usah diconvert lgi)        
        _whp_hitung=st.session_state._whp*2.31/_sgfluid

    # Friction Loss = (2.083*(100/TubingCoeff)^1.85*(Qdes         /34.3)^1.85/TubingID^4.8655)  *PSDft/1000
    #_friction_loss = (2.083*(100/_coefficient)**1.85*(_qdes/34.3)**1.85/_tubing_id**4.8655)*_psd/1000
    if st.session_state._id_measurement==1: # m (meter), PSD nya dikali 3.28084 dulu (dikonversi ke ft krn PSD hrs dlm ft)        
        _friction_loss = (2.083*(100/st.session_state._coefficient)**1.85*(st.session_state._qdes/34.3)**1.85/st.session_state._tubing_id**4.8655)*(st.session_state._psd*3.28084)/1000
        # lalu dirubah lgi ke mtr sesuai apa yg diinput di awal (yg diinginkan dlm mtr)
        _friction_loss *= 0.3048        
    elif st.session_state._id_measurement==2: # ft (tdk perlu diconvert)
        _friction_loss = (2.083*(100/st.session_state._coefficient)**1.85*(st.session_state._qdes/34.3)**1.85/st.session_state._tubing_id**4.8655)*st.session_state._psd/1000

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
    _qmax = st.session_state._sbhp * _pi               
    
    _flowrate1 = 0 
    _pressure1 = st.session_state._sbhp
    
    _flowrate2 = _qmax
    _pressure2 = 0
    
    df_ipr_data = pd.DataFrame({'Flow rate': [_flowrate1, _flowrate2],
                                'Pressure': [_pressure1, _pressure2]})
    
    df_ipr_data = df_ipr_data.sort_values(by=['Flow rate', 'Pressure'], ascending=[False, True])
    # ---------------------------- until here -----------------------------------------        

    # ---------- Counting data for Flowrate di PSD (2Fields, 2Records) -----------------------       
    _flowrate1b = 0
    _pressure1b = (_MidPerf - st.session_state._psd) * _sgfluid / 2.31 + _p_casing_hitung # cp dihapus, jadi kalau perlu cp, diganti dgn p.casing        
    _settingDepth_or_PSD = _pressure1b

    #_flowrate2b = _qmax * 1.05
    #_flowrate2b = (SettingDepthPSD - SBHP) / ((FBHP - SBHP) / (Qtest - 0))
    _flowrate2b = (_settingDepth_or_PSD - st.session_state._sbhp) / ((st.session_state._fbhp - st.session_state._sbhp) / (st.session_state._qtest - 0))
    _pressure2b = _pressure1b        
    
    #_flowrate3b = _qmax * 1.05
    _flowrate3b = _flowrate2b
    _pressure3b = _pressure1b    

    #_flowrate4b = _qmax * 1.05
    _flowrate4b = _flowrate2b
    _pressure4b = 0
    
    df_flowrate_psd = pd.DataFrame({'Flow rate': [_flowrate1b, _flowrate2b, _flowrate3b, _flowrate4b],
            'Pressure': [_pressure1b, _pressure2b, _pressure3b, _pressure4b]})
        
    df_flowrate_psd = df_flowrate_psd.sort_values(by=['Flow rate', 'Pressure'], ascending=[True, False])
    # ---------------------------- until here -----------------------------------------        

    # ---------- Counting data for Flowrate di Pwf@Qdes (2Fields, 4Records) ----------------------- 
    _flowrate1c = 0
    _pressure1c = _Pwf_at_Qdes

    _flowrate2c = st.session_state._qdes
    _pressure2c = _Pwf_at_Qdes

    _flowrate3c = st.session_state._qdes
    _pressure3c = _Pwf_at_Qdes

    _flowrate4c = st.session_state._qdes
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
        st.write('Qdes         : ', st.session_state._qdes, 'BPD')
        st.write('Composite SG : ', round(_composite_sg, 3)) #, '(selisih/beda 0.0003 lbh kecil)')
        #t.write('Di file xls: 0.490859')
        #st.write('\n')

        st.write('PSD          : ', st.session_state._psd, st.session_state._measurement, 'TVD')
        st.write('Vertical Lift (Hd)  : ', round(_wfl,3), st.session_state._measurement, 'TVD')
        #st.write('Di file xls: 4744.936')
        #st.write('Hitung2an:')
        #st.write('WFL = PSD - (PIP * 2.31 / SGFluid)')
        #st.write('=', _psd, '- ((', _pip, '* 2.31) /', _sgfluid)
        #st.write('=', _psd, '-', (_pip * 2.31), '/', _sgfluid)
        #st.write('=', _psd, '-', (_pip * 2.31) / _sgfluid)
        #st.write('=', round(_psd - (_pip * 2.31) / _sgfluid, 2), '(selisih/beda 1.6 lbh kecil)')
        #st.write('\n')
        
        st.write('PI (Well Prod-tvt Index)   : ', round(_pi,3), 'BPD')
        st.write('THP          : ', round(_whp_hitung,3), st.session_state._measurement, 'TVD')
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
        st.write('P. Casing    : ', _p_casing_hitung, st.session_state._measurement, 'TVD')
        st.write('Friction Loss: ', round(_friction_loss,3), st.session_state._measurement, 'TVD')
        st.write('% Free Gas     : ', round(_persen_free_gas,3), '%')
        #st.write('Di file xls: 51.80 %')
        #st.write('Hitung2an % Free Gas:')
        #st.write('Free Gas = (Vg / Vt) * 100')
        #st.write('= (', _Vg, '/', _Vt, ') * 100')
        #st.write('=', round((_Vg / _Vt) * 100, 2), '(selisih/beda 0.01 lbh kecil)')
        #st.write('\n')

        st.write('TDH            : ', round(_tdh,3), st.session_state._measurement, 'TVD')
        #st.write('Di file xls: 5376.58')
        #st.write('Hitung2an TDH:')
        #st.write('= WFL + WHP + CP + FrictionLoss')
        #st.write('CP Optional, bila tdk dinput, defaultnya nol')
        #st.write('=', _wfl, '+', _whp_hitung, '+', _cp, '+', _friction_loss)
        #st.write('=', round(_wfl + _whp_hitung + _cp + _friction_loss, 2), '(selisih/beda 1.2 lbh kecil)')
        #st.write('\n')

        st.write('SBHP           : ', round(st.session_state._sbhp, 3), 'psig')
        st.write('Fluid Over Pump: ', round(_fluid_over_pump,3), st.session_state._measurement, 'TVD')
        #st.write('Di file xls: 1205.1334')
        #st.write('Hitung2an Fluid Over Pump:')
        #st.write('= (PIP - CP) * 2.31 / SGFluid')
        #st.write('= ((', _pip, '-', _cp, ') * 2.31) /', _sgfluid)
        #st.write('= (', _pip - _cp, '* 2.31) /', _sgfluid)
        #st.write('=', (_pip - _cp) * 2.31, '/', _sgfluid)
        #st.write('=', round(((_pip - _cp) * 2.31) / _sgfluid, 2), '(selisih/beda 1.48 lbh besar)')
        #st.write('\n')

        st.write('FBHP           : ', round(st.session_state._fbhp, 3), 'psig')
        st.write('Fluid Gradient : ', round(_fluid_gradient,3), 'psi/', st.session_state._measurement, 'TVD')
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

    plt.legend()

    st.pyplot(fig)
    #with row5_2:
    #    st.dataframe(df_ipr_data, hide_index=True)        
    #    st.write('')

