# Option pricing with Dash front end

## Introduction
Create web app with [Dash](https://dash.plot.ly/), implementing Black Scholes model, Binomial model, Monte Carlo simulation for option pricing (ignore dividend payment), and deploy this web app to [AWS Elastic Beanstalk](https://aws.amazon.com/tw/elasticbeanstalk/).

## File description
There are four files:
1. **application.py**

   Main application.
2. **dash_reusable_components.py**

   Used in application, using "Card" component from this [repository](https://github.com/plotly/dash-svm/blob/master/utils/dash_reusable_components.py).
3. **formula.py**

   Used in application.py, contains three classes for option pricing:
   * Black_Scholes_model
   * Binomial_model
   * Monte_Carlo_simulation
   
   Each class contains two main functions: "call_price()" & "put_price()", after initiating these classes then calling above functions will return option price. 
4. **requirements.txt**

   Contain name and verison of required packages.
   
## Deployment process
Here will only cover main procedure, detail of command can be found in this [article](https://medium.com/@austinlasseter/plotly-dash-and-the-elastic-beanstalk-command-line-89fb6b67bb79).
### Virtual environment and requirement.txt
First, create a virtual environment then activate it, pip install all the required packages, and try to run the app in virtual environment. If everything goes well, then use below command to create *requirement.txt* (this will be used while deploying to AWS Elastic Beanstalk):
```
pip freeze > requirements.txt
```
There are two main reasons to create virtual environment:
1. Testing whether appliaction can run sucessfully under given packages (and its version).
2. Saving packages information to the *requirement.txt*.

After getting all the things we need, git bash and commit all the things in the given folder. Beware that we don't need to add virtual environment folder, because we had already get all the information from it - *requirements.txt*. If we add virtual environment folder, it will be useless and will slow down the process while deploying (use .gitignore to ignore).

### AWS Elastic Beanstalk
First, install Elastic Beanstalk Command Line Interface:
```
pip install awsebcli
```
Under the given floder initialize elastic beanstalk (choose default setting):
```
eb init
```
After committing all the things with git, deploy project to AWS Elastic Beanstalk:
```
eb deploy
```
If deployment is successfully done, you can access your app from url which could be found from CNAME in the command line. Make sure to git commit everytime after making a change, then *eb deploy* to update the app.

(At first, I thought that I need to push my code to github then Elastic Beanstalk will read my code from the repository. After figuring out how it works, I realize that the usage of git in the process is for version controlling, not like pushing stuff to online repositry.)

## Result
![result_chrome](https://i.imgur.com/6Rkn0zK.png)

Web page is also responsive to screen size:

![result_mobile](https://i.imgur.com/pHaFR9b.jpg)

## Reference
* **Option pricing**
  * Binomial

    https://www.hoadley.net/options/binomialtree.aspx?tree=B
     
    https://www.youtube.com/watch?v=lSnWkQYbWyA
  * Monte Carlo simulation

    http://www.codeandfinance.com/pricing-options-monte-carlo.html
* **Dash**
  * [Trigger an event by changing tab](https://community.plot.ly/t/trigger-an-event-by-changing-tab/5987)
  * Application example
    1. [Support Vector Machine (SVM) Explorer](https://github.com/plotly/dash-svm)

       https://github.com/plotly/dash-svm/blob/master/app.py
    2. [US opioid epidemic dataset and Dash app](https://opioid-epidemic.herokuapp.com/)

       https://github.com/plotly/dash-opioid-epidemic-demo
* **AWS Elastic Beanstalk Deployment**
  * [Plotly Dash and the Elastic Beanstalk Command Line](https://medium.com/@austinlasseter/plotly-dash-and-the-elastic-beanstalk-command-line-89fb6b67bb79)
  * [Deploying a Dash App with Elastic Beanstalk Console (with Docker)](https://medium.com/@austinlasseter/deploying-a-dash-app-with-elastic-beanstalk-console-27a834ebe91d)
* **CSS**
  * [CSS Flexbox](https://www.w3schools.com/css/css3_flexbox.asp)
  * [Flexbox Tutorial (CSS): Real Layout Examples](https://www.youtube.com/watch?v=k32voqQhODc)
  * [Responsive Web Design - The Viewport](https://www.w3schools.com/css/css_rwd_viewport.asp)