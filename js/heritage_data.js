const HERITAGE_DATA = [
    {
        state: "Andhra Pradesh",
        cities: [
            {
                city: "Tirupati",
                monument: "Tirumala Temple",
                image: "images/andhrapradesh/tirupati.jpg",
                lat: 13.6833,
                lng: 79.3474



            },
            {
                city: "Amaravati",
                monument: "Amaravati Stupa",
                image: "images/andhrapradesh/amaravati.jpg",

                lat: 16.5745,
                lng: 80.3575
            }
        ]
    },
    {
        state: "Arunachal Pradesh",
        cities: [
            {
                city: "Tawang",
                monument: "Tawang Monastery",
                image: "images/arunachal/tawang.jpg",
                lat: 27.5861,
                lng: 91.8656
            }
        ]
    },
    {
        state: "Assam",
        cities: [
            {
                city: "Guwahati",
                monument: "Kamakhya Temple",
                image: "images/assam/guwahati.jpg",
                lat: 26.1158,
                lng: 91.7086
            },
            {
                city: "Sivasagar",
                monument: "Rang Ghar",
                image: "images/assam/sivasagar.jpg",
                lat: 26.9826,
                lng: 94.6311
            }
        ]
    },
    {
        state: "Bihar",
        cities: [
            {
                city: "Bodh Gaya",
                monument: "Mahabodhi Temple",
                image: "images/bihar/bodhgaya.jpg",
                lat: 24.6961,
                lng: 84.9913
            },
            {
                city: "Nalanda",
                monument: "Nalanda University Ruins",
                image: "images/bihar/nalanda.jpg",
                lat: 25.1328,
                lng: 85.4522
            }
        ]
    },
    {
        state: "Chhattisgarh",
        cities: [
            {
                city: "Sirpur",
                monument: "Laxman Temple",
                image: "images/chhattisgarh/sirpur.jpg",
                lat: 21.3435,
                lng: 82.1764
            }
        ]
    },
    {
        state: "Goa",
        cities: [
            {
                city: "Old Goa",
                monument: "Basilica of Bom Jesus",
                image: "images/goa/oldgoa.jpg",
                lat: 15.5009,
                lng: 73.9116
            }
        ]
    },
    {
        state: "Gujarat",
        cities: [
            {
                city: "Ahmedabad",
                monument: "Sabarmati Ashram",
                image: "images/gujarat/ahmedabad.jpg",
                lat: 23.0225,
                lng: 72.5714
            },
            {
                city: "Modhera",
                monument: "Sun Temple",
                image: "images/gujarat/modhera.jpg",
                lat: 23.5835,
                lng: 72.1333
            }
        ]
    },
    {
        state: "Haryana",
        cities: [
            {
                city: "Kurukshetra",
                monument: "Brahma Sarovar",
                image: "images/haryana/kurukshetra.jpg",
                lat: 29.9691,
                lng: 76.8352
            }
        ]
    },
    {
        state: "Himachal Pradesh",
        cities: [
            {
                city: "Dharamshala",
                monument: "Tsuglagkhang Complex",
                image: "images/himachal/dharamshala.jpg",
                lat: 32.2190,
                lng: 76.3234
            },
            {
                city: "Chamba",
                monument: "Lakshmi Narayan Temple",
                image: "images/himachalpradesh/chamba.jpg",
                lat: 32.5534,
                lng: 76.1258
            }
        ]
    },
    {
        state: "Jharkhand",
        cities: [
            {
                city: "Deoghar",
                monument: "Baidyanath Dham",
                image: "images/jharkhand/deoghar.jpg",
                lat: 24.4820,
                lng: 86.7001
            }
        ]
    },
    {
        state: "Karnataka",
        cities: [
            {
                city: "Hampi",
                monument: "Group of Monuments",
                image: "images/karnataka/hampi.jpg",
                lat: 15.3350,
                lng: 76.4600
            },
            {
                city: "Mysuru",
                monument: "Mysore Palace",
                image: "images/karnataka/mysuru.jpg",
                lat: 12.3051,
                lng: 76.6551
            }
        ]
    },
    {
        state: "Kerala",
        cities: [
            {
                city: "Kochi",
                monument: "Mattancherry Palace",
                image: "images/kerala/kochi.jpg",
                lat: 9.9592,
                lng: 76.2589
            }
        ]
    },
    {
        state: "Madhya Pradesh",
        cities: [
            {
                city: "Khajuraho",
                monument: "Khajuraho Temples",
                image: "images/madhyapradesh/khajuraho.jpg",
                lat: 24.8518,
                lng: 79.9199
            },
            {
                city: "Sanchi",
                monument: "Sanchi Stupa",
                image: "images/madhyapradesh/sanchi.jpg",
                lat: 23.4754,
                lng: 77.7397
            }
        ]
    },
    {
        state: "Maharashtra",
        cities: [
            {
                city: "Aurangabad",
                monument: "Ajanta & Ellora Caves",
                image: "images/maharashtra/aurangabad.jpg",
                lat: 19.8762,
                lng: 75.3433
            },
            {
                city: "Mumbai",
                monument: "Gateway of India",
                image: "images/maharashtra/mumbai.jpg",
                lat: 18.9220,
                lng: 72.8347
            }
        ]
    },
    {
        state: "Manipur",
        cities: [
            {
                city: "Imphal",
                monument: "Kangla Fort",
                image: "images/manipur/imphal.jpg",
                lat: 24.8170,
                lng: 93.9493
            }
        ]
    },
    {
        state: "Meghalaya",
        cities: [
            {
                city: "Shillong",
                monument: "Elephant Falls",
                image: "images/meghalaya/shillong.jpg",
                lat: 25.5647,
                lng: 91.8837
            }
        ]
    },
    {
        state: "Mizoram",
        cities: [
            {
                city: "Aizawl",
                monument: "Solomon’s Temple",
                image: "images/mizoram/aizawl.jpg",
                lat: 23.7307,
                lng: 92.7173
            }
        ]
    },
    {
        state: "Nagaland",
        cities: [
            {
                city: "Kohima",
                monument: "Kohima War Cemetery",
                image: "images/nagaland/kohima.jpg",
                lat: 25.6616,
                lng: 94.1039
            }
        ]
    },
    {
        state: "Odisha",
        cities: [
            {
                city: "Bhubaneswar",
                monument: "Lingaraja Temple",
                image: "images/odisha/bhubaneswar.jpg",
                lat: 20.2359,
                lng: 85.8338
            },
            {
                city: "Konark",
                monument: "Sun Temple",
                image: "images/odisha/konark.jpg",
                lat: 19.8876,
                lng: 86.0945
            }
        ]
    },
    {
        state: "Punjab",
        cities: [
            {
                city: "Amritsar",
                monument: "Golden Temple",
                image: "images/punjab/amritsar.jpg",
                lat: 31.6200,
                lng: 74.8765
            }
        ]
    },
    {
        state: "Rajasthan",
        cities: [
            {
                city: "Jaipur",
                monument: "Hawa Mahal",
                image: "images/rajasthan/jaipur.jpg",
                lat: 26.9239,
                lng: 75.8267
            },
            {
                city: "Udaipur",
                monument: "City Palace",
                image: "images/rajasthan/udaipur.jpg",
                lat: 24.5764,
                lng: 73.6835
            }
        ]
    },
    {
        state: "Sikkim",
        cities: [
            {
                city: "Rumtek",
                monument: "Rumtek Monastery",
                image: "images/sikkim/rumtek.jpg",
                lat: 27.2833,
                lng: 88.5833
            }
        ]
    },
    {
        state: "Tamil Nadu",
        cities: [
            {
                city: "Thanjavur",
                monument: "Brihadeeswarar Temple",
                image: "images/tn/thanjavur.jpg",
                lat: 10.7828,
                lng: 79.1318
            },
            {
                city: "Mahabalipuram",
                monument: "Shore Temple",
                image: "images/tn/mahabalipuram.jpg",
                lat: 12.6167,
                lng: 80.1917
            }
        ]
    },
    {
        state: "Telangana",
        cities: [
            {
                city: "Hyderabad",
                monument: "Charminar",
                image: "images/telangana/charminar.jpg",
                lat: 17.3616,
                lng: 78.4747
            }
        ]
    },
    {
        state: "Tripura",
        cities: [
            {
                city: "Udaipur",
                monument: "Tripura Sundari Temple",
                image: "images/tripura/udaipur.jpg",
                lat: 23.5350,
                lng: 91.4880
            }
        ]
    },
    {
        state: "Uttar Pradesh",
        cities: [
            {
                city: "Agra",
                monument: "Taj Mahal",
                image: "images/up/tajmahal.jpg",
                lat: 27.1751,
                lng: 78.0421
            },
            {
                city: "Varanasi",
                monument: "Kashi Vishwanath Temple",
                image: "images/up/varanasi.jpg",
                lat: 25.3109,
                lng: 83.0107
            }
        ]
    },
    {
        state: "Uttarakhand",
        cities: [
            {
                city: "Rishikesh",
                monument: "Triveni Ghat",
                image: "images/uk/rishikesh.jpg",
                lat: 30.1033,
                lng: 78.2946
            },
            {
                city: "Kedarnath",
                monument: "Kedarnath Temple",
                image: "images/uk/kedarnath.jpg",
                lat: 30.7352,
                lng: 79.0669
            }
        ]
    },
    {
        state: "West Bengal",
        cities: [
            {
                city: "Kolkata",
                monument: "Victoria Memorial",
                image: "images/wb/kolkata.jpg",
                lat: 22.5448,
                lng: 88.3425
            }
        ]
    }
];

window.HERITAGE_DATA = HERITAGE_DATA;
