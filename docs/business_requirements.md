Here are 4 key business and analytical questions the final dataset (dbt Marts) is designed to answer:

1. **How do weather patterns vary seasonally across different geographic regions?**

- _Purpose:_ Identifies historical trends and temperature/precipitation anomalies by comparing monthly and quarterly aggregates across various locations.

2. **What are the peak extreme weather events recorded in each region?**

- _Purpose:_ Flags critical thresholds (e.g., maximum daily rainfall, heatwaves, or freezing temperatures) to support risk assessment and alert modeling.

3. **How accurately do short-term forecasts predict actual observed weather conditions?**

- _Purpose:_ Compares historic forecast data against actual daily readings to calculate variance metrics and measure forecast reliability over time.

4. **What is the correlation between temperature, humidity, and atmospheric pressure?**

- _Purpose:_ Provides cleansed, normalized multi-variable metrics in dimensional tables for downstream machine learning and predictive data science models.
