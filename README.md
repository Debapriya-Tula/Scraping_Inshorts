# Scraping_Inshorts
**Django tool to scrape news from inshorts.com for a given date and storing them in json files**

## How to run the program?
```bash
>>> cd Inshorts/
>>> python3 manage.py runserver
```

You will then be prompted to a page with today's news displayed. 
 1. Choose the ones you want to keep (in the write_yes and write_no json files).
 2. Or you could select news from some other date by choosing the required date in the date field.

## Use?
The news selected will be written to write_yes.json and the ones not selected into write_no.json.
This can thus be used to acquire data for use in some classification tasks.
I built this tool primarily to select news suitable for school children(cuss words are taken care of!).




