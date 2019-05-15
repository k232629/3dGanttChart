import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import style
import matplotlib.ticker as plticker
from random import randint


def get_cmap(n, name='hsv'):
    return plt.cm.get_cmap(name, n)

def project_counts(dataFrame):
	return (dataFrame["Project_id"],len(dataFrame["Project"]), len(set(dataFrame["Project"])))

def project_names(df, projects):
	project_names = list()
	project_names.append('0')
	start_proj_id = df.iloc[0,1]
	project_names.append(df.iloc[0,0])

	for i in range(1,len(projects)):
		project_id = df.iloc[i,1]
		if (project_id!=start_proj_id):
			project_names.append(df.iloc[i,0])
			start_proj_id = start_proj_id + 1
	return project_names



def plot_3d_bar(projects, df, ax1):
	start_proj_id = df.iloc[0,1]
	project_names = list()
	k = 0
	names_count = len(resource_names(dfResources))

	cmap = get_cmap(names_count)
	for i in range(0,len(projects)):
		project_id = df.iloc[i,1]
		
		
		task = df.iloc[i,2]
		task_time = df.iloc[i,3]
		if i == 0:
			x_start_time = 0
			x_next=task_time
			project_names.append('0')
			project_names.append(df.iloc[i,0])

		else:
			if (project_id!=start_proj_id):
				x_start_time = 0
				x_next=task_time
				k = k + division_value
				start_proj_id = start_proj_id + 1
				project_names.append(df.iloc[i,0])
				
			else:
				x_start_time = df.iloc[i-1,4]
				x_next = df.iloc[i,3] 

		resource_num = df.iloc[i,5]
		resources_from = df.iloc[i,6]
		#resources_to = df.iloc[i,7]

		resource_list = str(resources_from).split()
		print(resource_list)
		print(resource_num)
		for n in range(0, resource_num):
			ax1.bar3d(x_start_time, k ,int(resource_list[n])-1, x_next, division_value, 1, cmap(int(resource_list[n])-1))
		#ax1.bar3d(x_start_time, k ,resources_from, x_next, division_value, resource_num, cmap(randint(0,124)))

def resource_names(dfResources):
	resource_names = list()
	resource_names.append('0')

	resources = dfResources["Resource Name"]
	for i in range(0, len(resources)):
		resource_names.append(resources[i])

	return resource_names

def configure_axis(ax1):
	loc = plticker.MultipleLocator(base=division_value)
	loc1 = plticker.MultipleLocator(base=2.0)
	ax1.tick_params(axis='both', which='major', labelsize=10)
	ax1.tick_params(axis='both', which='minor', labelsize=6)
	ax1.yaxis.set_major_locator(loc)
	ax1.xaxis.set_major_locator(loc1)
	ax1.set_yticklabels(project_names(df,projects))
	ax1.set_zticklabels(resource_names(dfResources))
	ax1.set_xlabel('Time')
	ax1.set_ylabel('Projects')
	ax1.set_zlabel('Resources')


df = pd.DataFrame(pd.read_excel('3Ddata.xlsx', sheetname='Schedule'))
dfResources = pd.DataFrame(pd.read_excel('3Ddata.xlsx', sheetname='Resources'))

df["Project"].fillna(method='ffill',inplace = True)
df["Project_id"].fillna(method='ffill',inplace = True)
projects, project_num, project_set = project_counts(df)

resourse_numbers = dfResources["Resource number"]
resourse_name = dfResources["Resource Name"]


division_value = project_num / project_set

fig = plt.figure()
ax1 = fig.add_subplot(111, projection='3d')


plot_3d_bar(projects, df, ax1)
configure_axis(ax1)
plt.show()

    	
