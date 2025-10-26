import streamlit as st
import secrets
import string
import re
import numpy as np
from typing import List, Dict, Any, Optional
import json
import time
import hashlib
import pandas as pd
from datetime import datetime, timedelta
import base64

# Set page config
st.set_page_config(
    page_title="Password Generator Pro",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

class PasswordGenerator:
    """Enhanced password generator with multiple generation techniques"""
    
    def __init__(self):
        self.char_sets = {
            'lowercase': string.ascii_lowercase,
            'uppercase': string.ascii_uppercase,
            'digits': string.digits,
            'symbols': string.punctuation,
            'similar_chars': 'il1Lo0O',
            'ambiguous_chars': '{}[]()/\'"`~,;:.<>'
        }
    
    def generate_random_password(self, length: int = 16, use_lowercase: bool = True,
                               use_uppercase: bool = True, use_digits: bool = True,
                               use_symbols: bool = True, exclude_similar: bool = True,
                               exclude_ambiguous: bool = False) -> Optional[str]:
        """Generate a truly random password using secrets module"""
        try:
            if length < 4:
                st.error("Password length must be at least 4 characters")
                return None
            
            # Build character pool
            char_pool = ""
            if use_lowercase:
                char_pool += self.char_sets['lowercase']
            if use_uppercase:
                char_pool += self.char_sets['uppercase']
            if use_digits:
                char_pool += self.char_sets['digits']
            if use_symbols:
                char_pool += self.char_sets['symbols']
            
            if not char_pool:
                st.error("Please select at least one character type")
                return None
            
            # Remove similar characters if requested
            if exclude_similar:
                for char in self.char_sets['similar_chars']:
                    char_pool = char_pool.replace(char, '')
            
            # Remove ambiguous characters if requested
            if exclude_ambiguous:
                for char in self.char_sets['ambiguous_chars']:
                    char_pool = char_pool.replace(char, '')
            
            if not char_pool:
                st.error("Character pool is empty after exclusions")
                return None
            
            # Generate password ensuring at least one character from each selected type
            password_chars = []
            remaining_length = length
            
            # Add required characters
            if use_lowercase and self.char_sets['lowercase']:
                password_chars.append(secrets.choice(self.char_sets['lowercase']))
                remaining_length -= 1
            if use_uppercase and self.char_sets['uppercase']:
                password_chars.append(secrets.choice(self.char_sets['uppercase']))
                remaining_length -= 1
            if use_digits and self.char_sets['digits']:
                password_chars.append(secrets.choice(self.char_sets['digits']))
                remaining_length -= 1
            if use_symbols and self.char_sets['symbols']:
                password_chars.append(secrets.choice(self.char_sets['symbols']))
                remaining_length -= 1
            
            # Fill remaining length
            for _ in range(remaining_length):
                password_chars.append(secrets.choice(char_pool))
            
            # Shuffle the password
            secrets.SystemRandom().shuffle(password_chars)
            
            return ''.join(password_chars)
            
        except Exception as e:
            st.error(f"Error generating password: {str(e)}")
            return None

class AIPasswordGenerator:
    """AI-enhanced password analysis and generation"""
    
    def __init__(self):
        self.common_patterns = [
            r'12345678', r'password', r'qwerty', r'admin', r'welcome',
            r'123456789', r'111111', r'abc123', r'password1', r'1234567'
        ]
    
    def analyze_password_strength(self, password: Optional[str]) -> Dict[str, Any]:
        """Analyze password strength with comprehensive checks"""
        # First check if password is None or empty
        if password is None:
            return {
                "strength": "Very Weak",
                "score": 0,
                "feedback": ["Invalid password: Password is None"],
                "length_ok": False,
                "complexity_ok": False,
                "common_pattern_ok": False,
                "entropy": 0.0
            }
        
        if not isinstance(password, str) or len(password) == 0:
            return {
                "strength": "Very Weak",
                "score": 0,
                "feedback": ["Invalid password: Empty or invalid password"],
                "length_ok": False,
                "complexity_ok": False,
                "common_pattern_ok": False,
                "entropy": 0.0
            }

        try:
            score = 0
            feedback = []
            
            # Length check
            length_ok = len(password) >= 12
            if len(password) >= 16:
                score += 3
            elif len(password) >= 12:
                score += 2
            elif len(password) >= 8:
                score += 1
                feedback.append("Consider using a longer password (12+ characters)")
            else:
                feedback.append("Password is too short (minimum 8 characters recommended)")
            
            # Character variety
            has_lower = bool(re.search(r'[a-z]', password))
            has_upper = bool(re.search(r'[A-Z]', password))
            has_digit = bool(re.search(r'\d', password))
            has_symbol = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
            
            char_types = sum([has_lower, has_upper, has_digit, has_symbol])
            complexity_ok = char_types >= 3
            
            if char_types == 4:
                score += 3
            elif char_types == 3:
                score += 2
                feedback.append("Good character variety, but consider adding more symbol types")
            else:
                score += 1
                feedback.append("Add more character types (upper, lower, digits, symbols)")
            
            # Common pattern check
            common_pattern_ok = True
            for pattern in self.common_patterns:
                if pattern.lower() in password.lower():
                    score -= 2
                    common_pattern_ok = False
                    feedback.append(f"Avoid common patterns like '{pattern}'")
                    break
            
            # Entropy calculation
            pool_size = 0
            if has_lower: pool_size += 26
            if has_upper: pool_size += 26
            if has_digit: pool_size += 10
            if has_symbol: pool_size += 32
            
            if pool_size > 0:
                entropy = len(password) * (np.log2(pool_size))
            else:
                entropy = 0
            
            if entropy > 100:
                score += 3
            elif entropy > 80:
                score += 2
            elif entropy > 60:
                score += 1
            else:
                feedback.append("Password entropy is low, consider using more random characters")
            
            # Final strength assessment
            if score >= 8:
                strength = "Very Strong"
            elif score >= 6:
                strength = "Strong"
            elif score >= 4:
                strength = "Moderate"
            elif score >= 2:
                strength = "Weak"
            else:
                strength = "Very Weak"
            
            return {
                "strength": strength,
                "score": min(max(score, 0), 10),
                "feedback": feedback,
                "length_ok": length_ok,
                "complexity_ok": complexity_ok,
                "common_pattern_ok": common_pattern_ok,
                "entropy": round(entropy, 2)
            }
            
        except Exception as e:
            return {
                "strength": "Error",
                "score": 0,
                "feedback": [f"Error analyzing password: {str(e)}"],
                "length_ok": False,
                "complexity_ok": False,
                "common_pattern_ok": False,
                "entropy": 0.0
            }

class AdvancedPasswordGenerator:
    """Advanced password generation with multiple techniques"""
    
    def __init__(self):
        self.basic_gen = PasswordGenerator()
        self.ai_generator = AIPasswordGenerator()
        self.generation_history = []
    
    def generate_passphrase(self, word_count: int = 4, separator: str = "-",
                          capitalize: bool = True, add_number: bool = True) -> Optional[str]:
        """Generate a memorable passphrase"""
        try:
            # Common words list for passphrases
            words = [
                "apple", "brave", "cloud", "dragon", "eagle", "forest", "garden", "hammer",
                "island", "jupiter", "knight", "light", "mountain", "northern", "ocean",
                "planet", "quiet", "river", "sunset", "tiger", "unique", "victory", "water",
                "xray", "yellow", "zebra"
            ]
            
            if len(words) < word_count:
                st.error("Not enough words available for passphrase")
                return None
            
            selected_words = secrets.SystemRandom().sample(words, word_count)
            
            # Apply transformations
            if capitalize:
                selected_words = [word.capitalize() for word in selected_words]
            
            passphrase = separator.join(selected_words)
            
            # Add number if requested
            if add_number:
                passphrase += str(secrets.randbelow(90) + 10)  # Add 2-digit number
            
            return passphrase
            
        except Exception as e:
            st.error(f"Error generating passphrase: {str(e)}")
            return None
    
    def generate_pronounceable_password(self, length: int = 12) -> Optional[str]:
        """Generate a pronounceable password"""
        try:
            vowels = 'aeiou'
            consonants = 'bcdfghjklmnpqrstvwxyz'
            
            password = []
            for i in range(length):
                if i % 2 == 0:
                    password.append(secrets.choice(consonants))
                else:
                    password.append(secrets.choice(vowels))
            
            # Capitalize first letter
            if password:
                password[0] = password[0].upper()
            
            return ''.join(password)
            
        except Exception as e:
            st.error(f"Error generating pronounceable password: {str(e)}")
            return None

class PasswordManager:
    """Manage generated passwords and their metadata"""
    
    def __init__(self):
        self.passwords = {}
        if 'password_history' not in st.session_state:
            st.session_state.password_history = []
    
    def save_password(self, password: str, purpose: str = "", tags: List[str] = None) -> str:
        """Save a password with metadata and return its ID"""
        try:
            if password is None:
                return ""
                
            password_id = hashlib.md5(f"{password}{time.time()}".encode()).hexdigest()[:8]
            
            password_data = {
                'id': password_id,
                'password': password,
                'purpose': purpose,
                'tags': tags or [],
                'created_at': datetime.now().isoformat(),
                'strength': AIPasswordGenerator().analyze_password_strength(password)
            }
            
            self.passwords[password_id] = password_data
            st.session_state.password_history.append(password_data)
            
            # Keep only last 50 passwords
            if len(st.session_state.password_history) > 50:
                st.session_state.password_history = st.session_state.password_history[-50:]
            
            return password_id
            
        except Exception as e:
            st.error(f"Error saving password: {str(e)}")
            return ""
    
    def get_password_history(self) -> List[Dict[str, Any]]:
        """Get password generation history"""
        return st.session_state.password_history
    
    def clear_history(self):
        """Clear password history"""
        st.session_state.password_history = []
        self.passwords = {}

def init_session_state():
    """Initialize session state variables"""
    if 'generated_passwords' not in st.session_state:
        st.session_state.generated_passwords = []
    if 'password_manager' not in st.session_state:
        st.session_state.password_manager = PasswordManager()
    if 'advanced_gen' not in st.session_state:
        st.session_state.advanced_gen = AdvancedPasswordGenerator()

def display_password_strength(analysis: Dict[str, Any]):
    """Display password strength analysis"""
    strength_color = {
        "Very Strong": "green",
        "Strong": "lightgreen", 
        "Moderate": "orange",
        "Weak": "red",
        "Very Weak": "darkred",
        "Error": "gray"
    }
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Strength", analysis['strength'])
    
    with col2:
        st.metric("Score", f"{analysis['score']}/10")
    
    with col3:
        st.metric("Entropy", f"{analysis['entropy']:.1f}")
    
    with col4:
        # Strength indicator
        strength = analysis['strength']
        color = strength_color.get(strength, "gray")
        st.markdown(f"<div style='background-color: {color}; padding: 10px; border-radius: 5px; text-align: center; color: white;'>{strength}</div>", 
                   unsafe_allow_html=True)
    
    # Feedback
    if analysis['feedback']:
        with st.expander("Improvement Suggestions"):
            for suggestion in analysis['feedback']:
                st.write(f"• {suggestion}")

def render_basic_generator():
    """Render basic password generator interface"""
    st.header("🔐 Basic Password Generator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        length = st.slider("Password Length", min_value=8, max_value=50, value=16, key="basic_length")
        use_lowercase = st.checkbox("Lowercase (a-z)", value=True, key="basic_lower")
        use_uppercase = st.checkbox("Uppercase (A-Z)", value=True, key="basic_upper")
    
    with col2:
        use_digits = st.checkbox("Digits (0-9)", value=True, key="basic_digits")
        use_symbols = st.checkbox("Symbols (!@#$)", value=True, key="basic_symbols")
        exclude_similar = st.checkbox("Exclude Similar Characters (i,l,1,L,o,0,O)", value=True, key="basic_similar")
        exclude_ambiguous = st.checkbox("Exclude Ambiguous Symbols", value=False, key="basic_ambiguous")
    
    if st.button("Generate Password", key="basic_generate", type="primary"):
        with st.spinner("Generating secure password..."):
            password = st.session_state.advanced_gen.basic_gen.generate_random_password(
                length=length,
                use_lowercase=use_lowercase,
                use_uppercase=use_uppercase,
                use_digits=use_digits,
                use_symbols=use_symbols,
                exclude_similar=exclude_similar,
                exclude_ambiguous=exclude_ambiguous
            )
            
            if password:  # Only analyze if password is not None
                st.session_state.generated_passwords.append(password)
                analysis = st.session_state.advanced_gen.ai_generator.analyze_password_strength(password)
                
                # Display password
                st.subheader("Generated Password")
                st.code(password, language="text")
                
                # Display strength analysis
                display_password_strength(analysis)
                
                # Save to history
                st.session_state.password_manager.save_password(password, "Basic Generator")
            else:
                st.error("Failed to generate password. Please check your settings.")

def render_advanced_generator():
    """Render advanced password generator interface"""
    st.header("🚀 Advanced Password Generator")
    
    tab1, tab2 = st.tabs(["Passphrase Generator", "Pronounceable Password"])
    
    with tab1:
        st.subheader("Memorable Passphrase")
        
        col1, col2 = st.columns(2)
        
        with col1:
            word_count = st.slider("Number of Words", min_value=3, max_value=8, value=4, key="phrase_words")
            separator = st.selectbox("Separator", ["-", "_", ".", "", " "], key="phrase_separator")
        
        with col2:
            capitalize = st.checkbox("Capitalize Words", value=True, key="phrase_caps")
            add_number = st.checkbox("Add Random Number", value=True, key="phrase_number")
        
        if st.button("Generate Passphrase", key="phrase_generate", type="primary"):
            with st.spinner("Creating memorable passphrase..."):
                passphrase = st.session_state.advanced_gen.generate_passphrase(
                    word_count=word_count,
                    separator=separator,
                    capitalize=capitalize,
                    add_number=add_number
                )
                
                if passphrase:  # Only analyze if passphrase is not None
                    st.session_state.generated_passwords.append(passphrase)
                    analysis = st.session_state.advanced_gen.ai_generator.analyze_password_strength(passphrase)
                    
                    st.subheader("Generated Passphrase")
                    st.code(passphrase, language="text")
                    
                    display_password_strength(analysis)
                    
                    st.session_state.password_manager.save_password(passphrase, "Passphrase Generator")
                else:
                    st.error("Failed to generate passphrase. Please try again.")
    
    with tab2:
        st.subheader("Pronounceable Password")
        
        length = st.slider("Password Length", min_value=8, max_value=20, value=12, key="pronounce_length")
        
        if st.button("Generate Pronounceable Password", key="pronounce_generate", type="primary"):
            with st.spinner("Creating pronounceable password..."):
                password = st.session_state.advanced_gen.generate_pronounceable_password(length=length)
                
                if password:  # Only analyze if password is not None
                    st.session_state.generated_passwords.append(password)
                    analysis = st.session_state.advanced_gen.ai_generator.analyze_password_strength(password)
                    
                    st.subheader("Generated Password")
                    st.code(password, language="text")
                    
                    display_password_strength(analysis)
                    
                    st.session_state.password_manager.save_password(password, "Pronounceable Generator")
                else:
                    st.error("Failed to generate password. Please try again.")

def render_password_analyzer():
    """Render password analysis interface"""
    st.header("🔍 Password Analyzer")
    
    password_to_analyze = st.text_input("Enter password to analyze", type="password")
    
    if password_to_analyze:
        if len(password_to_analyze) == 0:
            st.warning("Please enter a password to analyze")
        else:
            analysis = st.session_state.advanced_gen.ai_generator.analyze_password_strength(password_to_analyze)
            
            st.subheader("Analysis Results")
            display_password_strength(analysis)
            
            # Additional security metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Length", len(password_to_analyze))
            
            with col2:
                char_types = sum([
                    bool(re.search(r'[a-z]', password_to_analyze)),
                    bool(re.search(r'[A-Z]', password_to_analyze)),
                    bool(re.search(r'\d', password_to_analyze)),
                    bool(re.search(r'[^a-zA-Z0-9]', password_to_analyze))
                ])
                st.metric("Character Types", char_types)
            
            with col3:
                # Estimate cracking time (simplified)
                entropy = analysis['entropy']
                if entropy > 80:
                    crack_time = "Centuries"
                elif entropy > 60:
                    crack_time = "Years"
                elif entropy > 40:
                    crack_time = "Months"
                elif entropy > 20:
                    crack_time = "Days"
                else:
                    crack_time = "Hours"
                st.metric("Estimated Crack Time", crack_time)

def render_password_manager():
    """Render password manager interface"""
    st.header("💼 Password Manager")
    
    history = st.session_state.password_manager.get_password_history()
    
    if not history:
        st.info("No passwords generated yet. Generate some passwords to see them here!")
        return
    
    # Filter and search
    col1, col2 = st.columns([2, 1])
    
    with col1:
        search_term = st.text_input("Search passwords by purpose")
    
    with col2:
        if st.button("Clear History", type="secondary"):
            st.session_state.password_manager.clear_history()
            st.rerun()
    
    # Display password history
    for i, pwd_data in enumerate(reversed(history[-20:])):  # Show last 20
        if search_term and search_term.lower() not in pwd_data.get('purpose', '').lower():
            continue
            
        with st.expander(f"Password {i+1} - {pwd_data.get('purpose', 'Unknown')} - {pwd_data['strength']['strength']}"):
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.code(pwd_data['password'], language="text")
                st.caption(f"Created: {pwd_data['created_at'][:16]}")
            
            with col2:
                strength = pwd_data['strength']['strength']
                score = pwd_data['strength']['score']
                st.metric("Strength", strength)
                st.metric("Score", f"{score}/10")
            
            with col3:
                if st.button("Copy", key=f"copy_{pwd_data['id']}"):
                    st.code(pwd_data['password'])
                    st.success("Password copied to clipboard!")
                
                if st.button("Delete", key=f"delete_{pwd_data['id']}"):
                    st.session_state.password_history = [
                        p for p in st.session_state.password_history 
                        if p['id'] != pwd_data['id']
                    ]
                    st.rerun()

def render_export_import():
    """Render export/import functionality"""
    st.header("📁 Export/Import Passwords")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Export Passwords")
        if st.button("Export as JSON", key="export_json"):
            history = st.session_state.password_manager.get_password_history()
            if history:
                # Remove actual passwords for security
                export_data = []
                for pwd in history:
                    export_data.append({
                        'purpose': pwd.get('purpose', ''),
                        'tags': pwd.get('tags', []),
                        'created_at': pwd.get('created_at', ''),
                        'strength': pwd.get('strength', {})
                    })
                
                json_str = json.dumps(export_data, indent=2)
                st.download_button(
                    label="Download JSON",
                    data=json_str,
                    file_name="password_export.json",
                    mime="application/json"
                )
            else:
                st.warning("No passwords to export")
    
    with col2:
        st.subheader("Security Notice")
        st.warning("""
        For security reasons, actual passwords are NOT included in exports.
        This export only contains metadata about your generated passwords.
        
        Always store passwords in a secure password manager!
        """)

def display_feature_badges():
    """Display feature badges in a Streamlit-compatible way"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(
            """
            <div style='
                background: linear-gradient(45deg, #667eea, #764ba2);
                padding: 0.5rem 1rem;
                border-radius: 25px;
                text-align: center;
                color: white;
                font-weight: bold;
                margin: 0.5rem 0;
            '>
                🎯 Free Tier Available
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            """
            <div style='
                background: linear-gradient(45deg, #f093fb, #f5576c);
                padding: 0.5rem 1rem;
                border-radius: 25px;
                text-align: center;
                color: white;
                font-weight: bold;
                margin: 0.5rem 0;
            '>
                🤖 AI-Powered Analysis
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            """
            <div style='
                background: linear-gradient(45deg, #4facfe, #00f2fe);
                padding: 0.5rem 1rem;
                border-radius: 25px;
                text-align: center;
                color: white;
                font-weight: bold;
                margin: 0.5rem 0;
            '>
                🔒 Military-Grade Security
            </div>
            """, 
            unsafe_allow_html=True
        )

def main():
    """Main application function"""
    # Initialize session state
    init_session_state()
    
    # Sidebar
    st.sidebar.title("🔒 Password Generator Pro")
    st.sidebar.markdown("---")
    
    # Navigation
    page = st.sidebar.radio(
        "Navigation",
        ["Basic Generator", "Advanced Generator", "Password Analyzer", "Password Manager", "Export/Import"]
    )
    
    # App info
    st.sidebar.markdown("---")
    st.sidebar.subheader("About")
    st.sidebar.info("""
    A secure password generator with multiple generation techniques, 
    strength analysis, and password management features.
    
    Uses cryptographically secure random number generation.
    """)
    
    # Main content area
    st.title("🔒 Password Generator Pro")
    st.markdown("Generate secure, random passwords with advanced analysis tools.")
    
    # Display feature badges
    display_feature_badges()
    
    # Render selected page
    if page == "Basic Generator":
        render_basic_generator()
    elif page == "Advanced Generator":
        render_advanced_generator()
    elif page == "Password Analyzer":
        render_password_analyzer()
    elif page == "Password Manager":
        render_password_manager()
    elif page == "Export/Import":
        render_export_import()

if __name__ == "__main__":
    main()
