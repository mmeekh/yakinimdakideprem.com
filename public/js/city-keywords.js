(function () {
  const baseKeywords = {
    istanbul: [
      "istanbul",
      "marmara",
      "marmara denizi",
      "tekirdag",
      "tekirdağ",
      "silivri",
      "adalar",
      "yalova",
      "kocaeli",
      "çınarcık",
      "boğaz",
      "princes islands"
    ],
    izmir: [
      "izmir",
      "izmir körfezi",
      "ege denizi",
      "seferihisar",
      "foça",
      "çesme",
      "çeşme",
      "urla",
      "manisa",
      "torbalı",
      "gaziemir",
      "bayındır"
    ],
    ankara: [
      "ankara",
      "kırıkkale",
      "polatlı",
      "çankırı",
      "beypazarı",
      "kızılcahamam",
      "çubuk",
      "etimesgut",
      "sincan",
      "gölbaşı",
      "kahramankazan"
    ],
    elazig: [
      "elazig",
      "elazığ",
      "karakoçan",
      "palu",
      "sivrice",
      "keban",
      "pertek",
      "bingol",
      "bingöl",
      "malatya",
      "tunceli"
    ],
    kahramanmaras: [
      "kahramanmaras",
      "kahramanmaraş",
      "maras",
      "elbistan",
      "pazarcık",
      "turkoglu",
      "türkoğlu",
      "nurdagi",
      "nurdağı",
      "afşin",
      "goksun",
      "göksun",
      "osmaniye",
      "antep",
      "gaziantep",
      "hatay"
    ]
  };

  const aliasMap = {
    "elazığ": "elazig",
    "elazÄ±ÄŸ": "elazig",
    "kahramanmaraş": "kahramanmaras",
    "kahramanmara\u015f": "kahramanmaras",
    "kahramanmaraÅŸ": "kahramanmaras"
  };

  const cityKeywords = Object.assign({}, baseKeywords);
  Object.keys(aliasMap).forEach((alias) => {
    const canonical = aliasMap[alias];
    cityKeywords[alias] = baseKeywords[canonical] || [];
  });

  window.CityKeywords = cityKeywords;
})();
