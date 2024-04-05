# Megami Tensei Fusion Tools - How to Use
## Navigation
* [All Fusion Tools](https://aqiu384.github.io/megaten-fusion-tool/home)
* [How to Use](./how-to-use)
* [Report Issue](https://github.com/aqiu384/megaten-fusion-tool/issues)

## General
* Demon/Persona List
  * Green: Special fusion recipe
  * Red: Non-standard fusion recipe
    * Fusion accident
    * Recruitment only
    * Party member
    * Enemy only
* Skill List
  * Red: Non-inheritable skill
* Fusion Settings
  * Add/remove unlockable demons from fusion calculations (enabled by default)
  * Add/remove DLC demons from fusion calculations (disabled by default)

## Save Offline
### iOS
1. Navigate to the [Megami Tensei Fusion Tools homepage](https://aqiu384.github.io/megaten-fusion-tool/home)
2. Add page to Home Screen: Safari > Action (Share) > Add to Home Screen > Add
3. Open the downloaded page from the Home Screen
4. Navigate to the skills page of each desired game (e.g. [List of Skills - Persona 5 Royal](https://aqiu384.github.io/megaten-fusion-tool/p5r/skills))
5. Close the downloaded page and disable Wi-Fi and Cellular Data
6. Reopen the page from the Home Screen and ensure each downloaded game is still accessible
7. Reenable Wi-Fi and repeat steps 4-6 if game does not load offline

## Shin Megami Tensei
### Data Sources
* http://ifs.nog.cc/fool-est.hp.infoseek.co.jp/shin_dds/index.html
* https://kaerukyo.net/dds_database/skill.php?title=3

## Shin Megami Tensei II
### Data Sources
* http://ifs.nog.cc/fool-est.hp.infoseek.co.jp/shin_dds2/index.html
* https://kaerukyo.net/dds_database/skill.php?title=4

## Shin Megami Tensei If...
### Data Sources
* http://ifs.nog.cc/fool-est.hp.infoseek.co.jp/shin_if/index.html
* https://kaerukyo.net/dds_database/skill.php?title=5

## Shin Megami Tensei NINE
### Data Sources
* http://ifs.nog.cc/fool-est.hp.infoseek.co.jp/shin_nine/index.html
* https://kaerukyo.net/dds_database/skill.php?title=17
* http://softtank.web.fc2.com/nine_index.html
* http://ゆめのしま.jp/nine.html

## Shin Megami Tensei IMAGINE
### Data Sources
* https://wikiwiki.jp/imagine/
* http://megatenonline.wiki.fc2.com/wiki/
* http://megaten.sesshou.com

## Shin Megami Tensei III: Nocturne
### Data Sources
* *Shin Megami Tensei III: Nocturne Maniax Ally Demon Compendium* (ISBN-13: 9784797326789)
* *Shin Megami Tensei III: Nocturne HD Remaster Official Perfect Guide* (ISBN-13: 9784047335141)
* http://www.phpsimplicity.com/heretic/
* https://pathshower.wordpress.com/smt/nocturne/
* http://ifs.nog.cc/fool-est.hp.infoseek.co.jp/shin_dds3/

## Shin Megami Tensei: Strange Journey
### Cheap Password Demons
* Passwords allow you to summon demons with stats and levels less than their default, decreasing their price and providing cheap fusion ingredients
* Some higher-end demons like Alilat with their stats capped will overflow the max price and come out to around a couple thousand
* Can also summon boss-exclusive demons with their corresponding passwords

### Shin Megami Tensei: Strange Journey Redux
* Womb of Grief added
* New endings added for all routes
* Password price overflow and boss-exclusives fixed

### Data Sources
* https://gamefaqs.gamespot.com/ds/961651-shin-megami-tensei-strange-journey/faqs/59384
* https://docs.google.com/spreadsheets/d/1R0Uq9YAW0yVwwHk020y6dLYR-EIsLOlIId05JFZpJcM
* https://github.com/yuggrdrasill/megaten-sj-pw-generator

## Shin Megami Tensei IV
### Data Sources
* https://erikku.github.io/smt4tool/
* https://gamefaqs.gamespot.com/3ds/672441-shin-megami-tensei-iv/faqs/67766

### Fusion Accident Skill Inheritance
* If demons A x B = C, but produces a fusion accident resulting in D instead
  * D's first 4 skills will be the highest ranked from the combined ABCD skill pool
  * D's last 4 skills will be randomly picked from the same pool
* If D is of the Famed race
  * D will inherit all of its innate skills
  * D will pick the highest ranked from ABC's skill pool for the rest

## Shin Megami Tensei IV Apocalypse
* Zealot made fusion accident exclusive
* Unique skills added to fusion accident inheritance pool

### Data Sources
* http://gamers-high.com/megami4-final/

### Skill Affinities
| Rank | Attack              | Ailment             | Recovery             | Support   |
| ---- | ------------------- | ------------------- | -------------------- | --------- |
| 9    | Dmg +70%, Cost -20% | Hit +35%, Cost -20% |                      |           |
| 8    | Dmg +60%, Cost -20% | Hit +30%, Cost -20% |                      |           |
| 7    | Dmg +50%, Cost -20% | Hit +25%, Cost -20% |                      |           |
| 6    | Dmg +40%, Cost -20% | Hit +20%, Cost -20% |                      |           |
| 5    | Dmg +30%, Cost -20% | Hit +15%, Cost -20% | Heal +45%, Cost -20% | Cost -50% |
| 4    | Dmg +30%, Cost -10% | Hit +15%, Cost -10% | Heal +45%, Cost -10% | Cost -40% |
| 3    | Dmg +20%, Cost -10% | Hit +10%, Cost -10% | Heal +30%, Cost -10% | Cost -30% |
| 2    | Dmg +10%, Cost -10% | Hit +5%, Cost -10%  | Heal +15%, Cost -10% | Cost -20% |
| 1    | Dmg +10%            | Hit +5%             | Heal +15%            | Cost -10% |
| -1   | Dmg -10%            | Hit -10%            | Cost +10%            | Cost +10% |
| -2   | Dmg -20%            | Hit -20%            | Cost +20%            | Cost +20% |
| -3   | Dmg -30%            | Hit -30%            | Cost +30%            | Cost +30% |
| -4   | Dmg -40%            | Hit -40%            | Cost +40%            | Cost +40% |
| -5   | Dmg -50%            | Hit -50%            | Cost +50%            | Cost +50% |
| -6   | Dmg -60%            | Hit -60%            |                      |           |
| -7   | Dmg -70%            | Hit -70%            |                      |           |
| -8   | Dmg -80%            | Hit -80%            |                      |           |
| -9   | Dmg -90%            | Hit -90%            |                      |           |

### Unique Skills Fusion Accident Exploit

## Shin Megami Tensei V
### Data Sources
* *Shin Megami Tensei V Official Perfect Guide* (ISBN-13: 9784047335806)
* https://hyperwiki.jp/smt5/
* https://dswiipspwikips3.jp/shin-megami-tensei-5/

### Formulas
* Recovery skill heal amount: \[(Skill base dmg) + (Skill boost %) * (Target max HP)\] * (Recovery skill potential heal boost) * (Heal pleroma boost) * (Bowl of Hygieia boost)

### Skill Potentials
| Rank | Attack              | Ailment             | Recovery             | Support   |
| ---- | ------------------- | ------------------- | -------------------- | --------- |
| +9   | Dmg +55%, Cost -40% | Hit +60%, Cost -40% |                      |           |
| +8   | Dmg +47%, Cost -34% | Hit +50%, Cost -34% |                      |           |
| +7   | Dmg +43%, Cost -31% | Hit +45%, Cost -31% |                      |           |
| +6   | Dmg +39%, Cost -28% | Hit +40%, Cost -28% |                      |           |
| +5   | Dmg +35%, Cost -25% | Hit +35%, Cost -25% | Heal +40%, Cost -40% | Cost -40% |
| +4   | Dmg +25%, Cost -19% | Hit +25%, Cost -19% | Heal +25%, Cost -30% | Cost -30% |
| +3   | Dmg +20%, Cost -16% | Hit +20%, Cost -16% | Heal +20%, Cost -25% | Cost -25% |
| +2   | Dmg +15%, Cost -13% | Hit +15%, Cost -13% | Heal +15%, Cost -20% | Cost -20% |
| +1   | Dmg +10%, Cost -10% | Hit +10%, Cost -10% | Heal +10%, Cost -15% | Cost -15% |
| -1   | Dmg -10%, Cost +10% | Hit -10%, Cost +10% | Heal -10%, Cost +20% | Cost +20% |
| -2   | Dmg -15%, Cost +15% | Hit -15%, Cost +15% | Heal -15%, Cost +30% | Cost +30% |
| -3   | Dmg -20%, Cost +20% | Hit -20%, Cost +20% | Heal -20%, Cost +40% | Cost +40% |
| -4   | Dmg -25%, Cost +25% | Hit -25%, Cost +25% | Heal -25%, Cost +50% | Cost +50% |
| -5   | Dmg -35%, Cost +35% | Hit -35%, Cost +35% | Heal -40%, Cost +60% | Cost +60% |
| -6   | Dmg -39%, Cost +40% | Hit -40%, Cost +40% |                      |           |
| -7   | Dmg -43%, Cost +45% | Hit -45%, Cost +45% |                      |           |

### Buff Effects
| Rank | Tarukaja (Attack) | Rakukaja (Defense) | Sukukaja (Hit) | Sukukaja (Evade) |
| ---- | ----------------- | ------------------ | -------------- | ---------------- |
| +2   | 140%              | 70%                | 120%           | 85%              |
| +1   | 120%              | 80%                | 110%           | 90%              |
| -1   | 80%               | 120%               | 90%            | 110%             |
| -2   | 70%               | 140%               | 85%            | 120%             |

### Level Difference Damage Modifier

| Diff | Dmg Mod |
| ---- | ------- |
| >+9  | 405%    |
| +9   | 352%    |
| +8   | 306%    |
| +7   | 266%    |
| +6   | 231%    |
| +5   | 201%    |
| +4   | 175%    |
| +3   | 152%    |
| +2   | 132%    |
| +1   | 115%    |
| -1   | 87%     |
| -2   | 76%     |
| -3   | 66%     |
| -4   | 57%     |
| -5   | 50%     |
| -6   | 43%     |
| -7   | 38%     |
| -8   | 33%     |
| -9   | 28%     |
| <-9  | 25%     |

### Filling the Magtsuhi Gauge
| Condition                 | Fill |
| ------------------------- | ---- |
| Red Magatsuhi Pickup      | 1%   |
| End Turn (Minimum)        | 15%  |
| End Turn (Maximum)        | 25%  |
| Forestall                 | 20%  |
| Constant Vigiliance       | 15%  |
| Embolden                  | 5%   |
| Vengeful Opportunist      | 3%   |
| Fell Swoop                | 1%   |
| Counter Incentive: Resist | 3%   |
| Counter Incentive: Null   | 10%  |
| Unyielding Will           | 5%   |
| Vengeance                 | 30%  |

### Ailments
* Sleep
  * Skips action
  * Cured when attacked
  * Disables counter skills
* Mirage
  * Halves hit/evade
  * 50% chance to hit a foe other than the selected target
* Poison
  * Loses HP after every action
* Panic
  * 35% chance to hit an ally
  * 15% chance to do nothing
  * Reduces evade to 0
  * Disables counter skills
* Charm
  * 20% chance to cast recovery skill on foe
  * 10% chance to cast support skill on foe
  * 20% chance to do nothing
  * Reduces evade to 0
  * Disables counter skills
* Seal
  * Cannot cast skills
  * Foe skips action when casting a skill
  * Disables counter skills
* Mud
  * Loses one press turn before every action
* Shroud
  * Loses MP before every action
  * Takes only 5% damage from Heliopolis Dawn

### Unlocking Magatsuhi Skills with Talismans (Tm)
* Herald: Clear "The Holy Ring"
* Megami: Clear "The Horn of Plenty"
* Avian: Find 30 Miman
* Divine: Talk to Angel NPC in Container Yard
* Yoma: Clear "Pollution Panic"
* Vile: Clear "Magic from the East"
* Raptor: Clear "Movin' on Up"
* Deity: Clear "The Bull God's Lineage"
* Wargod: Clear "No Stone Unturned"
* Avatar: Find 45 Miman
* Holy: Find 55 Miman
* Genma: Find 100 Miman
* Element: Find 10 Miman
* Fairy: Clear "The Root of the Problem"
* Beast: Clear "A Wish for a Fish"
* Jirae: Clear "Chakra Drop Chomp"
* Fiend: Find 70 Miman
* Jaki: Talk to Rakshasa NPC in Nagatacho
* Wilder: Talk to Nue NPC in Container Yard
* Fury: Clear "The Destined Leader"
* Lady: Clear "The Falcon's Head"
* Dragon: Clear "The Gold Dragon's Arrival"
* Kishin: Find 90 Miman
* Kunitsu: Clear "Clash with the Kunitsukami"
* Femme: Clear "The Demon of the Spring"
* Brute: Clear "Talisman Hunt"
* Fallen: Clear "To Cure a Curse"
* Night: Clear "Kumbhanda's Bottle"
* Snake: Talk to Yurlungur NPC in Chiyoda
* Tyrant: Clear "The Winged Sun"
* Drake: Clear "The Ultimate Omelette"
* Haunt: Clear "A Preta Predicament"
* Foul: Talk to Slime NPC in Hamamatsucho

## Shin Megami Tensei: Devil Summoner
### Data Sources
* https://gamefaqs.gamespot.com/psp/929271-shin-megami-tensei-devil-summoner/faqs/70850
* http://onpleruler.web.fc2.com/megami/pspds.htm
* http://www.geocities.co.jp/Hollywood-Miyuki/1871/dds/

## Devil Summoner: Soul Hackers
### Data Sources
* http://bmky.net/data/sh/system/unite/hero.html
* http://ifs.nog.cc/fool-est.hp.infoseek.co.jp/ds/sh/index.html

## Raidou Kuzunoha vs. The Soulless Army
### Data Sources
* https://kaerukyo.net/dds_database/devil.php?title=22

## Raidou Kuzunoha vs. King Abaddon
### Data Sources
* https://www31.atwiki.jp/abaddon/pages/37.html

## Soul Hackers 2
### Data Sources
* *Soul Hackers 2 The Complete Guide* (ISBN-13: 9784047336254)
* https://kamigame.jp/soul-hackers2/index.html

## Megami Ibunroku Persona
### Data Sources
* http://persona1.wikidot.com
* http://p1psp.gkwiki2.com/
* http://www.se-inst.com/html32/lib/pers_ms_dl.html

## Persona 2: Innocent Sin

## Persona 2: Eternal Punishment
### Data Sources
* https://tartarus.rpgclassics.com/persona2ep/

## Persona 3
### Persona 3 FES
* Aeon Social Link added
* Orpheus Telos added

### Persona 3 FES: The Answer
* No compendium available
* 4+ spreads removed, can create through normal and triple fusion instead

### Persona 3 Portable
* Skill cards added

### Data Sources
* *Persona 3 FES Perfect Guide* (ISBN-13: 9784757735767)
* *Persona 3 Portable Official Perfect Guide* (ISBN-13: 9784047262935)
* http://gamekouryaku.com/peru3/
* https://w.atwiki.jp/wiki10_persona3/
* http://game.daihouko.com/persona/3fes/
* https://plaza.rakuten.co.jp/personasite/
* https://gamefaqs.gamespot.com/ps2/937269-shin-megami-tensei-persona-3-fes/faqs/53404

### Skill List
* Rank ends in 0.5: Skill can mutate upon level up
* (Fs): Fusion Spell

## Persona 3
### Data Sources
* https://github.com/aqiu384/megaten-database

## Persona 4
### Persona 4 Golden
* Aeon and Jester Social Links added
* Skill cards added

### Data Sources
* *Persona 4 The Golden The Complete Guide* (ISBN-13: 9784048866637)
* https://p4g.gamekouryaku-no-ki.com/
* https://gamefaqs.gamespot.com/ps2/945498-shin-megami-tensei-persona-4/faqs/53550
* https://gamefaqs.gamespot.com/ps2/945498-shin-megami-tensei-persona-4/faqs/55266
* https://gamefaqs.gamespot.com/vita/641695-persona-4-golden/faqs/64587
* http://h1g.jp/p4g/

### Skill List
* Rank ends in 0.5: Skill can upgrade through Magician Card from Shuffle Time
* (S?): Learned at Social Link Lv. ?
* (Sx): Learned at Social Link Lv. 10
* (Sy): Learned at Social Link Lv. 11
* (B?): Learned during Bike Event ?

## Persona 5
### Persona 5 Royal
* Faith and Councillor Confidants added
* Fusion Alarm added
* Persona Traits added
* [Max Confidant Walkthrough](https://aqiu384.github.io/p5r-walkthrough/introduction)

### Data Sources
* *Persona 5 Official Complete Guide* (ISBN-13: 9784048924160)
* *Persona 5 The Royal Official Complete Guide* (ISBN-13: 9784049128871)
* https://h1g.jp/p5r/
* http://spwiki.net/persona5/
* https://wikiwiki.jp/persona5r/
* https://omoteura.com/persona5/
* https://p5r.gamekouryaku-no-ki.com/
* http://bozumemo.blogspot.com/p/5.html
* https://docs.google.com/spreadsheets/d/1kPsA9fwhOyqyh7qLNfW2Xprc7wDK6RQ5d3Re4f7cTKk

### Skill List
* (Cx): Learned at Confidant Lv. 10
* (Cy): Learned at Confidant Lv. 11
* (Fa): Itemize during Fusion Alarm
* (Tk): Negotiate during Hold Up

## Persona 5 Strikers
### Data Sources
* https://altema.jp/persona5s/
* https://gamewith.jp/p5s/
* https://h1g.jp/p5s/

### Skill List
* (C1): Combo Input #1 □□△△
* (C2): Combo Input #2 □□□△
* (C3): Combo Input #3 □□□□□△△

## Persona Q: Shadow of the Labyrinth
### Data Sources
* *Persona Q: Shadow of the Labyrinth Official Perfect Guide* (ISBN-13: 9784047298224)
* https://wikiwiki.jp/personaqr/
* https://gamers-high.com/persona-q/

### QR Code Unique Skills
* Unlike Strange Journey passwords, QR codes are valid even with unique skills
* Party member unique skills are still invalid

## Persona Q2: New Cinema Labyrinth
### Data Sources
* https://bozumemo.blogspot.com/p/pq2.html
* https://wiki.denfaminicogamer.jp/pq2/
* https://wikiwiki.jp/pq2/

## Majin Tensei
### Data Sources
* http://ifs.nog.cc/fool-est.hp.infoseek.co.jp/majin/majin1/index.html

## Majin Tensei II: Spiral Nemesis
### Data Sources
* http://www.demitree.jp/コンテンツ/魔神転生２/
* http://www.cam.hi-ho.ne.jp/oni2/oni1/Majin2/remix.htm
* http://majinntennsei2.kouryaku.red/
* http://oliva.m78.com/majin2.html
* http://bmky.net/data/m2/

## Devil Survivor
### Maxing All Demon Stats
* Like most games, there is a cap on how many bonus stats a demon can receive from Mitama fusion
* This can be bypassed with the following chain
  * 1-star auction demon x 1-star auction demon = Element with a negative stat penalty
  * Penalty Element x Penalty Element = Mitama with a negative stat penalty
* This Penalty Mitama will raise one stat and lower another, resulting in a net-zero change towards the bonus stat cap
* By raising two stats on a demon to 40 and lowering the other two stats below 0, the latter will underflow and loop back around to 40

### Devil Survivor Overclocked
* 8th Day added for 3 routes
* Compendium added

### Data Sources
* https://gamefaqs.gamespot.com/ds/954869-shin-megami-tensei-devil-survivor/faqs/56943
* https://gamefaqs.gamespot.com/3ds/997806-shin-megami-tensei-devil-survivor-overclocked/faqs/69601

### Skill List
* (A?): Comes with ?-star Auction

## Devil Survivor 2
* Max demon stat underflow fixed

### Devil Survivor 2 Record Breaker
* Triangulum Campaign added

### Data Sources
* http://i40.tinypic.com/f2j6mo.png
* http://spwiki.net/ds2br/

### Skill List
* (A?): Comes with ?-star Auction
* (Ar): Comes with Rare Auction

## Shin Megami Tensei: Liberation Dx2
### Data Sources
* https://altema.jp/megaten/
* https://d2-megaten-l.sega.com/en/
* https://oceanxdds.github.io/dx2_fusion/

### Skill List
* (Ac): Archetype Common
* (Aa): Archetype Aragami
* (Ap): Archetype Protector
* (Ay): Archetype Psychic
* (Ae): Archetype Elementalist
* (Ga): Gacha Aragami
* (Gp): Gacha Protector
* (Gy): Gacha Psychic
* (Ge): Gacha Elementalist
