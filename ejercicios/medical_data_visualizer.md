# Medical Data Visualizer

Este ejercicio forma parte del curso *Data Analysis with Python* de [freeCodeCamp](https://www.freecodecamp.org/learn/data-analysis-with-python/).

**Consigna.** En este proyecto deberá limpiar, filtrar, transformar y visualizar datos de exámenes médicos utilizando Pandas, Matplotlib y Seaborn.


```python
# import libraries
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
```


```python
# Read data
df = pd.read_csv("medical_examination.csv", index_col = "id")
df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>age</th>
      <th>gender</th>
      <th>height</th>
      <th>weight</th>
      <th>ap_hi</th>
      <th>ap_lo</th>
      <th>cholesterol</th>
      <th>gluc</th>
      <th>smoke</th>
      <th>alco</th>
      <th>active</th>
      <th>cardio</th>
    </tr>
    <tr>
      <th>id</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>18393</td>
      <td>2</td>
      <td>168</td>
      <td>62.0</td>
      <td>110</td>
      <td>80</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>20228</td>
      <td>1</td>
      <td>156</td>
      <td>85.0</td>
      <td>140</td>
      <td>90</td>
      <td>3</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>18857</td>
      <td>1</td>
      <td>165</td>
      <td>64.0</td>
      <td>130</td>
      <td>70</td>
      <td>3</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>17623</td>
      <td>2</td>
      <td>169</td>
      <td>82.0</td>
      <td>150</td>
      <td>100</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>17474</td>
      <td>1</td>
      <td>156</td>
      <td>56.0</td>
      <td>100</td>
      <td>60</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>




```python
df.shape
```




    (70000, 12)



Observamos que el conjunto de datos tiene 70000 filas y 12 columnas. Las variables son edad (días), género, peso (cm),  altura (kg), resultados de análisis clínicos (presión arterial sistólica y diastólica, colesterol, glucosa), estilos de vida (consumo de alcohol y tabaco, actividad física) y presencia/ausencia de enfermedad cardiovascular.

**1. Add an overweight column to the data. To determine if a person is overweight, first calculate their BMI. If that value is > 25 then the person is overweight. Use the value 0 for NOT overweight and the value 1 for overweight.**


```python
df["overweight"] = df["overweight"] = np.where(df["weight"] / (df["height"] / 100 ) ** 2 > 25, 1, 0)
df.head(3)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>age</th>
      <th>gender</th>
      <th>height</th>
      <th>weight</th>
      <th>ap_hi</th>
      <th>ap_lo</th>
      <th>cholesterol</th>
      <th>gluc</th>
      <th>smoke</th>
      <th>alco</th>
      <th>active</th>
      <th>cardio</th>
      <th>overweight</th>
    </tr>
    <tr>
      <th>id</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>18393</td>
      <td>2</td>
      <td>168</td>
      <td>62.0</td>
      <td>110</td>
      <td>80</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>20228</td>
      <td>1</td>
      <td>156</td>
      <td>85.0</td>
      <td>140</td>
      <td>90</td>
      <td>3</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>18857</td>
      <td>1</td>
      <td>165</td>
      <td>64.0</td>
      <td>130</td>
      <td>70</td>
      <td>3</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>



**2. Normalize the data by making *0 always good* and *1 always bad*. If the value of cholesterol or gluc is 1, make the value 0. If the value is more than 1, make the value 1.**


```python
df["cholesterol"] = np.where(df["cholesterol"] == 1, 0, 1)
df["gluc"] = np.where(df["gluc"] == 1, 0, 1)
df.head(3)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>age</th>
      <th>gender</th>
      <th>height</th>
      <th>weight</th>
      <th>ap_hi</th>
      <th>ap_lo</th>
      <th>cholesterol</th>
      <th>gluc</th>
      <th>smoke</th>
      <th>alco</th>
      <th>active</th>
      <th>cardio</th>
      <th>overweight</th>
    </tr>
    <tr>
      <th>id</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>18393</td>
      <td>2</td>
      <td>168</td>
      <td>62.0</td>
      <td>110</td>
      <td>80</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>20228</td>
      <td>1</td>
      <td>156</td>
      <td>85.0</td>
      <td>140</td>
      <td>90</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>18857</td>
      <td>1</td>
      <td>165</td>
      <td>64.0</td>
      <td>130</td>
      <td>70</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>



**3. Draw Categorical Plot**

##### 3.1. Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.


```python
df_cat = pd.melt(df, id_vars = "cardio", value_vars = ("cholesterol", "gluc", "smoke", "alco", "active", "overweight"))
df_cat.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>cardio</th>
      <th>variable</th>
      <th>value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>cholesterol</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>cholesterol</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1</td>
      <td>cholesterol</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1</td>
      <td>cholesterol</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0</td>
      <td>cholesterol</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>



##### 3.2 Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.


```python
df_cat = df_cat.value_counts().reset_index(name = "total")
df_cat.head(10)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>cardio</th>
      <th>variable</th>
      <th>value</th>
      <th>total</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>alco</td>
      <td>0</td>
      <td>33156</td>
    </tr>
    <tr>
      <th>1</th>
      <td>0</td>
      <td>alco</td>
      <td>0</td>
      <td>33080</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1</td>
      <td>smoke</td>
      <td>0</td>
      <td>32050</td>
    </tr>
    <tr>
      <th>3</th>
      <td>0</td>
      <td>smoke</td>
      <td>0</td>
      <td>31781</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0</td>
      <td>gluc</td>
      <td>0</td>
      <td>30894</td>
    </tr>
    <tr>
      <th>5</th>
      <td>0</td>
      <td>cholesterol</td>
      <td>0</td>
      <td>29330</td>
    </tr>
    <tr>
      <th>6</th>
      <td>0</td>
      <td>active</td>
      <td>1</td>
      <td>28643</td>
    </tr>
    <tr>
      <th>7</th>
      <td>1</td>
      <td>gluc</td>
      <td>0</td>
      <td>28585</td>
    </tr>
    <tr>
      <th>8</th>
      <td>1</td>
      <td>active</td>
      <td>1</td>
      <td>27618</td>
    </tr>
    <tr>
      <th>9</th>
      <td>1</td>
      <td>overweight</td>
      <td>1</td>
      <td>24440</td>
    </tr>
  </tbody>
</table>
</div>



##### 3.3. Draw the catplot with 'sns.catplot()'


```python
sns.catplot(data = df_cat, x = "variable", y = "total", hue = "value", col = "cardio", kind = "bar")
```




    <seaborn.axisgrid.FacetGrid at 0x50461d8>




    
![png](output_15_1.png)
    


**4. Draw Heat Map**

##### 4.1. Clean the data. Filter out the following patient segments that represent incorrect data: (a) diastolic pressure is higher than systolic; (b) height is less than the 2.5th percentile; (c) height is more than the 97.5th percentile; (d) weight is less than the 2.5th percentile; (e) weight is more than the 97.5th percentile.


```python
df_heat = df.loc[
        (df["ap_lo"] <= df["ap_hi"]) &
        (df["height"] >= df["height"].quantile(0.025)) &
        (df["height"] <= df["height"].quantile(0.975)) &
        (df["weight"] >= df["weight"].quantile(0.025)) &
        (df["weight"] <= df["weight"].quantile(0.975))]
```

##### 4.2. Calculate the correlation matrix


```python
corr = df_heat.corr()
```

##### 4.3. Generate a mask for the upper triangle 


```python
mask = np.triu(np.ones_like(corr, dtype = bool))
```

##### 4.4. Draw the heatmap with 'sns.heatmap()'


```python
plt.figure(figsize = (12, 8))
sns.heatmap(corr, mask = mask, fmt = ".1f", square = True, annot = True)
```




    <AxesSubplot:>




    
![png](output_24_1.png)
    

