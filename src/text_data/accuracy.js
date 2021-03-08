const accuracy =  {
                "unbiased": {"title": "Unbiased Race Accuracy (%)",
                "data": [
                    {"cat": "Black", "val": 85}, 
                    {"cat": "East Asian", "val": 70}, 
                    {"cat": "Indian", "val": 66},
                    {"cat": "Latino/Hispanic", "val": 58}, 
                    {"cat": "Middle Eastern", "val": 50}, 
                    {"cat": "SE Asian", "val": 60},
                    {"cat": "White", "val": 65}
                    ],
                "colors": ["#E323FF", "#7517F8"]
            },
                "biased": {
                    "title": "Biased Race Accuracy (%)",
                    "data": [
                        {"cat": "Black", "val": 86}, 
                        {"cat": "East Asian", "val": 42}, 
                        {"cat": "Indian", "val": 0},
                        {"cat": "Latino/Hispanic", "val": 52}, 
                        {"cat": "Middle Eastern", "val": 0}, 
                        {"cat": "SE Asian", "val": 24},
                        {"cat": "White", "val": 85}
                        ],
                    "colors": ["#00FFC7", "#00A3FF"]
                }};
export default accuracy;