import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv(r"medical_examination.csv", sep=',')

# Add 'overweight' column
df['BMI'] = df['weight']/((df['height']/100)**2)

def weight_cat(bmi):
  if bmi > 25:
      return 1
  else:
      return 0

df['overweight'] = df['BMI'].apply(weight_cat)

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
def normalize(data):
  if data > 1:
      return 1
  elif data == 1:
      return 0

df['cholesterol'] = df['cholesterol'].apply(normalize)
df['gluc'] = df['gluc'].apply(normalize)
df.drop(columns=['BMI'],inplace=True)

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = pd.melt(df, id_vars=['cardio'], value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'],
     var_name='variable', value_name='value')
  
    

    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    df_mod = df_cat.groupby(['cardio','variable','value']).size().reset_index(name='total')
    

    # Draw the catplot with 'sns.catplot()'
    graph = sns.catplot(x='variable', y='total',data= df_mod,hue='value', col='cardio',kind='bar')
    

    # Get the figure for the output
    fig = graph.fig


    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_heat = df[(df['ap_lo'] <= df['ap_hi']) &
     (df['height'] >= df['height'].quantile(0.025)) &
     (df['height'] <= df['height'].quantile(0.975)) &
     (df['weight'] >= df['weight'].quantile(0.025)) &
     (df['weight'] <= df['weight'].quantile(0.975))]

    # Calculate the correlation matrix
    corr = df_heat.corr().round(1)

    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))



    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(11, 9))

    # Draw the heatmap with 'sns.heatmap()'
    sns.heatmap(corr, mask=mask, cmap='coolwarm', vmax=0.24, vmin=-0.08, annot=True, fmt=".1f", linewidths=.5, ax=ax)




    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
