"""Preference-aware recommendation function for healthcare resource allocation."""
from typing import Dict, List, Any, Optional


def get_personalized_recommendation(scenario: str, context_id: Optional[str] = None) -> str:
    """
    Generate personalized recommendations based on user preferences and scenario.
    
    Args:
        scenario: The resource allocation scenario (required)
        context_id: Optional session context ID for tracking preferences
        
    Returns:
        str: Personalized recommendation based on user preferences
    """
    try:
        # Get user preferences from session storage (using simplified state management)
        liked_recommendations = []
        disliked_recommendations = []
        if context_id:
            # Here you would implement session storage lookup based on context_id
            # For now using empty lists as defaults
            pass
        
        # Analyze preference patterns
        preference_analysis = analyze_user_preferences(liked_recommendations, disliked_recommendations)
        
        # Generate base recommendations for the scenario
        base_recommendations = generate_base_recommendations(scenario)
        
        # Adapt recommendations based on preferences
        adapted_recommendations = adapt_recommendations_to_preferences(
            base_recommendations, 
            preference_analysis
        )
        
        # Format response with learning context
        response = format_personalized_response(
            adapted_recommendations, 
            preference_analysis, 
            len(liked_recommendations), 
            len(disliked_recommendations)
        )
        
        return response
        
    except Exception as e:
        return f"Error generating personalized recommendation: {str(e)}"


def analyze_user_preferences(liked: List, disliked: List) -> Dict[str, Any]:
    """Analyze user preference patterns from feedback history."""
    
    # Initialize preference scores
    preferences = {
        'cost_efficiency': 0,
        'patient_coverage': 0,
        'fairness_equity': 0,
        'speed_urgency': 0,
        'resource_optimization': 0
    }
    
    # Keywords that indicate different preference types
    preference_keywords = {
        'cost_efficiency': ['cost', 'budget', 'efficient', 'economical', 'affordable', 'savings'],
        'patient_coverage': ['coverage', 'patients', 'access', 'reach', 'serve', 'capacity'],
        'fairness_equity': ['fair', 'equitable', 'equal', 'balanced', 'distribute', 'share'],
        'speed_urgency': ['urgent', 'quick', 'fast', 'immediate', 'emergency', 'rapid'],
        'resource_optimization': ['optimize', 'maximize', 'utilization', 'efficiency', 'allocation']
    }
    
    # Analyze liked recommendations
    for item in liked:
        recommendation_text = item.get('recommendation', '').lower()
        for pref_type, keywords in preference_keywords.items():
            for keyword in keywords:
                if keyword in recommendation_text:
                    preferences[pref_type] += 1
    
    # Analyze disliked recommendations (negative weight)
    for item in disliked:
        recommendation_text = item.get('recommendation', '').lower()
        for pref_type, keywords in preference_keywords.items():
            for keyword in keywords:
                if keyword in recommendation_text:
                    preferences[pref_type] -= 0.5
    
    # Determine dominant preference
    dominant_preference = max(preferences.keys(), key=lambda k: preferences[k])
    
    return {
        'scores': preferences,
        'dominant': dominant_preference,
        'total_feedback': len(liked) + len(disliked),
        'like_ratio': len(liked) / (len(liked) + len(disliked)) if (len(liked) + len(disliked)) > 0 else 0
    }


def generate_base_recommendations(scenario: str) -> List[Dict]:
    """Generate base recommendations for different scenarios."""
    
    recommendations = []
    
    if 'ventilator' in scenario.lower() or 'icu' in scenario.lower():
        recommendations = [
            {
                'type': 'cost_efficiency',
                'title': 'Cost-Effective Ventilator Redistribution',
                'description': 'Redistribute ventilators from hospitals with low utilization to high-demand facilities to minimize transport costs.',
                'priority': 'Medium',
                'impact': 'Reduces operational costs by 15-20%'
            },
            {
                'type': 'patient_coverage',
                'title': 'Maximum Patient Coverage Strategy',
                'description': 'Prioritize ventilator allocation to hospitals serving the largest patient populations and emergency cases.',
                'priority': 'High',
                'impact': 'Increases patient access by 25-30%'
            },
            {
                'type': 'fairness_equity',
                'title': 'Equitable Distribution Model',
                'description': 'Ensure fair ventilator distribution across all regions based on population density and medical need.',
                'priority': 'High',
                'impact': 'Ensures equal access across all demographics'
            }
        ]
    
    elif 'staff' in scenario.lower() or 'doctor' in scenario.lower() or 'nurse' in scenario.lower():
        recommendations = [
            {
                'type': 'cost_efficiency',
                'title': 'Optimized Staff Scheduling',
                'description': 'Implement dynamic staff allocation to reduce overtime costs while maintaining coverage.',
                'priority': 'Medium',
                'impact': 'Reduces staffing costs by 10-15%'
            },
            {
                'type': 'patient_coverage',
                'title': 'Patient-Centered Staffing',
                'description': 'Allocate staff based on patient acuity and volume to ensure optimal care delivery.',
                'priority': 'High',
                'impact': 'Improves patient outcomes by 20%'
            },
            {
                'type': 'fairness_equity',
                'title': 'Balanced Workload Distribution',
                'description': 'Ensure equitable staff distribution to prevent burnout and maintain quality care.',
                'priority': 'High',
                'impact': 'Reduces staff burnout by 30%'
            }
        ]
    
    else:
        # General resource allocation
        recommendations = [
            {
                'type': 'cost_efficiency',
                'title': 'Resource Cost Optimization',
                'description': 'Optimize resource allocation to minimize total system costs while meeting demand.',
                'priority': 'Medium',
                'impact': 'Reduces overall costs by 12-18%'
            },
            {
                'type': 'patient_coverage',
                'title': 'Coverage Maximization Strategy',
                'description': 'Allocate resources to maximize patient coverage and accessibility across the network.',
                'priority': 'High',
                'impact': 'Increases service coverage by 22%'
            },
            {
                'type': 'resource_optimization',
                'title': 'Utilization Optimization',
                'description': 'Balance resource utilization across facilities to maximize efficiency and minimize waste.',
                'priority': 'Medium',
                'impact': 'Improves utilization by 25%'
            }
        ]
    
    return recommendations


def adapt_recommendations_to_preferences(recommendations: List[Dict], preferences: Dict) -> List[Dict]:
    """Adapt recommendations based on user preferences."""
    
    dominant_pref = preferences['dominant']
    
    # Sort recommendations by preference alignment
    def preference_score(rec):
        if rec['type'] == dominant_pref:
            return 3  # Highest priority for dominant preference
        elif preferences['scores'].get(rec['type'], 0) > 0:
            return 2  # Medium priority for liked types
        elif preferences['scores'].get(rec['type'], 0) < 0:
            return 0  # Lowest priority for disliked types
        else:
            return 1  # Default priority
    
    # Sort by preference alignment
    adapted = sorted(recommendations, key=preference_score, reverse=True)
    
    # Add preference reasoning to top recommendation
    if adapted and preferences['total_feedback'] > 0:
        adapted[0]['preference_note'] = f"Prioritized based on your preference for {dominant_pref.replace('_', ' ')}"
    
    return adapted


def format_personalized_response(recommendations: List[Dict], preferences: Dict, 
                                like_count: int, dislike_count: int) -> str:
    """Format the personalized recommendation response."""
    
    response = "🎯 **Personalized Resource Allocation Recommendations**\n\n"
    
    # Add learning context if user has provided feedback
    if preferences['total_feedback'] > 0:
        dominant = preferences['dominant'].replace('_', ' ').title()
        response += f"📊 **Learning from your preferences** (Based on {like_count} likes, {dislike_count} dislikes)\n"
        response += f"Your primary focus appears to be: **{dominant}**\n\n"
    
    # Add top recommendations
    for i, rec in enumerate(recommendations[:3], 1):
        response += f"**{i}. {rec['title']}** ({rec['priority']} Priority)\n"
        response += f"   {rec['description']}\n"
        response += f"   💡 Impact: {rec['impact']}\n"
        
        if 'preference_note' in rec:
            response += f"   🎯 {rec['preference_note']}\n"
        
        response += "\n"
    
    # Add adaptation note
    if preferences['total_feedback'] > 0:
        response += "🔄 **Adaptive Learning**: These recommendations are personalized based on your previous feedback. "
        response += "Continue providing feedback to help me learn your preferences better!\n\n"
    else:
        response += "💡 **New User**: Provide feedback on recommendations to help me learn your preferences!\n\n"
    
    response += "👍 Like this recommendation? 👎 Or would you prefer a different approach?"
    
    return response