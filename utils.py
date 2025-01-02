# Input validation utilities

def validate_user_input(num_days: str, country: str) -> bool:
    
    try:
        if not country.strip() or int(num_days) <= 0:
            return False
        return True
    
    except ValueError:
        return False