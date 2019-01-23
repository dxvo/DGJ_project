# Houston Housing Index Analysis - Oil Price and Other Key Factors 

## Background
-  Houston is recognized worldwide for its energy industry—particularly for oil and natural gas. Therefore, oil price fluctuation can affect many aspects of Houston in general.
- The basis for our project was the underlying belief that House Price Index (HPI) was driven by oil price since energy sector plays an important role in Houston local economy as mentioned above. 
- Out main project objective is to prove whether the belief above is correct. If not, we want to identify the driving force Housing Price Index. 

## Process
#### Data Souce
- All data are collected from FREd Economics St. Louis by performing API call
- All data is located under data folder.
- Note: most data are anual annual without season corrected. 
- Since these are time series data, for regression analysis, all data are transformed to avoid non-stationary effect by using the log of 1st difference. Please refer to cleaning.ipynb for more details 

#### Analysis
- We first investigated the relationship in oil price and HPI trends.  The Figure below shows 2 charts. The first one compares the HPI with the WTI Oil Price and the 2nd chart illustrates the downturn in the workforce employed in the Oil and Gas Sector. 

![image](https://user-images.githubusercontent.com/42792976/51590019-3ee74f00-1eae-11e9-926a-ea9c29a6a541.png)
- We expected to see a positive relationship between the HPI and Oil Price – especially given the 40,00 reduction in the labour force for this highly paid industry.  On carrying out a regression analysis, it was found that only 3% of the variation in the dependent variable (HPI) can be explained by variations in the independent variable, i.e. the oil price.  See results below:
![image](https://user-images.githubusercontent.com/42792976/51590060-5c1c1d80-1eae-11e9-82ff-5897d066a18a.png)

- On closer inspection of the workforce in Houston, it was found that oil and gas workers make up only 13% of the largest industry in Houston with respect to workforce numbers.
![image](https://user-images.githubusercontent.com/42792976/51590094-6b9b6680-1eae-11e9-8b98-1886815cca5d.png)

- We then consider other factors such as: Population, Mortgage & Interest Rates, Consumer Price Index (CPI), Building Permits, Unemployment, Construction Cost Index for our linear regression model. The result for all these factors is shown below (note that all these variables are log-transformed as mention above)
![image](https://user-images.githubusercontent.com/42792976/51588007-4b68a900-1ea8-11e9-8774-0b7827d4fc07.png)
- According to p-value, several additional linear regressions were performed. The final result is shown below
![image](https://user-images.githubusercontent.com/42792976/51588115-c3cf6a00-1ea8-11e9-91bc-a9a00d3f8b89.png)


#### Conclusion/Discussion
- We dont see much correlation between oil price and Houston House Price Index. 
- The two main factors that drive Housing Index according to our findings are: Population and the rising of construcion cost. The final regression equation is : HPI = -0.06 – (0.40*CMI) + (4.90*H_pop) where HPI = House Price Index, CMI = Construction Material Index, H_pop = Houston Population (thousands). The R-squared value is .501 which means the trend of HPI can be exlpained about 50% by these two factors. 
- The final linear regression line implies that when population raises by 1%, the HPI will go up by 4.9%. 

#### Limitation and future work 
- Our dataset sample size is small dues to the fact that population is can only measure annualy 
- The effect of oil price can be under-estimated. Future works can be done to find correlation between oil price and other independent factors.