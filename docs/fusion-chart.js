const SMT5_FUSION_CHART = {
  "races": [
    "Deity",  "Megami", "Genma",  "Yoma",   "Fairy",  "Night",  "Tyrant", "Dragon", "Snake",  "Drake",  "Avatar", "Holy",   "Beast",  "Wilder", "Fury",   "Lady",   "Kishin", "Wargod", "Kunitsu","Vile",   "Herald", "Divine", "Fallen", "Avian",  "Raptor", "Femme",  "Brute",  "Jaki",   "Jirae",  "Haunt",  "Foul",   "Fiend"
  ],
  "table": [
    ["-"],
    ["Herald", "Aquans"],
    ["Wargod", "Avian",  "-"],
    ["Fairy",  "Avatar", "Night",  "Aeros"],
    ["Genma",  "Wargod", "Deity",  "Divine", "Aeros"],
    ["Lady",   "Femme",  "Lady",   "Divine", "Divine", "Erthys"],
    ["-",      "-",      "-",      "Vile",   "Haunt",  "Yoma",   "-"],
    ["Kunitsu","Lady",   "Night",  "Genma",  "Night",  "Foul",   "-",      "-"],
    ["Beast",  "Wargod", "Wargod", "Night",  "Avian",  "Yoma",   "Drake",  "Fallen", "Flaemis"],
    ["-",      "-",      "-",      "Night",  "Femme",  "Femme",  "Wilder", "-",      "Wilder", "Flaemis"],
    ["-",      "Deity",  "Deity",  "Jirae",  "Kishin", "Beast",  "-",      "Fury",   "Dragon", "-",      "Aquans"],
    ["Wargod", "Avian",  "Fairy",  "Beast",  "Beast",  "Jirae",  "-",      "Wargod", "Dragon", "-",      "-",      "Aeros"],
    ["Avatar", "Fallen", "Holy",   "Holy",   "Night",  "Wargod", "Wilder", "Wilder", "Wilder", "Foul",   "Jirae",  "Avian",  "Erthys"],
    ["-",      "-",      "-",      "Beast",  "Holy",   "Brute",  "Drake",  "-",      "Drake",  "Avian",  "-",      "-",      "Fairy",  "Aquans"],
    ["-",      "-",      "-",      "-",      "-",      "-",      "-",      "-",      "-",      "-",      "-",      "-",      "-",      "-",      "-"],
    ["Holy",   "Deity",  "Kunitsu","Haunt",  "Genma",  "Femme",  "-",      "Fury",   "Femme",  "-",      "Dragon", "Deity",  "Snake",  "-",      "-",      "Erthys"],
    ["Fury",   "Genma",  "Brute",  "Tyrant", "Kunitsu","Tyrant", "-",      "Wargod", "Dragon", "-",      "Dragon", "Brute",  "Avatar", "-",      "-",      "Femme",  "-"],
    ["Kishin", "Deity",  "Deity",  "Kishin", "Genma",  "Beast",  "-",      "Snake",  "Kishin", "-",      "Genma",  "Kishin", "Fallen", "-",      "-",      "Kishin", "Fury",   "-"],
    ["Fury",   "Femme",  "Lady",   "Genma",  "Yoma",   "Beast",  "-",      "Snake",  "Dragon", "-",      "Dragon", "Fairy",  "Holy",   "-",      "-",      "Jirae",  "Fury",   "Deity",  "Flaemis"],
    ["-",      "-",      "-",      "Jaki",   "Jaki",   "Tyrant", "Jaki",   "-",      "Drake",  "Wilder", "-",      "-",      "Wilder", "Raptor", "-",      "-",      "-",      "-",      "-",      "-"],
    ["-",      "-",      "-",      "-",      "-",      "-",      "-",      "-",      "-",      "-",      "-",      "-",      "-",      "-",      "-",      "-",      "-",      "-",      "-",      "-",      "-"],
    ["Herald", "Avian",  "Wargod", "Fallen", "Megami", "Megami", "Vile",   "Fallen", "Fallen", "Raptor", "Fairy",  "Avatar", "Brute",  "Raptor", "-",      "Fairy",  "Snake",  "Holy",   "Yoma",   "Tyrant", "-",      "Aeros"],
    ["Fury",   "Foul",   "Vile",   "Fairy",  "Night",  "Brute",  "Drake",  "Snake",  "Dragon", "Raptor", "Snake",  "Beast",  "Jirae",  "Raptor", "-",      "Femme",  "Dragon", "Lady",   "Fairy",  "-",      "-",      "-",      "Flaemis"],
    ["Holy",   "Herald", "Holy",   "Divine", "Megami", "Raptor", "-",      "Avatar", "Kunitsu","-",      "Herald", "Avatar", "Fairy",  "-",      "-",      "Fury",   "Kunitsu","Avatar", "Lady",   "-",      "-",      "Yoma",   "Raptor", "Aeros"],
    ["-",      "-",      "-",      "Divine", "Megami", "Megami", "Vile",   "-",      "Vile",   "Beast",  "-",      "-",      "Fairy",  "Beast",  "-",      "-",      "-",      "-",      "-",      "Drake",  "-",      "Avian",  "Tyrant", "-",      "Aeros"],
    ["Snake",  "-",      "Kunitsu","Haunt",  "Lady",   "Brute",  "Jaki",   "Fallen", "Drake",  "Foul",   "-",      "Jirae",  "Night",  "-",      "-",      "Brute",  "Jirae",  "Fallen", "-",      "Jaki",   "-",      "Megami", "Lady",   "-",      "Divine", "Aquans"],
    ["Jirae",  "Femme",  "Kishin", "Jaki",   "Femme",  "Femme",  "Jaki",   "Kunitsu","Dragon", "Haunt",  "Kunitsu","Jaki",   "Femme",  "-",      "-",      "Kishin", "Femme",  "Fallen", "Kishin", "Jaki",   "-",      "Jirae",  "Night",  "Genma",  "Haunt",  "Fallen", "Aquans"],
    ["-",      "-",      "-",      "Haunt",  "Jirae",  "Jirae",  "Vile",   "-",      "Drake",  "Brute",  "-",      "-",      "Jirae",  "-",      "-",      "-",      "-",      "-",      "-",      "Haunt",  "-",      "Fairy",  "Drake",  "-",      "Wilder", "Haunt",  "Foul",   "Flaemis"],
    ["Brute",  "Lady",   "Night",  "Fairy",  "Wargod", "Fairy",  "Night",  "Lady",   "Fallen", "Jaki",   "Holy",   "Beast",  "Yoma",   "Beast",  "-",      "Kishin", "Femme",  "-",      "Lady",   "Jaki",   "-",      "Fallen", "Dragon", "Yoma",   "Divine", "Kunitsu","Fairy",  "Brute",  "Erthys"],
    ["-",      "-",      "-",      "Brute",  "Femme",  "Yoma",   "Jaki",   "-",      "Drake",  "Foul",   "-",      "-",      "Wilder", "Drake",  "-",      "-",      "-",      "-",      "-",      "Tyrant", "-",      "Jaki",   "Yoma",   "-",      "Jirae",  "Brute",  "Foul",   "Megami", "Femme",  "Aquans"],
    ["-",      "-",      "-",      "Jirae",  "Wargod", "Yoma",   "Haunt",  "-",      "Beast",  "Haunt",  "-",      "-",      "Wilder", "-",      "-",      "-",      "-",      "-",      "-",      "Tyrant", "-",      "Fallen", "Divine", "-",      "Wilder", "Brute",  "Haunt",  "Brute",  "Fairy",  "Drake",  "-"],
    ["Herald", "Vile",   "Deity",  "Night",  "Jaki",   "Femme",  "Vile",   "Drake",  "Drake",  "Avian",  "Dragon", "Fairy",  "Wilder", "Foul",   "-",      "Megami", "Brute",  "Kishin", "Fury",   "Tyrant", "-",      "Jirae",  "Tyrant", "Kunitsu","Beast",  "Lady",   "Haunt",  "Haunt",  "Night",  "Fallen", "Tyrant", "-"]
  ]
}