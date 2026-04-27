# core/analysis.py

def analyze_damages(detections: list, config: dict) -> list:
    """Assigns severity and zone to each damage."""
    processed_damages = []
    severity_map = config['grading']['severity_map']
    
    for det in detections:
        confidence = det['confidence']
        severity = "minor"
        if confidence >= severity_map['critical']: severity = "critical"
        elif confidence >= severity_map['major']: severity = "major"
        
        det['severity'] = severity
        det['zone'] = "side" # Placeholder; advanced logic would determine this
        processed_damages.append(det)
        
    return processed_damages

def grade_container_condition(damages: list, config: dict) -> str:
    """Determines the overall container condition based on the worst damage."""
    if not damages:
        return "Good"
    
    condition_map = config['grading']['condition_map']
    severities = {d['severity'] for d in damages}
    
    if 'critical' in severities: return condition_map['critical']
    if 'major' in severities: return condition_map['major']
    return condition_map['minor']

def estimate_repair_cost(damages: list, config: dict) -> (list, float):
    """Calculates repair costs for each damage item in INR."""
    cost_table = config['repair_costs_inr']
    total_cost = 0.0
    
    for d in damages:
        cost_info = cost_table.get(d['type'], {})
        cost = cost_info.get(d['severity'], 0)
        d['estimated_cost'] = cost
        total_cost += cost
        
    return damages, total_cost

def determine_discard_status(damages: list, condition: str) -> dict:
    """Determines if container should be discarded based on damage severity.
    
    Returns:
        dict: {
            'should_discard': bool,
            'reason': str,
            'reusable': bool
        }
    """
    # Count critical damages
    critical_damages = [d for d in damages if d.get('severity') == 'critical']
    
    # Discard criteria
    should_discard = False
    reason = "Container is reusable"
    reusable = True
    
    # Check for multiple critical damages
    if len(critical_damages) >= 3:
        should_discard = True
        reason = "Multiple critical damages detected - container structurally compromised"
        reusable = False
    # Check for specific critical damage types
    elif any(d.get('type') in ['bent_frame', 'deformation', 'hole'] and d.get('severity') == 'critical' 
             for d in damages):
        should_discard = True
        reason = "Critical structural damage - container unsafe for future use"
        reusable = False
    # Check overall condition
    elif condition in ['Critical', 'Critical Repair']:
        should_discard = True
        reason = "Overall condition critical - repair cost exceeds container value"
        reusable = False
    
    return {
        'should_discard': should_discard,
        'reason': reason,
        'reusable': reusable
    }