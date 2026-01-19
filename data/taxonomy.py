# ==============================================================================
# 1. TAXONOMY STRING (UPDATED FROM EXCEL BOOK3.XLSX)
# ==============================================================================
TAXONOMY_STR = """
[
  {
    "market_segment": "Air Platforms",
    "definition": "Defense aircrafts such as fighter jets, helicopters, and UAVs.",
    "system_types_general": [
      {
        "name": "Fixed Wing",
        "definition": "Aircraft with stationary wings.",
        "system_types_specific": [
          { "name": "Fighter", "definition": "Combat aircraft designed for air-to-air combat." },
          { "name": "Bomber", "definition": "Aircraft designed for dropping bombs." },
          { "name": "Light Combat Aircraft", "definition": "Lightweight multirole jet or turboprop." },
          { "name": "Gunship", "definition": "Heavily armed aircraft for ground support." },
          { "name": "Trainers", "definition": "Aircraft for pilot instruction." },
          { "name": "Tanker", "definition": "Aircraft for in-flight refuelling." },
          { "name": "Maritime Aircraft", "definition": "Aircraft for naval surveillance and strike." },
          { "name": "ISR-Strike", "definition": "Intelligence, Surveillance, Reconnaissance with strike capability." },
          { "name": "C4ISR", "definition": "Airborne Command and Control platforms (e.g., AWACS)." },
          { "name": "AEW&C", "definition": "Airborne Early Warning and Control." },
          { "name": "Transport Aircraft", "definition": "Aircraft used for troop and cargo transport." },
          { "name": "Target Drone", "definition": "Unmanned aerial target for training." },
          { "name": "Fixed Wing Other", "definition": "Miscellaneous fixed-wing platforms." },
          { "name": "Not Applicable", "definition": "Select this when the specific system type is not listed." }
        ]
      },
      {
        "name": "Rotary Wing",
        "definition": "Helicopters and tiltrotors.",
        "system_types_specific": [
          { "name": "Rotary Wing Attack", "definition": "Helicopters for offensive missions." },
          { "name": "Rotary Wing Maritime", "definition": "Naval helicopters." },
          { "name": "Rotary Wing Scout", "definition": "Reconnaissance helicopters." },
          { "name": "Rotary Wing Transport", "definition": "Helicopters for transport." },
          { "name": "Rotary Wing Other", "definition": "Other rotary wing platforms." },
          { "name": "Not Applicable", "definition": "Select this when the specific system type is not listed." }
        ]
      },
      {
        "name": "Other Lift Types",
        "definition": "Non-traditional aircraft.",
        "system_types_specific": [
          { "name": "Hybrid", "definition": "Aircraft with fixed and rotary traits (e.g., V-22)." },
          { "name": "Airship", "definition": "Lighter-than-air craft." },
          { "name": "Parafoil", "definition": "Parachute-based lift systems." },
          { "name": "Not Applicable", "definition": "Select this when the specific system type is not listed." }
        ]
      },
      {
        "name": "Not Applicable",
        "definition": "General Air Platforms.",
        "system_types_specific": [{ "name": "Not Applicable", "definition": "Select this when specific type is not applicable." }]
      }
    ]
  },
  {
    "market_segment": "Land Platforms",
    "definition": "Tanks, armored vehicles, logistic vehicles.",
    "system_types_general": [
      {
        "name": "Artillery",
        "definition": "Large-caliber guns.",
        "system_types_specific": [
          { "name": "Self-Propelled Artillery", "definition": "Mobile artillery vehicles." },
          { "name": "Towed Artillery", "definition": "Stationary artillery moved by other vehicles." },
          { "name": "Mortar", "definition": "Indirect fire weapon." },
          { "name": "MRL (Multiple Rocket Launcher)", "definition": "Rocket artillery systems." },
          { "name": "Other", "definition": "Other artillery systems." },
          { "name": "Not Applicable", "definition": "Select this when the specific system type is not listed." }
        ]
      },
      {
        "name": "Armoured Fighting Vehicles",
        "definition": "Combat vehicles.",
        "system_types_specific": [
          { "name": "Main Battle Tank", "definition": "Heavily armoured front-line tank." },
          { "name": "Tracked Armoured Fighting Vehicles", "definition": "Armoured combat vehicles on tracks." },
          { "name": "Wheeled Armoured Fighting Vehicles", "definition": "Armoured combat vehicles on wheels." },
          { "name": "Amphibious Assault Vehicles", "definition": "Vehicles designed for beach landings." },
          { "name": "Light Tank", "definition": "Lighter weight tank platforms." },
          { "name": "Assault Vehicle", "definition": "Vehicles designed for direct assault." },
          { "name": "Reconnaissance Vehicle", "definition": "Scout vehicles." },
          { "name": "IFV (Infantry Fighting Vehicle)", "definition": "Carries infantry into battle with fire support." },
          { "name": "APC (Armoured Personnel Carrier)", "definition": "Transports infantry." },
          { "name": "AUV (Armoured Utlity Vehicle)", "definition": "Armoured support vehicles." },
          { "name": "Other", "definition": "Other AFVs." },
          { "name": "Not Applicable", "definition": "Select this when the specific system type is not listed." }
        ]
      },
      {
        "name": "Logistics & Support",
        "definition": "Vehicles for support.",
        "system_types_specific": [
          { "name": "All-Terrain Vehicles", "definition": "Light mobility vehicles." },
          { "name": "Combat Engineering Vehicles", "definition": "Vehicles for engineering tasks under fire." },
          { "name": "Construction Vehicles", "definition": "Earthmoving and construction." },
          { "name": "Engineering Equipment", "definition": "Specialized engineering tools." },
          { "name": "Light Tactical/Utility Vehicles", "definition": "Jeeps, light trucks." },
          { "name": "Medical Equipment", "definition": "Ambulances and medical support." },
          { "name": "Military Bridges", "definition": "Bridging layers." },
          { "name": "NBC Equipment", "definition": "Nuclear, Biological, Chemical defense." },
          { "name": "Trucks", "definition": "General transport/resupply." },
          { "name": "Other", "definition": "Other logistics vehicles." },
          { "name": "Not Applicable", "definition": "Select this when the specific system type is not listed." }
        ]
      },
      {
        "name": "Rolling Stock",
        "definition": "Railway systems.",
        "system_types_specific": [
          { "name": "Other", "definition": "Railway platforms." },
          { "name": "Not Applicable", "definition": "Not applicable." }
        ]
      },
      {
        "name": "Other Land",
        "definition": "Miscellaneous land systems.",
        "system_types_specific": [
          { "name": "Soldier Fighting Systems", "definition": "Individual soldier gear and tech." },
          { "name": "Not Applicable", "definition": "Not applicable." }
        ]
      },
      {
        "name": "Not Applicable",
        "definition": "General Land Platforms.",
        "system_types_specific": [{ "name": "Not Applicable", "definition": "Select this when specific type is not applicable." }]
      }
    ]
  },
  {
    "market_segment": "Naval Platforms",
    "definition": "Military vessels, ships, submarines.",
    "system_types_general": [
      {
        "name": "Sub-Surface",
        "definition": "Submarines.",
        "system_types_specific": [
          { "name": "Diesel-Powered Submarine", "definition": "Conventional submarines." },
          { "name": "Nuclear-Powered Submarine", "definition": "Nuclear propulsion submarines." },
          { "name": "Other", "definition": "Other sub-surface vessels." },
          { "name": "Not Applicable", "definition": "Select this when the specific system type is not listed." }
        ]
      },
      {
        "name": "Surface Combatants",
        "definition": "Warships.",
        "system_types_specific": [
          { "name": "Aircraft Carrier", "definition": "Ship for launching aircraft." },
          { "name": "Cruisers", "definition": "Large multi-role warships." },
          { "name": "Destroyers", "definition": "Fast, maneuverable long-endurance warships." },
          { "name": "Frigates", "definition": "Warships sized between destroyer and corvette." },
          { "name": "Corvettes", "definition": "Small warships." },
          { "name": "Other Surface Combatants", "definition": "Other surface fighting ships." },
          { "name": "Not Applicable", "definition": "Select this when the specific system type is not listed." }
        ]
      },
      {
        "name": "Patrol and Costal Combatants",
        "definition": "Coastal defense vessels.",
        "system_types_specific": [
          { "name": "Patrol Boat/Craft - Coastal", "definition": "Short range patrol." },
          { "name": "Patrol Boat/Craft - Ocean", "definition": "Long range patrol." },
          { "name": "Patrol Boat/Craft - Riverine", "definition": "River patrol." },
          { "name": "Not Applicable", "definition": "Select this when the specific system type is not listed." }
        ]
      },
      {
        "name": "Mine Warfare/Mine Countermeasures (Maritime)",
        "definition": "Mine detection/removal.",
        "system_types_specific": [
          { "name": "Mine Sweeper", "definition": "Detects and clears mines." },
          { "name": "Mine Counter-Measures", "definition": "Systems to neutralize mines." },
          { "name": "Mine Hunter", "definition": "Actively hunts mines." },
          { "name": "Not Applicable", "definition": "Select this when the specific system type is not listed." }
        ]
      },
      {
        "name": "Amphibious (Maritime)",
        "definition": "Ships for amphibious assault.",
        "system_types_specific": [
          { "name": "Amphibious Assault Ship", "definition": "Supports landings (LHD/LHA)." },
          { "name": "Landing Ship", "definition": "Transports vehicles/troops to shore." },
          { "name": "Landing Craft", "definition": "Small craft for beach landing." },
          { "name": "Landing Platform Dock", "definition": "LPD class ships." },
          { "name": "Amphibious Other (Maritime)", "definition": "Other amphibious vessels." },
          { "name": "Not Applicable", "definition": "Select this when the specific system type is not listed." }
        ]
      },
      {
        "name": "Logistics and Support (Maritime)",
        "definition": "Support vessels.",
        "system_types_specific": [
          { "name": "Research/Survey Vessels", "definition": "Oceanographic ships." },
          { "name": "Icebreakers", "definition": "Polar region ships." },
          { "name": "Combat Support Ship", "definition": "Replenishment and support." },
          { "name": "Repair Ships", "definition": "Maintenance at sea." },
          { "name": "Ocean Transport/Tanker/Cargo/Oiler", "definition": "Fuel and cargo transport." },
          { "name": "Hospital Ship", "definition": "Medical facilities at sea." },
          { "name": "Logistics and Support Other (Maritime)", "definition": "Other support." },
          { "name": "Not Applicable", "definition": "Select this when the specific system type is not listed." }
        ]
      },
      {
        "name": "Other Maritime",
        "definition": "Miscellaneous naval.",
        "system_types_specific": [
          { "name": "Training Ship", "definition": "Vessels for training sailors." },
          { "name": "Other Maritime", "definition": "Other." },
          { "name": "Not Applicable", "definition": "Select this when the specific system type is not listed." }
        ]
      },
      {
        "name": "Not Applicable",
        "definition": "General Naval Platforms.",
        "system_types_specific": [{ "name": "Not Applicable", "definition": "Select this when specific type is not applicable." }]
      }
    ]
  },
  {
    "market_segment": "Space Systems",
    "definition": "Weapons or platforms based on space technologies.",
    "system_types_general": [
      {
        "name": "Launch Vehicle",
        "definition": "Launch systems.",
        "system_types_specific": [
          { "name": "Launch Vehicle", "definition": "Rockets for space launch." },
          { "name": "Not Applicable", "definition": "Not applicable." }
        ]
      },
      {
        "name": "Satellite",
        "definition": "Orbiting objects.",
        "system_types_specific": [
          { "name": "Satellite", "definition": "General satellites." },
          { "name": "Radar Satellite", "definition": "SAR/Radar equipped satellites." },
          { "name": "Not Applicable", "definition": "Not applicable." }
        ]
      },
      {
        "name": "Anti-Space",
        "definition": "Systems to deny space usage.",
        "system_types_specific": [
          { "name": "Anti-Space", "definition": "ASAT systems." },
          { "name": "Not Applicable", "definition": "Not applicable." }
        ]
      },
      {
        "name": "Other",
        "definition": "Other space systems.",
        "system_types_specific": [
          { "name": "Other", "definition": "Other." },
          { "name": "Not Applicable", "definition": "Not applicable." }
        ]
      },
      {
        "name": "Not Applicable",
        "definition": "General Space Systems.",
        "system_types_specific": [
          { "name": "Not Applicable", "definition": "Not applicable." }
        ]
      }
    ]
  },
  {
    "market_segment": "C4ISR Systems",
    "definition": "Command, Control, Comms, Intel, Surveillance.",
    "system_types_general": [
      {
        "name": "Electro-optic Sensor",
        "definition": "Optical systems.",
        "system_types_specific": [
          { "name": "Imaging EO/IR", "definition": "Cameras and Infrared sensors." },
          { "name": "Targeting EO/IR", "definition": "Used for weapon guidance." },
          { "name": "Not Applicable", "definition": "Select this when the specific system type is not listed." }
        ]
      },
      {
        "name": "Radar",
        "definition": "Radar systems.",
        "system_types_specific": [
          { "name": "Air Search Radar", "definition": "Detects airborne targets." },
          { "name": "Surface Surveillance Radar", "definition": "Detects surface targets." },
          { "name": "Fire Control Radar", "definition": "Directs weapons." },
          { "name": "Navigation Radar", "definition": "For navigation." },
          { "name": "Weather Radar", "definition": "For weather." },
          { "name": "Multi-Mission Radar", "definition": "Versatile radar systems." },
          { "name": "Not Applicable", "definition": "Select this when the specific system type is not listed." }
        ]
      },
      {
        "name": "Sonar",
        "definition": "Underwater detection.",
        "system_types_specific": [
          { "name": "Sonar", "definition": "Sonar systems." },
          { "name": "Not Applicable", "definition": "Not applicable." }
        ]
      },
      {
        "name": "Command and Control",
        "definition": "C2 systems.",
        "system_types_specific": [
          { "name": "Command and Control System", "definition": "C2 software and hardware." },
          { "name": "Not Applicable", "definition": "Not applicable." }
        ]
      },
      {
        "name": "Communications",
        "definition": "Comms gear.",
        "system_types_specific": [
          { "name": "Radios", "definition": "Tactical radios." },
          { "name": "Data links", "definition": "Tactical data links." },
          { "name": "Satellite Communications", "definition": "SATCOM." },
          { "name": "Not Applicable", "definition": "Select this when the specific system type is not listed." }
        ]
      },
      {
        "name": "Computers",
        "definition": "Computing hardware.",
        "system_types_specific": [
          { "name": "Military IT Systems", "definition": "Ruggedized or mil-spec IT." },
          { "name": "Not Applicable", "definition": "Not applicable." }
        ]
      },
      {
        "name": "Cyber",
        "definition": "Cyber warfare.",
        "system_types_specific": [
          { "name": "Cyber Defense", "definition": "Protective cyber systems." },
          { "name": "Cyber Offense", "definition": "Offensive cyber capabilities." },
          { "name": "Not Applicable", "definition": "Not applicable." }
        ]
      },
      {
        "name": "Artificial Intelligence",
        "definition": "AI systems.",
        "system_types_specific": [
          { "name": "Artificial Intelligence", "definition": "AI/ML software." },
          { "name": "Not Applicable", "definition": "Not applicable." }
        ]
      },
      {
        "name": "Other C4ISR",
        "definition": "Miscellaneous C4ISR.",
        "system_types_specific": [
          { "name": "PNT Systems", "definition": "Positioning, Navigation, and Timing." },
          { "name": "Other", "definition": "Other." },
          { "name": "Not Applicable", "definition": "Not applicable." }
        ]
      },
      {
        "name": "Integrated C4ISR System",
        "definition": "Combined C4ISR.",
        "system_types_specific": [
          { "name": "Integrated C4ISR System", "definition": "System of systems." },
          { "name": "Not Applicable", "definition": "Not applicable." }
        ]
      },
      {
        "name": "Defensive Systems",
        "definition": "Countermeasures.",
        "system_types_specific": [
          { "name": "Defensive Aid Suite", "definition": "Integrated defensive system." },
          { "name": "Not Applicable", "definition": "Select this when the specific system type is not listed." }
        ]
      },
      {
        "name": "Not Applicable",
        "definition": "General C4ISR.",
        "system_types_specific": [{ "name": "Not Applicable", "definition": "Select this when specific type is not applicable." }]
      }
    ]
  },
  {
    "market_segment": "Weapon Systems",
    "definition": "Missiles, bombs, guns.",
    "system_types_general": [
      {
        "name": "Missile",
        "definition": "Guided weapons (powered).",
        "system_types_specific": [
          { "name": "Air-to-Air", "definition": "AAM." },
          { "name": "Air-to-Surface", "definition": "ASM." },
          { "name": "Air-to-Ship", "definition": "Anti-ship missile." },
          { "name": "Surface-to-Air", "definition": "SAM." },
          { "name": "Surface-to-Surface", "definition": "SSM." },
          { "name": "Surface-to-Ship", "definition": "Coastal defense missile." },
          { "name": "Ship-to-Air", "definition": "Naval SAM." },
          { "name": "Ship-to-Surface", "definition": "Naval strike missile." },
          { "name": "Ship-to-Ship", "definition": "Naval anti-ship missile." },
          { "name": "Ballistic Missile", "definition": "Rocket-propelled strategic-weapons." },
          { "name": "Other", "definition": "Other missile types." },
          { "name": "Not Applicable", "definition": "Select this when the specific system type is not listed." }
        ]
      },
      {
        "name": "Precision Guided Weapons",
        "definition": "Smart munitions.",
        "system_types_specific": [
          { "name": "Guided Rocket", "definition": "Guided unpowered or short burn rockets." },
          { "name": "Guided Bomb", "definition": "Smart bombs (JDAM etc)." },
          { "name": "Guided Artillery Round", "definition": "Smart shells." },
          { "name": "Loitering Munitions", "definition": "Suicide drones." },
          { "name": "Other", "definition": "Other PGMs." },
          { "name": "Not Applicable", "definition": "Select this when the specific system type is not listed." }
        ]
      },
      {
        "name": "Torpedo",
        "definition": "Underwater missiles.",
        "system_types_specific": [
          { "name": "Heavy Weight Torpedo", "definition": "Submarine launched torpedo." },
          { "name": "Light Weight Torpedo", "definition": "Air/Surface launched torpedo." },
          { "name": "Other", "definition": "Other." },
          { "name": "Not Applicable", "definition": "Select this when the specific system type is not listed." }
        ]
      },
      {
        "name": "Directed Energy Weapon",
        "definition": "Lasers and high-power microwaves.",
        "system_types_specific": [
          { "name": "Radar", "definition": "High power radar as weapon." },
          { "name": "Laser", "definition": "High energy laser." },
          { "name": "Microwave", "definition": "HPM weapons." },
          { "name": "Sonic", "definition": "Acoustic weapons." },
          { "name": "Not Applicable", "definition": "Select this when the specific system type is not listed." }
        ]
      },
      {
        "name": "Integrated Weapon Systems",
        "definition": "Combined weapon platforms.",
        "system_types_specific": [
          { "name": "Air and Missile Defense System", "definition": "Integrated AMD." },
          { "name": "Ballistic Missile Defense System", "definition": "BMD." },
          { "name": "Coastal Defense System", "definition": "Coastal protection batteries." },
          { "name": "Border Defense System", "definition": "Border security weapons." },
          { "name": "Other", "definition": "Other." },
          { "name": "Not Applicable", "definition": "Select this when the specific system type is not applicable." }
        ]
      },
      {
        "name": "Swarm Drones",
        "definition": "Drone swarms.",
        "system_types_specific": [
          { "name": "EW Swarm Drones", "definition": "Swarms for electronic warfare." },
          { "name": "Kinetic Strike Swarm Drones", "definition": "Swarms for attack." },
          { "name": "Other", "definition": "Other." },
          { "name": "Not Applicable", "definition": "Not applicable." }
        ]
      },
      {
        "name": "Launchers",
        "definition": "Weapon firing systems.",
        "system_types_specific": [
          { "name": "Launchers", "definition": "Missile or rocket launchers." },
          { "name": "Remote Weapon System", "definition": "RWS." },
          { "name": "Not Applicable", "definition": "Not applicable." }
        ]
      },
      {
        "name": "Mines",
        "definition": "Explosive traps.",
        "system_types_specific": [
          { "name": "Anti-Personnel Mine", "definition": "Targeting foot traffic." },
          { "name": "Anti-Tank Mine", "definition": "Targeting vehicles." },
          { "name": "Sea Mine", "definition": "Targeting ships." },
          { "name": "Mine Dispersal System", "definition": "Systems to scatter mines." },
          { "name": "Not Applicable", "definition": "Not applicable." }
        ]
      },
      {
        "name": "Small Arms & Ammunition",
        "definition": "Guns and bullets.",
        "system_types_specific": [
          { "name": "Small Arms", "definition": "Rifles, pistols, machine guns." },
          { "name": "Ammunition", "definition": "Bullets and shells." },
          { "name": "Rockets", "definition": "Unguided rockets." },
          { "name": "Bombs", "definition": "Unguided bombs." },
          { "name": "Explosives", "definition": "C4, TNT, etc." },
          { "name": "Not Applicable", "definition": "Not applicable." }
        ]
      },
      {
        "name": "Electronic Warfare Systems",
        "definition": "EW Systems.",
        "system_types_specific": [
          { "name": "Electronic Jamming", "definition": "Jamming systems." },
          { "name": "Electronic Attack", "definition": "Offensive EW." },
          { "name": "Other", "definition": "Other EW." },
          { "name": "Not Applicable", "definition": "Select this when the specific system type is not listed." }
        ]
      },
      {
        "name": "Not Applicable",
        "definition": "General Weapon Systems.",
        "system_types_specific": [{ "name": "Not Applicable", "definition": "Select this when specific type is not applicable." }]
      }
    ]
  },
  {
    "market_segment": "Infrastructure",
    "definition": "Military buildings and facilities.",
    "system_types_general": [
      {
        "name": "Shipyards/Ports/Harbours",
        "definition": "Maritime infrastructure.",
        "system_types_specific": [{ "name": "Shipyards/Ports/Harbours", "definition": "Shipyards/Ports/Harbours" }, { "name": "Not Applicable", "definition": "N/A" }]
      },
      {
        "name": "Aircraft Basing",
        "definition": "Air infrastructure.",
        "system_types_specific": [{ "name": "Aircraft Basing", "definition": "Aircraft Basing" }, { "name": "Not Applicable", "definition": "N/A" }]
      },
      {
        "name": "Accomodation",
        "definition": "Housing.",
        "system_types_specific": [{ "name": "Accomodation", "definition": "Accomodation" }, { "name": "Not Applicable", "definition": "N/A" }]
      },
      {
        "name": "Non-military IT",
        "definition": "Office IT.",
        "system_types_specific": [{ "name": "Non-military IT", "definition": "Non-military IT" }, { "name": "Not Applicable", "definition": "N/A" }]
      },
      {
        "name": "Land",
        "definition": "Real estate.",
        "system_types_specific": [{ "name": "Land", "definition": "Land" }, { "name": "Not Applicable", "definition": "N/A" }]
      },
      {
        "name": "Training Facilities",
        "definition": "Schools and ranges.",
        "system_types_specific": [{ "name": "Training Facilities", "definition": "Training Facilities" }, { "name": "Not Applicable", "definition": "N/A" }]
      },
      {
        "name": "Air Traffic Management",
        "definition": "ATC infra.",
        "system_types_specific": [{ "name": "Air Traffic Management", "definition": "Air Traffic Management" }, { "name": "Not Applicable", "definition": "N/A" }]
      },
      {
        "name": "RDT&E Facilities",
        "definition": "Research labs.",
        "system_types_specific": [{ "name": "RDT&E Facilities", "definition": "RDT&E Facilities" }, { "name": "Not Applicable", "definition": "N/A" }]
      },
      {
        "name": "Production Facilities",
        "definition": "Factories.",
        "system_types_specific": [{ "name": "Production Facilities", "definition": "Production Facilities" }, { "name": "Not Applicable", "definition": "N/A" }]
      },
      {
        "name": "Maintenance Facilities",
        "definition": "Repair and maintenance buildings.",
        "system_types_specific": [{ "name": "Maintenance Facilities", "definition": "Maintenance Facilities" }, { "name": "Not Applicable", "definition": "N/A" }]
      },
      {
        "name": "Utilities",
        "definition": "Power, water, waste.",
        "system_types_specific": [{ "name": "Utilities", "definition": "Utilities" }, { "name": "Not Applicable", "definition": "N/A" }]
      },
      {
        "name": "Other",
        "definition": "Other infrastructure.",
        "system_types_specific": [{ "name": "Other", "definition": "Other" }, { "name": "Not Applicable", "definition": "N/A" }]
      },
      {
        "name": "Not Applicable",
        "definition": "General construction.",
        "system_types_specific": [
          { "name": "Not Applicable", "definition": "N/A" }
        ]
      }
    ]
  },
  {
    "market_segment": "Training & Simulation",
    "definition": "Training services and equipment.",
    "system_types_general": [
      {
        "name": "Simulators",
        "definition": "Simulation hardware/software.",
        "system_types_specific": [
          { "name": "Simulators", "definition": "Simulators." },
          { "name": "Not Applicable", "definition": "N/A" }
        ]
      },
      {
        "name": "Training Aids",
        "definition": "Tools for training.",
        "system_types_specific": [
          { "name": "Training Aids", "definition": "Training Aids." },
          { "name": "Not Applicable", "definition": "N/A" }
        ]
      },
      {
        "name": "Other",
        "definition": "Other training.",
        "system_types_specific": [
          { "name": "Other", "definition": "Other." },
          { "name": "Not Applicable", "definition": "N/A" }
        ]
      },
      {
        "name": "Not Applicable",
        "definition": "General Training.",
        "system_types_specific": [{ "name": "Not Applicable", "definition": "Select this when specific type is not applicable." }]
      }
    ]
  },
  {
    "market_segment": "Unknown",
    "definition": "Unknown segment.",
    "system_types_general": [
      {
        "name": "Not Applicable",
        "definition": "Select this when the system type is not applicable.",
        "system_types_specific": [{ "name": "Not Applicable", "definition": "Select this when the specific system type is not applicable." }]
      }
    ]
  }
]
"""

# ==============================================================================
# 2. CONSTANTS (EXISTING)
# ==============================================================================

VALID_DEPENDENCIES = {
    "Air Platforms": [
        "Fixed Wing", "Rotary Wing", "Other Lift Types", "Not Applicable"
    ],
    "Land Platforms": [
        "Artillery", "Armoured Fighting Vehicles", "Logistics & Support",
        "Rolling Stock", "Other Land", "Not Applicable"
    ],
    "Naval Platforms": [
        "Sub-Surface", "Surface Combatants", "Patrol and Costal Combatants",
        "Mine Warfare/Mine Countermeasures (Maritime)", "Amphibious (Maritime)",
        "Logistics and Support (Maritime)", "Other Maritime", "Not Applicable"
    ],
    "Space Systems": [
        "Launch Vehicle", "Satellite", "Anti-Space", "Other", "Not Applicable"
    ],
    "C4ISR Systems": [
        "Electro-optic Sensor", "Radar", "Sonar", "Command and Control",
        "Communications", "Computers", "Cyber", "Artificial Intelligence",
        "Other C4ISR", "Integrated C4ISR System", "Defensive Systems", "Not Applicable"
    ],
    "Weapon Systems": [
        "Missile", "Precision Guided Weapons", "Torpedo", "Directed Energy Weapon",
        "Integrated Weapon Systems", "Swarm Drones", "Launchers", "Mines",
        "Small Arms & Ammunition", "Electronic Warfare Systems", "Not Applicable"
    ],
    "Infrastructure": [
        "Shipyards/Ports/Harbours", "Aircraft Basing", "Accomodation", "Non-military IT",
        "Land", "Training Facilities", "Air Traffic Management", "RDT&E Facilities",
        "Production Facilities", "Maintenance Facilities", "Utilities", "Other", "Not Applicable"
    ],
    "Training & Simulation": ["Simulators", "Training Aids", "Other", "Not Applicable"],
    "Unknown": ["Not Applicable"]
}

# ==============================================================================
# 3. OPTIMIZED PROMPT (Add this to your LLM call)
# ==============================================================================
TAXONOMY_PROMPT = """
You are an expert Defense Market Analyst. Your task is to classify defense contracts into a strict three-level taxonomy based on the text description provided.

## Input
Description: {description}

## Taxonomy Logic
1. **Market Segment**: Identify the broad domain (e.g., Air Platforms, Weapon Systems).
2. **System Type (General)**: Based *only* on the selected Market Segment, choose the General category that fits best.
   - Example: If Segment is "Air Platforms", "Fighter" is NOT a General type; "Fixed Wing" IS.
3. **System Type (Specific)**: Based *only* on the selected General type, choose the Specific category.
   - Example: If General is "Fixed Wing", "Fighter" is valid.

## Rules
- Use "Not Applicable" if a specific level is not mentioned or unclear.
- Do not invent new categories. You must strictly use the provided JSON taxonomy structure.
- **Hierarchy Enforcement**: You cannot select a Specific type that does not belong to the selected General type.

## Output Format (JSON)
{
  "market_segment": "String",
  "system_type_general": "String",
  "system_type_specific": "String",
  "reasoning": "Brief explanation."
}
"""

GEOGRAPHY_MAPPING = {
    "Sub-Saharan Africa": [
        "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi", "Cameroon", "Cape Verde",
        "Central African Republic", "Chad", "Congo, Democratic Republic of", "Congo, Republic of",
        "Djibouti", "Equatorial Guinea", "Eritrea", "Eswatini", "Ethiopia", "Gabon", "Gambia",
        "Ghana", "Guinea", "Guinea-Bissau", "Ivory Coast", "Kenya", "Lesotho", "Liberia",
        "Madagascar", "Malawi", "Mali", "Mauritius", "Mozambique", "Namibia", "Niger",
        "Nigeria", "Rwanda", "Senegal", "Seychelles", "Sierra Leone", "Somalia", "South Africa",
        "South Sudan", "Sudan", "Tanzania", "Togo", "Uganda", "Zambia", "Zimbabwe"
    ],
    "Asia-Pacific": [
        "Australia", "Brunei", "Cambodia", "China", "Hong Kong", "Indonesia", "Japan", "Laos",
        "Malaysia", "Mongolia", "Myanmar", "New Zealand", "North Korea", "Papua New Guinea",
        "Philippines", "Singapore", "South Korea", "Taiwan", "Thailand", "Vietnam"
    ],
    "Europe": [
        "Albania", "Austria", "Belgium", "Bosnia and Herzegovina", "Bulgaria", "Croatia", "Cyprus",
        "Czech Republic", "Denmark", "Estonia", "Finland", "France", "Georgia", "Germany", "Greece",
        "Hungary", "Iceland", "Ireland", "Italy", "Kosovo", "Latvia", "Lithuania", "Luxembourg",
        "Malta", "Montenegro", "Netherlands", "North Macedonia", "Norway", "Poland", "Portugal",
        "Romania", "Serbia", "Slovakia", "Slovenia", "Spain", "Sweden", "Switzerland", "Turkey",
        "Ukraine", "United Kingdom"
    ],
    "Latin America": [
        "Argentina", "Bahamas", "Barbados", "Belize", "Bolivia", "Brazil", "Chile", "Colombia",
        "Costa Rica", "Cuba", "Curacao", "Dominican Republic", "Ecuador", "El Salvador", "Guatemala",
        "Guyana", "Haiti", "Honduras", "Jamaica", "Mexico", "Nicaragua", "Panama", "Paraguay",
        "Peru", "Suriname", "Trinidad and Tobago", "Uruguay", "Venezuela"
    ],
    "Middle East and North Africa": [
        "Algeria", "Bahrain", "Egypt", "Iran", "Iraq", "Israel", "Jordan", "Kuwait", "Lebanon",
        "Libya", "Mauritania", "Morocco", "Oman", "Qatar", "Saudi Arabia", "Syria", "Tunisia",
        "United Arab Emirates", "Yemen"
    ],
    "North America": ["Canada", "USA"],
    "Russia & CIS": [
        "Armenia", "Azerbaijan", "Belarus", "Kazakhstan", "Kyrgyzstan", "Moldova", "Russia",
        "Tajikistan", "Turkmenistan", "Uzbekistan"
    ],
    "South Asia": [
        "Afghanistan", "Bangladesh", "India", "Maldives", "Nepal", "Pakistan", "Sri Lanka"
    ],
    "Unknown": [
        "Andorra", "Antigua and Barbuda", "Bhutan", "Comoros", "Dominica", "Federated States of Micronesia",
        "Fiji", "Grenada", "Kiribati", "Liechtenstein", "Marshall Islands", "Monaco", "Nauru", "Palau",
        "Palestine", "Puerto Rico", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines",
        "Samoa", "San Marino", "Sao Tom and Principe", "Solomon Islands", "Timor-Leste", "Tonga", "Tuvalu",
        "Unknown", "Vanuatu", "Vatican City", "Western Sahara"
    ]
}

VALID_OPERATORS = [
    "Army", "Navy", "Air Force", "Defense Wide",
    "Ukraine (Assistance)", "Foreign Assistance", "Other"
]

SUPPLIER_LIST = [
    "22nd Century Tech", "A&P Group", "A&R Pacific -Garney Federal", "AAR Supply Chain Inc.", "Aardvark Clear", "AASKI Technology", "AAVCO", "Abacus Tech Corp", "Abdallah Al-Faris", "Abeking Rasmuss",
    "ABG Shipyards", "ABM Shipyard", "Absher Construction Co.", "Abu Dhabi MAR", "Abu Dhabi SB", "ACC Construction Co.", "Accenture", "Accurate Energetic Systems", "ACE Technology", "Aceinfo Solutions",
    "ACHILE Consortium", "Achleitner", "ACMI", "ACT-Corp", "ActioNet", "ADCOM Systems", "ADI Group", "Admiralty Ship", "Advanced Navigation and Positioning Corp.", "Advanced Technology International",
    "AdvElect Co (AEC)", "AECOM", "Aegis Technologies", "Aeraccess", "Aero Def Systems", "Aero Synergie", "Aero Vodochody", "Aerodata AG", "Aerodyca", "Aerojet Rocketdyne", "Aeromaritime Grp", "Aeromot",
    "Aeronautical Development Establishment", "Aeronautics Defense Systems", "Aerospace Corp", "Aerostar", "Aerostar S.A.", "Aerotree", "AeroVironment", "AeroVolga", "Affigent",
    "Africa Automotive Distribution Service", "Agat", "AgEagle", "Agiliti Health", "AICI-Archirodon JV", "AIDC", "AIM Defence", "Air Center Helicopters", "Air Tractor", "Airbus", "Airbus-Rheinmetall",
    "Airborne Tactical Advantage Co.", "Aircell", "Aircraft Readiness Alliance", "AirRobot", "AIS Engineering", "Akkodis", "Albadeey", "Albatross Industria Aeronautica Ltd.", "Alcatel-Lucent", "Alcock Ashdown",
    "Alexandria Ship", "Alion Science", "Allen-Vanguard", "Alliant Techsystems Operations", "Allison Transmission", "Alpha Marine", "Alpine Armoring Inc.", "Altawest", "Altec Industries", "ALTECH Services",
    "Aleut Federal", "Alzchem Trostberg", "AM General", "Amazon", "Amentum Services", "American International Contractors", "American States Utilities Services", "American SysCorp", "American Systems Corp",
    "AMESYS", "AMI Industries", "AMO ZIL", "Amper Group", "AMSL Aero", "AMTEC Corp.", "AMX International", "Amyx Inc", "AMZ-Kutno", "Anadolu Shipyard", "Analytic Services", "Ananda Shipyard", "Andrea Systems",
    "Andritz Hydro Corp.", "Anduril Industries", "Antonov", "ANVL", "AOI", "Apogee Engeineering", "Applied Mechanics", "Applied Technology", "Applied Visual Technology", "APS", "Aquacopters", "Aquila Aerospace",
    "Arab Contractors", "Arcfield Canada", "Archer Aviation", "Archer Western", "Arcturus UAV", "ARES Shipyard", "Aresa Shipyard", "ARGE K-130", "ARGE NNbS Consortium", "Argon ST Inc.", "ARGE DiNa 155", "ARIS",
    "Arma", "Armenian Air Force Institute", "American Electronics Warfare Associates", "American Ordnance", "Armour International", "Armoured Car Sys", "ARMSCOR", "Armtec Defense Products",
    "Arnold Defense and Elec", "ARO SA", "Arotech Corp", "Arquus", "Array Information", "Arrow Edge LLC", "AR-SAT", "Arsenal d' Marinha", "Arsenal JSCO", "ARTEC", "ARTEL, Inc", "ASC Pty Ltd",
    "Ascent Flight Training Consotium", "Ascom Group", "Aselsan", "ASENAV", "Asian ArmoredVeh", "ASIMAR", "ASISGUARD", "Ashot Ashkelon", "ASL Group", "Aslemetals Oy", "ASMAR", "ASRC Federal", "ASRY",
    "Assurance Tech", "Assured Information Security Inc.", "Aster Engineering", "Astilleros Armon Vigo SA", "Astilleros Navales", "ASTIMAR", "Astronics Test Systems", "ASTRUM", "AT&T", "A-techSYN",
    "Atheeb Integraph Saudi Co.", "Atlas", "Atlas Elektronik", "Atlas Group", "ATR", "August Schell Enterprises", "Aurora Flight Sciences", "Austal Limited", "Australian Target Systems", "Autoespar SA",
    "Automotive Ind Ltd", "AUVERLAND", "Aviation Repair Technologies", "Aviation Systems Engineering", "Aviation Training Consulting", "Avibras", "AVIC", "AVNL", "Avtech Corporation", "Avtokraz Holding Co",
    "AWEIL", "AWSR Shipping", "B&F", "Babcock Group", "BAE Systems", "Ball Corporation", "Baltic Workboats", "BAMS", "Bangkok Dock", "Barrett Comm", "Basler", "Bason Shipyard", "Bath Iron Works", "Battelle",
    "Baud Telecom Co", "Baykar", "Bechtel Group", "Becker Avionics", "Beechcraft", "Beherman Demoen", "Beijing JeepCorp", "Bell", "Bell Boeing", "Bell Textron", "Bellanca", "BEML-India", "Bender Shipbldg",
    "Bergen Group", "Beriev", "BGI-ASI JV", "Bharat Dynamics", "Bharat Elec Ltd", "Bharat Heavy Electricals", "Bharat Sanchar", "Bharati Shipyard", "Bigelow Family Holdings", "Bin Jabr Group", "Bird Aerosystems",
    "Birdon", "Bittium", "BL Halbert International", "Black Box Corp", "Black Micro Corp", "Black River Systems", "Blackberry", "Blackned", "BlackSky", "BlindermanPower", "Blue Air Training", "Blue Ivy Partners",
    "Blue River Consortium", "Blue Tech Inc", "Bluebird", "BlueHalo", "Boeing", "Boelwerf Shipyard", "Bollinger Shipyard", "Bombardier", "Booz Allen Hamilton", "Boresight", "Boustead DCNS JV",
    "Boustead Holding", "Bowhead", "Brahmos Ltd", "BrainGu LLC", "Bridgestone Aircraft Tire Inc.", "Britten-Norman", "Brodosplit Shipyard", "Brooke Marine", "Bryan 77 Construction", "BSVT", "BSVT-NT",
    "BT Group", "BUAA", "BwFuhrparkService", "BWI", "By Light", "CACI", "CAE USA", "Cairns Slipways", "Calian", "Calidus", "Cambridge Intl Systems", "Cammell Laird SB", "Canadair", "Cantieri Navali",
    "Carahsoft Inc.", "Cardama", "Carnegie Mellon University", "CASC", "CASIC", "C-Astral Aerospace", "C-AT", "Caterpillar", "CATIC", "CDO Technologies", "CDW Corporation", "CEA Tech Pty Ltd", "Celier Aviation",
    "CENTECH GROUP", "Cerbair", "Cessna", "CFM International", "CGI", "Chaiseri Metal & Rubber", "Changhe", "Chantier Davie Ship", "Charles Stark Draper", "Chas Kurz", "Chemring", "Chengdu",
    "Chowgule and Company", "Chrysler Group", "Chugach Technical Solutions", "Chung Shan Inst", "Cianbro", "CINAR", "CIO", "Cirrus Aircraft", "Cisco Systems", "Clark Construction Group",
    "CM de N (France)", "CNF Technologies", "CNIM", "CNN Navigation", "Coastal Defense Inc.", "Cobham", "Cochin Shipyard", "CODALTEC", "Codan", "Cohort plc", "Cohu Inc", "Colby Co. LLC",
    "Cole Engineering Services", "Collins Aerospace", "COLSA", "Colt's Manufacturing Co.", "Columbia Helicopters Inc.", "COM DEV International", "Comlenia", "Commander Aircraft Corporation",
    "Commtact", "Computacentre", "CompQsoft", "Computer World Services", "COMSOFT", "ComtechTelecomm", "Conco Inc.", "Conlog Group", "Conoship Intl", "Conquest USA", "Consigli Construction",
    "Consortium Management Group", "Conti Federal Services", "Continental Maritime", "Core Tech International", "Core4ce", "Corporacion De La Industria Aeronautica Colombiana", "Corvid Technologies",
    "COTECMAR", "CounterTrade", "CoVant Technologies", "CPMIEC", "Credence Mgmnt Sol", "Creotech", "Crew Training International", "CRIST", "Criterion Solutions", "CRL Technologies", "Crowley Maritime",
    "CRSA", "Crystal", "CSBC Corp., Taiwan", "CSC", "Cubic Corporation", "Cukurova Holding", "Cummins Inc.", "Curt Nyberg", "Curtiss-Wright", "Cybaero AB", "Dae Sun Shipbldg", "Daewoo", "Daher", "Daimler AG",
    "Dakota Creek", "Dalnyaya Radio", "Damen Shipyards", "DAMEX Shipbldg", "Danbury Mission Technologies", "Danish Maritime", "Danish Yacht", "Danyard Aalborg", "Darkhive", "DARPA", "Dassault", "Dassault Dornier",
    "Data Link Solutions", "Data Sys Analysts", "Datamir", "DataPath", "Day & Zimmerman Lone Star", "Dayton T. Brown Inc.", "DCCA", "DCD-DORBYL", "DCI", "DCNS Odebrecht", "DCS Corp.", "De Havilland Canada",
    "Dearsan Shipyard", "Decisive Analytics", "Deep Trekker", "Defense Ind Org", "Defense Industries Organization Of Iran", "Defense Solutions", "Defense Technology Institute", "Defenture", "Deftools",
    "Delaware Nation Industries Emerging Technologies", "Dell Inc", "Deloitte", "Denel", "Derecktor Shipyard", "DESA", "Design West Technologies", "Destini Berhad", "Detyens Shipyard", "DEW Ltd", "DFDS Group",
    "Diamond Aircraft", "DIANCA", "DIDEP", "Diehl", "Digital Angel Corp", "Digital Management", "Diligent Consulting", "Divelink Underwater", "Diversified Tech Svcs", "DJI", "DKW Communications", "DOF ASA",
    "Domo Tactical Communications", "Doosan Group", "Dornier", "Draken", "Draper Labs", "DRB-HICOM", "DRDC Canada", "DRDO", "Drew Marine USA", "DRS Network and Imaging Systems", "DSD Laboratories", "DSG",
    "DSN Corp", "DSTA", "Ducommun Inc.", "DXC Technology", "Dynamic Systems", "Dynamics Resrch", "Dynamit Nobel", "DynCorp Int'l", "Dynetics Technical Solutions", "Eastern Shipbuilding", "ECAN", "ECRN",
    "ECS Federal", "Emcube Inc", "Edgar Brothers", "Edge Autonomy", "EDGE Group", "Edison Chouest", "EFR Ltd", "eGlobalTech", "EID S.A.", "Eire Forge and Steel", "EINSA", "ELAC Sonar GmbH", "Elbit Systems",
    "ELBO", "Elebra", "Electra", "Electric Boat Corp.", "Electro Optic Systems", "Elettronica SpA", "ELINC", "EllisDon", "EM Solutions", "Embraer", "EMESEC", "EMGEPRON", "Emit Aviation", "EMPL Austria", "EMPORDEF",
    "EMS Tech", "EMT", "EMW", "ENAER", "EnerSys Energy Products", "Engility Corporation", "Engine Eng Oman", "ENICS", "Ensign Bickford", "Enstrom Helicopter", "Entrol", "Environics Oy",
    "Environmental Chemical Corp", "Envision Technology", "Envisioneering Inc.", "EONIC", "EOS", "EPC2 Consortium", "EPE", "EPIIC Consortium", "Eprius", "EPS Corporation", "Epsilon Systems", "ESSI/SEI",
    "Esterline", "Eurofighter", "EuroMIDS", "EUROPAAMS", "Eurosam", "Euroshop SA", "EuroSpike", "Exail", "Excellus Solutions", "Exeter Group", "Extra", "FABREQUIPA", "Fabryka Broni", "FAdeA",
    "Fairchild", "Famae", "FAME SAC", "Fasharkan Ship", "Fassmer", "FAW Group", "FCN Technology Sol", "FEDITC", "Federal Contracting", "FedStore Corp", "FemmeCompInc", "Fenix Air Inc.", "FFA", "FFA Emmen",
    "Firestorm Labs", "Five Rivers Analytics", "Fiat Group", "Fiat-Leonardo", "Flatter Inc.", "Fidelity Technologies", "Fincantieri", "Fischer Panda", "Flensburger Fahrzeugbau", "Flensburger SB",
    "Flight Technologies", "Flightcell Intl", "FLightSafety", "FLIR", "Fluor Marine Propulsion", "Flyer", "Flying Legend", "FMA", "FN Herstal", "FNSS", "Fokker", "Force 3", "Ford Motor Co.",
    "Forum Energy Technologies", "FREIRE Shipyard", "Frequentis GmbH", "Fresia SPA", "Frontgrade Technologies", "Frontier Electronic Systems", "FSC Lublin Auto", "FSUE Neptune", "Fujitsu",
    "Furuno Electric", "G & F Technology", "G1 Aviation", "Gabler Maschine", "GAF", "Game Composites", "Garco Construction Inc.", "Garden Reach SB", "Garmin", "Gate Elektronik", "GC Rieber Shipping",
    "GDELS-Mowag", "GECI", "Gemelli", "Genasys", "GenCorp", "General Atomics Aeronautical Systems", "General Dynamics", "General Electric", "General Motors", "Generic Supplier", "Geneset Powerplants",
    "Georgia Tech", "German Naval Yards", "GESPI", "GFE", "Gibbs & Cox Inc.", "GIDS", "Gilbane Federal", "GKN Aerospace", "Gladding-Hearn", "Global GndSpt LLC", "Global Military Products", "Global Services LLC",
    "Global Tech Res", "Global Technical Sys", "Globecomm", "GMV Aerospace and Defense", "Goa Shipyard Ltd", "Golcuk", "Goodrich Corp.", "Goodyear Tire and Rubber Co.", "Grabba", "Granite-Obayashi",
    "Granta Autonomy", "Grevicom SAC", "Griffon Corporation", "Grob", "GRYFIA", "GTRI", "Guimbal", "Guizhou", "Gulf Island Marine Fabricators LLC", "Gulfstream", "Guyco Inc.", "GZAS", "H2O Guam JV", "Hadean", "Hai Minh Corporation", "Haivision Systems Inc.", "HAL", "Hanjin Indust'l SB", "Hanwha", "Harbin", "Harland & Wolff", "Harper Construction", "Harris", "Harwar International Aviation Technology", "Hatehof", "Hawaiian Rock Products Corp.", "HB Utveckling AB", "HAVELSAN", "HDT Expeditionary Systems", "Head/Diaz 2022", "Heavy Ind. Taxila", "Heckler & Koch", "Helibras", "Helicentro Peru SAC", "Hellenic Aerospace Industries", "Hellfire LLC", "Hensel Phelps Construction", "Hensoldt", "HESA", "HexagonComposite", "Hinduja Group", "Hindustan Ship", "Hi-Q Engineering", "Hisdesat SA", "Hitachi", "Hitachi Kokusai", "Hitzler Werft", "HKV", "Hodges Transportation", "Honeywell", "Hong Ha Shipbuilding", "Hong Leong Group", "Hongdu", "Horizon Technologies", "Hornbeck Offshore Operators", "Howe and Howe", "HP", "HPI Solutions", "HTX Labs", "Hughes Comm", "Humbert Aviation", "Huneed Tech", "Huntington Ingalls", "Huta Stalowa Wola", "HV Joint Venture", "Hydra Technologies", "Hydrema", "Hyundai", "Hyundai J Comm", "IAI", "IAP Worldwide Svc", "IAR", "IBM", "ICF", "Icom Inc.", "ICOMM Tele Ltd.", "IdeaForge", "iGOV", "IHI", "II-VI Aerospace and Defense", "Ilyushin", "ImagineOneT&M", "IMBEL", "IMC Group", "IMCO", "immixGroup", "IMMSI SPA", "IMPSA", "Imtech Marine", "INACE", "Indonesian Aerospace", "Indra", "Indrasoft", "INDUS Technology", "InDyne", "InfoReliance Corp", "Infotron", "Inmarsat", "Innocon", "Innnovaero", "Insitu", "Insta ILS", "Institute of International Education", "INTA", "Integ Surv Tech", "Integral Consulting Services", "Integral Systems", "Integrated Convoy", "Integrated Defense Solutions/Greit", "Integrated Dynamic", "Integrated Dynamics", "Integrated Surveillance and Defense", "Integration Innovation", "Intelligent Decisions", "Intelligent Waves", "INTELSAT", "Inter-Coastal Electronics", "InterCaribbean Airways", "Intermarine", "International Business Machines Corp.", "Intl Shipholding Corp", "Intman SA", "Intracom SA", "INVAP", "Invariant Corp.", "INVISIO", "IOMAX", "IPS Inc", "Iridium Satellite", "Iron Bow Tech", "Irving Shipbldg", "Israel Military Industries", "Israel Shipyards", "ISRO Internal", "Istanbul Shipyard", "Isuzu Motor Co", "Italcantieri", "Italtel", "Italthai Marine", "ITG", "ITI Limited", "ITP Aero", "ITT", "Iveco Defence Vehicles", "Iveco-Oto Melara Consortium", "IVEMA", "IWI", "IXBlue", "Izhmash Unmanned Systems", "Jacobs Eng Group", "Jacobs/B&V JV", "James Fisher", "Jankel", "Japan Marine United", "Japan Steel Works", "Javelin JV Team", "JCB", "Jelcz-Komponenty", "Jet Tekno", "JetZero", "JF Taylor", "JHU/APL", "Joby Aviation", "Johns Hopkins University", "Jong Shyn Ship", "JRC Group", "JSC Almaz-Antey", "JSC Kurganmashzavod", "JSC Tactical Missiles Corp", "Junghans Microtec", "Jupiter Wagons Ltd.", "KADDB", "Kader", "KAI", "Kaman", "KAMAZ", "Kamov", "Kangnam Corp", "Karachi Shipyard (KSEW)", "Katmai Management Services", "Katmerciler", "KATO Engineering", "Kawasaki", "Kay and Associates", "Kazakhstan Eng", "Kazan", "KBM Kolumna", "KBP Instrument", "KBR", "Kearfott Corp", "Keppel Corp", "Kerametal", "Kership", "Khan ResLabs", "Kharkiv Morozov", "Khulna Shipyard", "Kiewit-Alberici SIOP MACC", "King ICT", "King Technologies", "KIRINTEC", "KNDS", "Knight Sky", "Knights Armament Co.", "Koam Engineering", "Koc Group", "KomatsuIndustries", "Kongsberg", "KONSTRUKTA", "Kord Technologies", "Korea Shipbuilding & Offshore Engineering", "Korte Construction", "Agency for Defense Development", "Korean Air Aerospace Division", "KRAS - India", "Krasmashzavod", "Kratos Defense", "Kronshtadt Group", "Krauss-Maffei Wegmann", "Kryukov Car Bldg", "KT Consulting", "KVH Industries", "Kyndryl Finland", "L3 Technologies", "Lancair", "Landmarc", "Lane Construction Corp.", "Larsen & Toubro", "Leidos", "Leonardo", "LET", "Level 3 Comm", "Life Cycle Engineering", "LG Group", "LIG Nex1 Co", "LinQuest Corp", "LinTech Pragmatics JV", "Lite Comms LLC", "Lockheed Martin", "Loc Performance Products", "LOM PRAHA", "Long Wave Inc", "Longbow LLC", "Loral", "Lumen", "Lumenier", "Lung Teh Shipbldg", "Lurssen Group", "Lutch", "Lutsk", "M Ship Co", "M1 Support Services", "M2 Technologies", "M7 Aerospace", "Mach Industry Grp", "Mack Defense", "Mackay Comm", "MAESTRAL", "Maestranza AMSU", "MAG Aerospace", "Magellan Aerospace Corporation", "Mahindra", "MA Mortenson", "MAN", "Manhattan Construction", "ManTech", "Mapiex Aviation", "Marine Alutech Oy", "Marine Hydraulics", "Marine United", "MarineTec", "Marinette Marine Corp.", "MARS Shipyards", "Marsh Aviation", "Marshall Aerospace", "MARSS", "Marsun Company", "Martifer Group", "Marvin Land System", "Mastodon Design", "Mathtech", "Maule Air", "MAV", "Maxar Technologies", "Mazagon Dock", "MBB", "MBDA", "McCrone Associates", "McDermott Marine", "McLean Contracting", "MD Helicopters", "MDA Space", "MDT Armour", "MechDB S Africa", "Mectron", "MEDAV GmbH", "Mercedes-Benz", "Mercer Engineering Research Centre", "Mercury Systems Inc.", "Merlin Labs Inc.", "Merwede", "Mesko", "MESIT holding", "Messer Construction", "Metal Shark", "MetalCraft Marine", "Metalnor SA", "Meyer Werft", "Michelin", "Micro Aviation", "Microdis Electronics", "Micropol Fiberoptic AB", "Microsoft", "MicroTech", "Middle East Def", "Mikal Group", "Mikoyan", "Mil", "MilDef", "Milenium Veladi Corp.", "Millenium Space", "MilSOFT Software", "MineWolf Systems", "MISC Berhad", "Mission1st", "Mistral Inc.", "Mitie", "Mitsubishi", "Mitsui SB", "MKEK", "MMIST", "MNDI Pacific JV", "MO Porte-Avions", "Modern Technology Solutions", "Moller-Maersk", "Moog Inc.", "MorseCorp Inc.", "Morye Shipyard", "Motorola Solutions", "MSI", "Mudry", "Mugin", "MVL USA", "MW Builders", "Mythics", "Nakilat", "Nakupuna Consulting", "NAMC", "Nammo", "Nan Inc.", "Nanchang", "National Academy of Sciences of Belarus", "National Steel and Shipbuilding", "Natl Radio Telecom", "Nautica Nova", "Naval Gijon Ship", "Naval Group", "Naval Shipyard Gdynia", "Navantia", "Naviris", "Navistar International", "Navmar", "NCI Info Sys", "NCSIST", "ND Defense", "NDMA", "NEC", "Neiva", "Neorion Group", "NES Associates", "NetCentrics Corp", "Netline Comm", "New Directions Technologies", "NewSpace India", "NEWTEC", "Nexter", "NGV Tech", "NH Industries", "NICCO Comm", "Nigerian Dockyard", "NII STT", "Niigata Shipbuilding", "NIMR Auto", "Nissan", "nLIGHT Nutronics", "Noble Supply and Logistics", "Noblis MSD", "Nokia", "Nordic Terrain Solutions", "Norinco", "Norma Precision AB", "Nortel", "North Sea Boats", "Northrop Grumman", "Northstar Aviation", "Nostromo", "Novadem", "NP Aerospace", "NPO Elektro'ka", "NPO Lavochkin", "NRL", "NSSL", "NSWC", "NT Service", "NTConcepts", "nTSI", "NTT Group", "NUBURU", "Nurol Co.", "NVL Group", "Oakwell Engineer", "OBRUM", "OCEA Group", "Ocean Shipholdings", "Ocean Tech Sys", "Oceaneering", "OCR Global", "Odebrecht Group", "Odyssey Systems Consulting Group", "OGMA", "OHB System AG", "OIP Land Systems", "Old North Utility Services", "Olin Winchester", "Omnisec AG", "Omnisys", "Ondas", "Optics1 Inc.", "Optima Government Solutions", "Orbit Technologies", "Orizzonte Sistemi Navali", "Orskov Group", "Oshkosh", "OSI", "Otobus Karoseri", "Otokar", "OTT Technologies", "Out of Business", "Overaasen AS", "Ovzon", "PAC", "Paccar", "Pacific Aerospace", "Pacific Rim Constructors", "Pacifics Propeller International", "PAE Aviation and Technical Services", "Pakistan Aeronautical Complex", "Palantir Technologies", "Palantir USG", "Palfinger", "PAMA-SP", "PanAmSat", "Panavia", "Panha", "Paramount Group", "Parker-Hannifin", "Parrot", "Parsons Government Services", "Patria", "Patriot Contract Svcs", "PCCI", "PCM", "Pearson Engineering", "Peerless Technologies", "Pelatron", "Pelegrin", "Penman Company", "Peraton Technology Services", "Persistent Systems", "Peterson Bldrs", "PGSUS", "PGZ", "PGZ-PILICA Consortium", "PGZ-NAREW Consortium", "Phacil Inc", "Phoenix Air Group", "Philadelphia Yard", "Philippine Telephone", "Piaggio", "Pilatus", "Pindad", "Piper", "Pipistrel", "Piriou Naval Svcs", "PJ Aviation", "PKL Services", "Plath", "PN Dockyard", "Polaris Industries", "Polish Defence Holding", "Polska Grupa", "Polskie Zaklady Lotnicze", "Poly Technologies", "Polyot", "Polysentry", "Pragmatics", "Presidio", "Priboy", "PRIMA Research", "Proforce Defence", "Programs Management Analytics and Technologies", "Propmech Corp", "Prox Dynamics", "PS Engineering", "PSI", "PSM", "PT Batam", "Pt Bhinneka Dwi Persada", "PT Citra Barahi Shipyard", "PT Daya Radar Utama", "PT Dirgantara", "PT Dumas Shipyard", "PT Kodja Bahari", "PT PAL Indonesia", "PT Palindo", "PT Republik Defensindo", "PZL-Mielec", "PZL-Okęcie", "PZL-Swidnik", "Q-Techn LLC", "Qbase, LLC.", "QED Systems Inc", "QinetiQ", "Qioptiq", "Qods Aviation Industries", "Quad City Aircraft", "QualX Corp.", "Quantum Research", "Quantum Systems", "QuantX Labs", "Qwest", "R&W Contractors", "Radiance Tech", "Radmor SA", "Rafael", "RAM Systems", "RAMET", "Range Generation Next", "Rannoch Corp", "Rauma Marine", "Ravenswood Solutions Inc.", "RAVN Group", "Raytheon Technologies", "RC Construction", "Rebellion Defense", "ReconCraft LLC", "Record Steel & Construction", "Red Peak Technical Services", "Red River Computer", "Redflex Group", "Redwire", "Regional One", "Reims-Cessna", "Reiser", "Reliance Defence", "Reliance Test and Technology", "Remdiesel", "Remontowa Group", "Remoy Shipping", "Renk America", "Repkon USA-Defense", "Reshetnev Company", "Ressenig", "Reunert", "Revolution Aviation", "Rh-Alan", "RHEA Group", "Rheinmetall", "Rheinmetall BAE Systems Land", "Rheinmetall Denel", "Rheinmetall MAN", "Ribcraft USA", "Ricardo PLC", "Riga Shipyard", "RIO Design Bureau", "Rio Santiago Shipyard", "Rise8 Inc.", "RiverHawk Group", "Robertson Fuel Systems", "Robin Radar Systems", "Robinson", "Roboteam", "Rocket Lab National Security LLC", "Rockwell Collins", "Rodman Group", "Rohde & Schwarz", "Roke", "Roketsan", "Rolls-Royce plc", "Roman Brasov", "ROMARM", "Rosomak", "Rostec", "Rothe Development", "Rovsing A/S", "RQ Construction", "RS-UAS", "RTX", "RUAG", "RV Connex", "RWG Repair & Overhauls USA", "Saab", "Sabiex Group", "Sabre Systems", "Sabreliner Corporation", "SAFAT", "Safe Boats Intl", "Safran", "Sagemcom", "SAIC", "Sako", "SAL", "Salient CRGT Inc", "Sallyport Global Holdings", "SAN", "San Yang", "Sandia Nat Labs", "Sanmina-SCI", "Sanska", "Santana Motors", "Santierul Naval", "SANUKI Shipbldg", "SAPURA", "Sapura Thales", "Sarco Defense", "Sasebo Heavy Ind", "Satuma", "Savox Communications", "SBIC", "Scandinavian Avionics", "Scania", "Scheepvaart KB", "Schiebel", "Schweizer", "Schutt Industries", "Science and Engineering Services", "Science Applications International", "Scientia Global", "Scientific Research Corp.", "Scorpene JV", "SCOTTY Group", "SCR", "SEA", "Seabird Aviation", "Sealift Inc", "Seaspan Marine", "Seaward Marine Services", "Second-Hand", "Sectra Comm Sys", "SecuriGence", "Sedef Shipbuilding", "Seed Innovations", "Seemann Composites LLC", "Sefine Shipyard", "Segue Technologies", "Selah Shipbuilding", "SELEX Elsag", "Selex ES", "SEMAN Peru", "SEPECAT", "SEPI", "Sepura", "Serbian State", "Serco Group plc", "SES", "SETEL/REMSCO", "SGJV", "Shaanxi", "Shaanxi Auto Grp", "Shenyang", "Shijiazhuang", "Shin Maywa Industries", "Shin Yang", "Shoft Shipyard", "Short Brothers", "SI Systems Technologies", "SICC", "Sielman S.A.", "Siemens", "Sierra Nevada", "SIG Sauer", "Sigen Consortium", "Sikorsky", "Silent Sentinel", "Silver Ships Inc.", "SIMA Peru", "Singapore Tech.", "SingTel Group", "SISDEF", "Sistemprom", "Sisu Auto", "SITAB Consortium", "SK Holdings", "Skanska", "SkyAlyne", "Skydio", "Slingsby", "SmartShooter", "Smartronix Inc", "SMS Data Products", "SNC-Lavalin", "SNVI", "Sobeca", "Soby Vaerft", "Socarenam", "Socata", "Sodexo Management Inc.", "SOFIS-TRG", "SOFRAME", "Sojitz Corporation", "Soko", "Solar Industries", "Solers", "Solstad Offshore", "SONAK", "Sonalysts Inc.", "Songthu Corporation", "Southern African Ship", "Southern Maryland Electric Cooperative", "Southern Resc'h", "Southwest Resc'h", "Soviet Tank Plant", "Sozvezdie JSC", "SPA", "Spaceflux", "SpaceX", "Spanish Missile Systems", "Sparton De Leon Springs LLC", "Special Technology Ctr", "Spectra", "Spectrum Comm", "SpearUAV", "SpeedCast", "Sprint", "SR Telecom", "SRC", "SRCTec", "ST Aerospace", "StandardAero Inc.", "Stark Aerospace", "Stauder Technologies", "Sterling Computers", "Steyr", "STG", "Stinger ProjectGP", "STM Group", "Streit Group", "STS International", "STX Corporation", "Subaru", "Submarine Manufacturing and Products", "Sukhoi", "Sumaria Systems", "Sumidagawa Ship", "Sumitomo", "Summit Aviation", "Sunair", "Supacat", "Superior Govt Sol", "Superior Marine Ways", "Surrey Satellite Technology", "Survey Copter", "Suzuki Motor Corp", "SVI Engineering", "Swan Hunter", "Swecon", "Swede Ship", "SwedishSpace Cp", "Swiftships SB LLC", "Symetrics", "Synectic Group", "Sypaq Systems", "Sypris Solutions", "Sys for Def/GVS", "System Studies & Simulation", "Systematic", "Systems Planning and Analysis", "T. Mariotti", "Tactical Air Support Inc.", "Tactical Engineer", "TADANO", "TAE Aerospace", "TAI", "Talbert Manufacturing Inc.", "Target Technologia", "Taskizak Shipyard", "TAT Technologies", "Tata Advanced Systems", "Tata Group", "TATRA", "Taurus Systems", "Taylor Defense Products", "TCG", "TCIL", "TDW GmbH", "TDX International", "Technica Corp", "Technical Comms", "Technology Unlim", "Tecnam", "TECNOBIT", "Tekever", "Telecomm Systems", "Teledyne", "Teledyne FLIR", "Telephonics Corp.", "Telespazio", "Teletronics Technology", "Telia Finland", "Tellumat", "Telos Corp", "Telstra", "Terberg Group", "Terma A/S", "Tesat Spacecom", "TESCO INDOMARITIM", "TESLA", "TESS Defence", "Tesseract Ventures", "TETRAEDR", "Texas A&M", "Textron", "Thales", "Thales Alenia Sp", "ThalesRaytheon", "The MIL Corp.", "The Whiting-Turner Contracting Co.", "TWPG", "THEON International", "ThirdEye", "Thoma-Sea Ship", "Thrane & Thrane", "Threod Systems", "Thuraya", "ThyssenKrupp AG", "Timken Gears & Services", "Titan Aircraft", "TKC Global Solutions", "TNO", "Tobyhanna Army", "Tomahawk Robotics", "Top Aces", "Toshiba", "Toyota Motor Corp", "Trans-Ce Cargo SA", "Transall", "Transas Group", "Transbit", "Transfield Services", "TRAX International", "TrellisWare Tech", "Trideum Corp", "Triman Industries", "Triton Group Hold", "TRU Simulation Plus Training", "TRX System", "TSS Solutions", "TTC TELEKOM", "TUBITAK", "Tupolev", "Turkish AFF", "Turner Construction", "Twin Commander Aircraft", "TYBRIN", "Tyco Intl", "Tyovene", "Tyto Athene", "Tyvak International", "UAV Communications", "UAV Solutions", "Uavision Aeronautics", "UCOCAR", "Uconsystem", "UK Docks Marine Services", "Ukraine Weapons", "UkraineTank Plant", "Ukroboronprom", "Ukrspecsystems", "Ulijanovsk", "UltiSat", "Ultra Dimensions Pvt. Ltd.", "Ultra Electronics", "Ultra I&C", "Ultra Maritime", "UMM", "Umoe Group", "Unicom", "Unicom Government", "Unknown", "Unified Industries", "UNIMO Technology", "Unimor Radiocom", "Unisys", "Unit Co.", "United Crane and Excavation Inc.", "United Electronics", "United Launch Alliance", "Univ of Texas", "Univ of Toronto", "Universal Shipbldg", "Unman'dDynamics", "Ural Works Civil Aviation", "Uralvagonzavod", "URC Systems", "UROVESA", "US Marine Inc", "US Ordnance", "USCG YARD", "UTVA", "UVision Global Aero", "Valero Marketing and Supply", "Valiant Global Defense", "Valkyrie Aero", "Van's Aircraft", "Multiple", "Vector Scientific", "Vector Solutions", "Vectrus Systems Corp.", "Vega Company", "Vencore", "Veritas Capital", "Verizon", "Vertex Aerospace", "Vertex Standard", "Vestel", "ViaSat Inc", "Victory Solutions Inc.", "VideoRay LLC", "Viettel Group", "Vigor Industrial", "Viking Air", "Viking Arms", "Vimpel", "Vladimir Radio", "Volkswagen Group", "Volvo Group", "Von Wolf", "VOP 025", "VOP 026 Sternberk", "VPK", "VSE Corp.", "Vulcanair", "V2X", "Walsh Federal LLC", "Wartsila", "Watterson Construction Co.", "WB Electronics", "WBA Blindajes Alemanes", "West Sea Shipyard", "Weststar Group", "WG Yates and Sons", "Wildflower Intl", "Windmill Intl", "World Wide Tech", "WULCO Inc.", "WZE", "WZM", "X-Bow", "Xian", "Xian ASN Technical Group", "XTAR", "Yakovlev", "Yamaha", "Yaroslavl Radio", "Yeonhab Precision", "Yokohama Yacht", "Yoland Corp.", "Yonca-Onuk", "Yugoimport-SDPR", "Zala", "Zamil Offshore", "Zen Technologies", "Zenair LTD", "Zenit Shipyard", "Zenith", "Zlin", "Zwijnenburg", "ZyXEL Comm", "Hydroid Inc", "West Coast JV,", "University of Dayton Research Institute", "Saguaro Business Solutions LLC", "Learjet", "General Dynamics Electric Boat", "Ball Aerospace & Technologies", "TCOM", "Raytheon Missiles and Defense", "Lockheed Martin Missile and Fire Control", "EFW", "Amherst Systems", "Lockheed Martin Sippican", "Hamilton Sundstrand", "Northrop Grumman Aerospace", "R.A. Burch Construction", "Lockheed Martin – Rotary and Mission Systems", "Trace Systems", "Northrop Grumman Space Systems Sector", "L-3 Communications Integrated Systems", "Flint Electric Membership", "Gray Analytics", "Lockheed Martin Aeronautics", "Lockheed Martin Space", "LTM Inc", "Alberici-Mortenson", "Atlantic Signal", "Haight Bey & Associates", "Container Research Corp", "Essex Electro Engineers", "TechFlow Mission Support", "Chugach Range and Facilities Services", "Raytheon Space and Airborne Systems", "Innovative Scientific Solutions", "Delavan", "Covalus", "Chromalloy Component Services", "Armorworks Enterprises", "Metro Machine", "Alloy Surfaces", "Valley Tech Systems", "Keysight Technologies", "Azure Summit Technology", "Isometrics", "Stratascorp", "Synergy Electric Company", "Custom Manufacturing & Engineering", "East West Industries", "MPR Associates", "ARCTOS Technology Solutions", "Enlighten IT Consulting", "Barrett Firearms", "Ametek Programmable Power", "Applied Physical Sciences", "SupplyCore", "Federal Resources", "General Atomics", "Penguin Computing", "Mancon", "Integrated Marine Services", "Compass Systems", "DRS Sustainment Systems", "IronMountain Solutions", "Ball Aerospace & Technologies", "Yulista Services", "SyQwest", "Advanced Technology Systems", "Cleveland Construction", "Canadian Commercial Corp", "Systima Technologies", "Ocean Ships", "Metro Machine Corp", "ImSAR LLC", "Systems Application & Technologies", "Twin Disc", "Konecranes Nuclear Equipment and Services", "Progeny Systems", "WEBCO", "REEL COH", "Waterman Transport", "Western Metal Supply", "Security Signals", "Wolverine Tube", "BC Customs LLC", "TLD America", "Crane Technologies Group", "IDSC Holdings", "AAR Manufacturing", "B & D Electric", "Vector CSP LLC", "Accurate Machine & Tool Corp", "Mississippi State University", "Stephenson Stellar Corp", "Earthly Dynamics", "Woolpert Inc", "Halter Marine", "Marion Manufacturing", "FN America LLC", "CDM Constructors", "Florida State University - Center for Advanced Power Systems", "International Marine & Industrial Applicators", "Zodiac-Poettker HBZ JV II LLC", "DigiFlight", "Globe Composite Solutions", "Meggitt Polymers and Composites", "Martin-Baker Aircraft", "United Kingdom Ministry of Defence", "Ultimate Training Munitions", "PAS Technologies", "DCM Clean Air Products", "Management Services", "Technology Service Corp", "General Electric Aviation", "ACME/RHB", "Howell Industries", "Airdyne Aerospace", "Dominion Energy", "Bionetics", "Choctaw Defense Manufacturing", "Centauri", "DRS Naval Power Systems", "Sentry View Systems", "ERAPSCO", "AAR Government Services", "Management Services", "L3 Doss Aviation", "AgustaWestland Philadelphia", "Marvin Engineering", "Collins Elbit Vision Systems", "FGS", "Navistar Defense LLC", "Voith Hydro", "Delfasco"
]

PROGRAM_TYPES = [
    "Training", 
    "Procurement", 
    "MRO/Support", 
    "RDT&E",
    "Upgrade", 
    "Other Service",
    "Unknown"
]

DOMESTIC_CONTENT_OPTIONS = [
    "Indigenous", 
    "Imported", 
    "Local Assembly", 
    "License Production"
]