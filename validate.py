
import pandas as pd,numpy as np
from analysis import load_data
t,a,*_=load_data(); d=t[t.completed]
s=pd.concat([d[d.source_system=="legacy_fd"].head(250),d[d.source_system=="helpdesk"].head(250)]).drop_duplicates("ticket_id")
r=pd.to_datetime(s.resolved_at)+pd.to_timedelta(np.where(s.source_system.eq("legacy_fd"),330,0),unit="m")
expected=((r-pd.to_datetime(s.first_response_at)).dt.total_seconds()/60).to_numpy()
h=s.handle_mins.to_numpy(); he=np.sum(~np.isclose(expected,h,equal_nan=True))
targets={"chat":15,"voice":120,"social":240,"email":480}
expected_b=((pd.to_datetime(s.first_response_at)-pd.to_datetime(s.created_at)).dt.total_seconds()/60)>s.channel.map(targets)
be=np.sum(expected_b.to_numpy()!=s.breach.to_numpy())
print(f"Sample checked: {len(s)} completed tickets"); print(f"Handle mismatches: {he}"); print(f"SLA mismatches: {be}"); print(f"Observed error rate: {(he+be)/(2*len(s)):.2%}")
assert he==0 and be==0
assert (t.loc[t.resolved_ist.notna(),"resolved_ist"]>=t.loc[t.resolved_ist.notna(),"first_response_at"]).all()
assert set(t.agent_id)==set(a.agent_id); print("Full-data invariants: PASS")
