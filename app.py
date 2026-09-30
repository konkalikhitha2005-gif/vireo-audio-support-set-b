
import streamlit as st,pandas as pd,numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from analysis import load_data,agent_metrics,training_candidates,kpis
st.set_page_config(page_title="Vireo Audio Support",layout="wide")
st.title("Vireo Audio — Support Performance"); st.caption("Set B · Jan 2025–Jun 2026 · local/offline analysis")
t,a,o,p,c=load_data(); m=agent_metrics(t,a); kp=kpis(t,a)
with st.sidebar:
    teams=sorted(m[m.tier==1].team.unique()); chosen=st.multiselect("Tier-1 teams",teams,teams); mins=st.slider("Minimum CSAT responses",20,150,50,5)
f=m[(m.tier==1)&m.team.isin(chosen)&(m.csat_responses>=mins)]
tab1,tab2,tab3=st.tabs(["Overview","Training candidates","Ticket explorer"])
with tab1:
    c1,c2,c3,c4=st.columns(4); c1.metric("Tier-1 CSAT",f"{kp['csat']:.2f}/5"); c2.metric("CSAT responses",f"{kp['csat_responses']:,}")
    c3.metric("Tier-1 breach rate",f"{kp['tier1_breach_rate']*100:.2f}%"); c4.metric("Q savings at 6%",f"₹{kp['quarterly_sla_savings_at_6pct']:,.0f}")
    st.info("Tier-2 is excluded from Tier-1 comparison per policy. Candidates use within-team percentiles to reduce queue-mix bias.")
    out=f[["agent_id","name","team","site","shift","tickets","csat_responses","csat","median_handle_min","breach_rate","low_csat_rate"]].copy()
    out["breach_rate"]*=100; out["low_csat_rate"]*=100
    st.dataframe(out.rename(columns={"csat":"CSAT","median_handle_min":"Median handle (min)","breach_rate":"Breach %","low_csat_rate":"Low CSAT %"}).sort_values(["CSAT","Median handle (min)"]),use_container_width=True,hide_index=True)
with tab2:
    st.subheader("10 training candidates"); st.caption("Prioritization aid, not a disciplinary ranking. Tier-1, ≥50 CSAT responses; CSAT 60%, handle 25%, breach 15%, all within team.")
    x=training_candidates(t,a); out=x[["agent_id","name","team","tickets","csat_responses","csat","median_handle_min","breach_rate","low_csat_rate","training_risk"]].copy()
    out["breach_rate"]*=100; out["low_csat_rate"]*=100
    st.dataframe(out.rename(columns={"csat":"CSAT","median_handle_min":"Median handle (min)","breach_rate":"Breach %","low_csat_rate":"Low CSAT %","training_risk":"Training risk"}),use_container_width=True,hide_index=True)
    st.download_button("Download CSV",out.to_csv(index=False).encode(),"training_candidates.csv","text/csv")
with tab3:
    st.subheader("Ticket explorer + local text similarity")
    chosen_ticket=st.selectbox("Ticket",t.ticket_id.tolist()); row=t[t.ticket_id==chosen_ticket].iloc[0]
    st.write("**Customer message:**",row.customer_message or "(blank)"); st.write("**Agent notes:**",row.agent_notes or "(blank)")
    if st.button("Find similar tickets"):
        corpus=(t.customer_message.fillna("")+" "+t.agent_notes.fillna("")).astype(str)
        v=TfidfVectorizer(stop_words="english",max_features=15000,ngram_range=(1,2),min_df=2); X=v.fit_transform(corpus)
        idx=t.index[t.ticket_id==chosen_ticket][0]; sims=cosine_similarity(X[idx],X).ravel(); order=np.argsort(-sims)
        rows=[]
        for i in order:
            if t.iloc[i].ticket_id==chosen_ticket: continue
            rows.append({"ticket_id":t.iloc[i].ticket_id,"similarity":round(float(sims[i]),3),"channel":t.iloc[i].channel,"category":t.iloc[i].category,"csat":t.iloc[i].csat_score})
            if len(rows)==5: break
        st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True)
