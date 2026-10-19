// Generated from the trained model's metadata.
export interface Feature {
  name: string;
  label: string;
  kind: 'number' | 'text';
}

export const FEATURES: Feature[] = [
  {
    "name": "Quarter",
    "label": "Quarter",
    "kind": "number"
  },
  {
    "name": "Month",
    "label": "Month",
    "kind": "number"
  },
  {
    "name": "DayofMonth",
    "label": "DayofMonth",
    "kind": "number"
  },
  {
    "name": "DayOfWeek",
    "label": "DayOfWeek",
    "kind": "number"
  },
  {
    "name": "CRSDepTime",
    "label": "CRSDepTime",
    "kind": "number"
  },
  {
    "name": "CRSArrTime",
    "label": "CRSArrTime",
    "kind": "number"
  },
  {
    "name": "CRSElapsedTime",
    "label": "CRSElapsedTime",
    "kind": "number"
  },
  {
    "name": "Distance",
    "label": "Distance",
    "kind": "number"
  },
  {
    "name": "DistanceGroup",
    "label": "DistanceGroup",
    "kind": "number"
  },
  {
    "name": "Flight_Number_Marketing_Airline",
    "label": "Flight Number Marketing Airline",
    "kind": "number"
  },
  {
    "name": "Flight_Number_Operating_Airline",
    "label": "Flight Number Operating Airline",
    "kind": "number"
  },
  {
    "name": "DOT_ID_Marketing_Airline",
    "label": "DOT ID Marketing Airline",
    "kind": "number"
  },
  {
    "name": "DOT_ID_Operating_Airline",
    "label": "DOT ID Operating Airline",
    "kind": "number"
  },
  {
    "name": "OriginAirportID",
    "label": "OriginAirportID",
    "kind": "number"
  },
  {
    "name": "OriginAirportSeqID",
    "label": "OriginAirportSeqID",
    "kind": "number"
  },
  {
    "name": "OriginCityMarketID",
    "label": "OriginCityMarketID",
    "kind": "number"
  },
  {
    "name": "OriginStateFips",
    "label": "OriginStateFips",
    "kind": "number"
  },
  {
    "name": "OriginWac",
    "label": "OriginWac",
    "kind": "number"
  },
  {
    "name": "DestAirportID",
    "label": "DestAirportID",
    "kind": "number"
  },
  {
    "name": "DestAirportSeqID",
    "label": "DestAirportSeqID",
    "kind": "number"
  },
  {
    "name": "DestCityMarketID",
    "label": "DestCityMarketID",
    "kind": "number"
  },
  {
    "name": "DestStateFips",
    "label": "DestStateFips",
    "kind": "number"
  },
  {
    "name": "DestWac",
    "label": "DestWac",
    "kind": "number"
  },
  {
    "name": "Airline",
    "label": "Airline",
    "kind": "text"
  },
  {
    "name": "Origin",
    "label": "Origin",
    "kind": "text"
  },
  {
    "name": "Dest",
    "label": "Dest",
    "kind": "text"
  },
  {
    "name": "OriginState",
    "label": "OriginState",
    "kind": "text"
  },
  {
    "name": "DestState",
    "label": "DestState",
    "kind": "text"
  },
  {
    "name": "Marketing_Airline_Network",
    "label": "Marketing Airline Network",
    "kind": "text"
  },
  {
    "name": "Operated_or_Branded_Code_Share_Partners",
    "label": "Operated or Branded Code Share Partners",
    "kind": "text"
  },
  {
    "name": "DepTimeBlk",
    "label": "DepTimeBlk",
    "kind": "text"
  },
  {
    "name": "ArrTimeBlk",
    "label": "ArrTimeBlk",
    "kind": "text"
  },
  {
    "name": "Operating_Airline",
    "label": "Operating Airline",
    "kind": "text"
  },
  {
    "name": "IATA_Code_Marketing_Airline",
    "label": "IATA Code Marketing Airline",
    "kind": "text"
  },
  {
    "name": "IATA_Code_Operating_Airline",
    "label": "IATA Code Operating Airline",
    "kind": "text"
  },
  {
    "name": "Tail_Number",
    "label": "Tail Number",
    "kind": "text"
  },
  {
    "name": "DepHour",
    "label": "DepHour",
    "kind": "number"
  },
  {
    "name": "ArrHour",
    "label": "ArrHour",
    "kind": "number"
  },
  {
    "name": "DayOfYear",
    "label": "DayOfYear",
    "kind": "number"
  },
  {
    "name": "IsWeekend",
    "label": "IsWeekend",
    "kind": "number"
  },
  {
    "name": "Route",
    "label": "Route",
    "kind": "text"
  }
];

export const SAMPLE: Record<string, string | number> = {
  "Quarter": 2,
  "Month": 4,
  "DayofMonth": 21,
  "DayOfWeek": 4,
  "CRSDepTime": 950,
  "CRSArrTime": 1125,
  "CRSElapsedTime": 155.0,
  "Distance": 725.0,
  "DistanceGroup": 3,
  "Flight_Number_Marketing_Airline": 1672,
  "Flight_Number_Operating_Airline": 1672,
  "DOT_ID_Marketing_Airline": 19393,
  "DOT_ID_Operating_Airline": 19393,
  "OriginAirportID": 12953,
  "OriginAirportSeqID": 1295304,
  "OriginCityMarketID": 31703,
  "OriginStateFips": 36,
  "OriginWac": 22,
  "DestAirportID": 13232,
  "DestAirportSeqID": 1323202,
  "DestCityMarketID": 30977,
  "DestStateFips": 17,
  "DestWac": 41,
  "Airline": "Southwest Airlines Co.",
  "Origin": "LGA",
  "Dest": "MDW",
  "OriginState": "NY",
  "DestState": "IL",
  "Marketing_Airline_Network": "WN",
  "Operated_or_Branded_Code_Share_Partners": "WN",
  "DepTimeBlk": "0900-0959",
  "ArrTimeBlk": "1100-1159",
  "Operating_Airline": "WN",
  "IATA_Code_Marketing_Airline": "WN",
  "IATA_Code_Operating_Airline": "WN",
  "Tail_Number": "N8810L",
  "DepHour": 9,
  "ArrHour": 11,
  "DayOfYear": 111,
  "IsWeekend": 0,
  "Route": "LGA_MDW"
};
