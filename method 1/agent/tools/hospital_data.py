"""Simplified Hospital data query tool for CSV analysis."""
import pandas as pd
import os
from typing import Optional
from math import radians, sin, cos, sqrt, atan2


class HospitalDataTool:
    """Tool for querying hospital data from CSV."""
    
    def __init__(self, csv_path="agent/data/hospital_trends.csv"):
        """Initialize with CSV file path."""
        self.csv_path = csv_path
        self.df = None
        self._load_data()
        self._add_location_column()
    
    def _load_data(self):
        """Load CSV data into pandas DataFrame."""
        if os.path.exists(self.csv_path):
            self.df = pd.read_csv(self.csv_path)
        else:
            raise FileNotFoundError(f"CSV file not found: {self.csv_path}")
    
    def _add_location_column(self):
        """Add location column to CSV if it doesn't exist."""
        if 'location' not in self.df.columns:
            # Define locations for each hospital
            location_mapping = {
                'H001': 'New York, NY',
                'H002': 'Los Angeles, CA',
                'H003': 'Chicago, IL',
                'H004': 'Houston, TX',
                'H005': 'Phoenix, AZ'
            }
            
            # Add location column
            self.df['location'] = self.df['hospital_id'].map(location_mapping)
            
            # Save updated CSV
            self.df.to_csv(self.csv_path, index=False)
            print(f"✓ Added location column to {self.csv_path}")
    
    def get_hospital_count(self) -> int:
        """Get total number of unique hospitals."""
        return self.df['hospital_id'].nunique()
    
    def get_hospital_names(self) -> list:
        """Get list of all hospital names with IDs and locations."""
        hospitals = self.df[['hospital_id', 'hospital_name', 'location']].drop_duplicates()
        return hospitals.to_dict('records')
    
    def get_hospital_details_by_date(self, hospital_name: str, date: str) -> dict:
        """
        Get details of a specific hospital for a specific date.
        
        Args:
            hospital_name: Name of the hospital
            date: Date in format 'YYYY-MM-DD'
            
        Returns:
            dict: Hospital details for that date
        """
        # Filter by hospital name and date
        hospital_data = self.df[
            (self.df['hospital_name'] == hospital_name) & 
            (self.df['date'] == date)
        ]
        
        if hospital_data.empty:
            return {"error": f"No data found for hospital '{hospital_name}' on date '{date}'"}
        
        # Convert to dictionary
        return hospital_data.iloc[0].to_dict()
    
    def get_column_value(self, hospital_name: str, column_name: str, date: Optional[str] = None) -> dict:
        """
        Get specific column value for a hospital.
        
        Args:
            hospital_name: Name of the hospital
            column_name: Name of the column to retrieve
            date: Optional date (if not provided, returns latest)
            
        Returns:
            dict: Column value(s)
        """
        # Check if column exists
        if column_name not in self.df.columns:
            return {"error": f"Column '{column_name}' not found. Use get_column_names() to see available columns."}
        
        # Filter by hospital name
        hospital_data = self.df[self.df['hospital_name'] == hospital_name]
        
        if hospital_data.empty:
            return {"error": f"Hospital '{hospital_name}' not found"}
        
        # Filter by date if provided
        if date:
            hospital_data = hospital_data[hospital_data['date'] == date]
            if hospital_data.empty:
                return {"error": f"No data found for hospital '{hospital_name}' on date '{date}'"}
            
            return {
                "hospital_name": hospital_name,
                "column": column_name,
                "date": date,
                "value": hospital_data.iloc[0][column_name]
            }
        else:
            # Return all dates
            values = hospital_data[['date', column_name]].to_dict('records')
            return {
                "hospital_name": hospital_name,
                "column": column_name,
                "values": values
            }
    
    def get_column_names(self) -> list:
        """Get all column names available in the CSV."""
        return list(self.df.columns)
    
    def get_hospital_location(self, hospital_name: str) -> dict:
        """
        Get location of a specific hospital.
        
        Args:
            hospital_name: Name of the hospital
            
        Returns:
            dict: Hospital location information with coordinates
        """
        hospital_data = self.df[self.df['hospital_name'] == hospital_name]
        
        if hospital_data.empty:
            return {"error": f"Hospital '{hospital_name}' not found"}
        
        row = hospital_data.iloc[0]
        
        # Parse coordinates from location column (format: "lat,lon")
        coords = row['location'].split(',')
        latitude = float(coords[0])
        longitude = float(coords[1])
        
        return {
            "hospital_name": hospital_name,
            "hospital_id": row['hospital_id'],
            "location": row['location'],
            "region": row['region'],
            "latitude": latitude,
            "longitude": longitude
        }
    
    def calculate_distance(self, hospital_name1: str, hospital_name2: str) -> dict:
        """
        Calculate distance between two hospitals using Haversine formula.
        
        Args:
            hospital_name1: Name of first hospital
            hospital_name2: Name of second hospital
            
        Returns:
            dict: Distance information in kilometers
        """
        # Get coordinates for both hospitals
        hosp1_data = self.df[self.df['hospital_name'] == hospital_name1]
        hosp2_data = self.df[self.df['hospital_name'] == hospital_name2]
        
        if hosp1_data.empty:
            return {"error": f"Hospital '{hospital_name1}' not found"}
        if hosp2_data.empty:
            return {"error": f"Hospital '{hospital_name2}' not found"}
        
        # Parse coordinates from location column (format: "lat,lon")
        coords1 = hosp1_data.iloc[0]['location'].split(',')
        lat1 = float(coords1[0])
        lon1 = float(coords1[1])
        
        coords2 = hosp2_data.iloc[0]['location'].split(',')
        lat2 = float(coords2[0])
        lon2 = float(coords2[1])
        
        # Haversine formula
        R = 6371  # Earth's radius in kilometers
        
        lat1_rad = radians(lat1)
        lat2_rad = radians(lat2)
        delta_lat = radians(lat2 - lat1)
        delta_lon = radians(lon2 - lon1)
        
        a = sin(delta_lat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(delta_lon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance_km = R * c
        
        return {
            "from_hospital": hospital_name1,
            "to_hospital": hospital_name2,
            "distance_km": round(distance_km, 2),
            "from_coordinates": {"latitude": lat1, "longitude": lon1},
            "to_coordinates": {"latitude": lat2, "longitude": lon2}
        }
    
    def get_all_distances(self) -> dict:
        """
        Calculate distances between all pairs of hospitals.
        
        Returns:
            dict: Distance matrix for all hospitals
        """
        hospitals = self.df[['hospital_id', 'hospital_name']].drop_duplicates()
        distances = []
        
        for i, hosp1 in hospitals.iterrows():
            for j, hosp2 in hospitals.iterrows():
                if hosp1['hospital_id'] < hosp2['hospital_id']:  # Avoid duplicates
                    dist_info = self.calculate_distance(hosp1['hospital_name'], hosp2['hospital_name'])
                    if "error" not in dist_info:
                        distances.append(dist_info)
        
        return {
            "total_pairs": len(distances),
            "distances": distances
        }
    
    def get_date_range(self) -> dict:
        """Get the date range of available data."""
        dates = sorted(self.df['date'].unique())
        return {
            "start_date": dates[0],
            "end_date": dates[-1],
            "total_days": len(dates),
            "all_dates": dates
        }


# Initialize global instance
hospital_tool = HospitalDataTool()
