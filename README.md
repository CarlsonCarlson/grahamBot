# grahamBot
## Current Features
Asks for company name, autocompletes ticker<br>
Writes report of all annual EPS and dividend payouts since 1989 <br>
Writes report on if EPS increased by 33% in the last 10 years, if dividends have been paid for the last 20 years, and <br>
if the earnings have been positive for the last 10 years<br>
takes 26 minutes to run 3 spiders on all 500<br>

##Required Packages:
os<br>
pandas<br>
scrapy<br>
datetime<br>
importlib<br>
crochet <br>
time<br>

### Big thanks to https://github.com/cmusam/fortune500 for publishing csv's of the fortune500 lists from 1955-2019
### Also thanks to https://github.com/timarbuckle/yahoofinance for the easy ticker/name converter

## For my reference
I will be using macrotrends for historical data since 2005, and marketwatch for ticker lookup <br>
ycharts seems to have data from earlier but I need an account. <br/>
guru focus also has 30 year financials but you need an account <br/>
for more in-depth analysis I will try one of these^ <br/>

## Spiders TODO:
quarterly balance sheet spider<br>
price to book ratio spider<br>

## Finish run through all fortune 500 companies function in central
solve ticker lookup problems<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Looking up Jabil and eBay gives you AAPL as the ticker for some reason, make it confirm that the text found corresponds with the company<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Other known ticker errors are: Calpine, oshkosh, UGI, M&T, Cintas, S&P Global, intuit, zoetis, <br>
find out how many companies could not be found on macrotrends<br>

### Expected behavior: 
get ticker from company name in csv (complete)
run through each f500 company and write ones that happen to pass all criteria (their passed row is 'Yes')<br>
companies that pass all criteria get a folder with a graham report and main report <br>
folder names start with company rank <br>
have a file that stores all the companies that had data that couldnt be found for further inspection (complete)<br>


## Stats to analyze in order of utility
diluted EPS increase by 1.33 in the past 10 years using three year averages at the beginning and end (complete)

Positive earnings over the past 10 years

Dividend record should be uninterrupted for 20 years (possible to except depression periods such as 2008)
### Strong financial condition check
quarterly balance sheet spider is all that is required <br>
Long-term debt should be less than net current assets

(for industrial firms) Current ratio should be greater than 2. Current assets should be at least twice current liabilities

(for public utilities) debt should not exceed 2x the equity (what does this mean) shareholder equity?
## Price filters
price to book ratio spider <br>
###todo: re-evaluate what the actual P/E ratio test should be. (different sources are saying different things)<br>
Price should not be more than 20 times the average earnings of the past 5 years (source: intelligent investor)<br>
graham suggests not more than 25 times the average earnings if those earnings are from a depression/recession period <br>
price should not be more than 15 times the average earnings of the past 3 years (source: intelligent investor summary)<br>

Price to book ratio should be no more than 1.5

A low PE ratio (below 15) can justify a high P/B so, PE ratio x PB ratio should be less than or equal to 22.5

## Low priority
write reports in html or csv to allow for line breaks and overall pretty formatting.<br>
scrape the fortune500 website to get most up to date f500 lists independently, and compile into csv<br>
create schema_df to explain each criterion<br>
make architecture diagram (UML) for README<br>
move everything from grahamBot project dir to top level grahamBot package<br>
(make sure it still writes files to project)