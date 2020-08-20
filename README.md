# grahamBot
## Current Features
Asks for company name, autocompletes ticker<br>
Writes report of all annual EPS and dividend payouts since 1989 <br>
Takes 36 minutes to run on all 2019 Fortune 500 companies<br>
Can run 12 tests total<br>

## Terms as defined by me
I. I. = An abbreviation for the Intelligent Investor<br>
Net Working Capital = Current Assets - Current Liabilities<br>
Current Ratio = Current Assets / Current Liabilities<br>
Shareholder Equity = Total assets - Total Liabilities<br>
EPS = Earnings per Share (Graham always refers to diluted EPS rather than basic EPS)<br>
P/E (Ratio) = Current Price / EPS of a certain number of years<br>
P/B (Ratio) = Current Price / Most recently reported book value per share<br>
TTM = Trailing Twelve Month (Average)<br>

## The Tests:
All of these tests come from either the original 1949 version or the revised 1972 version of the Intelligent Investor.
### Strong Earnings and dividends
1. Diluted EPS increase by 1.33 in the past 10 years using three year averages at the beginning and end
2. Positive earnings over the past 10 years
3. Dividend record should be uninterrupted for 20 years 
### Strong financial condition
4. Shareholder Equity / Total Assets > 0.5 (I. I. 1949)
5. Long-term debt should be less than Net Working Capital (I. I. 1972)
6. (For industrial firms) Current ratio should be greater than 2.
7. (For public utilities) Long term debt should not exceed 2x the Shareholder Equity (I. I. 1972)
## Price filters
8. Trailing Twelve Month Average P/E < 20 (I. I. 1972 Chapter 5)
9. 7 year P/E < 25 (I. I. 1972 Chapter 5)<br>
10. Price should not be more than 15 times the average earnings of the past 3 years (I. I. 1972 Chapter 14)
11. Price to book ratio should be no more than 1.5 (Intelligent Investor 1972 Chapter 14)
12. A low PE ratio (below 15) can justify a high P/B so, PE ratio x PB ratio should be less than or equal to 22.5 (The text from which the Graham Number was deduced) (I. I. 1972 Chapter 14)

#Required Packages:
os<br>
pandas<br>
scrapy<br>
datetime<br>
importlib<br>
crochet <br>
time<br>

### Big thanks to https://github.com/cmusam/fortune500 for publishing csv's of the fortune500 lists from 1955-2019

### Expected behavior TODOs: 
run through each f500 company and write ones that happen to pass all criteria (their passed row is 'Yes')<br>
companies that pass all criteria get a folder with a graham report and main report <br>
folder names start with company rank <br>
have a file that stores all the companies that had data that couldnt be found for further inspection (complete)<br>

## Major TODOs: 
solve ticker lookup problems<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Looking up Jabil and eBay gives you AAPL as the ticker for some reason, make it confirm that the text found corresponds with the company<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Other known ticker errors are: Calpine, oshkosh, UGI, M&T, Cintas, S&P Global, intuit, zoetis, AT&T, NCR <br>
find out how many companies could not be found on macrotrends<br>
Make GUI <br>
only run price tests on certain list<br>
allow selection of fortune 500 list<br>
allow importing of lists to run on<br>

## TODOs
make architecture diagram (UML) for README<br>
write reports in html or csv to allow for line breaks and overall pretty formatting.<br>
scrape the fortune500 website to get most up to date f500 lists independently, and compile into csv<br>
create schema_df to explain each criterion<br>
move everything from grahamBot project dir to top level grahamBot package<br>

## For my reference
I will be using macrotrends for historical data since 2005, and marketwatch for ticker lookup <br>
ycharts seems to have data from earlier but I need an account. <br/>
guru focus also has 30 year financials but you need an account <br/>

