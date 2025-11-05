"""Simplified hospital data query functions for ADK agent."""
from typing import Optional
from agent.tools.hospital_data import hospital_tool


def get_hospital_count() -> str:
    """
    Get the total number of hospitals in the system.
    
    Returns:
        str: Number of hospitals
    """
    try:
        count = hospital_tool.get_hospital_count()
        return f"There are {count} hospitals in the system."
    except Exception as e:
        return f"Error: {str(e)}"


def get_hospital_names() -> str:
    """
    Get the names, IDs, and locations of all hospitals.
    
    Returns:
        str: List of hospital names with IDs and locations
    """
    try:
        hospitals = hospital_tool.get_hospital_names()
        result = "Hospitals in the system:\n\n"
        for hosp in hospitals:
            result += f"• {hosp['hospital_name']} (ID: {hosp['hospital_id']})\n"
            result += f"  Location: {hosp['location']}\n\n"
        return result
    except Exception as e:
        return f"Error: {str(e)}"


def get_hospital_details_by_date(hospital_name: str, date: str) -> str:
    """
    Get detailed information for a specific hospital on a specific date.
    
    Args:
        hospital_name: The hospital name (e.g., 'City General Hospital')
        date: Date in format 'YYYY-MM-DD' (e.g., '2024-10-20')
        
    Returns:
        str: Detailed hospital information for that date
    """
    try:
        info = hospital_tool.get_hospital_details_by_date(hospital_name, date)
        
        if "error" in info:
            return info["error"]
        
        # Format the output
        result = f"📊 Hospital Details for {hospital_name} on {date}\n\n"
        result += f"Hospital ID: {info['hospital_id']}\n"
        result += f"Location: {info['location']}\n"
        result += f"Region: {info['region']}\n\n"
        
        result += f"🛏️ Beds:\n"
        result += f"  • Capacity: {info['bed_capacity']}\n"
        result += f"  • Occupied: {info['beds_occupied']}\n"
        result += f"  • Available: {info['beds_available']}\n\n"
        
        result += f"🏥 ICU:\n"
        result += f"  • Total: {info['icu_beds_total']}\n"
        result += f"  • Occupied: {info['icu_beds_occupied']}\n\n"
        
        result += f"🫁 Ventilators:\n"
        result += f"  • Total: {info['ventilators_total']}\n"
        result += f"  • In Use: {info['ventilators_in_use']}\n"
        result += f"  • Available: {info['ventilators_available']}\n\n"
        
        result += f"👨‍⚕️ Staff:\n"
        result += f"  • Doctors: {info['doctors_available']}/{info['doctors_total']} available\n"
        result += f"  • Nurses: {info['nurses_available']}/{info['nurses_total']} available\n"
        result += f"  • Paramedics: {info['paramedics_available']}/{info['paramedics_total']} available\n\n"
        
        result += f"📈 Patient Activity:\n"
        result += f"  • Admissions: {info['patient_admissions']}\n"
        result += f"  • Discharges: {info['patient_discharges']}\n"
        result += f"  • Emergency Visits: {info['emergency_visits']}\n"
        result += f"  • Surgeries: {info['surgery_count']}\n\n"
        
        result += f"🦠 Infectious Cases:\n"
        result += f"  • COVID: {info['covid_cases']}\n"
        result += f"  • Flu: {info['flu_cases']}\n"
        result += f"  • Other: {info['other_infectious_cases']}\n\n"
        
        result += f"⚠️ Burnout Risk: {info['burnout_risk_score']}\n"
        result += f"⭐ Patient Satisfaction: {info['avg_patient_satisfaction']}/5.0\n"
        
        return result
    except Exception as e:
        return f"Error: {str(e)}"


def get_column_value(hospital_name: str, column_name: str, date: Optional[str] = None) -> str:
    """
    Get a specific column value for a hospital.
    
    Args:
        hospital_name: The hospital name
        column_name: The column name to retrieve
        date: Optional date (if not provided, returns all dates)
        
    Returns:
        str: Column value(s)
    """
    try:
        result = hospital_tool.get_column_value(hospital_name, column_name, date)
        
        if "error" in result:
            return result["error"]
        
        if date:
            return f"{column_name} for {hospital_name} on {date}: {result['value']}"
        else:
            output = f"{column_name} for {hospital_name} across all dates:\n\n"
            for item in result['values']:
                output += f"  • {item['date']}: {item[column_name]}\n"
            return output
    except Exception as e:
        return f"Error: {str(e)}"


def get_column_names() -> str:
    """
    Get all available column names in the hospital data CSV.
    
    Returns:
        str: List of column names
    """
    try:
        columns = hospital_tool.get_column_names()
        result = "Available columns in hospital data:\n\n"
        for i, col in enumerate(columns, 1):
            result += f"{i}. {col}\n"
        return result
    except Exception as e:
        return f"Error: {str(e)}"


def get_hospital_location(hospital_name: str) -> str:
    """
    Get the location of a specific hospital.
    
    Args:
        hospital_name: The hospital name
        
    Returns:
        str: Hospital location information
    """
    try:
        info = hospital_tool.get_hospital_location(hospital_name)
        
        if "error" in info:
            return info["error"]
        
        result = f"📍 Location Information\n\n"
        result += f"Hospital: {info['hospital_name']}\n"
        result += f"ID: {info['hospital_id']}\n"
        result += f"Location: {info['location']}\n"
        result += f"Region: {info['region']}\n"
        
        return result
    except Exception as e:
        return f"Error: {str(e)}"


def get_data_date_range() -> str:
    """
    Get the date range of available hospital data.
    
    Returns:
        str: Date range information
    """
    try:
        info = hospital_tool.get_date_range()
        result = f"📅 Available Data Range\n\n"
        result += f"Start Date: {info['start_date']}\n"
        result += f"End Date: {info['end_date']}\n"
        result += f"Total Days: {info['total_days']}\n\n"
        result += f"All Dates:\n"
        for date in info['all_dates']:
            result += f"  • {date}\n"
        return result
    except Exception as e:
        return f"Error: {str(e)}"


def calculate_distance_between_hospitals(hospital_name1: str, hospital_name2: str) -> str:
    """
    Calculate the distance between two hospitals.
    
    Args:
        hospital_name1: Name of the first hospital
        hospital_name2: Name of the second hospital
        
    Returns:
        str: Distance information
    """
    try:
        info = hospital_tool.calculate_distance(hospital_name1, hospital_name2)
        
        if "error" in info:
            return info["error"]
        
        result = f"📏 Distance Calculation\n\n"
        result += f"From: {info['from_hospital']}\n"
        result += f"  Coordinates: ({info['from_coordinates']['latitude']}, {info['from_coordinates']['longitude']})\n\n"
        result += f"To: {info['to_hospital']}\n"
        result += f"  Coordinates: ({info['to_coordinates']['latitude']}, {info['to_coordinates']['longitude']})\n\n"
        result += f"Distance: {info['distance_km']} km\n"
        
        return result
    except Exception as e:
        return f"Error: {str(e)}"


def get_all_hospital_distances() -> str:
    """
    Get distances between all pairs of hospitals.
    
    Returns:
        str: Distance matrix for all hospitals
    """
    try:
        info = hospital_tool.get_all_distances()
        
        result = f"📏 Hospital Distance Matrix\n\n"
        result += f"Total Hospital Pairs: {info['total_pairs']}\n\n"
        
        for dist in info['distances']:
            result += f"• {dist['from_hospital']} ↔ {dist['to_hospital']}: {dist['distance_km']} km\n"
        
        return result
    except Exception as e:
        return f"Error: {str(e)}"
