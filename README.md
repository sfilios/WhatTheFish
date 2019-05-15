# WhatTheFish

https://whatthefish.ml 
Project for Insight Data Science Fellowship
A web app written from scratch using Python and Dash (a Flask based framework).
The code to perform exploratory data analysis and train the model also written from scratch using Python and packages including Pandas, Numpy, Sci-kit Learn, and Matplotlib.

**"What the Fish?"** is a web-app that uses data from the National Oceanic and Atmospheric Administration to predict the most likely fish that a recreational fisher will catch. It takes user inputs regarding their proposed fishing trip, and uses previous catch data to make predictions. The currently implemented model was trained on 2017 fishing data from 'catch' and 'trip' level data, which has information about fish caught as well as the people who caught them. It uses a Random Forest model, and predicts with approximately 60% accuracy on an "out-of-bag" sample. This compares to 12-15% accuracy if the most common fish or most common fish by subregion are always predicted. 

This project was the result of my first 4 weeks at Insight Data Science. During the first week, I iterated through a number of ideas of potential projects, ultimately selecting what I present here. The second and third weeks were primarily spent getting data, exploring that data, and iteratively generating and interpreting models. The final week was spent creating a web interface for the model and putting it on an AWS instance for public use.

### A note about Random Forest Size
As far as the size of Random Forests, *hoo boy* do they ever grow fast. Because they get so big so fast with more data, I had to find a number of different ways to deal with this problem. One method is to use less trees. This is obviously not the best option because the whole point of a random forest is to get a lot of different trees that are finding unrelated patterns in the data to generate a prediction. It's an ensembling method, and if you aren't ensembling, then it's just not very good. So that wasn't a great option for me. Another way is to limit the depth of each tree. Instead of trying to separate every single item, you can set a "max depth" for each tree and this will cut it off after a certain number of splits. This too is going to make you lose predictive power. Instead of limiting the depth and number of trees, I decided to scale down the data that I was using. Sure, I had data for 30 years of fishing, but is the fishing data from 30 years ago really the most relevant? Instead, I wound up using 1-3 years of the most recent fishing data. Even then, the model was too large to run on the smallest EC2 instance. Since I was working within significant financial constraints, I had to find another way of making the model smaller instead of making the compute power larger. I figured out that my model was hardly ever guessing certain species, and I was asking it to make a prediction for hundreds of different species. Because many of these species hardly ever were caught, it was very rare that they would be predicted. Instead, I combined species that had less than a fixed number of catches into one "other" species, and was able to therefore predict the 50 most common species. Putting this all together, I was able to get the model down from 3 gigabytes to less than 300 megabytes, while still retaining about 60% accuracy. 

### Other Considerations
It would have been relatively straightforward to also include a feature in the application that takes a fish and then returns the most likely parameters (location, month, etc.) This would be a useful feature for targeting a certain species, but there's a problem with this and it isn't technical. It's important to think about the potential implications for your work, and if there's a certain kind of fish that everyone wants to catch, and I'm able to point them to where to get it, that could potentially have the consequence of overfishing for that species. Now, I'm not suggesting that my app is actually good enough to cause that problem right now, but I think it's important to think about the potential impact of data products before you go ahead and make them.

However, with some more time to work on this project there are some "nice to have" features that I would like to add. One would be to incorporate weather data into the predictions. Right now, all of the data comes from NOAA surveys, but it would be nice to pull in historical weather data and see how that potentially impacts catch. Then, the web interface could take a near-future data and get the weather forecast and tell you the most likely fish for that day instead of basing it solely on the month/season data as it does right now.

