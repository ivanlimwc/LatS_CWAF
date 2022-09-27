import pandas as pd
import preprocessing_computemastery as computemastery


def parse_PSAGF4(df_temp):
    user_ids = df_temp.loc[df_temp.psa_id == "PSAGF4"].user_id.unique()
    for user_id in user_ids:
        control_treatment = df_temp.loc[
            ((df_temp.psa_id == "PSAGF4") & (df_temp.user_id == user_id))].section_names.unique()
        if '{"S1 [treatment1]"}' in control_treatment:
            df_temp.loc[
                ((df_temp.psa_id == "PSAGF4") & (df_temp.user_id == user_id)), "control_treatments"] = "control"
        elif '{"S2 [treatment2]"}' in control_treatment:
            df_temp.loc[
                ((df_temp.psa_id == "PSAGF4") & (df_temp.user_id == user_id)), "control_treatments"] = "treatment"
    computemastery.check_for_mastery_wheel_spinning(df_temp, "PSAGF4")
    return df_temp


def parse_PSAHQV(df_temp):
    user_ids = df_temp.loc[df_temp.psa_id == "PSAHQV"].user_id.unique()
    for user_id in user_ids:
        control_treatment = df_temp.loc[
            ((df_temp.psa_id == "PSAHQV") & (df_temp.user_id == user_id))].section_names.unique()
        if '{"S1 [treatment1]"}' in control_treatment:
            df_temp.loc[
                ((df_temp.psa_id == "PSAHQV") & (df_temp.user_id == user_id)), "control_treatments"] = "control"
        elif '{"S2 [treatment2]"}' in control_treatment:
            df_temp.loc[
                ((df_temp.psa_id == "PSAHQV") & (df_temp.user_id == user_id)), "control_treatments"] = "treatment"
    computemastery.check_for_mastery_wheel_spinning(df_temp, "PSAHQV")
    return df_temp


df_v1 = pd.read_csv("../data/processed0.1/df_v1.csv")
df_v2 = pd.read_csv("../data/processed0.1/df_v2.csv")

df_v1["control_treatments"] = "unassigned"
df_v2["control_treatments"] = "unassigned"

df_v1['mastery'] = False
df_v1['skb_mastery_count'] = 0
df_v1['wheel_spinning'] = False
df_v1['skb_problem_count'] = 0

df_v2['mastery'] = False
df_v2['skb_mastery_count'] = 0
df_v2['wheel_spinning'] = False
df_v2['skb_problem_count'] = 0

df_v1.rename({'correct': 'continuous_score'}, axis=1, inplace=True)

df_v1 = parse_PSAHQV(df_v1)
print("DONE:: -> parse_PSAHQV(df_v1)")
df_v2 = parse_PSAHQV(df_v2)
print("DONE:: -> parse_PSAHQV(df_v2)")

df_v1 = parse_PSAGF4(df_v1)
print("DONE:: -> parse_PSAGF4(df_v1)")
df_v2 = parse_PSAGF4(df_v2)
print("DONE:: -> parse_PSAGF4(df_v2)")


df_v1.rename({
    "start_time": "problem_log_start_time",
    "end_time": "problem_log_end_time"
}, axis=1, inplace=True)
df_v2.rename({
    "owner_xid": "teacher_id",
    "group_context_xid": "student_class_id",
    "first_action_type_id": "first_action"
}, axis=1, inplace=True)

df_v1_ = df_v1[['problem_log_id', 'assignment_id', 'problem_id', 'continuous_score', 'answer_text',
                'first_action', 'hint_count', 'bottom_hint',
                'attempt_count', 'problem_log_start_time', 'problem_log_end_time', 'first_response_time',
                'user_id', 'assistment_id',
                'sequence_id', 'name', 'student_class_id', 'teacher_id',
                'academic_year', 'psa_id', 'pra_id', 'parent_ids', 'section_types',
                'section_names', 'array_agg', 'control_treatments', 'mastery', 'skb_mastery_count',
                'wheel_spinning', 'skb_problem_count']]

df_v2_ = df_v2[['problem_log_id', 'assignment_id', 'problem_id', 'continuous_score', 'answer_text',
                'first_action', 'hint_count', 'bottom_hint',
                'attempt_count', 'problem_log_start_time', 'problem_log_end_time', 'first_response_time',
                'user_id', 'assistment_id',
                'sequence_id', 'name', 'student_class_id', 'teacher_id',
                'academic_year', 'psa_id', 'pra_id', 'parent_ids', 'section_types',
                'section_names', 'array_agg', 'control_treatments', 'mastery', 'skb_mastery_count',
                'wheel_spinning', 'skb_problem_count']]

df_v1_.to_csv("../data/processed0.2/motivational_v1_new.csv", index=False)
df_v2_.to_csv("../data/processed0.2/motivational_v2_new.csv", index=False)

print(df_v1_.groupby(['psa_id', 'control_treatments']).size().reset_index(name='frequency'))
print(df_v2_.groupby(['psa_id', 'control_treatments']).size().reset_index(name='frequency'))
