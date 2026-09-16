"""Fixed storage/handling tip library for Module 2 (Loss-Reduction Nudges).
Deliberately a lookup table, not a diagnostic system, to keep the hackathon
build simple and honest about what it actually checks."""

STORAGE_TIPS = {
    "Sorghum": "Kausha nafaka vizuri kabla ya kuhifadhi. Angalia dalili za ukungu kabla ya kuweka gunia.",
    "Green grams": "Hifadhi kwenye chombo kisicho na hewa kuzuia wadudu. Kausha vizuri kabla ya kufunga.",
    "Cowpeas": "Changanya na majivu au dawa salama ya kuhifadhi kuzuia wadudu wa ghalani.",
    "Maize": "Kausha hadi unyevu uwe chini kabla ya kuhifadhi. Tumia gunia safi, si zilizotumika kwa kemikali.",
    "Millet": "Pepeta vizuri kuondoa uchafu na kausha juani kabla ya kuhifadhi mahali pakavu.",
    "Pigeon peas": "Hakikisha zimekauka kabisa, ganda likikatika kwa urahisi, kabla ya kuhifadhi.",
}

GENERIC_FALLBACK = "Hakikisha mazao yamekauka vizuri kabla ya kuhifadhi."

def get_storage_tip(crop_name: str) -> str:
    if crop_name in STORAGE_TIPS:
        return STORAGE_TIPS[crop_name]
    else:
        return GENERIC_FALLBACK