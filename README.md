The USCG (US Coast Guard) publishes on the water incident data, which is accessible for 56 jurisdictions over 13 years across 15 attributes. We would like to use this data in a visualization and need it provided as a CSV/XLSX file with one row per combination of dimension, jurisdiction and year. The web form has three fields and you should iterate through all possible combinations. 

The output data set should have the following header columns: 
State: 2 Character State Abbreviation, no need for ALL 
Year: 4 digit year from picklist, no need for all 
Dimension: value of the first picklist "Select" (e.g., Time of Day) 
Dimension Detail: the values returned by the Dimension (e.g., 12:00am - 02:30am) 
Accidents: INT, number from accidents column, if present, else NULL 
Vessels: INT, number from vessels column, if present, else NULL 
Injuries: INT, number from injuries column, if present, else NULL 
Deaths: INT, number from deaths column, if present, else NULL 

The web form is available here: https://bard.knightpoint.systems/PublicInterface/Report1.aspx 
