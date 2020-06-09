Acknowledgments\

# StockDSL
##### To run the client: 
- cd client
- npm start

##### To run the server:
- cd server
- bin/www

##### StockDSL Grammar and Documentation:
\*\*\****Language is not case-sensitive******

**PROGRAM** ::= STATEMENT

**STATEMENT** ::= CREATE | DELETE | ADDSTOCK | REMOVESTOCK | COMPUTEINFO | SHOWINFO

**CREATE** ::= "create" ("stock" | "portfolio") ITEM

-   Brings specified stock into existence for current session

-   Name must be one continuous string with no special characters

-   Example: Creating an Apple Inc. stock

    -   "create stock APPL"

-   Example: Creating a portfolio called "myPortfolio"

    -   "create portfolio myPortfolio

**DELETE** ::= "delete" ("stock" | "portfolio") ITEM

-   Deletes an existing stock or portfolio from current session

-   Example: Deleting an Apple Inc. stock

    -   "delete stock APPL"

-   Example: Deleting a portfolio called "myPortfolio"

    -   "delete portfolio myPortfolio"

**ITEM** ::= STOCK |  PORTFOLIO  

**ADDSTOCK** ::= "add" "{ " TICKER ("," TICKER)* " }"  PORTFOLIOTAG

-   Add existing stock(s) into an existing portfolio

-   Must have spaces after open curly brackets and before close curly brackets

-   Example:  Add an Apple Inc. stock to portfolio called "myPortfolio"

    -   "add { APPL } myPortfolio"

-   Example: Add an Apple Inc. and Tesla stock to portfolio called "myPortfolio"

    -   "add { APPL, TSLA } myPortfolio"

**REMOVESTOCK** ::= "remove" " {"  TICKER ("," TICKER)* "}"  PORTFOLIOTAG

-   Remove existing stock(s) from an existing portfolio

-   Must have spaces after open curly brackets and before close curly brackets

-   Example:  Remove an Apple Inc. stock to portfolio called "myPortfolio"

    -   "remove { APPL } myPortfolio"

-   Example: Remove an Apple Inc. and Tesla stock to portfolio called "myPortfolio"

    -   "remove { APPL, TSLA } myPortfolio"

**COMPUTEINFO** ::= "compute" COMMAND

-   Execute available commands

-   Convert currency type

-   Compute future value of a stock(s) over a given time period and interest rate

-   Example: Converting currency type to Canadian

    -   "compute CAD"

-   Example: Compute future value of 5 Apple Inc. stocks over 12 months at an interest rate of 15%

    -   "compute stock APPL quantity 5 months 12 interest 0.15"

**SHOWINFO** := "show" ("stock" | "portfolio") ITEM "as" VISUALIZATION

-   Displays stock or portfolio in specified visualization type

-   Example: Show Apple Inc. data in a time-series graph

    -   "show stock APPL as time"

-   Example: Show portfolio called "myPortfolio" in a bar graph

    -   "show myPortfolio as bar"

**VISUALIZATION** := "bar" | "line" | "text"

**STOCK** := TICKER

**TICKER** ::= STRING

-   Only valid stock ticker names

-   Example: "APPL", "TSLA", etc.

**PORTFOLIO** ::= PORTFOLIOTAG 

**PORTFOLIOTAG** ::= STRING

**COMMAND** ::= CURRENCYCONVERSION |  FUTUREVAL

**CURRENCYCONVERSION** ::= "currency" CURRENCY

**CURRENCY** ::= STRING

-   Only valid currency symbols

-   Example: "CAD", "USD", etc.

**FUTUREVAL** ::= ("stock" | "portfolio") (TICKER | PORTFOLIOTAG)  "quantity" QUANTITY "months" MONTHS "interest" INTERESTRATE

**QUANTITY** ::= INT

**MONTHS** ::= INT

**INTERESTRATE** ::= FLOAT

-   Takes both decimal or whole value

-   Example: "0.15" or "15"
