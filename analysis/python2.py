import pandas as pd
import statsmodels.formula.api as smf

df_v2_new = pd.read_csv("../data/processed0.2/motivational_v2_new.csv")
df_v2_randomization_balance = df_v2_new.loc[((df_v2_new.psa_id == "PSABTZFT") &
                                             (df_v2_new.control_treatments.isin([
                                                 'treatment2_initial', 'control_initial', 'treatment1_initial'])))]
df_v2_new = df_v2_new.loc[((df_v2_new.psa_id == "PSABTZFT") &
                           (df_v2_new.control_treatments == "posttest"))]
df_v2_new = df_v2_new[['continuous_score', 'user_id', 'assignment_id']]
df_v2_new.rename({"continuous_score": "posttest_score"}, axis=1, inplace=True)
df_v2_randomization_balance = df_v2_randomization_balance.merge(
    df_v2_new, how='left', on=['user_id', 'assignment_id'])

c_ = df_v2_randomization_balance.groupby([
    'psa_id', 'control_treatments', 'user_id', 'mastery', 'wheel_spinning', 'skb_problem_count',
    'posttest_score']).size().reset_index(name='frequency')
c_['mastery'] = c_['mastery'].astype(int)
c_['wheel_spinning'] = c_['wheel_spinning'].astype(int)

print("===================================================")

log_regression = smf.logit('posttest_score ~ control_treatments',
                           data=c_).fit()
print(log_regression.summary())
print("===================================================")
