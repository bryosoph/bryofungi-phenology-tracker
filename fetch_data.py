import os
import requests
import json
from datetime import datetime

# ==========================================
# TARGET BRYOPHILOUS TAXA FILTER CONFIGURATION
# ==========================================

TARGET_SPECIES = {
    "arrhenia retiruga", "bryobroma microcarpum", "bryobroma microcarpum var. racomitrii",
    "bryobroma velenovskyi", "bryocentria brongniartii", "bryocentria hypothallina",
    "bryocentria metzgeriae", "bryocentria octosporelloides", "bryochiton macrosporus",
    "bryochiton microscopicus", "bryochiton monascus", "bryoglossum gracile",
    "bryorutstroemia fulva", "bryoscyphus conocephali", "bryoscyphus dicrani",
    "bryoscyphus turbinatus", "bryosphaeria bryophila", "bryostroma trichostomi",
    "chromocyphella muscicola", "cistella polytrichi", "dactylospora scapanaria",
    "durella polytrichina", "eocronartium muscicola", "epibryon bryophilum",
    "epibryon casaresii", "epibryon diaphanum", "epibryon dicrani",
    "epibryon hepaticicola", "epibryon interlamellare", "epibryon metzgeriae",
    "epibryon muscicola", "epibryon plagiochilae", "epibryon turfosorum",
    "helotium schimperi", "hilberina sphagnorum", "hymenoscyphus vasaensis",
    "hyphodiscus delitescens", "lamprospora hispanica", "lamprospora miniata",
    "lamprospora tortulae-ruralis", "lamprospora wrightii", "lizonia baldinii",
    "luteodiscus hemiamyloideus", "mniaecia gloeocapsae", "mniaecia jungermanniae",
    "mniaecia nivea", "muscinupta laevis", "neottiella ricciae",
    "neottiella rutilans", "octospora affinis", "octospora axillaris",
    "octospora coccinea", "octospora excipulata", "octospora fissidentis",
    "octospora gemmicola", "octospora gyalectoides", "octospora humosa",
    "octospora itzerottii", "octospora leucoloma", "octospora lilacina",
    "octospora musci-muralis", "octospora orthotrichi", "octospora rustica",
    "octosporella perforata", "pezoloma marchantiae", "pithyella chalaudii",
    "pleostigma jungermannicola", "rickenella swartzii", "rimbachia arachnoidea",
    "rimbachia bryophila", "rimbachia neckerae"
}

OPEN_GENERA = {
    "bryobroma", "bryocentria", "bryochiton", "bryonectria", "bryopistillaria", 
    "bryoscyphus", "bryosphaeria", "chromocyphella", "eocronartium", "epibryon", 
    "gloeopeziza", "helotium", "lamprospora", "lizonia", "loreleia", "luteodiscus", 
    "octosporella", "pithyella", "potridiscus", "rimbachia"
}

EXCLUDED_CONIOCHAETA = {
    "coniochaeta ambigua", "coniochaeta leucoplaca", "coniochaeta ligniaria", 
    "coniochaeta pulveracea", "coniochaeta vagans", "coniochaeta velutina"
}

def matches_target_taxa(scientific_name):
    if not scientific_name:
        return False
    name_clean = scientific_name.lower().strip()
    words = name_clean.split()
    if not words:
        return False
    genus = words[0]
    
    if name_clean in TARGET_SPECIES:
        return True
    if len(words) >= 2:
        binomial = f"{words[0]} {words[1]}"
        if binomial in TARGET_SPECIES:
            return True
        if genus == "coniochaeta":
            return binomial not in EXCLUDED_CONIOCHAETA
    if genus in OPEN_GENERA:
        return True
    return False

# ==========================================
# MULTI-PLATFORM DATA RETRIEVAL PIPELINE
# ==========================================

SEARCH_TERMS = sorted(OPEN_GENERA.union({
    "arrhenia", "bryoglossum", "bryorutstroemia", "cistella", "dactylospora", 
    "durella", "hilberina", "hymenoscy
