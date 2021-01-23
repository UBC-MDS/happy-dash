# HappyDash

## Motivation and Purpose

Role: Data science team at an intergovernmental agency <br>
Target audience: Politicians/Decision makers in government

As the world has experienced a very difficult 2020, it becomes ever more important that governments look after the mental well being of their citizens. Looking at annual reports gives a snapshot of the current state of each country - but seeing trends over time and between countries is a valuable addition. With our app, we hope to allow for exploration of the trends in happiness reports by country/region/continent over time to evaluate changes needed in public policy.

## Dataset Description

The description we will be working with is an aggregate of five years worth of data from the [World Happiness Report](https://worldhappiness.report/) (WHR). The data spans from 2015 - 2019 inclusive. As part of the annual surveys - the WHR has modelled the average happiness score (from 1-10) as a sum of 6 key variables.

These 6 factors, with our naming convention are:
- Gross Domestic Product (GDP) = 'gdp_per_capita'
- Life Expectancy = 'health_life_expectancy'
- Generosity = 'generosity'
- Social Support = 'family'
- Freedom = 'freedom'
- Corruption Levels = 'perceptions_of_corruption'

The modelling methodology for arriving at this contributions can be found in the statistical appendix [here](https://s3.amazonaws.com/happiness-report/2019/WHR19_Ch2A_Appendix1.pdf).

We will be accessing a collection of the reports from Kaggle to show trends over time. The raw data can be found [here](https://www.kaggle.com/unsdsn/world-happiness).

## Concepts being investigated
John is a psychologist in a country with an increasing rate of mental issues. He is getting more patients and believes that his patients' mental problems have a source in their country's recent changes. There are changes in economics, federal policies regarding social supports and many other changes. He thinks that by knowing the factors most affecting his patients, he would be able to give them better advice and to be able to be of more help to them. 
He wants to explore the happiness dataset, which has the average happiness of a country's people and other important factors of the countries such as GDP, Health Life expectancy, perception of corruption, etc. 
By opening the happiness data dashboard, he could see how those factors have been changed in his country and see the trend of change in happiness in his country by specifying the range of years he wants to study. He can select his own country and countries which he thinks are similar to his own country in terms of culture, geographics, etc. and see them in one plot to compare how well they have been doing in terms of happiness index. Other than the happiness index, other charts show the different parameters, and by reviewing those, he could find out which parameter has the most effect on a countries happiness.
By looking at the plots, he finds out that some factors, such as the perception of corruption, are not correlated to the happiness index. Still, some are positively correlated, such as GDP and social support, with social support being the most correlated factor of all. 
He concludes which factors are the most effective, and based on the results; he decides that when he meets a new patient, he would first check if the root of the problems are in the factors that he is concluded that are more critical and if not slowly work his way down to the less essential elements. He is also prepared about the things and manner he will talk to his patients by knowing what is probably going on in their lives and would have more success helping out his patients.
