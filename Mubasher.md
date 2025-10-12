/update Scraping to use the `mubasher.info` site and open APIs to get this data
 
`https://english.mubasher.info/api/1/listed-companies?country=eg&size={}` for English data
`https://www.mubasher.info/api/1/listed-companies?country=eg&size={}` for Arabic data
 
and JSON example en

```
{
    "rows": [
        {
            "name": "CIB",
            "url": "/markets/EGX/stocks/COMI",
            "market": "Egyptian Stock Exchange",
            "sector": "Banks",
            "marketUrl": null,
            "currency": null,
            "profileUrl": "/markets/EGX/stocks/COMI/profile",
            "symbol": "COMI",
            "price": 95.71,
            "changePercentage": -0.3,
            "lastUpdate": "23 September 2025"
        },
        {
            "name": "ALICO",
            "url": "/markets/EGX/stocks/RREI",
            "market": "Egyptian Stock Exchange",
            "sector": "Real Estate",
            "marketUrl": null,
            "currency": null,
            "profileUrl": "/markets/EGX/stocks/RREI/profile",
            "symbol": "RREI",
            "price": 2.1,
            "changePercentage": -2.33,
            "lastUpdate": "23 September 2025"
        }
    ],
    "numberOfPages": 1,
    "validCriteria": true
}
```

ar

```
{
    "rows": [
        {
            "name": "سي أي بي",
            "url": "/markets/EGX/stocks/COMI",
            "market": "البورصة المصرية",
            "sector": "بنوك",
            "marketUrl": null,
            "currency": null,
            "profileUrl": "/markets/EGX/stocks/COMI/profile",
            "symbol": "COMI",
            "price": 95.71,
            "changePercentage": -0.3,
            "lastUpdate": "23 سبتمبر 2025"
        },
        {
            "name": "اليكو",
            "url": "/markets/EGX/stocks/RREI",
            "market": "البورصة المصرية",
            "sector": "عقارات",
            "marketUrl": null,
            "currency": null,
            "profileUrl": "/markets/EGX/stocks/RREI/profile",
            "symbol": "RREI",
            "price": 2.1,
            "changePercentage": -2.33,
            "lastUpdate": "23 سبتمبر 2025"
        }
    ],
    "numberOfPages": 1,
    "validCriteria": true
}
```

Get fair values recommendations by looping through the API
 
`https://www.mubasher.info/api/1/fairValues?country=eg&size={n=> max 30}&start={size*page number}`
 
`https://english.mubasher.info/api/1/fairValues?country=eg&size={n=> max 30}&start={size*page number}`
 

```
{
    "rows": [
        {
            "releasedAt": "14 February 2019",
            "name": "CIB",
            "url": "/markets/EGX/stocks/COMI",
            "source": "Beltone Holding",
            "recommendation": "Buy",
            "market": "Egyptian Stock Exchange",
            "sector": "Banks",
            "marketUrl": "/markets/EGX",
            "value": 82.4,
            "price": 73.89,
            "lastPrice": 95.71,
            "change": 8.510000000000005,
            "changePercentage": 11.517120043307626
        }
    ],
    "numberOfPages": 152,
    "validCriteria": true
}
```

 

```
{
    "rows": [
        {
            "releasedAt": "01 سبتمبر 2025",
            "name": "مستشفى كليوباترا",
            "url": "/markets/EGX/stocks/CLHO_r1",
            "source": "مباشر تداول",
            "recommendation": "شراء",
            "market": "البورصة المصرية",
            "sector": "مؤشر قطاع رعاية صحية و ادوية",
            "marketUrl": "/markets/EGX",
            "value": 11.6,
            "price": 8.71,
            "lastPrice": 10.22,
            "change": 2.889999999999999,
            "changePercentage": 33.18025258323764
        }
    ],
    "numberOfPages": 152,
    "validCriteria": true
}
```

Get IPOs by looping through the API
 
`https://www.mubasher.info/api/1/ipos?country=eg&size={n=> max 30}&start={size*page number}`
 
`https://english.mubasher.info/api/1/ipos?country=eg&size={n=> max 30}&start={size*page number}`
 

```
{
    "rows": [
        {
            "name": "ايفاكو",
            "url": null,
            "status": "التفاصيل التي تم الافصاح عنها",
            "attachment": "",
            "type": "اولى",
            "market": "البورصة المصرية",
            "sector": "مؤشر قطاع موارد أساسية",
            "marketUrl": "/markets/EGX",
            "volume": 0,
            "announcedAt": "09 فبراير 2023"
        }
    ],
    "numberOfPages": 152,
    "validCriteria": true
}
```

 

```
{
    "rows": [
        {
            "name": "Efaco",
            "url": null,
            "status": "Up comming",
            "attachment": "",
            "type": "IPO",
            "market": "Egyptian Stock Exchange",
            "sector": "Basic Resources Index",
            "marketUrl": "/markets/EGX",
            "volume": 0,
            "announcedAt": "09 February 2023"
        }
    ],
    "numberOfPages": 152,
    "validCriteria": true
}
```

capital increase
`https://www.mubasher.info/api/1/capital-increase?country=eg&size={n=> max 30}&start={size*page number}`
 
`https://english.mubasher.info/api/1/capital-increase?country=eg&size={n=> max 30}&start={size*page number}`
 

```
{
    "rows": [
        {
            "name": "ايبيكو",
            "url": "/markets/EGX/stocks/PHAR",
            "status": "يتم تداولها",
            "attachment": "",
            "market": "البورصة المصرية",
            "sector": "رعاية صحية و ادوية",
            "marketUrl": "/markets/EGX",
            "volume": 20000000,
            "price": 50.0,
            "start": "26 يناير 2025",
            "end": "24 فبراير 2025"
        }
    ],
    "numberOfPages": 152,
    "validCriteria": true
}
```

 

```
{
    "rows": [
        {
            "name": "Qalaa Holding",
            "url": "/markets/EGX/stocks/CCAP",
            "status": "To be traded",
            "attachment": "",
            "market": "Egyptian Stock Exchange",
            "sector": "Non-bank financial services",
            "marketUrl": "/markets/EGX",
            "volume": 2181939002,
            "price": 5.0,
            "start": "21 September 2025",
            "end": "23 September 2025"
        }
    ],
    "numberOfPages": 152,
    "validCriteria": true
}
```

 
earnings
 
 
`https://www.mubasher.info/api/1/earnings?country=eg&size={n=> max 30}&start={size*page number}`
 
`https://english.mubasher.info/api/1/earnings?country=eg&size={n=> max 30}&start={size*page number}`
 

```
{
    "rows": [
        {
            "name": "القاهرة الوطنية للاستثمار والاوراق المالية",
            "url": "/markets/EGX/stocks/KWIN",
            "sector": "خدمات مالية غير مصرفية",
            "market": "البورصة المصرية",
            "quarter": "الربع الثانى - تراكمي",
            "year": "2010",
            "currency": "جنيه مصري",
            "marketUrl": "/markets/EGX",
            "announced": -3297000.0,
            "changePercentage": -122.46963562753037,
            "compared": -1482000.0
        }
    ],
    "numberOfPages": 152,
    "validCriteria": true
}
```

 

```
{
    "rows": [
        {
            "name": "Alex Cont",
            "url": "/markets/EGX/stocks/ALCN",
            "sector": "Shipping & Transportation Services",
            "market": "Egyptian Stock Exchange",
            "quarter": "Annual",
            "year": "2025",
            "currency": "Egyptian Pound",
            "marketUrl": "/markets/EGX",
            "announced": 6.627568E9,
            "changePercentage": 5.480018684612808,
            "compared": 6.283245E9
        }
    ],
    "numberOfPages": 152,
    "validCriteria": true
}
```

 
insider trades
 
`https://www.mubasher.info/api/1/insider-trades?country=eg&size={n=> max 30}&start={size*page number}`
 
`https://english.mubasher.info/api/1/insider-trades?country=eg&size={n=> max 30}&start={size*page number}`
 

```
{
    "rows": [
        {
            "name": "بالم هيلز",
            "url": "/markets/EGX/stocks/PHDC",
            "trader": "غير معلن",
            "type": "شراء",
            "market": "البورصة المصرية",
            "sector": "عقارات",
            "marketUrl": "/markets/EGX",
            "volume": 75500,
            "price": 7.52,
            "updatedAt": "07 سبتمبر 2025"
        }
    ],
    "numberOfPages": 152,
    "validCriteria": true
}
```

 

```
{
    "rows": [
        {
            "name": "Atlas",
            "url": "/markets/EGX/stocks/AIFI",
            "trader": "Undisclosed",
            "type": "Sell",
            "market": "Egyptian Stock Exchange",
            "sector": "Real Estate",
            "marketUrl": "/markets/EGX",
            "volume": 740,
            "price": 1.93,
            "updatedAt": "07 September 2025"
        }
    ],
    "numberOfPages": 152,
    "validCriteria": true
}
```

 
Scrape the site for the news
 
`https://www.mubasher.info/markets/EGX/stocks/{symbol}/news`
 
`https://english.mubasher.info/markets/EGX/stocks/{symbol}/news`
 
-----------------------------------------------------------------
 
Scrape the site for the news
 
`https://www.mubasher.info/markets/EGX/stocks/{symbol}/announcements`
 
`https://english.mubasher.info/markets/EGX/stocks/{symbol}/announcements`
 
Scrape the site for the profile
 
`https://www.mubasher.info/markets/EGX/stocks/{symbol}/profile`
 
`https://english.mubasher.info/markets/EGX/stocks/{symbol}/profile`
 
And there will be more data to be collected