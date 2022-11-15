#!/usr/bin/env python
# coding: utf-8

# ### Note
# * Instructions have been included for each segment. You do not have to follow them exactly, but they are included to help you think through the steps.

# In[41]:


# Dependencies and Setup
import pandas as pd

# File to Load (Remember to Change These)
school_data_to_load = "Resources/schools_complete.csv"
student_data_to_load = "Resources/students_complete.csv"

# Read School and Student Data File and store into Pandas DataFrames
school_data = pd.read_csv(school_data_to_load)
student_data = pd.read_csv(student_data_to_load)

# Combine the data into a single dataset.  
school_data_complete = pd.merge(student_data, school_data, how="left", on=["school_name", "school_name"])
school_data_complete.head()


# ## District Summary
# 
# * Calculate the total number of schools
# 
# * Calculate the total number of students
# 
# * Calculate the total budget
# 
# * Calculate the average math score 
# 
# * Calculate the average reading score
# 
# * Calculate the percentage of students with a passing math score (70 or greater)
# 
# * Calculate the percentage of students with a passing reading score (70 or greater)
# 
# * Calculate the percentage of students who passed math **and** reading (% Overall Passing)
# 
# * Create a dataframe to hold the above results
# 
# * Optional: give the displayed data cleaner formatting

# In[50]:


total_schools=school_data["school_name"].count()


total_students=student_data["student_name"].count()


total_budget=school_data["budget"].sum()


avg_math=student_data[("math_score")].mean()


avg_reading=student_data[("reading_score")].mean()


overall_avg=((avg_math + avg_reading) /2)


perc_math_pass=(school_data_complete["math_score"]>70).sum() / school_data_complete["math_score"].count()* 100


perc_reading_pass= (school_data_complete["reading_score"]>70).sum() / school_data_complete["reading_score"].count()* 100



District_Summary = pd.DataFrame({"Total Schools":[total_schools], "Total Students":[total_students],"Total Budget":[total_budget],
                                "Average Math Score":[avg_math], "Average Reading Score":[avg_reading], "% Passing Math":[perc_math_pass],
                                "% Passing Reading":[perc_reading_pass],"% Overall Passing Rate":[overall_avg]})
District_Summary


District_Summary_DF=pd.DataFrame(District_Summary, columns=["Total Schools","Total Students","Total Budget",
                                                           "Average Math Score","Average Reading Score","% Passing Math","% Passing Reading",
                                                          "% Overall Passing Rate"])
District_Summary_DF

District_Summary_DF["Total Students"]=District_Summary_DF["Total Students"].map("{:,}".format)
District_Summary_DF["Total Budget"]=District_Summary_DF["Total Budget"].map("{:,}".format)


District_Summary_DF["Average Math Score"]=District_Summary_DF["Average Math Score"].map("{:,.2f}".format)

District_Summary_DF


# ## School Summary

# * Create an overview table that summarizes key metrics about each school, including:
#   * School Name
#   * School Type
#   * Total Students
#   * Total School Budget
#   * Per Student Budget
#   * Average Math Score
#   * Average Reading Score
#   * % Passing Math
#   * % Passing Reading
#   * % Overall Passing (The percentage of students that passed math **and** reading.)
#   
# * Create a dataframe to hold the above results

# In[58]:


sch_count= len(school_data_complete["school_name"].unique())

sch_types=school_data.set_index(["school_name"])["type"]

stu_per_sch=school_data_complete["school_name"].value_counts()

sch_budget=school_data_complete.groupby(["school_name"])["budget"].mean()

per_stu_bud=sch_budget/stu_per_sch

avg_math_perSch=school_data_complete.groupby(["school_name"])["math_score"].mean()

avg_red_perSch= school_data_complete.groupby(["school_name"])["reading_score"].mean()

pas_math_scor=school_data_complete.loc[school_data_complete["math_score"]>=70]


group_math_sch=pas_math_scor["school_name"].value_counts()

percent_math=group_math_sch/stu_per_sch*100

read_scor=school_data_complete.loc[school_data_complete["reading_score"]>=70]

by_read_PerSch= read_scor["school_name"].value_counts()

percent_read=by_read_PerSch/stu_per_sch*100

overall=percent_math + percent_read/stu_per_sch

school_summery_df = pd.DataFrame({"School Type":sch_types, "Total Students":stu_per_sch, "Total School Budget":sch_budget
                                ,"Per Student Budget":per_stu_bud ,"Average Math Score" :avg_math_perSch,
                             "Average Reading Score":avg_red_perSch,
                             "% Passing Math":percent_math, "% Passing Reading":percent_read,
                            "% Overall Passing Rate":overall})
school_summery_df


# ## Top Performing Schools (By % Overall Passing)

# * Sort and display the top five performing schools by % overall passing.

# In[57]:


TopSch_df=school_summery_df.sort_values(["% Passing Math","% Passing Reading","% Overall Passing Rate" ], 
                                        ascending=False)
TopSch_df["Total School Budget"]=TopSch_df["Total School Budget"].map("${:,.2f}".format)
TopSch_df["Per Student Budget"]=TopSch_df["Per Student Budget"].map("${:,.2f}".format)

TopSch_df


# ## Bottom Performing Schools (By % Overall Passing)

# * Sort and display the five worst-performing schools by % overall passing.

# In[60]:


BottomSch_df=school_summery_df.sort_values("% Overall Passing Rate")
BottomSch_df.head()

BottomSch_df.style.format({"Total School Budget":"${:,.2f}","Per Student Budget":"${:,.2f}"})


# ## Math Scores by Grade

# * Create a table that lists the average Reading Score for students of each grade level (9th, 10th, 11th, 12th) at each school.
# 
#   * Create a pandas series for each grade. Hint: use a conditional statement.
#   
#   * Group each series by school
#   
#   * Combine the series into a dataframe
#   
#   * Optional: give the displayed data cleaner formatting

# In[63]:


math_9th=student_data.loc[student_data["grade"] == "9th"].groupby(["school_name"])['math_score'].mean()
math_9th.head()
math_10th=student_data.loc[student_data["grade"] == "10th"].groupby(["school_name"])['math_score'].mean()
math_10th.head()
math_11th=student_data.loc[student_data["grade"] == "11th"].groupby(["school_name"])["math_score"].mean()
math_11th.head()
math_12th=student_data.loc[student_data["grade"] == "12th"].groupby(["school_name"])["math_score"].mean()
math_12th.head()


math_byGrad=pd.DataFrame({"9th":math_9th, "10th": math_10th, "11th":math_11th, "12th":math_12th })
math_byGrad


# ## Reading Score by Grade 

# * Perform the same operations as above for reading scores

# In[64]:


read_9th=student_data.loc[student_data["grade"] == "9th" ].groupby(["school_name"])["reading_score"].mean()
read_10th=student_data.loc[student_data["grade"] == "10th" ].groupby(["school_name"])["reading_score"].mean()
read_11th=student_data.loc[student_data["grade"] == "11th" ].groupby(["school_name"])["reading_score"].mean()
read_12th=student_data.loc[student_data["grade"] == "12th" ].groupby(["school_name"])["reading_score"].mean()
reading_byGrade=pd.DataFrame({"9th":read_9th,"10th":read_10th, "11th":read_11th, "12th":read_12th })
reading_byGrade


# ## Scores by School Spending

# * Create a table that breaks down school performances based on average Spending Ranges (Per Student). Use 4 reasonable bins to group school spending. Include in the table each of the following:
#   * Average Math Score
#   * Average Reading Score
#   * % Passing Math
#   * % Passing Reading
#   * Overall Passing Rate (Average of the above two)

# In[66]:


school_summery_df.head()
bins = [0, 585, 615, 645, 675]
group_names = ["<$585", "$585-615", "$615-645", "$645-675"]
school_summery_df["Spending Ranges (Per Student)"]=pd.cut(school_summery_df["Total School Budget"]/school_summery_df["Total Students"]
                                            ,bins , labels=group_names)
school_summery_df.head()
scores_by_sch=school_summery_df .drop(columns=["Total Students", "Total School Budget","School Type", "Per Student Budget"])
scores_by_sch
by_spending =scores_by_sch.groupby(["Spending Ranges (Per Student)"])
by_spending.mean()


# ## Scores by School Size

# * Perform the same operations as above, based on school size.

# In[67]:


school_summery_df.head()

size_bins = [0, 1000, 2000, 5000]
group_names = ["Small (<1000)", "Medium (1000-2000)", "Large (2000-5000)"]
type("School Size")
str

scores_by_sch["School Size"]=pd.cut(school_summery_df["Total Students"],size_bins , labels=group_names)
scores_by_sch.head()


# ## Scores by School Type

# * Perform the same operations as above, based on school type

# In[69]:



scores_by_type= school_summery_df.drop(columns=["Total Students","Total School Budget", "Per Student Budget"])
scores_by_type.head()


# In[ ]:




