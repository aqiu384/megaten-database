# Persona 3 Reload
## Combat
* Miscellaneous info regarding combat
  * Personas
  * Skills
  * Shuffle Time

### Personas
{{ all_personas('') }}

### Skills
{{ all_skills('') }}

### Shuffle Time
#### Occurence
| Encounter Type | Persona | Minor | Major |
| --- | --- | --- | --- |
| Normal | 40% | 57% | 3% |
| Formidable | - | - | 15% |
| Rare | - | - | 20% |
| Monad | - | - | 100% |
#### Persona
{{ shuffle_time('Persona') }}
#### Sword
{{ shuffle_time('Sword') }}
#### Coin
| Rank | Min Money | Max Money |
| --- | --- | --- |
| 1 | 100 | 500 |
| 2 | 900 | 1000 |
| 3 | 400 | 1500 |
| 4 | 000 | 2000 |
| 5 | 800 | 2500 |
| 6 | 700 | 3400 |
| 7 | 600 | 4300 |
| 8 | 700 | 5400 |
| 9 | 000 | 6500 |
| 10 | 4000 | 7700 |
| J | 2000 | 15000 |
| Q | 0000 | 35000 |
| K | 0000 | 70000 |
#### Wand
| Rank | EXP Multiplier |
| --- | --- |
| 1 | 1.1 |
| 2 | 1.2 |
| 3 | 1.3 |
| 4 | 1.4 |
| 5 | 1.5 |
| 6 | 1.6 |
| 7 | 1.7 |
| 8 | 1.8 |
| 9 | 1.9 |
| 10 | 2.0 |
| J | 2.1 |
| Q | 2.2 |
| K | 2.5 |
#### Cup
{{ shuffle_time('Cup') }}
#### Fool
* EXP x1.1
#### Magician
{{ shuffle_time('Magician Card') }}
#### Priestess
* All-Out Attack damage up
#### Empress
* En +2, Ag +2, Lu +2 to all personas in stock
#### Emperor
* St +2, Ma +2 to all personas in stock
#### Hierophant
* Lv. +1 to equipped persona
#### Lovers
| SL Rank | SL Bonus EXP | Lovers Bonus EXP |
| --- | --- | --- |
| 1 | 130% | 230% |
| 2 | 200% | 300% |
| 3 | 250% | 350% |
| 4 | 300% | 400% |
| 5 | 350% | 450% |
| 6 | 400% | 500% |
| 7 | 430% | 530% |
| 8 | 480% | 580% |
| 9 | 500% | 600% |
| 10 | 500% | 600% |
#### Chariot
* Your Max HP +10
#### Justice
* Pick +1 card during Shuffle Time
#### Hermit
* Your Max SP +7
#### Fortune
* All active party members Max HP +8
#### Strength
* All active party members Max SP +5
#### Hanged
{{ shuffle_time('Hanged Card') }}
#### Temperance
* Increase Social Stats gained during the next day
#### Devil
* Items x2 from breakables and non-floor guardian fights
#### Tower
* All Stats +1 to all personas in stock
#### Star
* Pick +1 card during Shuffle Time
#### Moon
* All active party members recover full HP and SP
#### Sun
* Fuse personas up to +5 above your current level
#### Judgement
* Active party member with the lowest level will gain the most EXP

### Calculations
#### Limits
| Property | Min | Max |
| --- | --- | --- |
| Damage | - | 99999 |
| X Boost, Amp | - | 500% |
| Critical Hit | - | - |
| Accuracy | 50% | 99% |
| Ailment Hit | - | 99% |
| Escape | 50% | 99% |

#### Damage
| Effect | Multiplier |
| --- | --- |
| Critical | 1.5 |
| Weak | 1.25 |
| Down | 1.25 |
| Guarding | 0.4 |

#### Ailments
* Freeze: Crit +100%
* Shock: Crit +35%
* Charm: Lasts at least 1 turn
* Poison: Lose 20% HP per turn
* Distress: Crit +60%
* Confuse: Crit +20%
* Fear: Crit +20%
* Rage: Accuracy -50%
* Down: Crit +15%
* Overheat: Lasts 2 turns
* Ally with ailment: 70% recovery rate
* Enemy with ailment: 30% recovery rate

#### Level Difference
* Being overlevelled against a boss will not reduce your damage taken.

| Lv. Difference | EXP Gained | Damage Taken |
| --- | --- | --- |
| -13 | 0.32 | 0.5 |
| -12 | 0.32 | 0.51 |
| -11 | 0.32 | 0.53 |
| -10 | 0.32 | 0.59 |
| -9 | 0.4 | 0.66 |
| -8 | 0.48 | 0.75 |
| -7 | 0.53 | 0.84 |
| -6 | 0.59 | 0.91 |
| -5 | 0.64 | 0.97 |
| -4 | 0.73 | 0.99 |
| -3 | 0.8 | 1.0 |
| -2 | 0.86 | 1.0 |
| -1 | 0.91 | 1.0 |
| 0 | 1.0 | 1.0 |
| 1 | 1.0 | 1.01 |
| 2 | 1.0 | 1.03 |
| 3 | 1.0 | 1.09 |
| 4 | 1.04 | 1.16 |
| 5 | 1.19 | 1.25 |
| 6 | 1.46 | 1.34 |
| 7 | 1.77 | 1.41 |
| 8 | 2.3 | 1.47 |
| 9 | 3.1 | 1.49 |
| 10 | 4.0 | 1.5 |

#### Moon Phase
| Moon Phase | Getsu-ei Bonus | Zan-ei Bonus |
| --- | --- | --- |
| 1 | 1.0 | 1.7 |
| 2 | 1.0 | 1.6 |
| 3 | 1.05 | 1.5 |
| 4 | 1.1 | 1.45 |
| 5 | 1.15 | 1.4 |
| 6 | 1.2 | 1.35 |
| 7 | 1.25 | 1.3 |
| 8 | 1.3 | 1.25 |
| 9 | 1.35 | 1.2 |
| 10 | 1.4 | 1.15 |
| 11 | 1.45 | 1.1 |
| 12 | 1.5 | 1.05 |
| 13 | 1.6 | 1.0 |
| 14 | 1.7 | 1.0 |
| 15 | 1.75 | 1.0 |
| 16 | 1.7 | 1.0 |
| 17 | 1.6 | 1.0 |
| 18 | 1.5 | 1.05 |
| 19 | 1.45 | 1.1 |
| 20 | 1.4 | 1.15 |
| 21 | 1.35 | 1.2 |
| 22 | 1.3 | 1.25 |
| 23 | 1.25 | 1.3 |
| 24 | 1.2 | 1.35 |
| 25 | 1.15 | 1.4 |
| 26 | 1.1 | 1.45 |
| 27 | 1.05 | 1.5 |
| 28 | 1.0 | 1.6 |
| 29 | 1.0 | 1.7 |
| 30 | 1.0 | 1.75 |
