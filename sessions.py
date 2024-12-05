import streamlit as st
import pandas as pd
import datetime as dt
from streamlit_gsheets import GSheetsConnection

def sessionstates():
    if "mycalc3" not in st.session_state:
        st.session_state["mycalc3"] = pd.DataFrame()
    if "mycalc3c" not in st.session_state:
        st.session_state["mycalc3c"] = pd.DataFrame()

    if "_well_name_search" not in st.session_state:
        st.session_state["_well_name_search"] = ''  # in mycalc.py that called this funct
    if "id_calc_01" not in st.session_state:
        st.session_state["id_calc_01"] = 0
    if "id_calc_02" not in st.session_state:
        st.session_state["id_calc_02"] = 0
    #if "new_id_calc" not in st.session_state:
    #    st.session_state["new_id_calc"] = last_id_calc

    if "user_id" not in st.session_state:
        st.session_state["_user_id"] = ''    
    if "_username" not in st.session_state:
        st.session_state["_username"] = ''    
    if "_id_calc_method" not in st.session_state:
        st.session_state["_id_calc_method"] = ''            
    if "_id_welltype" not in st.session_state:
        st.session_state["_id_welltype"] = ''
    if "_id_measurement" not in st.session_state:
        st.session_state["_id_measurement"] = ''
    if "_well_name" not in st.session_state:
        st.session_state["_well_name"] = ''
    if "_field_name" not in st.session_state:
        st.session_state["_field_name"] = ''
    if "_company" not in st.session_state:
        st.session_state["_company"] = ''    
    if "_engineer" not in st.session_state:
        st.session_state["_engineer"] = ''
    if "_id_instrument" not in st.session_state:
        st.session_state["_id_instrument"] = 0
    if "_comment_or_info" not in st.session_state:
        st.session_state["_comment_or_info"] = ''

    if "_top_perfo_tvd" not in st.session_state:
        st.session_state["_top_perfo_tvd"] = 0.00
    if "_bottom_perfo_tvd" not in st.session_state:
        st.session_state["_bottom_perfo_tvd"] = 0.00    

    if "_top_perfo_md" not in st.session_state:
        st.session_state["_top_perfo_md"] = 0.00
    if "_bottom_perfo_md" not in st.session_state:
        st.session_state["_bottom_perfo_md"] = 0.00       

    if "_sfl" not in st.session_state:
        st.session_state["_sfl"] = 0.00       
    if "_smgFreeGasAtQtest" not in st.session_state:
        st.session_state["_smgFreeGasAtQtest"] = 0.00       
    if "_qtest" not in st.session_state:
        st.session_state["_qtest"] = 0.00       
    if "_sbhp" not in st.session_state:
        st.session_state["_sbhp"] = 0.00       
    if "_fbhp" not in st.session_state:
        st.session_state["_fbhp"] = 0.00       
    if "_producing_gor" not in st.session_state:
        st.session_state["_producing_gor"] = 0.00       
    if "_wc" not in st.session_state:
        st.session_state["_wc"] = 0.00       
    if "_bht" not in st.session_state:
        st.session_state["_bht"] = 0.00       
    if "_sgw" not in st.session_state:
        st.session_state["_sgw"] = 0.00       
    if "_sgg" not in st.session_state:
        st.session_state["_sgg"] = 0.00       
    if "_qdes" not in st.session_state:
        st.session_state["_qdes"] = 0.00       
    if "_psd" not in st.session_state:
        st.session_state["_psd"] = 0.00       
    if "_psd_md" not in st.session_state:
        st.session_state["_psd_md"] = 0.00       
    if "_whp" not in st.session_state:
        st.session_state["_whp"] = 0.00       

    if "_p_casing" not in st.session_state:
        st.session_state["_p_casing"] = 0.00       
    if "_pb" not in st.session_state:
        st.session_state["_pb"] = 0.00    

    if "_api" not in st.session_state:
        st.session_state["_api"] = 0.00          
    if "_sgo" not in st.session_state:
        st.session_state["_sgo"] = 0.00       
    if "lbs" not in st.session_state:
        st.session_state["lbs"] = 0.00          
    if "kg" not in st.session_state:
        st.session_state["kg"] = 0.00       

    if "_liner_id" not in st.session_state:
        st.session_state["_liner_id"] = 0.00       
    if "_top_liner_at_tvd" not in st.session_state:
        st.session_state["_top_liner_at_tvd"] = 0.00       
    if "_top_liner_at_md" not in st.session_state:
        st.session_state["_top_liner_at_md"] = 0.00       
    if "_bottom_liner_at_tvd" not in st.session_state:
        st.session_state["_bottom_liner_at_tvd"] = 0.00       
    if "_bottom_liner_at_md" not in st.session_state:
        st.session_state["_bottom_liner_at_md"] = 0.00       

    if "_id_casing_size" not in st.session_state:
        st.session_state["_id_casing_size"] = 0     
    if "_id_casing_id" not in st.session_state:
        st.session_state["_id_casing_id"] = 0.00
    if "_casing_size" not in st.session_state:
        st.session_state["_casing_size"] = ''      
    if "_casing_id" not in st.session_state:
        st.session_state["_casing_id"] = 0.00

    if "_id_tubing_size" not in st.session_state:
        st.session_state["_id_tubing_size"] = 0
    if "_id_tubing_id" not in st.session_state:
        st.session_state["_id_tubing_id"] = 0
    if "_tubing_size" not in st.session_state:
        st.session_state["_tubing_size"] = 0.00
    if "_tubing_id" not in st.session_state:
        st.session_state["_tubing_id"] = 0.00

    if "_id_tubing_coeff" not in st.session_state:
        st.session_state["_id_tubing_coeff"] = 0
    if "_tubing_coeff_type" not in st.session_state:
        st.session_state["_tubing_coeff_type"] = ''  
    if "_coefficient" not in st.session_state:
        st.session_state["_coefficient"] = 0       
