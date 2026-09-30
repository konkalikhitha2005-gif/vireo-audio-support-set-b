
from pathlib import Path
import pandas as pd
from config import SLA_TARGETS_MIN,SLA_BREACH_CREDIT_INR,TIER1_MIN_CSAT_RESPONSES
BASE=Path(__file__).resolve().parent; DATA=BASE/"data"
def load_data():
    t=pd.read_csv(DATA/"tickets.csv"); a=pd.read_csv(DATA/"agents.csv")
    o=pd.read_csv(DATA/"orders.csv"); p=pd.read_csv(DATA/"products.csv"); c=pd.read_csv(DATA/"customers.csv")
    for x in ["created_at","first_response_at","resolved_at"]: t[x]=pd.to_datetime(t[x],errors="coerce")
    t["csat_score"]=pd.to_numeric(t["csat_score"],errors="coerce"); t["transfers"]=pd.to_numeric(t["transfers"],errors="coerce").fillna(0)
    t["resolved_ist"]=t["resolved_at"]; legacy=t.source_system.eq("legacy_fd")&t.resolved_at.notna()
    t.loc[legacy,"resolved_ist"]+=pd.Timedelta(minutes=330)
    t["first_response_mins"]=(t.first_response_at-t.created_at).dt.total_seconds()/60
    t["handle_mins"]=(t.resolved_ist-t.first_response_at).dt.total_seconds()/60
    t["sla_target_mins"]=t.channel.map(SLA_TARGETS_MIN); t["breach"]=t.first_response_mins>t.sla_target_mins
    t["low_csat"]=t.csat_score<=2; t["completed"]=t.status.isin(["resolved","closed"])
    return t,a,o,p,c
def agent_metrics(t,a):
    d=t[t.completed]
    m=d.groupby("agent_id").agg(tickets=("ticket_id","size"),csat_responses=("csat_score","count"),csat=("csat_score","mean"),
      median_handle_min=("handle_mins","median"),mean_handle_min=("handle_mins","mean"),breach_rate=("breach","mean"),
      low_csat_responses=("low_csat","sum"))
    m["low_csat_rate"]=m.low_csat_responses/m.csat_responses
    r=a.drop_duplicates("agent_id")[["agent_id","name","site","team","shift","tier"]].set_index("agent_id")
    return m.join(r).reset_index()
def training_candidates(t,a,n=10):
    m=agent_metrics(t,a); x=m[(m.tier==1)&(m.csat_responses>=TIER1_MIN_CSAT_RESPONSES)].copy()
    x["csat_team_pct"]=x.groupby("team").csat.rank(pct=True); x["handle_team_pct"]=x.groupby("team").median_handle_min.rank(pct=True)
    x["breach_team_pct"]=x.groupby("team").breach_rate.rank(pct=True)
    x["training_risk"]=(1-x.csat_team_pct)*.60+x.handle_team_pct*.25+x.breach_team_pct*.15
    return x.sort_values("training_risk",ascending=False).head(n)
def kpis(t,a):
    d=t[t.completed]; t1=d.merge(a[["agent_id","tier"]],on="agent_id").query("tier==1"); r=t1[t1.csat_score.notna()]
    br=t1.breach.mean(); target=.06
    return dict(completed=len(d),tier1_completed=len(t1),csat=r.csat_score.mean(),csat_responses=len(r),
      low_csat_rate=(r.csat_score<=2).mean(),tier1_breach_rate=br,
      quarterly_sla_savings_at_6pct=650*13*max(0,br-target)*SLA_BREACH_CREDIT_INR,open_pending=int((~t.completed).sum()))
if __name__=="__main__":
    t,a,*_=load_data(); print(training_candidates(t,a)[["agent_id","name","team","csat","median_handle_min","breach_rate","training_risk"]].to_string(index=False)); print(kpis(t,a))
