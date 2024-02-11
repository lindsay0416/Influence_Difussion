import matplotlib.pyplot as plt

# Data

# S1
iterations = list(range(1, 10))
# aspects = ['Enhanced Traffic Flow', 'Economic Growth', 'Environmental Improvements',
#            'Safety Enhancements', 'Short-term Traffic Disruptions',
#            'Financial Considerations', 'Environmental and Community Impact']

# scores = [
#     [0, 0, 0, 0, 0.17082573198631743, 0.16808667467236937, 0.08867768160458644],
#     [0, 0, 0, 0, 0.2302452677020931, 0.28317953619047453, 0.1225],
#     [0.1879838223393469, 0.07030492086459506, 0.06804963087832473,
#      0.03574720087172335, 0.13899042045098578, 0.21509143492055313,
#      0.26592617011394365],
#     [0.27020682863926404, 0.1509000452121099, 0.26259621627597807,
#      0.38764109422168797, 0.2077342909798754, 0.42505523846178084,
#      0.2172862714295712],
#     [0.25913008684938627, 0.15648917026677844, 0.26259621627597807,
#      0.4964968820278432, 0.309008745557929, 0.44537388496571323,
#      0.47630685657556543],
#     [0.17658789117918572, 0.1943498907289551, 0.3871959040567256,
#      0.5060510855718533, 0.32573035552747504, 0.5212214629846595,
#      0.45439882361349715],
#     [0.18245455054355206, 0.1943498907289551, 0.3916491872628638,
#      0.5228087304966818, 0.36135694958054226, 0.5407519962078301,
#      0.45188665408642326],
#     [0.21896978115803933, 0.22406318131959685, 0.42331576814181904,
#      0.5228087304966818, 0.3851421139028632, 0.5372936795215444,
#      0.43866615210175514],
#     [0.25896978115803933, 0.27406318131959685, 0.49331576814181904,
#      0.6828087304966818, 0.41496941693112674, 0.5468888086196532,
#      0.441766615210175514]
# ]

# S2
# aspects = ['Technical Proficiency', 'Data Wrangling and Visualization', 'Statistical Savvy',
#            'Machine Learning Mastery', 'Behavioral Balance',
#            'Industry Insight', 'Portfolio']
#
# scores = [
# [0.22773564261716758, 0.5905375291692205, 0, 0.14564803704307705, 0.20608363501393825, 0.2605556710562624, 0.06437099366532754],
# [0.272074731667965, 0.5248463705495657, 0.2428232395201225, 0.45026814465562653, 0.17875255395197676, 0.22858816137955915, 0.26055567105626243],
# [0.14130040998960136, 0.274234159180337, 0.11651799976847813, 0.28520015975349405, 0.2234744174835012, 0.15583663956455512, 0.08011947727590159],
# [0.18106301764710325, 0.2211219817664637, 0.24705217159920073, 0.29731594500453645, 0.24110288959227233, 0.14837664502293943, 0.15312858329780435],
# [0.2027363014412089, 0.2466124395591544, 0.22705327174000542, 0.30059406588556925, 0.252419857917029, 0.161713780662529, 0.12793729981999782],
# [0.27753499599061615, 0.28686222634181624, 0.24955921435386463, 0.2674074373373825, 0.24579384025993983, 0.1757860783933462, 0.19431434016858148],
# [0.3221284837846647, 0.3425829800435699, 0.3361368300821982, 0.28520015975349405, 0.2586941888148862, 0.18590934746393004, 0.33143664349790486],
# [0.20924543805067491, 0.4729266980725786, 0.44978807836528534, 0.37990319823534724, 0.34889326507105706, 0.20260164868909072, 0.2801888545173854],
# # [0.2476105150686072, 0.4372398884290367, 0.4361666737951996, 0.39175009019140217, 0.37023794145648836, 0.265214002826966, 0.24799747855559118]
# [0.28816745328695176, 0.4761442079203573, 0.4758714591089397, 0.41732709053720546, 0.39514662695099984, 0.2504356154757147, 0.22937949898142296]
# ]


## S3
aspects = [
    "First Impressions",
    "Features",
    "Performance Parameters",
    "Design Dialogue",
    "Price Point Perspective",
    "Constructive Critiques",
    "Marketing Messages"
]

scores = [
    [0.1130143992474642, 0.06123094334544521, 0.15022971628691553, 0.10318898533313868, 0.10011031656225383, 0.1337850929463124, 0.1265720102125355],
  [0.09228786705409497, 0.09469853796540419, 0.10657035539480765, 0.044937392134091016, 0.20186771310742205, 0.06121417088719625, 0.21859743304579002],
  [0.16425160384675824, 0.1667119835629982, 0.08311614691404554, 0.053031492227115264, 0.2014294229052878, 0.1115502882981172, 0.20412155301328383],
  [0.21986404587623995, 0.23619913327787193, 0.10388845602691692, 0.09174351209153192, 0.19866436201896284, 0.158893184499188, 0.1999023871658969],
  [0.2325891346620457, 0.24840805434861682, 0.11074647998946077, 0.21363563948374828, 0.18388050123115396, 0.172281347323555, 0.19709291920271296],
  [0.239881691606765, 0.25093778723798627, 0.14071951846118122, 0.26265773225855676, 0.2420075434753251, 0.21952835131734616, 0.2338125544435859],
  # [0.23566134736622585, 0.2879964974792196, 0.12783857928811268, 0.31164816196709383, 0.26293549204062844, 0.23192232768628962, 0.24861071903382942],
  [0.24702513631618278, 0.30774255532727246, 0.14221882139116676, 0.33229595406413676, 0.29419066483102013, 0.24968339965888042, 0.2876987199173385],
  [0.2394133012249648, 0.31224248005546584, 0.16243183940235353, 0.38027819531304163, 0.30065107270257213, 0.25557426422304147, 0.3079006985827005],
  [0.24217339650689185, 0.32104723428667364, 0.17945844982655432, 0.41283792989377216, 0.30064550127011314, 0.2614424932768966, 0.308784934628222]
]


# Plotting
plt.figure(figsize=(10, 6))
for i, aspect in enumerate(aspects):
    plt.plot(iterations, [score[i] for score in scores], marker='o', label=aspect)

# Customizing the plot
plt.title('Score Changes Over 9 Iterations', fontsize=16)
plt.xlabel('Iterations', fontsize=14)
plt.ylabel('Score', fontsize=14)
plt.xticks(iterations)
plt.grid(True, linestyle='--', linewidth=0.5)
plt.legend(loc='best', fontsize=10)

plt.tight_layout()
plt.show()
