import pandas as pd

df_v1 = pd.read_csv("../data/processed0.2/motivational_v1_new.csv")
df_v2 = pd.read_csv("../data/processed0.2/motivational_v2_new.csv")
df_v1_v2 = pd.concat([df_v1, df_v2], ignore_index=True)
df_v1_v2['academic_year_merged'] = df_v1_v2['academic_year'].str[3:]

a = df_v1.groupby(['psa_id', 'academic_year', 'control_treatments', 'user_id']).size().reset_index(name='frequency')
b = df_v2.groupby(['psa_id', 'academic_year', 'control_treatments', 'user_id']).size().reset_index(name='frequency')
c = df_v1_v2.groupby(['psa_id', 'academic_year', 'control_treatments', 'user_id']).size().reset_index(name='frequency')
c_ = df_v1_v2.groupby(['psa_id', 'academic_year_merged', 'control_treatments', 'user_id']).size().reset_index(name='frequency')

a_count_frequency = a.groupby(['psa_id', 'academic_year', 'control_treatments']).size().reset_index(name='frequency')
b_count_frequency = b.groupby(['psa_id', 'academic_year', 'control_treatments']).size().reset_index(name='frequency')
c_count_frequency = c.groupby(['psa_id', 'academic_year', 'control_treatments']).size().reset_index(name='frequency')
c_count_frequency_ = c_.groupby(['psa_id', 'academic_year_merged', 'control_treatments']).size().reset_index(name='frequency')

a_count_frequency.sort_values(by=['psa_id', 'academic_year', 'control_treatments'], inplace=True)
b_count_frequency.sort_values(by=['psa_id', 'academic_year', 'control_treatments'], inplace=True)
c_count_frequency.sort_values(by=['psa_id', 'academic_year', 'control_treatments'], inplace=True)
c_count_frequency_.sort_values(by=['psa_id', 'academic_year_merged', 'control_treatments'], inplace=True)

