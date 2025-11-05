"""Enhanced CrewAI tools for hospital data analysis with advanced analytics."""
from crewai.tools import tool
from typing import Optional, List, Dict
from agent.tools.hospital_data import hospital_tool


@tool("Get Hospital Count")
def get_hospital_count_tool() -> str:
    """Get the total number of hospitals in the system with additional statistics."""
    try:
        count = hospital_tool.get_hospital_count()
        regions = hospital_tool.get_region_distribution()
        
        result = f"📊 Hospital System Overview\n\n"
        result += f"Total Hospitals: {count}\n"
        result += f"\nRegional Distribution:\n"
        for region, count in regions.items():
            result += f"  • {region}: {count} hospital(s)\n"
        
        return result
    except Exception as e:
        return f"Error retrieving hospital count: {str(e)}"


@tool("Get Hospital Names")
def get_hospital_names_tool(region: Optional[str] = None) -> str:
    """
    Get names, IDs, and locations of all hospitals.
    
    Args:
        region: Optional filter by region (e.g., 'North', 'South', 'East', 'West', 'Central')
    """
    try:
        hospitals = hospital_tool.get_hospital_names(region=region)
        
        if not hospitals:
            return f"No hospitals found{f' in {region} region' if region else ''}."
        
        result = f"🏥 Hospitals{f' in {region} Region' if region else ' in System'}:\n\n"
        
        for hosp in hospitals:
            result += f"• {hosp['hospital_name']} (ID: {hosp['hospital_id']})\n"
            result += f"  📍 Location: {hosp['location']}\n"
            result += f"  🗺️  Region: {hosp['region']}\n\n"
        
        return result
    except Exception as e:
        return f"Error retrieving hospital names: {str(e)}"


@tool("Get Hospital Details")
def get_hospital_details_tool(hospital_name: str, date: str = "2024-10-20") -> str:
    """
    Get detailed information for a specific hospital on a specific date.
    
    Args:
        hospital_name: The hospital name (e.g., 'City General Hospital')
        date: Date in format 'YYYY-MM-DD' (default: '2024-10-20')
    """
    try:
        info = hospital_tool.get_hospital_details_by_date(hospital_name, date)
        
        if "error" in info:
            return info["error"]
        
        # Calculate utilization rates
        bed_utilization = (info['beds_occupied'] / info['bed_capacity'] * 100) if info['bed_capacity'] > 0 else 0
        icu_utilization = (info['icu_beds_occupied'] / info['icu_beds_total'] * 100) if info['icu_beds_total'] > 0 else 0
        ventilator_utilization = (info['ventilators_in_use'] / info['ventilators_total'] * 100) if info['ventilators_total'] > 0 else 0
        
        # Assess capacity status
        capacity_status = "🟢 Normal"
        if bed_utilization > 90:
            capacity_status = "🔴 Critical"
        elif bed_utilization > 80:
            capacity_status = "🟡 High"
        
        result = f"📊 Hospital Details: {hospital_name}\n"
        result += f"📅 Date: {date}\n"
        result += f"{'=' * 50}\n\n"
        
        result += f"🏥 FACILITY INFORMATION\n"
        result += f"  Hospital ID: {info['hospital_id']}\n"
        result += f"  Location: {info['location']}\n"
        result += f"  Region: {info['region']}\n"
        result += f"  Capacity Status: {capacity_status}\n\n"
        
        result += f"🛏️  BED CAPACITY\n"
        result += f"  Total Capacity: {info['bed_capacity']}\n"
        result += f"  Occupied: {info['beds_occupied']} ({bed_utilization:.1f}%)\n"
        result += f"  Available: {info['beds_available']}\n\n"
        
        result += f"🏥 ICU CAPACITY\n"
        result += f"  Total ICU Beds: {info['icu_beds_total']}\n"
        result += f"  Occupied: {info['icu_beds_occupied']} ({icu_utilization:.1f}%)\n"
        result += f"  Available: {info['icu_beds_total'] - info['icu_beds_occupied']}\n\n"
        
        result += f"🫁 VENTILATOR STATUS\n"
        result += f"  Total: {info['ventilators_total']}\n"
        result += f"  In Use: {info['ventilators_in_use']} ({ventilator_utilization:.1f}%)\n"
        result += f"  Available: {info['ventilators_available']}\n\n"
        
        result += f"👨‍⚕️ STAFF AVAILABILITY\n"
        result += f"  Doctors: {info['doctors_available']}/{info['doctors_total']} available ({info['doctors_available']/info['doctors_total']*100:.0f}%)\n"
        result += f"  Nurses: {info['nurses_available']}/{info['nurses_total']} available ({info['nurses_available']/info['nurses_total']*100:.0f}%)\n"
        result += f"  Paramedics: {info['paramedics_available']}/{info['paramedics_total']} available ({info['paramedics_available']/info['paramedics_total']*100:.0f}%)\n"
        result += f"  Overtime Hours: {info['staff_overtime_hours']} hrs\n"
        result += f"  Staff on Sick Leave: {info['staff_sick_leave']}\n\n"
        
        result += f"📈 PATIENT ACTIVITY\n"
        result += f"  Admissions: {info['patient_admissions']}\n"
        result += f"  Discharges: {info['patient_discharges']}\n"
        result += f"  Emergency Visits: {info['emergency_visits']}\n"
        result += f"  Surgeries Performed: {info['surgery_count']}\n"
        result += f"  Avg Wait Time: {info['avg_wait_time_minutes']} minutes\n\n"
        
        result += f"🦠 INFECTIOUS CASES\n"
        result += f"  COVID-19: {info['covid_cases']}\n"
        result += f"  Flu: {info['flu_cases']}\n"
        result += f"  Other: {info['other_infectious_cases']}\n\n"
        
        result += f"🏥 RESOURCES & EQUIPMENT\n"
        result += f"  Masks: {info['supply_masks']}\n"
        result += f"  Gloves: {info['supply_gloves']}\n"
        result += f"  Sanitizer: {info['supply_sanitizer']} units\n"
        result += f"  Medicine Stock: {info['supply_medicines_stock_level']}%\n"
        result += f"  X-Ray Machines: {info['equipment_xray_functional']} functional\n"
        result += f"  CT Scanners: {info['equipment_ct_scan_functional']} functional\n"
        result += f"  MRI Machines: {info['equipment_mri_functional']} functional\n\n"
        
        result += f"🚑 AMBULANCE FLEET\n"
        result += f"  Total: {info['ambulances_total']}\n"
        result += f"  Available: {info['ambulances_available']}\n"
        result += f"  Cost per km: ${info['transport_cost_per_km']}\n\n"
        
        result += f"⚠️  RISK INDICATORS\n"
        result += f"  Patient Satisfaction: {info['avg_patient_satisfaction']}/5.0\n"
        result += f"  Staff Burnout Risk: {info['burnout_risk_score']}\n"
        
        return result
    except Exception as e:
        return f"Error retrieving hospital details: {str(e)}"


@tool("Compare Hospitals")
def compare_hospitals_tool(hospital_name1: str, hospital_name2: str, date: str = "2024-10-20") -> str:
    """
    Compare two hospitals side by side on key metrics.
    
    Args:
        hospital_name1: First hospital name
        hospital_name2: Second hospital name
        date: Date in format 'YYYY-MM-DD' (default: '2024-10-20')
    """
    try:
        h1 = hospital_tool.get_hospital_details_by_date(hospital_name1, date)
        h2 = hospital_tool.get_hospital_details_by_date(hospital_name2, date)
        
        if "error" in h1:
            return h1["error"]
        if "error" in h2:
            return h2["error"]
        
        result = f"⚖️  Hospital Comparison ({date})\n"
        result += f"{'=' * 70}\n\n"
        
        result += f"{'Metric':<30} | {hospital_name1[:20]:<20} | {hospital_name2[:20]:<20}\n"
        result += f"{'-' * 30}-+-{'-' * 20}-+-{'-' * 20}\n"
        
        # Bed capacity comparison
        result += f"{'Bed Capacity':<30} | {h1['bed_capacity']:<20} | {h2['bed_capacity']:<20}\n"
        result += f"{'Beds Occupied':<30} | {h1['beds_occupied']:<20} | {h2['beds_occupied']:<20}\n"
        result += f"{'Bed Utilization':<30} | {h1['beds_occupied']/h1['bed_capacity']*100:<20.1f}% | {h2['beds_occupied']/h2['bed_capacity']*100:<20.1f}%\n\n"
        
        # ICU comparison
        result += f"{'ICU Beds Total':<30} | {h1['icu_beds_total']:<20} | {h2['icu_beds_total']:<20}\n"
        result += f"{'ICU Beds Occupied':<30} | {h1['icu_beds_occupied']:<20} | {h2['icu_beds_occupied']:<20}\n\n"
        
        # Ventilators
        result += f"{'Ventilators Available':<30} | {h1['ventilators_available']:<20} | {h2['ventilators_available']:<20}\n\n"
        
        # Staff
        result += f"{'Doctors Available':<30} | {h1['doctors_available']}/{h1['doctors_total']:<20} | {h2['doctors_available']}/{h2['doctors_total']:<20}\n"
        result += f"{'Nurses Available':<30} | {h1['nurses_available']}/{h1['nurses_total']:<20} | {h2['nurses_available']}/{h2['nurses_total']:<20}\n\n"
        
        # Patient metrics
        result += f"{'Emergency Visits':<30} | {h1['emergency_visits']:<20} | {h2['emergency_visits']:<20}\n"
        result += f"{'Avg Wait Time (min)':<30} | {h1['avg_wait_time_minutes']:<20} | {h2['avg_wait_time_minutes']:<20}\n"
        result += f"{'Patient Satisfaction':<30} | {h1['avg_patient_satisfaction']:<20} | {h2['avg_patient_satisfaction']:<20}\n\n"
        
        # Risk
        result += f"{'Burnout Risk':<30} | {h1['burnout_risk_score']:<20} | {h2['burnout_risk_score']:<20}\n"
        
        return result
    except Exception as e:
        return f"Error comparing hospitals: {str(e)}"


@tool("Analyze Capacity Trends")
def analyze_capacity_trends_tool(hospital_name: str) -> str:
    """
    Analyze capacity trends for a hospital across all available dates.
    
    Args:
        hospital_name: The hospital name
    """
    try:
        trends = hospital_tool.analyze_capacity_trends(hospital_name)
        
        if "error" in trends:
            return trends["error"]
        
        result = f"📈 Capacity Trend Analysis: {hospital_name}\n"
        result += f"{'=' * 60}\n\n"
        
        result += f"📊 BED CAPACITY TRENDS\n"
        result += f"  Average Utilization: {trends['avg_bed_utilization']:.1f}%\n"
        result += f"  Peak Utilization: {trends['max_bed_utilization']:.1f}% on {trends['max_bed_date']}\n"
        result += f"  Lowest Utilization: {trends['min_bed_utilization']:.1f}% on {trends['min_bed_date']}\n"
        result += f"  Trend: {trends['bed_trend']}\n\n"
        
        result += f"🏥 ICU TRENDS\n"
        result += f"  Average ICU Utilization: {trends['avg_icu_utilization']:.1f}%\n"
        result += f"  Peak ICU Utilization: {trends['max_icu_utilization']:.1f}%\n\n"
        
        result += f"📈 PATIENT ACTIVITY\n"
        result += f"  Total Admissions: {trends['total_admissions']}\n"
        result += f"  Total Discharges: {trends['total_discharges']}\n"
        result += f"  Total Emergency Visits: {trends['total_emergency_visits']}\n"
        result += f"  Avg Daily Admissions: {trends['avg_daily_admissions']:.1f}\n\n"
        
        result += f"⚠️  RISK ASSESSMENT\n"
        result += f"  Days at Critical Capacity (>90%): {trends['critical_capacity_days']}\n"
        result += f"  Days at High Capacity (80-90%): {trends['high_capacity_days']}\n"
        result += f"  Average Burnout Risk: {trends['avg_burnout_risk']}\n"
        
        return result
    except Exception as e:
        return f"Error analyzing trends: {str(e)}"


@tool("Get Column Names")
def get_column_names_tool() -> str:
    """Get all available column names in the hospital data with descriptions."""
    try:
        columns = hospital_tool.get_column_names()
        
        # Group columns by category
        categories = {
            'Identification': ['date', 'hospital_id', 'hospital_name', 'region', 'location'],
            'Bed Capacity': ['bed_capacity', 'beds_occupied', 'beds_available', 'icu_beds_total', 'icu_beds_occupied'],
            'Equipment': ['ventilators_total', 'ventilators_in_use', 'ventilators_available', 
                         'equipment_xray_functional', 'equipment_ct_scan_functional', 'equipment_mri_functional'],
            'Patient Activity': ['patient_admissions', 'patient_discharges', 'emergency_visits', 
                                'surgery_count', 'avg_wait_time_minutes', 'avg_patient_satisfaction'],
            'Staff': ['doctors_total', 'doctors_available', 'nurses_total', 'nurses_available', 
                     'paramedics_total', 'paramedics_available', 'staff_overtime_hours', 'staff_sick_leave', 'burnout_risk_score'],
            'Supplies': ['supply_masks', 'supply_gloves', 'supply_sanitizer', 'supply_medicines_stock_level'],
            'Transportation': ['ambulances_total', 'ambulances_available', 'transport_cost_per_km'],
            'Infectious Cases': ['covid_cases', 'flu_cases', 'other_infectious_cases']
        }
        
        result = "📋 Available Data Columns\n\n"
        
        for category, cols in categories.items():
            result += f"🔹 {category}:\n"
            for col in cols:
                if col in columns:
                    result += f"   • {col}\n"
            result += "\n"
        
        result += f"Total Columns: {len(columns)}\n"
        
        return result
    except Exception as e:
        return f"Error retrieving column names: {str(e)}"


@tool("Get Date Range")
def get_date_range_tool() -> str:
    """Get the date range of available hospital data."""
    try:
        info = hospital_tool.get_date_range()
        result = f"📅 Available Data Range\n\n"
        result += f"Start Date: {info['start_date']}\n"
        result += f"End Date: {info['end_date']}\n"
        result += f"Total Days: {info['total_days']}\n\n"
        result += f"All Available Dates:\n"
        for date in info['all_dates']:
            result += f"  • {date}\n"
        return result
    except Exception as e:
        return f"Error retrieving date range: {str(e)}"


@tool("Calculate Distance")
def calculate_distance_tool(hospital_name1: str, hospital_name2: str) -> str:
    """
    Calculate the distance between two hospitals with travel time estimate.
    
    Args:
        hospital_name1: Name of the first hospital
        hospital_name2: Name of the second hospital
    """
    try:
        info = hospital_tool.calculate_distance(hospital_name1, hospital_name2)
        
        if "error" in info:
            return info["error"]
        
        # Estimate travel time (assuming average speed of 40 km/h in urban areas)
        estimated_time_hours = info['distance_km'] / 40
        estimated_time_minutes = estimated_time_hours * 60
        
        result = f"📏 Distance Calculation\n\n"
        result += f"From: {info['from_hospital']}\n"
        result += f"  📍 Coordinates: ({info['from_coordinates']['latitude']}, {info['from_coordinates']['longitude']})\n\n"
        result += f"To: {info['to_hospital']}\n"
        result += f"  📍 Coordinates: ({info['to_coordinates']['latitude']}, {info['to_coordinates']['longitude']})\n\n"
        result += f"✈️  Distance: {info['distance_km']} km\n"
        result += f"⏱️  Estimated Travel Time: {estimated_time_minutes:.0f} minutes (at 40 km/h avg)\n"
        
        return result
    except Exception as e:
        return f"Error calculating distance: {str(e)}"


@tool("Get All Distances")
def get_all_distances_tool() -> str:
    """Get distances between all pairs of hospitals, sorted by distance."""
    try:
        info = hospital_tool.get_all_distances()
        
        # Sort by distance
        sorted_distances = sorted(info['distances'], key=lambda x: x['distance_km'])
        
        result = f"📏 Hospital Distance Matrix\n\n"
        result += f"Total Hospital Pairs: {info['total_pairs']}\n\n"
        
        result += f"{'From':<30} | {'To':<30} | Distance (km)\n"
        result += f"{'-' * 30}-+-{'-' * 30}-+-{'-' * 12}\n"
        
        for dist in sorted_distances:
            from_name = dist['from_hospital'][:28]
            to_name = dist['to_hospital'][:28]
            result += f"{from_name:<30} | {to_name:<30} | {dist['distance_km']:>10.2f}\n"
        
        result += f"\n📊 Statistics:\n"
        distances_only = [d['distance_km'] for d in sorted_distances]
        result += f"  Closest: {min(distances_only):.2f} km\n"
        result += f"  Farthest: {max(distances_only):.2f} km\n"
        result += f"  Average: {sum(distances_only)/len(distances_only):.2f} km\n"
        
        return result
    except Exception as e:
        return f"Error retrieving distances: {str(e)}"


@tool("Find Nearest Hospital")
def find_nearest_hospital_tool(hospital_name: str) -> str:
    """
    Find the nearest hospital to a given hospital.
    
    Args:
        hospital_name: The reference hospital name
    """
    try:
        nearest = hospital_tool.find_nearest_hospital(hospital_name)
        
        if "error" in nearest:
            return nearest["error"]
        
        result = f"🎯 Nearest Hospital to {hospital_name}\n\n"
        result += f"Closest Hospital: {nearest['nearest_hospital']}\n"
        result += f"Distance: {nearest['distance_km']} km\n"
        result += f"Estimated Travel Time: {nearest['distance_km'] / 40 * 60:.0f} minutes\n"
        
        return result
    except Exception as e:
        return f"Error finding nearest hospital: {str(e)}"


@tool("Get System Statistics")
def get_system_statistics_tool(date: str = "2024-10-20") -> str:
    """
    Get system-wide statistics across all hospitals for a specific date.
    
    Args:
        date: Date in format 'YYYY-MM-DD' (default: '2024-10-20')
    """
    try:
        stats = hospital_tool.get_system_statistics(date)
        
        if "error" in stats:
            return stats["error"]
        
        result = f"🏥 Healthcare System Statistics\n"
        result += f"📅 Date: {date}\n"
        result += f"{'=' * 60}\n\n"
        
        result += f"🏥 SYSTEM CAPACITY\n"
        result += f"  Total Hospitals: {stats['total_hospitals']}\n"
        result += f"  Total Bed Capacity: {stats['total_bed_capacity']}\n"
        result += f"  Total Beds Occupied: {stats['total_beds_occupied']}\n"
        result += f"  System Bed Utilization: {stats['system_bed_utilization']:.1f}%\n"
        result += f"  Total ICU Beds: {stats['total_icu_beds']}\n"
        result += f"  ICU Utilization: {stats['icu_utilization']:.1f}%\n\n"
        
        result += f"🫁 VENTILATOR STATUS\n"
        result += f"  Total Ventilators: {stats['total_ventilators']}\n"
        result += f"  Ventilators Available: {stats['ventilators_available']}\n"
        result += f"  Utilization: {stats['ventilator_utilization']:.1f}%\n\n"
        
        result += f"👨‍⚕️ WORKFORCE\n"
        result += f"  Total Doctors: {stats['total_doctors']}\n"
        result += f"  Doctors Available: {stats['doctors_available']}\n"
        result += f"  Total Nurses: {stats['total_nurses']}\n"
        result += f"  Nurses Available: {stats['nurses_available']}\n\n"
        
        result += f"📈 DAILY ACTIVITY\n"
        result += f"  Total Admissions: {stats['total_admissions']}\n"
        result += f"  Total Discharges: {stats['total_discharges']}\n"
        result += f"  Total Emergency Visits: {stats['total_emergency_visits']}\n"
        result += f"  Total Surgeries: {stats['total_surgeries']}\n\n"
        
        result += f"🦠 INFECTIOUS CASES\n"
        result += f"  COVID-19: {stats['total_covid_cases']}\n"
        result += f"  Flu: {stats['total_flu_cases']}\n"
        result += f"  Other: {stats['total_other_infectious']}\n\n"
        
        result += f"⚠️  SYSTEM ALERTS\n"
        if stats['critical_hospitals']:
            result += f"  🔴 Critical Capacity ({len(stats['critical_hospitals'])}): {', '.join(stats['critical_hospitals'])}\n"
        if stats['high_capacity_hospitals']:
            result += f"  🟡 High Capacity ({len(stats['high_capacity_hospitals'])}): {', '.join(stats['high_capacity_hospitals'])}\n"
        if stats['high_burnout_hospitals']:
            result += f"  ⚠️  High Burnout Risk ({len(stats['high_burnout_hospitals'])}): {', '.join(stats['high_burnout_hospitals'])}\n"
        
        return result
    except Exception as e:
        return f"Error retrieving system statistics: {str(e)}"



@tool("Get Specific Column Value")
def get_column_value_tool(hospital_name: str, column_name: str, date: str = None) -> str:
    """
    Get ONLY a specific column value for a hospital. Use this when user asks for ONE specific metric.
    This returns ONLY the requested data, not all hospital information.
    
    Args:
        hospital_name: The hospital name (e.g., 'City General Hospital')
        column_name: The EXACT column name (e.g., 'beds_available', 'ventilators_total', 'doctors_available')
        date: Optional date in format 'YYYY-MM-DD' (if not provided, returns all dates)
    
    Examples:
        - "What are the available beds at City General Hospital?" -> use column_name='beds_available'
        - "How many ventilators does Regional Medical Center have?" -> use column_name='ventilators_total'
        - "Show me ICU beds at Metropolitan Hospital" -> use column_name='icu_beds_total'
    """
    try:
        result = hospital_tool.get_column_value(hospital_name, column_name, date)
        
        if "error" in result:
            return result["error"]
        
        if date:
            return f"📊 {column_name} for {hospital_name} on {date}: {result['value']}"
        else:
            output = f"📊 {column_name} for {hospital_name} across all dates:\n\n"
            for item in result['values']:
                output += f"  • {item['date']}: {item[column_name]}\n"
            return output
    except Exception as e:
        return f"Error: {str(e)}"



@tool("Calculate Travel Cost Between Hospitals")
def calculate_travel_cost_tool(hospital_name1: str, hospital_name2: str, date: str = "2024-10-20") -> str:
    """
    Calculate the travel cost between two hospitals based on distance and transport cost per km.
    
    Args:
        hospital_name1: Name of the first hospital
        hospital_name2: Name of the second hospital
        date: Date to get transport cost (default: '2024-10-20')
    """
    try:
        # Get distance
        distance_info = hospital_tool.calculate_distance(hospital_name1, hospital_name2)
        
        if "error" in distance_info:
            return distance_info["error"]
        
        # Get transport cost for both hospitals
        h1_data = hospital_tool.get_hospital_details_by_date(hospital_name1, date)
        h2_data = hospital_tool.get_hospital_details_by_date(hospital_name2, date)
        
        if "error" in h1_data:
            return h1_data["error"]
        if "error" in h2_data:
            return h2_data["error"]
        
        # Calculate costs
        distance_km = distance_info['distance_km']
        cost_from_h1 = distance_km * h1_data['transport_cost_per_km']
        cost_from_h2 = distance_km * h2_data['transport_cost_per_km']
        avg_cost = (cost_from_h1 + cost_from_h2) / 2
        
        # Estimate travel time
        estimated_time_minutes = (distance_km / 40) * 60
        
        result = f"💰 Travel Cost Analysis\n"
        result += f"{'=' * 60}\n\n"
        
        result += f"🏥 Route: {hospital_name1} ↔ {hospital_name2}\n"
        result += f"📏 Distance: {distance_km} km\n"
        result += f"⏱️  Estimated Travel Time: {estimated_time_minutes:.0f} minutes\n\n"
        
        result += f"💵 TRANSPORT COSTS:\n"
        result += f"  From {hospital_name1}:\n"
        result += f"    • Cost per km: ${h1_data['transport_cost_per_km']}\n"
        result += f"    • Total Cost: ${cost_from_h1:.2f}\n\n"
        
        result += f"  From {hospital_name2}:\n"
        result += f"    • Cost per km: ${h2_data['transport_cost_per_km']}\n"
        result += f"    • Total Cost: ${cost_from_h2:.2f}\n\n"
        
        result += f"  📊 Average Cost: ${avg_cost:.2f}\n\n"
        
        # Add ambulance availability
        result += f"🚑 AMBULANCE AVAILABILITY:\n"
        result += f"  {hospital_name1}: {h1_data['ambulances_available']}/{h1_data['ambulances_total']} available\n"
        result += f"  {hospital_name2}: {h2_data['ambulances_available']}/{h2_data['ambulances_total']} available\n\n"
        
        # Recommendation
        if cost_from_h1 < cost_from_h2:
            result += f"💡 RECOMMENDATION: Transport from {hospital_name1} is more cost-effective (${cost_from_h1:.2f} vs ${cost_from_h2:.2f})\n"
        elif cost_from_h2 < cost_from_h1:
            result += f"💡 RECOMMENDATION: Transport from {hospital_name2} is more cost-effective (${cost_from_h2:.2f} vs ${cost_from_h1:.2f})\n"
        else:
            result += f"💡 RECOMMENDATION: Both hospitals have equal transport costs (${avg_cost:.2f})\n"
        
        return result
    except Exception as e:
        return f"Error calculating travel cost: {str(e)}"
