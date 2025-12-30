/**
 * Handles location context selection and cascading dropdowns
 */
const LOCATION_CONFIG = {
    "India": {
        "Andhra Pradesh": ["Visakhapatnam", "Vijayawada", "Guntur", "Nellore", "Kurnool"],
        "Arunachal Pradesh": ["Itanagar", "Tawang", "Ziro", "Pasighat"],
        "Assam": ["Guwahati", "Dibrugarh", "Silchar", "Jorhat"],
        "Bihar": ["Patna", "Gaya", "Bhagalpur", "Muzaffarpur"],
        "Chhattisgarh": ["Raipur", "Bhilai", "Bilaspur", "Korba"],
        "Goa": ["Panaji", "Margao", "Vasco da Gama", "Mapusa"],
        "Gujarat": ["Ahmedabad", "Surat", "Vadodara", "Rajkot"],
        "Haryana": ["Gurugram", "Faridabad", "Panipat", "Ambala"],
        "Himachal Pradesh": ["Shimla", "Manali", "Dharamshala", "Solan"],
        "Jharkhand": ["Ranchi", "Jamshedpur", "Dhanbad", "Bokaro"],
        "Karnataka": ["Bengaluru", "Mysuru", "Hubballi", "Mangaluru"],
        "Kerala": ["Thiruvananthapuram", "Kochi", "Kozhikode", "Thrissur"],
        "Madhya Pradesh": ["Indore", "Bhopal", "Jabalpur", "Gwalior"],
        "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Thane", "Nashik"],
        "Manipur": ["Imphal", "Thoubal", "Bishnupur"],
        "Meghalaya": ["Shillong", "Tura", "Jowai"],
        "Mizoram": ["Aizawl", "Lunglei", "Champhai"],
        "Nagaland": ["Kohima", "Dimapur", "Mokokchung"],
        "Odisha": ["Bhubaneswar", "Cuttack", "Rourkela", "Puri"],
        "Punjab": ["Ludhiana", "Amritsar", "Jalandhar", "Patiala"],
        "Rajasthan": ["Jaipur", "Jodhpur", "Udaipur", "Ajmer", "Bikaner"],
        "Sikkim": ["Gangtok", "Namchi", "Geyzing"],
        "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Tiruchirappalli"],
        "Telangana": ["Hyderabad", "Warangal", "Nizamabad", "Khammam"],
        "Tripura": ["Agartala", "Udaipur", "Dharmanagar"],
        "Uttar Pradesh": ["Lucknow", "Kanpur", "Varanasi", "Agra", "Prayagraj"],
        "Uttarakhand": ["Dehradun", "Haridwar", "Roorkee", "Haldwani"],
        "West Bengal": ["Kolkata", "Howrah", "Durgapur", "Siliguri"]
    }
};

class LocationManager {
    constructor() {
        this.countrySelect = document.getElementById('countrySelect');
        this.stateSelect = document.getElementById('stateSelect');
        this.citySelect = document.getElementById('citySelect');
        this.notice = document.getElementById('locationNotice');

        this.currentCountry = "India";
        this.currentState = "Uttar Pradesh";
        this.currentCity = "Agra";

        this.init();
    }

    init() {
        this.populateStates();
        this.stateSelect.value = this.currentState;
        this.populateCities();
        this.citySelect.value = this.currentCity;

        this.bindEvents();
    }

    bindEvents() {
        this.stateSelect.addEventListener('change', (e) => {
            this.currentState = e.target.value;
            this.populateCities();
            this.updateContext();
        });

        this.citySelect.addEventListener('change', (e) => {
            this.currentCity = e.target.value;
            this.updateContext();
        });
    }

    populateStates() {
        const states = Object.keys(LOCATION_CONFIG[this.currentCountry]);
        this.stateSelect.innerHTML = states.map(s => `<option value="${s}">${s}</option>`).join('');
    }

    populateCities() {
        if (!this.currentState) {
            this.citySelect.innerHTML = '<option value="">Select City</option>';
            return;
        }

        const cities = LOCATION_CONFIG[this.currentCountry][this.currentState];
        this.citySelect.innerHTML = cities.map(c => `<option value="${c}">${c}</option>`).join('');
        this.currentCity = cities[0];
    }

    updateContext() {
        if (this.currentCity) {
            this.notice.classList.remove('hidden');
        } else {
            this.notice.classList.add('hidden');
        }
    }

    getContext() {
        return {
            country: this.currentCountry,
            state: this.currentState,
            city: this.currentCity
        };
    }
}

const locationManager = new LocationManager();
window.locationManager = locationManager;
