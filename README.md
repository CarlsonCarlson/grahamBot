# grahamBot
## Current Features
Asks for company name and ticker <br>
Writes report of all annual EPS and dividend payouts since 1989 <br>
Writes report on if EPS increased by 33% in the last 10 years <br>


## For my reference
I will be using macrotrends for historical data since 2005 <br>
ycharts seems to have data from earlier but I need an account. <br/>
guru focus also has 30 year financials but you need an account <br/>
for more in-depth analysis I will try one of these^ <br/>

# TODO: 
## Web scraping and Collection
### make it get all the stats needed to analyze
## Data Analysis
## UI elements
make it so automatically gets the ticker of the company
analyze all the companies

### Make Feeder Class
webscrape page that is a list of fortune 500 companies

## Low priority
create schema_df to explain each criterion

## Stats to analyze in order of utility
diluted EPS increase by 1.33 in the past 10 years using three year averages at the beginning and end

Positive earnings over the past 10 years

Dividend record should be uninterrupted for 20 years
### Strong financial condition check
Long-term debt should be less than net current assets

(for industrial firms) Current ratio should be greater than 2. Current assets should be at least twice current liabilities

(for public utilities) debt should not exceed 2x the equity (what does this mean)
### Price filters
Price should not be more than 15 times the average earnings of the past 3 years 

Price to book ratio should be no more than 1.5

A low PE ratio can justify a high P/B so, PE ratio x PB ratio should be less than or equal to 22.5
