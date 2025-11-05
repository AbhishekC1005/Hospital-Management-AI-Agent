"""Enhanced Hospital data query tool with advanced analytics capabilities."""
import pandas as pd
import os
from typing import Optional, List, Dict, Tuple
from math import radians, sin, cos, sqrt, atan2
import numpy as np


class HospitalDataTool:
    """Enhanced tool for querying and analyzing hospital data from CSV."""
    
    def __init__(self, csv_path="agent/data/hospital_trends.csv"):
        """Initialize with CSV file path."""
        self.csv_path = csv_path
        self.df = None
        self._load_data()
        self._add_location_column()
        self._validate_data()
    
    def _load_data(self):
        """Load CSV data into pandas DataFrame with error handling."""
        try:
            if os.path.exists(self.csv_path):
                self.df = pd.read_csv(self.csv_path)
                print(f"✓ Loaded {len(self.df)} records from {self.csv_path}")
            else:
                raise FileNotFoundError(f"CSV file not found: {self.csv_path}")
        except Exception as e:
            raise Exception(f"Error loading data: {str(e)}")
    
    def _add_location_column(self):
        """Add location column to CSV if it doesn't exist."""
        if 'location' not in self.df.columns or self.df['location'].isna().any():
            location_mapping = {
                'H001': '40.7580,-73.9855',  # New York coordinates
                'H002': '40.7489,-73.9680',  # Brooklyn coordinates
                'H003': '40.7614,-73.9776',  # Manhattan coordinates
                'H004': '40.7505,-73.9934',  # Bronx coordinates
                'H005': '40.7690,-73.9712'   # Queens coordinates
            }
            self.df['location'] = self.df['hospital_id'].map(location_mapping)
            self.df.to_csv(self.csv_path, index=False)
    
    def _validate_data(self):
        """Validate data integrity."""
        required_columns = ['hospital_id', 'hospital_name', 'date', 'bed_capacity', 'location']
        missing_columns = [col for col in required_columns if col not in self.df.columns]
        
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        print(f"✓ Data validation passed")
    
    def get_hospital_count(self) -> int:
        """Get total number of unique hospitals."""
        return self.df['hospital_id'].nunique()
    
    def get_region_distribution(self) -> Dict[str, int]:
        """Get distribution of hospitals by region."""
        return self.df.groupby('region')['hospital_id'].nunique().to_dict()
    
    def get_hospital_names(self, region: Optional[str] = None) -> List[Dict]:
        """
        Get list of all hospital names with IDs and locations.
        
        Args:
            region: Optional filter by region
        """
        hospitals = self.df[['hospital_id', 'hospital_name', 'location', 'region']].drop_duplicates()
        
        if region:
            hospitals = hospitals[hospitals['region'].str.lower() == region.lower()]
        
        return hospitals.to_dict('records')
    
    def get_hospital_details_by_date(self, hospital_name: str, date: str) -> Dict:
        """Get details of a specific hospital for a specific date."""
        hospital_data = self.df[
            (self.df['hospital_name'].str.lower() == hospital_name.lower()) & 
            (self.df['date'] == date)
        ]
        
        if hospital_data.empty:
            # Try fuzzy matching
            hospitals = self.df['hospital_name'].unique()
            suggestions = [h for h in hospitals if hospital_name.lower() in h.lower()]
            
            error_msg = f"No data found for hospital '{hospital_name}' on date '{date}'."
            if suggestions:
                error_msg += f" Did you mean: {', '.join(suggestions)}?"
            
            return {"error": error_msg}
        
        return hospital_data.iloc[0].to_dict()
    
    def analyze_capacity_trends(self, hospital_name: str) -> Dict:
        """Analyze capacity trends for a hospital across all dates."""
        hospital_data = self.df[self.df['hospital_name'].str.lower() == hospital_name.lower()]
        
        if hospital_data.empty:
            return {"error": f"Hospital '{hospital_name}' not found"}
        
        # Calculate utilization rates
        hospital_data['bed_utilization'] = (
            hospital_data['beds_occupied'] / hospital_data['bed_capacity'] * 100
        )
        hospital_data['icu_utilization'] = (
            hospital_data['icu_beds_occupied'] / hospital_data['icu_beds_total'] * 100
        )
        
        # Find peak and low points
        max_bed_idx = hospital_data['bed_utilization'].idxmax()
        min_bed_idx = hospital_data['bed_utilization'].idxmin()
        
        # Determine trend
        bed_util_trend = np.polyfit(range(len(hospital_data)), hospital_data['bed_utilization'], 1)[0]
        trend_direction = "Increasing" if bed_util_trend > 0.5 else "Decreasing" if bed_util_trend < -0.5 else "Stable"
        
        # Count critical days
        critical_days = len(hospital_data[hospital_data['bed_utilization'] > 90])
        high_capacity_days = len(hospital_data[(hospital_data['bed_utilization'] > 80) & (hospital_data['bed_utilization'] <= 90)])
        
        return {
            'hospital_name': hospital_name,
            'data_points': len(hospital_data),
            'avg_bed_utilization': hospital_data['bed_utilization'].mean(),
            'max_bed_utilization': hospital_data.loc[max_bed_idx, 'bed_utilization'],
            'min_bed_utilization': hospital_data.loc[min_bed_idx, 'bed_utilization'],
            'max_bed_date': hospital_data.loc[max_bed_idx, 'date'],
            'min_bed_date': hospital_data.loc[min_bed_idx, 'date'],
            'bed_trend': trend_direction,
            'avg_icu_utilization': hospital_data['icu_utilization'].mean(),
            'max_icu_utilization': hospital_data['icu_utilization'].max(),
            'total_admissions': hospital_data['patient_admissions'].sum(),
            'total_discharges': hospital_data['patient_discharges'].sum(),
            'total_emergency_visits': hospital_data['emergency_visits'].sum(),
            'avg_daily_admissions': hospital_data['patient_admissions'].mean(),
            'critical_capacity_days': critical_days,
            'high_capacity_days': high_capacity_days,
            'avg_burnout_risk': hospital_data['burnout_risk_score'].mode()[0] if not hospital_data['burnout_risk_score'].empty else 'N/A'
        }
    
    def get_system_statistics(self, date: str) -> Dict:
        """Get system-wide statistics for a specific date."""
        date_data = self.df[self.df['date'] == date]
        
        if date_data.empty:
            return {"error": f"No data found for date '{date}'"}
        
        # Calculate system-wide metrics
        total_bed_capacity = date_data['bed_capacity'].sum()
        total_beds_occupied = date_data['beds_occupied'].sum()
        system_bed_utilization = (total_beds_occupied / total_bed_capacity * 100) if total_bed_capacity > 0 else 0
        
        # Identify hospitals at risk
        date_data['bed_utilization'] = (date_data['beds_occupied'] / date_data['bed_capacity'] * 100)
        critical_hospitals = date_data[date_data['bed_utilization'] > 90]['hospital_name'].tolist()
        high_capacity_hospitals = date_data[
            (date_data['bed_utilization'] > 80) & (date_data['bed_utilization'] <= 90)
        ]['hospital_name'].tolist()
        high_burnout_hospitals = date_data[date_data['burnout_risk_score'] == 'critical']['hospital_name'].tolist()
        
        return {
            'date': date,
            'total_hospitals': len(date_data),
            'total_bed_capacity': int(total_bed_capacity),
            'total_beds_occupied': int(total_beds_occupied),
            'system_bed_utilization': system_bed_utilization,
            'total_icu_beds': int(date_data['icu_beds_total'].sum()),
            'icu_utilization': (date_data['icu_beds_occupied'].sum() / date_data['icu_beds_total'].sum() * 100),
            'total_ventilators': int(date_data['ventilators_total'].sum()),
            'ventilators_available': int(date_data['ventilators_available'].sum()),
            'ventilator_utilization': (date_data['ventilators_in_use'].sum() / date_data['ventilators_total'].sum() * 100),
            'total_doctors': int(date_data['doctors_total'].sum()),
            'doctors_available': int(date_data['doctors_available'].sum()),
            'total_nurses': int(date_data['nurses_total'].sum()),
            'nurses_available': int(date_data['nurses_available'].sum()),
            'total_admissions': int(date_data['patient_admissions'].sum()),
            'total_discharges': int(date_data['patient_discharges'].sum()),
            'total_emergency_visits': int(date_data['emergency_visits'].sum()),
            'total_surgeries': int(date_data['surgery_count'].sum()),
            'total_covid_cases': int(date_data['covid_cases'].sum()),
            'total_flu_cases': int(date_data['flu_cases'].sum()),
            'total_other_infectious': int(date_data['other_infectious_cases'].sum()),
            'critical_hospitals': critical_hospitals,
            'high_capacity_hospitals': high_capacity_hospitals,
            'high_burnout_hospitals': high_burnout_hospitals
        }
    
    def get_column_value(self, hospital_name: str, column_name: str, date: Optional[str] = None) -> Dict:
        """Get specific column value for a hospital."""
        if column_name not in self.df.columns:
            available_columns = ', '.join(self.df.columns.tolist()[:10])
            return {"error": f"Column '{column_name}' not found. Available columns include: {available_columns}..."}
        
        hospital_data = self.df[self.df['hospital_name'].str.lower() == hospital_name.lower()]
        
        if hospital_data.empty:
            return {"error": f"Hospital '{hospital_name}' not found"}
        
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
            values = hospital_data[['date', column_name]].to_dict('records')
            return {
                "hospital_name": hospital_name,
                "column": column_name,
                "values": values
            }
    
    def get_column_names(self) -> List[str]:
        """Get all column names available in the CSV."""
        return list(self.df.columns)
    
    def get_hospital_location(self, hospital_name: str) -> Dict:
        """Get location of a specific hospital."""
        hospital_data = self.df[self.df['hospital_name'].str.lower() == hospital_name.lower()]
        
        if hospital_data.empty:
            return {"error": f"Hospital '{hospital_name}' not found"}
        
        row = hospital_data.iloc[0]
        coords = row['location'].split(',')
        latitude = float(coords[0])
        longitude = float(coords[1])
        
        return {
            "hospital_name": row['hospital_name'],
            "hospital_id": row['hospital_id'],
            "location": row['location'],
            "region": row['region'],
            "latitude": latitude,
            "longitude": longitude
        }
    
    def calculate_distance(self, hospital_name1: str, hospital_name2: str) -> Dict:
        """Calculate distance between two hospitals using Haversine formula."""
        hosp1_data = self.df[self.df['hospital_name'].str.lower() == hospital_name1.lower()]
        hosp2_data = self.df[self.df['hospital_name'].str.lower() == hospital_name2.lower()]
        
        if hosp1_data.empty:
            hospitals = self.df['hospital_name'].unique()
            suggestions = [h for h in hospitals if hospital_name1.lower() in h.lower()]
            error_msg = f"Hospital '{hospital_name1}' not found."
            if suggestions:
                error_msg += f" Did you mean: {', '.join(suggestions)}?"
            return {"error": error_msg}
        
        if hosp2_data.empty:
            hospitals = self.df['hospital_name'].unique()
            suggestions = [h for h in hospitals if hospital_name2.lower() in h.lower()]
            error_msg = f"Hospital '{hospital_name2}' not found."
            if suggestions:
                error_msg += f" Did you mean: {', '.join(suggestions)}?"
            return {"error": error_msg}
        
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
            "from_hospital": hosp1_data.iloc[0]['hospital_name'],
            "to_hospital": hosp2_data.iloc[0]['hospital_name'],
            "distance_km": round(distance_km, 2),
            "from_coordinates": {"latitude": lat1, "longitude": lon1},
            "to_coordinates": {"latitude": lat2, "longitude": lon2}
        }
    
    def find_nearest_hospital(self, hospital_name: str) -> Dict:
        """Find the nearest hospital to a given hospital."""
        hospital_data = self.df[self.df['hospital_name'].str.lower() == hospital_name.lower()]
        
        if hospital_data.empty:
            return {"error": f"Hospital '{hospital_name}' not found"}
        
        all_hospitals = self.df['hospital_name'].unique()
        min_distance = float('inf')
        nearest_hospital = None
        
        for other_hospital in all_hospitals:
            if other_hospital.lower() != hospital_name.lower():
                dist_info = self.calculate_distance(hospital_name, other_hospital)
                if "error" not in dist_info and dist_info['distance_km'] < min_distance:
                    min_distance = dist_info['distance_km']
                    nearest_hospital = other_hospital
        
        return {
            "reference_hospital": hospital_name,
            "nearest_hospital": nearest_hospital,
            "distance_km": min_distance
        }
    
    def get_all_distances(self) -> Dict:
        """Calculate distances between all pairs of hospitals."""
        hospitals = self.df[['hospital_id', 'hospital_name']].drop_duplicates()
        distances = []
        
        for i, hosp1 in hospitals.iterrows():
            for j, hosp2 in hospitals.iterrows():
                if hosp1['hospital_id'] < hosp2['hospital_id']:
                    dist_info = self.calculate_distance(hosp1['hospital_name'], hosp2['hospital_name'])
                    if "error" not in dist_info:
                        distances.append(dist_info)
        
        return {
            "total_pairs": len(distances),
            "distances": distances
        }
    
    def get_date_range(self) -> Dict:
        """Get the date range of available data."""
        dates = sorted(self.df['date'].unique())
        return {
            "start_date": dates[0],
            "end_date": dates[-1],
            "total_days": len(dates),
            "all_dates": dates
        }
    
    def search_hospitals(self, **criteria) -> List[Dict]:
        """
        Search hospitals based on multiple criteria.
        
        Args:
            **criteria: Search criteria (e.g., region='North', min_beds=300)
        """
        result = self.df.copy()
        
        for key, value in criteria.items():
            if key in result.columns:
                if isinstance(value, str):
                    result = result[result[key].str.lower() == value.lower()]
                else:
                    result = result[result[key] == value]
        
        return result[['hospital_id', 'hospital_name', 'region', 'location']].drop_duplicates().to_dict('records')


# Initialize the tool
hospital_tool = HospitalDataTool()