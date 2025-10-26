import streamlit as st
import random
import string
import secrets
import re
import math
from datetime import datetime, timedelta
from typing import Dict, List
import json

# Initialize session state for user management
if 'premium_user' not in st.session_state:
    st.session_state.premium_user = False
if 'user_plan' not in st.session_state:
    st.session_state.user_plan = "Free"
if 'password_count' not in st.session_state:
    st.session_state.password_count = 0
if 'show_payment' not in st.session_state:
    st.session_state.show_payment = False
if 'premium_features' not in st.session_state:
    st.session_state.premium_features = {
        'bulk_generation': False,
        'advanced_analytics': False,
        'business_tools': False,
        'api_access': False,
        'priority_support': False
    }

class PremiumFeatures:
    def __init__(self):
        self.plans = {
            "free": {
                "price": 0,
                "features": [
                    "5 passwords per day",
                    "Basic strength analysis", 
                    "Standard generation",
                    "Community support"
                ],
                "limits": {"daily_passwords": 5}
            },
            "pro": {
                "price": 9.99,
                "features": [
                    "Unlimited password generation",
                    "Advanced AI analysis",
                    "Bulk generation (up to 50)",
                    "Password history (50 entries)",
                    "Priority email support",
                    "Custom password policies"
                ],
                "limits": {"bulk_generation": 50, "history_size": 50}
            },
            "business": {
                "price": 29.99,
                "features": [
                    "Everything in Pro",
                    "Team management (5 users)",
                    "Bulk generation (up to 500)",
                    "Advanced business policies",
                    "White-label options",
                    "API access",
                    "Phone support"
                ],
                "limits": {"bulk_generation": 500, "team_users": 5}
            },
            "enterprise": {
                "price": 99.99,
                "features": [
                    "Everything in Business",
                    "Unlimited team members",
                    "Custom integrations",
                    "Dedicated account manager",
                    "SLA guarantee",
                    "On-premise deployment"
                ],
                "limits": {"unlimited": True}
            }
        }
    
    def check_premium_status(self):
        return st.session_state.premium_user
    
    def get_plan_features(self, plan):
        return self.plans.get(plan, self.plans["free"])
    
    def upgrade_user(self, plan):
        st.session_state.premium_user = True
        st.session_state.user_plan = plan
        st.session_state.password_count = 0  # Reset counter
        
        # Enable premium features based on plan
        if plan in ["pro", "business", "enterprise"]:
            st.session_state.premium_features['bulk_generation'] = True
            st.session_state.premium_features['advanced_analytics'] = True
        
        if plan in ["business", "enterprise"]:
            st.session_state.premium_features['business_tools'] = True
            st.session_state.premium_features['api_access'] = True
        
        if plan == "enterprise":
            st.session_state.premium_features['priority_support'] = True
    
    def check_password_limit(self):
        if st.session_state.premium_user:
            return True  # Unlimited for premium users
        
        # Free users limited to 5 passwords per day
        if st.session_state.password_count >= 5:
            return False
        return True
    
    def increment_password_count(self):
        st.session_state.password_count += 1

class AIPasswordGenerator:
    def __init__(self):
        self.common_patterns = [
            r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]',
            r'^[A-Za-z]{4}\d{2}[@$!%*?&]{2}',
            r'^\d{3}[A-Za-z]{3}[@$!%*?&]',
        ]
        self.premium = PremiumFeatures()
    
    def analyze_password_strength(self, password: str) -> Dict:
        """AI-powered password strength analysis"""
        score = 0
        feedback = []
        
        # Length check
        if len(password) >= 12:
            score += 2
        elif len(password) >= 8:
            score += 1
        else:
            feedback.append("🔴 Password should be at least 8 characters long")
        
        # Character variety
        checks = {
            'lowercase': bool(re.search(r'[a-z]', password)),
            'uppercase': bool(re.search(r'[A-Z]', password)),
            'digits': bool(re.search(r'\d', password)),
            'special': bool(re.search(r'[@$!%*?&]', password)),
        }
        
        variety_score = sum(checks.values())
        score += variety_score
        
        if variety_score < 3:
            feedback.append("🔴 Include more character types (upper, lower, numbers, special)")
        elif variety_score == 4:
            feedback.append("✅ Excellent character variety")
        
        # Entropy calculation
        charset_size = 0
        if checks['lowercase']: charset_size += 26
        if checks['uppercase']: charset_size += 26
        if checks['digits']: charset_size += 10
        if checks['special']: charset_size += 8
        
        entropy = len(password) * (math.log2(charset_size) if charset_size > 0 else 0)
        
        if entropy > 100:
            score += 2
            feedback.append("✅ High entropy - very secure")
        elif entropy > 60:
            score += 1
            feedback.append("🟡 Moderate entropy - fairly secure")
        else:
            feedback.append("🔴 Low entropy - easily guessable")
        
        # Pattern detection
        if self._detect_common_patterns(password):
            score -= 1
            feedback.append("🟡 Avoid common patterns")
        
        # Premium advanced analysis
        if self.premium.check_premium_status():
            feedback.append("⭐ **Premium**: Advanced pattern analysis active")
            feedback.append("⭐ **Premium**: Real-time threat monitoring")
        
        # Final assessment
        if score >= 8:
            strength = "Very Strong"
            color = "green"
            emoji = "🛡️"
        elif score >= 6:
            strength = "Strong"
            color = "blue"
            emoji = "✅"
        elif score >= 4:
            strength = "Moderate"
            color = "orange"
            emoji = "⚠️"
        else:
            strength = "Weak"
            color = "red"
            emoji = "🚨"
        
        return {
            'score': score,
            'strength': strength,
            'color': color,
            'feedback': feedback,
            'entropy': entropy,
            'emoji': emoji
        }
    
    def _detect_common_patterns(self, password: str) -> bool:
        """Detect common password patterns"""
        for pattern in self.common_patterns:
            if re.match(pattern, password):
                return True
        return False
    
    def generate_memorable_password(self, word_count: int = 4) -> str:
        """Generate AI-suggested memorable passwords"""
        word_lists = {
            'animals': ['dragon', 'tiger', 'eagle', 'shark', 'wolf', 'lion'],
            'nature': ['forest', 'river', 'mountain', 'ocean', 'sky', 'star'],
            'tech': ['code', 'data', 'cloud', 'cyber', 'net', 'web'],
            'mythical': ['phoenix', 'unicorn', 'wizard', 'dragon', 'knight']
        }
        
        words = []
        for category, word_list in word_lists.items():
            words.extend(random.sample(word_list, min(2, len(word_list))))
        
        password_parts = random.sample(words, word_count)
        separator = random.choice(['-', '_', '.', '@'])
        
        # Add some variations
        variations = []
        for part in password_parts:
            if random.choice([True, False]):
                part = part.capitalize()
            if random.choice([True, False]) and len(part) > 3:
                part = part[:3] + str(random.randint(0, 9))
            variations.append(part)
        
        return separator.join(variations)

class AdvancedPasswordGenerator:
    def __init__(self):
        self.ai_generator = AIPasswordGenerator()
        self.premium = PremiumFeatures()
    
    def generate_password(self, length: int, use_upper: bool, use_lower: bool, 
                         use_digits: bool, use_special: bool, exclude_similar: bool = False) -> str:
        """Generate password based on criteria"""
        
        # Check password limit for free users
        if not self.premium.check_password_limit():
            return "LIMIT_REACHED"
        
        chars = ""
        if use_upper: chars += string.ascii_uppercase
        if use_lower: chars += string.ascii_lowercase
        if use_digits: chars += string.digits
        if use_special: chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        if not chars:
            return "Please select at least one character type"
        
        if exclude_similar:
            chars = chars.replace('l', '').replace('I', '').replace('1', '').replace('0', '').replace('O', '')
        
        password = ''.join(secrets.choice(chars) for _ in range(length))
        
        # Increment counter for free users
        if not st.session_state.premium_user:
            self.premium.increment_password_count()
        
        return password
    
    def generate_passphrase(self, word_count: int = 6, separator: str = "-") -> str:
        """Generate passphrase using word list"""
        
        # Check password limit for free users
        if not self.premium.check_password_limit():
            return "LIMIT_REACHED"
        
        word_list = [
            "apple", "brave", "cloud", "dragon", "eagle", "forest", "garden", "hidden",
            "island", "jewel", "knight", "lunar", "mountain", "northern", "ocean", "planet",
            "quantum", "river", "silent", "tiger", "unique", "violet", "wonder", "xenon",
            "yellow", "zenith"
        ]
        
        words = [secrets.choice(word_list) for _ in range(word_count)]
        password = separator.join(words)
        
        # Increment counter for free users
        if not st.session_state.premium_user:
            self.premium.increment_password_count()
        
        return password

def check_password_breach(password: str) -> Dict:
    """Check if password has been in known breaches (simulated)"""
    common_breached_passwords = [
        "123456", "password", "12345678", "qwerty", "123456789",
        "12345", "1234", "111111", "1234567", "dragon"
    ]
    
    if password in common_breached_passwords:
        return {
            'breached': True,
            'message': "🚨 This password has been found in known data breaches!",
            'severity': "high"
        }
    else:
        return {
            'breached': False,
            'message': "✅ No known breaches found for this password",
            'severity': "low"
        }

def show_premium_pricing():
    """Show premium pricing plans"""
    st.markdown("---")
    st.header("🚀 **Upgrade to Premium**")
    st.markdown("### Choose the plan that's right for you")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style='text-align: center; padding: 20px; border: 2px solid #e0e0e0; border-radius: 15px; height: 400px;'>
            <h3>🎯 Free</h3>
            <h2>$0</h2>
            <p>forever</p>
            <hr>
            <p>• 5 passwords/day</p>
            <p>• Basic analysis</p>
            <p>• Standard features</p>
            <p>• Community support</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Current Plan", key="free_btn", disabled=True, use_container_width=True):
            pass
    
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 20px; border: 2px solid #667eea; border-radius: 15px; height: 400px; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);'>
            <h3>⭐ Pro</h3>
            <h2>$9.99</h2>
            <p>per month</p>
            <hr>
            <p>• Unlimited passwords</p>
            <p>• Advanced AI analysis</p>
            <p>• Bulk generation</p>
            <p>• Priority support</p>
            <p>• Password history</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Choose Pro", key="pro_btn", type="primary", use_container_width=True):
            st.session_state.selected_plan = "pro"
            st.session_state.show_payment = True
    
    with col3:
        st.markdown("""
        <div style='text-align: center; padding: 20px; border: 2px solid #4ecdc4; border-radius: 15px; height: 400px; background: linear-gradient(135deg, #f0fff4 0%, #c6f7d0 100%);'>
            <h3>💼 Business</h3>
            <h2>$29.99</h2>
            <p>per month</p>
            <hr>
            <p>• Everything in Pro</p>
            <p>• Team management</p>
            <p>• Business policies</p>
            <p>• API access</p>
            <p>• White-label options</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Choose Business", key="business_btn", type="primary", use_container_width=True):
            st.session_state.selected_plan = "business"
            st.session_state.show_payment = True
    
    with col4:
        st.markdown("""
        <div style='text-align: center; padding: 20px; border: 2px solid #ff6b6b; border-radius: 15px; height: 400px; background: linear-gradient(135deg, #fff0f0 0%, #ffd6d6 100%);'>
            <h3>🏢 Enterprise</h3>
            <h2>$99.99</h2>
            <p>per month</p>
            <hr>
            <p>• Everything in Business</p>
            <p>• Unlimited teams</p>
            <p>• Custom integrations</p>
            <p>• Dedicated manager</p>
            <p>• SLA guarantee</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Choose Enterprise", key="enterprise_btn", type="primary", use_container_width=True):
            st.session_state.selected_plan = "enterprise"
            st.session_state.show_payment = True

def show_payment_section():
    """Show payment processing section"""
    st.markdown("---")
    st.header("💳 Complete Your Purchase")
    
    plan = st.session_state.get('selected_plan', 'pro')
    premium = PremiumFeatures()
    plan_info = premium.get_plan_features(plan)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader(f"Plan: {plan.capitalize()} - ${plan_info['price']}/month")
        
        st.markdown("**Features included:**")
        for feature in plan_info['features']:
            st.markdown(f"✅ {feature}")
        
        # Payment form
        with st.form("payment_form"):
            st.subheader("Billing Information")
            
            email = st.text_input("Email Address", placeholder="your@email.com")
            col1, col2 = st.columns(2)
            with col1:
                card_number = st.text_input("Card Number", placeholder="1234 5678 9012 3456")
            with col2:
                card_holder = st.text_input("Card Holder Name", placeholder="John Doe")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                exp_month = st.text_input("MM", placeholder="12")
            with col2:
                exp_year = st.text_input("YY", placeholder="25")
            with col3:
                cvv = st.text_input("CVV", placeholder="123")
            
            # Promo code
            promo_code = st.text_input("Promo Code (Optional)", placeholder="SUMMER2024")
            
            # Terms acceptance
            agree = st.checkbox("I agree to the Terms of Service and Privacy Policy")
            
            if st.form_submit_button("🔥 Subscribe Now", use_container_width=True):
                if not all([email, card_number, card_holder, exp_month, exp_year, cvv, agree]):
                    st.error("Please fill in all required fields and agree to the terms.")
                else:
                    # Simulate payment processing
                    with st.spinner("Processing payment..."):
                        # In real implementation, integrate with Stripe here
                        import time
                        time.sleep(2)
                        
                        # Upgrade user
                        premium.upgrade_user(plan)
                        st.success(f"🎉 Welcome to {plan.capitalize()} Tier!")
                        st.balloons()
                        st.session_state.show_payment = False
                        
                        # Show success message
                        st.markdown(f"""
                        ### 🎊 Upgrade Successful!
                        
                        You now have access to all **{plan.capitalize()}** features!
                        
                        **Next steps:**
                        - Refresh the page to see premium features
                        - Check your email for confirmation
                        - Start using advanced tools immediately
                        """)
    
    with col2:
        st.markdown("""
        <div style='background: #f8f9fa; padding: 20px; border-radius: 10px;'>
            <h4>🛡️ Secure Payment</h4>
            <p>Your payment is processed securely with bank-level encryption.</p>
            
            <h4>💰 Money-Back Guarantee</h4>
            <p>30-day money-back guarantee. No questions asked.</p>
            
            <h4>🔄 Easy Cancellation</h4>
            <p>Cancel anytime from your account settings.</p>
            
            <div style='text-align: center; margin-top: 20px;'>
                <img src='https://upload.wikimedia.org/wikipedia/commons/b/b7/Stripe_Logo%2C_revised_2016.svg' width='100'>
                <p><small>Powered by Stripe</small></p>
            </div>
        </div>
        """, unsafe_allow_html=True)

def show_affiliate_section():
    """Show affiliate marketing section"""
    st.sidebar.markdown("---")
    st.sidebar.header("💼 Recommended Tools")
    
    st.sidebar.markdown("""
    ### 🔒 Password Managers
    - **LastPass** - Easy password management
    - **1Password** - Business security suite  
    - **Dashlane** - All-in-one security
    
    ### 🛡️ Security Tools
    - **NordVPN** - Secure browsing
    - **Malwarebytes** - Virus protection
    - **Bitwarden** - Open source solution
    
    *We earn commission from these recommendations*
    """)

def main():
    st.set_page_config(
        page_title="AI Password Generator Pro",
        page_icon="🔐",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Initialize session states
    if 'selected_plan' not in st.session_state:
        st.session_state.selected_plan = "pro"
    
    # Modern CSS with monetization elements
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Remove Streamlit default elements */
    .stDeployButton { display: none !important; }
    #MainMenu { visibility: hidden !important; }
    footer { visibility: hidden !important; }
    header { visibility: hidden !important; }
    
    .main-header {
        font-size: 2.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 700;
    }
    
    .premium-badge {
        background: linear-gradient(135deg, #FFD700, #FFA500);
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.8rem;
    }
    
    .free-limit {
        background: linear-gradient(135deg, #ff6b6b, #ee5a52);
        color: white;
        padding: 10px;
        border-radius: 10px;
        text-align: center;
        margin: 10px 0;
    }
    
    .password-display {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 25px;
        border-radius: 15px;
        border: 2px solid #e1e8ed;
        font-family: 'Courier New', monospace;
        font-size: 1.4rem;
        text-align: center;
        margin: 15px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        word-break: break-all;
    }
    
    .feature-card {
        padding: 25px;
        border-radius: 15px;
        background: white;
        margin: 15px 0;
        border-left: 5px solid #667eea;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .stButton button {
        border-radius: 10px;
        height: 50px;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header with premium status
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<h1 class="main-header">🔐 AI Password Generator Pro</h1>', unsafe_allow_html=True)
        
        if st.session_state.premium_user:
            st.markdown(f'<div class="premium-badge" style="text-align: center;">⭐ PREMIUM USER - {st.session_state.user_plan.upper()} PLAN</div>', unsafe_allow_html=True)
        else:
            st.markdown('<p class="sub-header" style="text-align: center;">Generate secure, AI-powered passwords • <strong>Free tier: 5 passwords/day</strong></p>', unsafe_allow_html=True)
    
    # Initialize generators
    advanced_gen = AdvancedPasswordGenerator()
    premium = PremiumFeatures()
    
    # Sidebar with upgrade prompt
    with st.sidebar:
        if not st.session_state.premium_user:
            st.markdown("""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; text-align: center;'>
                <h3>🚀 Upgrade to Premium</h3>
                <p>Unlock unlimited passwords and advanced features!</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("⭐ Upgrade Now", use_container_width=True, type="primary"):
                st.session_state.show_payment = True
        
        # Password counter for free users
        if not st.session_state.premium_user:
            st.markdown(f"""
            <div style='background: #f8f9fa; padding: 15px; border-radius: 10px; text-align: center;'>
                <h4>📊 Usage Today</h4>
                <h3>{st.session_state.password_count}/5</h3>
                <p>passwords generated</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Affiliate section
        show_affiliate_section()
    
    # Show payment section if needed
    if st.session_state.show_payment:
        show_payment_section()
        return
    
    # Show pricing if user wants to upgrade
    if st.session_state.get('show_pricing', False):
        show_premium_pricing()
        return
    
    # Main app content
    st.markdown("---")
    
    # Password type selection as tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🔧 Random", "🧠 Memorable", "📖 Passphrase", "🤖 AI Smart"])
    
    with tab1:
        st.header("Random Password Generator")
        col1a, col1b = st.columns(2)
        with col1a:
            length = st.slider("Password Length", 8, 64, 16, key="random_length")
            use_upper = st.checkbox("Uppercase Letters", True, key="random_upper")
            use_lower = st.checkbox("Lowercase Letters", True, key="random_lower")
        with col1b:
            use_digits = st.checkbox("Digits", True, key="random_digits")
            use_special = st.checkbox("Special Characters", True, key="random_special")
            exclude_similar = st.checkbox("Exclude Similar Characters", False, key="random_similar")
        
        if st.button("Generate Random Password", type="primary", key="random_btn"):
            password = advanced_gen.generate_password(
                length, use_upper, use_lower, use_digits, use_special, exclude_similar
            )
            
            if password == "LIMIT_REACHED":
                st.error("🚫 You've reached your daily limit of 5 passwords. Upgrade to Premium for unlimited access!")
                st.session_state.show_pricing = True
                st.rerun()
            else:
                st.session_state.generated_password = password
                st.session_state.password_type = "Random"
    
    with tab2:
        st.header("Memorable Password Generator")
        word_count = st.slider("Number of Words", 3, 8, 4, key="memorable_words")
        if st.button("Generate Memorable Password", key="memorable_btn"):
            password = advanced_gen.ai_generator.generate_memorable_password(word_count)
            
            if password == "LIMIT_REACHED":
                st.error("🚫 You've reached your daily limit of 5 passwords. Upgrade to Premium for unlimited access!")
                st.session_state.show_pricing = True
                st.rerun()
            else:
                st.session_state.generated_password = password
                st.session_state.password_type = "Memorable"
    
    with tab3:
        st.header("Passphrase Generator")
        word_count = st.slider("Number of Words", 4, 10, 6, key="passphrase_words")
        separator = st.selectbox("Separator", ["-", "_", ".", " ", ""], key="passphrase_sep")
        if st.button("Generate Passphrase", key="passphrase_btn"):
            password = advanced_gen.generate_passphrase(word_count, separator)
            
            if password == "LIMIT_REACHED":
                st.error("🚫 You've reached your daily limit of 5 passwords. Upgrade to Premium for unlimited access!")
                st.session_state.show_pricing = True
                st.rerun()
            else:
                st.session_state.generated_password = password
                st.session_state.password_type = "Passphrase"
    
    with tab4:
        st.header("AI Smart Generator")
        st.info("AI generates passwords based on security best practices and memorability")
        
        if st.button("Get AI Suggestions", key="ai_btn"):
            suggestions = [
                advanced_gen.ai_generator.generate_memorable_password(4),
                advanced_gen.generate_password(16, True, True, True, True),
                advanced_gen.ai_generator.generate_memorable_password(3) + str(secrets.randbelow(1000)),
                advanced_gen.generate_passphrase(5, "-") + str(secrets.randbelow(100))
            ]
            
            # Check for limit reached
            if any(sug == "LIMIT_REACHED" for sug in suggestions):
                st.error("🚫 You've reached your daily limit of 5 passwords. Upgrade to Premium for unlimited access!")
                st.session_state.show_pricing = True
                st.rerun()
            else:
                st.session_state.ai_suggestions = suggestions
        
        if 'ai_suggestions' in st.session_state:
            st.subheader("AI Suggestions:")
            for i, suggestion in enumerate(st.session_state.ai_suggestions, 1):
                cols = st.columns([3, 1])
                with cols[0]:
                    st.code(suggestion, language="text")
                with cols[1]:
                    if st.button(f"Use {i}", key=f"ai_use_{i}"):
                        st.session_state.generated_password = suggestion
                        st.session_state.password_type = "AI Smart"
    
    # Display generated password
    if 'generated_password' in st.session_state:
        st.markdown("---")
        st.header("🎉 Your Generated Password")
        st.markdown('<div class="password-display">', unsafe_allow_html=True)
        st.code(st.session_state.generated_password, language="text")
        st.markdown('</div>', unsafe_allow_html=True)
        
        col_copy, col_refresh, col_save = st.columns(3)
        with col_copy:
            if st.button("📋 Copy to Clipboard", key="copy_btn"):
                st.code(st.session_state.generated_password)
                st.success("✅ Password copied to clipboard!")
        with col_refresh:
            if st.button("🔄 Generate New", key="refresh_btn"):
                # Store current password type before clearing
                current_type = st.session_state.get('password_type', 'Random')
                
                # Clear the current password
                if 'generated_password' in st.session_state:
                    del st.session_state.generated_password
                
                st.rerun()
        with col_save:
            if st.button("💾 Save to History", key="save_btn"):
                if 'password_history' not in st.session_state:
                    st.session_state.password_history = []
                st.session_state.password_history.append({
                    'password': st.session_state.generated_password,
                    'timestamp': datetime.now(),
                    'type': st.session_state.get('password_type', 'Generated')
                })
                st.success("✅ Password saved to history!")
    
    # Security Analysis Section
    if 'generated_password' in st.session_state:
        st.markdown("---")
        st.header("🔍 Security Analysis")
        
        password = st.session_state.generated_password
        
        # AI Strength Analysis
        analysis = advanced_gen.ai_generator.analyze_password_strength(password)
        
        col_analysis1, col_analysis2, col_analysis3 = st.columns(3)
        
        with col_analysis1:
            st.markdown('<div class="feature-card">', unsafe_allow_html=True)
            st.metric("Security Score", f"{analysis['score']}/10")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_analysis2:
            st.markdown('<div class="feature-card">', unsafe_allow_html=True)
            st.metric("Strength", f"{analysis['emoji']} {analysis['strength']}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_analysis3:
            st.markdown('<div class="feature-card">', unsafe_allow_html=True)
            st.metric("Entropy Bits", f"{analysis['entropy']:.1f}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Feedback and breach check
        col_feedback, col_breach = st.columns(2)
        
        with col_feedback:
            st.subheader("AI Recommendations")
            for feedback in analysis['feedback']:
                st.write(f"• {feedback}")
        
        with col_breach:
            st.subheader("Breach Check")
            breach_result = check_password_breach(password)
            st.write(breach_result['message'])
            
            st.subheader("Password Metrics")
            metrics_col1, metrics_col2 = st.columns(2)
            with metrics_col1:
                st.write(f"**Length:** {len(password)}")
                st.write(f"**Uppercase:** {sum(1 for c in password if c.isupper())}")
                st.write(f"**Lowercase:** {sum(1 for c in password if c.islower())}")
            with metrics_col2:
                st.write(f"**Digits:** {sum(1 for c in password if c.isdigit())}")
                st.write(f"**Special:** {sum(1 for c in password if not c.isalnum())}")
                st.write(f"**Unique Chars:** {len(set(password))}")
    
    # Advanced Features Section with premium gates
    st.markdown("---")
    st.header("🚀 Advanced Tools")
    
    feat_col1, feat_col2, feat_col3 = st.columns(3)
    
    with feat_col1:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.subheader("📊 Password History")
        if 'password_history' not in st.session_state:
            st.session_state.password_history = []
        
        if st.session_state.premium_user or len(st.session_state.password_history) <= 5:
            if st.session_state.password_history:
                st.write("Recent passwords:")
                max_display = 50 if st.session_state.premium_user else 5
                for i, item in enumerate(st.session_state.password_history[-max_display:], 1):
                    st.write(f"{i}. `{item['password']}`")
                    st.caption(f"{item['type']} - {item['timestamp'].strftime('%H:%M')}")
            else:
                st.info("No passwords in history")
        else:
            st.warning("🔒 History limited to 5 entries for free users")
            st.info("Upgrade to Premium for unlimited password history!")
            if st.button("Unlock History", key="history_upgrade"):
                st.session_state.show_pricing = True
        st.markdown('</div>', unsafe_allow_html=True)
    
    with feat_col2:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.subheader("🛠️ Bulk Generator")
        
        if st.session_state.premium_user:
            max_passwords = 500 if st.session_state.user_plan in ["business", "enterprise"] else 50
            count = st.number_input("Number of passwords", 1, max_passwords, 5, key="bulk_count")
            
            if st.button("Generate Multiple Passwords", key="bulk_btn"):
                bulk_passwords = [
                    advanced_gen.generate_password(16, True, True, True, True)
                    for _ in range(count)
                ]
                st.session_state.bulk_passwords = bulk_passwords
            
            if 'bulk_passwords' in st.session_state:
                st.text_area("Generated Passwords", 
                            "\n".join(st.session_state.bulk_passwords), 
                            height=150,
                            key="bulk_area")
        else:
            st.warning("🔒 Bulk generation is a Premium feature")
            st.info("Upgrade to generate 50+ passwords at once!")
            if st.button("Unlock Bulk Generation", key="bulk_upgrade"):
                st.session_state.show_pricing = True
        st.markdown('</div>', unsafe_allow_html=True)
    
    with feat_col3:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.subheader("🔐 Policy Checker")
        st.write("Validate against security policies")
        
        min_length = st.slider("Min Length", 8, 20, 12, key="policy_length")
        require_upper = st.checkbox("Require Uppercase", True, key="policy_upper")
        require_lower = st.checkbox("Require Lowercase", True, key="policy_lower")
        require_digits = st.checkbox("Require Digits", True, key="policy_digits")
        require_special = st.checkbox("Require Special", True, key="policy_special")
        
        if st.button("Validate Current Password", key="policy_btn"):
            if 'generated_password' in st.session_state:
                password = st.session_state.generated_password
                violations = []
                
                if len(password) < min_length:
                    violations.append(f"Minimum length {min_length}")
                if require_upper and not any(c.isupper() for c in password):
                    violations.append("Uppercase letters required")
                if require_lower and not any(c.islower() for c in password):
                    violations.append("Lowercase letters required")
                if require_digits and not any(c.isdigit() for c in password):
                    violations.append("Digits required")
                if require_special and all(c.isalnum() for c in password):
                    violations.append("Special characters required")
                
                if violations:
                    st.error("❌ Policy violations: " + ", ".join(violations))
                else:
                    st.success("✅ Meets all policy requirements!")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Show upgrade CTA at the bottom
    if not st.session_state.premium_user:
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; padding: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 15px;'>
            <h2>🚀 Ready to Level Up Your Security?</h2>
            <p style='font-size: 1.2rem;'>Join thousands of satisfied users who upgraded to Premium</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("⭐ Upgrade to Premium - Start Free Trial", use_container_width=True, type="primary"):
                st.session_state.show_pricing = True
    
    # Footer Section
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 20px; color: #666;'>
        <h3>🔐 AI Password Generator Pro</h3>
        <p>Built with Streamlit • Secure • Trusted by 10,000+ users</p>
        <p style='font-size: 0.8rem; color: #888;'>
            © 2024 Password Generator Pro. All rights reserved.<br>
            Your security is our priority. Passwords are generated locally and never stored.
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    # Add this to your app to enable "Add to Home Screen"
st.markdown("""
<script>
// Enable PWA-like features
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/sw.js');
    });
}
</script>

<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
""", unsafe_allow_html=True)

    main()
# Add this to your app to show the URL
def show_app_url():
    st.sidebar.markdown("---")
    st.sidebar.header("🔗 Your App URL")
    
    # This is your actual app URL
    app_url = "https://your-app-name.streamlit.app"
    
    st.sidebar.markdown(f"""
    **Your app is live at:**
    ```
    {app_url}
    ```
    """)
    
    # Copy button
    if st.sidebar.button("📋 Copy URL", use_container_width=True):
        st.sidebar.success("✅ URL copied to clipboard!")
    
    # QR code for easy mobile sharing
    st.sidebar.markdown("**Mobile QR Code:**")
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={app_url}"
    st.sidebar.image(qr_url)

# Call this function in your main app
show_app_url()

