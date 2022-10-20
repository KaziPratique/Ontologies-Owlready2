from owlready2 import *
onto = get_ontology("http://test.org/onto_pays.owl")

with onto:
    class abbrev(Thing >> str): pass
    class part_of(Thing >> Thing, TransitiveProperty): pass
    
    # Pays
    class Country(Thing): pass
    # Region
    class State(Thing): pass
    class in_country(part_of): pass
    
    # Ville
    class City(Thing): pass
    class in_state(part_of): pass
    class zip_code(City >> str): pass
    class population(City >> int): pass
    
    AllDisjoint([Country, State, City])
    
    # infered classes
    class BigCity(City): pass
    class SmallCity(City): pass
    
    class BigCityinFR(BigCity): pass
    class SmallCityinFR(SmallCity): pass
    
    # Pays 1 France
    fr = Country("France")
    fr.abbrev.append("FR")
    # region
    occitanie = State("Occitanie", in_country = [fr])
    iledefrance = State("IleDeFrance", in_country = [fr])
    
    toulouse = City("Toulouse", in_state = [occitanie])
    toulouse.zip_code.append("31000")
    toulouse.population.append(471941)
    
    montpellier = City("Montpellier", in_state = [occitanie])
    montpellier.zip_code.append("34000")
    montpellier.population.append(409000)
    
    melun = City("Melun", in_state = [iledefrance])
    melun.zip_code.append("77000")
    melun.population.append(40844)
    
    paris = City("Paris", in_state = [iledefrance])
    paris.zip_code.append("75000")
    paris.population.append(2165423)
    
    AllDifferent([toulouse, montpellier,melun,paris])
    
    # Pays 2 Canada
    canada = Country("Canada")
    canada.abbrev.append("CA")
    # region
    quebec = State("Quebec", in_country = [canada])
    # ville
    montreal = City("Montreal", in_state = [quebec])
    montreal.zip_code.append("66023")
    montreal.population.append(1704694)
    
    Imp().set_as_rule("City(?c), population(?c, ?pop), greaterThan(?pop, 200000) ->BigCity(?c)")
    Imp().set_as_rule("City(?c), population(?c, ?pop), lessThan(?pop, 30000) -> SmallCity(?c)")
    Imp().set_as_rule("BigCity(?c), part_of(?c, ?country), abbrev(?country, ?ab), stringEqualIgnoreCase(?ab, 'FR') -> BigCityinFR(?c)")   
    Imp().set_as_rule("SmallCity(?c), part_of(?c, ?country), abbrev(?country, ?ab), stringEqualIgnoreCase(?ab, 'FR') -> SmallCityinFR(?c)")   
    
#
onto.save(file="./pays.owl")

sync_reasoner_pellet(infer_property_values = True, infer_data_property_values = True)
graph = default_world.as_rdflib_graph()