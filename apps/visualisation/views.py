from django.shortcuts import render
import rdflib 
import os
from apps.connaissance.models import Connaissance
from apps.commentaire.models import Commentaire

# Create your views here.

def visualisation(request):
    #Tache 

    g_tache = rdflib.Graph()
    g_tache.parse("apps/connaissance/static/viz-onto/viz_tache.ttl")
    query_tache = """
    SELECT ?tache
    WHERE {
        ?tache a :Tache .
    }"""
    qres_tache = g_tache.query(query_tache)
    taches = []

    for row in qres_tache:
        tache = str(row.tache).replace('http://dig.isi.edu/', '')
        taches.append(tache)


    #Activite
    g_activite = rdflib.Graph()
    g_activite.parse("apps/connaissance/static/viz-onto/viz_activite.ttl")
    query_activite = """
    SELECT ?activite
    WHERE {
        ?activite a :Activite .
    }"""
    qres_activite = g_activite.query(query_activite)
    activites = []

    for row in qres_activite:
        activite = str(row.activite).replace('http://dig.isi.edu/', '')
        activites.append(activite)

    #Historique
    g_historique = rdflib.Graph()
    g_historique.parse("apps/connaissance/static/viz-onto/viz_historique.ttl")
    query_historique = """
    SELECT ?generation
    WHERE {
        ?generation a :Generation .
    }"""
    qres_generation = g_historique.query(query_historique)
    generations = []

    for row in qres_generation:
        generation = str(row.generation).replace('http://dig.isi.edu/', '')
        generations.append(generation)
    
    #Phenomenes
    g_phenomene = rdflib.Graph()
    g_phenomene.parse("apps/connaissance/static/viz-onto/viz_phenomene.ttl")
    query_phenomene = """
    SELECT ?phenomene
    WHERE {
        ?phenomene a :Phenomene_Metier .
    }"""
    qres_phenomene = g_phenomene.query(query_phenomene)
    phenomenes = []

    for row in qres_phenomene:
        phenomene = str(row.phenomene).replace('http://dig.isi.edu/', '')
        phenomenes.append(phenomene)


    #Domaines
    g_domaine = rdflib.Graph()
    g_domaine.parse("apps/connaissance/static/viz-onto/viz_domaine.ttl")
    query_domaine = """
    SELECT ?domaine
    WHERE {
        ?domaine a :Domaine .
    }"""
    qres_domaine = g_domaine.query(query_domaine)
    domaines = []

    for row in qres_domaine:
        domaine = str(row.domaine).replace('http://dig.isi.edu/', '')
        domaines.append(domaine)

    #Strategique
    g_strategie = rdflib.Graph()
    g_strategie.parse("apps/connaissance/static/viz-onto/viz_strategie.ttl")
    query_strategie = """
    SELECT ?strategie
    WHERE {
        ?strategie a :Strategie .
    }"""
    qres_strategie = g_strategie.query(query_strategie)
    strategies = []

    for row in qres_strategie:
        strategie = str(row.strategie).replace('http://dig.isi.edu/', '')
        strategies.append(strategie)

    print(strategies)

    connaissanceNotification = Connaissance.objects.filter(status_vue=False).count()
    commentaires = Commentaire.objects.all()
    connaissanceNotification += commentaires.count()

    context = {
        'taches': taches,
        'activites': activites,
        'generations': generations,
        'phenomenes_metier': phenomenes,
        'domaines':domaines,
        'strategies':strategies,
        'connaissanceNotification': connaissanceNotification,
    }
    
    
    return render(request, 'visualisation/visualisation.html', context)


def visualisation_tache():
    
    g = rdflib.Graph()
    g.parse("apps/connaissance/static/viz-onto/viz_tache.ttl")
    query = """
    SELECT ?tache
    WHERE {
        ?tache a :Tache .
    }"""
    qres = g.query(query)
    taches = []

    for row in qres:
        tache = str(row.tache).replace('http://dig.isi.edu/', '')
        taches.append(tache)

    nbr=len(taches)
    nbr = nbr + 1
    nbr = str(nbr)

    file = open("apps/connaissance/static/viz-onto/viz_tache.ttl", "a")

    a = '\n:tache'+ nbr +' a :Tache ;\n'
    a +='\t' + ':nom ' + '"'+nom_tache+'"' + ' ;\n' + '\t' +':type ' + '"'+type_tache+'"' + " ;\n"
    a +='\t' + ':condition ' + '"'+ind_condition+'"' + ' ;\n'
    a += '\t' + ':objectif ' + '"'+ind_objectif+'"' + ' .\n'

    file.write(a)
    file.close()

    filewrite = open("tache"+nbr+".ttl", "w")

    filewrite.write("@prefix : <http://dig.isi.edu/> .\n"+
                    "@prefix rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n"+
                    "@prefix owl:   <http://www.w3.org/2002/07/owl#> .\n"+
                    "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n\n")

    filewrite.write(a)
    filewrite.close()

    os.system("python apps/visualisation/ontology_viz.py -o tache"+nbr+".dot tache"+nbr+".ttl -O apps/connaissance/static/ontologie-data/ontology_tache.ttl")
    os.remove("tache"+nbr+".ttl")
    os.system("dot -Tpng -o "+ "apps/connaissance/static/formalismes/tache/tache" +nbr+".png tache"+nbr+".dot")
    os.remove("tache"+nbr+".dot")


def visualisation_activite():
    g = rdflib.Graph()
    g.parse("apps/connaissance/static/viz-onto/viz_activite.ttl")
    query = """
    SELECT ?activite
    WHERE {
        ?activite a :Activite .
    }"""
    qres = g.query(query)
    activites = []

    for row in qres:
        activite = str(row.activite).replace('http://dig.isi.edu/', '')
        activites.append(activite)

    nbr=len(activites)
    nbr = nbr + 1
    nbr = str(nbr)

    file = open("apps/connaissance/static/viz-onto/viz_tache.ttl", "a")

    a = '\n:activite' + nbr + ' a :Activite ;\n'
    a +='\t' + ':nom ' + '"'+nom_activite+'"' + ' ;\n'
    a +='\t' + ':possede :act ;\n'
    a += '\t' + ':ressource ' + '"'+nom_ressource+'"' + ' ;\n'
    a += '\t' + ':entre ' + '"'+nom_entre+'"' + ' ;\n'
    a += '\t' + ':sortie ' + '"'+nom_sortie+'"' + ' .\n'
    a += ':act a :Acteur ;\n'
    a += '\t' + ':nom ' + '"'+nom_acteur+'"' + ' ;\n'
    a += '\t' + ':caracteristique ' + '"'+caracteristique_acteur+'"' + ' .\n'


    file.write(a)
    file.close()

    filewrite = open("activite"+nbr+".ttl", "w")

    filewrite.write("@prefix : <http://dig.isi.edu/> .\n"+
                    "@prefix rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n"+
                    "@prefix owl:   <http://www.w3.org/2002/07/owl#> .\n"+
                    "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n\n")

    filewrite.write(a)
    filewrite.close()

    os.system("python apps/visualisation/ontology_viz.py -o activite"+nbr+".dot activite"+nbr+".ttl -O apps/connaissance/static/ontologie-data/ontology_activite.ttl")
    os.remove("activite"+nbr+".ttl")
    os.system("dot -Tpng -o "+ "apps/connaissance/static/formalismes/activite/activite" +nbr+".png activite"+nbr+".dot")
    os.remove("activite"+nbr+".dot")


def visualisation_phenomene():
    g = rdflib.Graph()
    g.parse("apps/connaissance/static/viz-onto/viz_phenomene.ttl")
    query = """
    SELECT ?phenomene
    WHERE {
        ?phenomene a :Phenomene_Metier .
    }"""
    qres = g.query(query)
    phenomenes = []

    for row in qres:
        phenomene = str(row.phenomene).replace('http://dig.isi.edu/', '')
        phenomenes.append(phenomene)

    nbr=len(phenomenes)
    nbr = nbr + 1
    nbr = str(nbr)

    file = open("apps/connaissance/static/viz-onto/viz_phenomene.ttl", "a")

    a = '\n:' + nom_phenomene + ' a :Phenomene_Metier ;\n'
    a +='\t' + ':nom ' + '"'+nom_phenomene+'"' + ' ;\n'
    a += '\t' + ':possede' + ' :f, :ss, :sc ;\n'  #flux --- f, system_source --- ss
    a +='\t' + ':evenment_influenceur ' + '"'+nom_evenement_influenceur+'"' + ' .\n'
    a += ':ss a :System_Source ;\n'
    a += '\t' + ':nom ' + '"'+nom_system_source+'"' + ' ;\n'
    a += '\t' + ':action_source ' + '"'+action_system_source+'"' + ' ;\n'
    a += '\t' + ':evenment_initiateur ' + '"'+nom_evenement_initiateur+'"' + ' .\n'
    a += ':f a :Flux ;\n'
    a += '\t' + ':nom ' + '"'+nom_flux+'"' + ' ;\n'
    a += '\t' + ':type_flux ' + '"'+nom_information+'"' + ' .\n'
    a += ':sc a :System_Cible ;\n'#system_cible --- sc
    a += '\t' + ':nom ' + '"'+nom_system_cible+'"' + ' ;\n'
    a += '\t' + ':champ_actif ' + '"'+nom_champ_actif+'"' + ' ;\n'
    a += '\t' + ':consequence ' + '"'+nom_consequence+'"' + ' .\n'

    file.write(a)
    file.close()
    filewrite = open("phenomene"+nbr+".ttl", "w")
    filewrite.write("@prefix : <http://dig.isi.edu/> .\n"+
                    "@prefix rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n"+
                    "@prefix owl:   <http://www.w3.org/2002/07/owl#> .\n"+
                    "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n\n")
    filewrite.write(a)
    filewrite.close()
    os.system("python apps/visualisation/ontology_viz.py -o phenomene"+nbr+".dot phenomene"+nbr+".ttl -O apps/connaissance/static/ontologie-data/ontology_phenomene.ttl")
    os.remove("phenomene"+nbr+".ttl")
    os.system("dot -Tpng -o "+ "apps/connaissance/static/formalismes/phenomene/phenomene" +nbr+".png phenomene"+nbr+".dot")
    os.remove("phenomene"+nbr+".dot")


def visualisation_historique():
    g = rdflib.Graph()
    g.parse("apps/connaissance/static/viz-onto/viz_historique.ttl")
    query = """
    SELECT ?generation
    WHERE {
        ?generation a :Generation .
    }"""
    qres = g.query(query)
    generations = []

    for row in qres:
        generation = str(row.generation).replace('http://dig.isi.edu/', '')
        taches.append(generation)

    nbr=len(generations)
    nbr = nbr + 1
    nbr = str(nbr)

    file = open("apps/connaissance/static/viz-onto/viz_historique.ttl", "a")

    a = '\n:generation' + nbr + ' a :Generation ;\n'
    a +='\t' + ':nom ' + '"'+nom_generation+'"' + ' ;\n'
    a +='\t' + ':debut_periode ' + '"'+debut_periode+'"' + ' ;\n'
    a +='\t' + ':fin_periode ' + '"'+fin_periode+'"' + ' ;\n'
    a += '\t' + ':possede' + ' :arg, :ele .\n' #argumentation --- arg, element---ele

    a += ':arg a :Argumentation ;\n'
    a +='\t' + ':nom ' + '"'+ nom_argumentation+'"' + ' .\n'

    a += ':ele a :Element ;\n'
    a +='\t' + ':nom ' + '"'+nom_element+'"' + ' ;\n'
    a += '\t' + ':appartient' + ' :cls .\n'  

    a += ':cls a :Classe ;\n' #classse--- cls
    a +='\t' + ':nom ' + '"'+nom_classe+'"' + ' ;\n'
    a += '\t' + ':objectif' +'"'+nom_objectif+'"' + ' .\n'

    file.write(a)
    file.close()

    filewrite = open("generation"+nbr+".ttl", "w")

    filewrite.write("@prefix : <http://dig.isi.edu/> .\n"+
                    "@prefix rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n"+
                    "@prefix owl:   <http://www.w3.org/2002/07/owl#> .\n"+
                    "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n\n")

    filewrite.write(a)
    filewrite.close()

    os.system("python apps/visualisation/ontology_viz.py -o generation"+nbr+".dot generation"+nbr+".ttl -O apps/connaissance/static/ontologie-data/ontology_historique.ttl")
    os.remove("generation"+nbr+".ttl")
    os.system("dot -Tpng -o "+ "apps/connaissance/static/formalismes/historique/generation" +nbr+".png generation"+nbr+".dot")
    os.remove("generation"+nbr+".dot")



    g = rdflib.Graph()
    g.parse("apps/connaissance/static/viz-onto/viz_domaine.ttl")
    query = """
    SELECT ?domaine
    WHERE {
        ?domaine a :Generation .
    }"""
    qres = g.query(query)
    generations = []

    for row in qres:
        generation = str(row.generation).replace('http://dig.isi.edu/', '')
        taches.append(generation)

    nbr=len(generations)
    nbr = nbr + 1
    nbr = str(nbr)

    file = open("apps/connaissance/static/viz-onto/viz_historique.ttl", "a")

    a = '\n:generation' + nbr + ' a :Generation ;\n'
    a +='\t' + ':nom ' + '"'+nom_generation+'"' + ' ;\n'
    a +='\t' + ':debut_periode ' + '"'+debut_periode+'"' + ' ;\n'
    a +='\t' + ':fin_periode ' + '"'+fin_periode+'"' + ' ;\n'
    a += '\t' + ':possede' + ' :arg, :ele .\n' #argumentation --- arg, element---ele

    a += ':arg a :Argumentation ;\n'
    a +='\t' + ':nom ' + '"'+ nom_argumentation+'"' + ' .\n'

    a += ':ele a :Element ;\n'
    a +='\t' + ':nom ' + '"'+nom_element+'"' + ' ;\n'
    a += '\t' + ':appartient' + ' :cls .\n'  

    a += ':cls a :Classe ;\n' #classse--- cls
    a +='\t' + ':nom ' + '"'+nom_classe+'"' + ' ;\n'
    a += '\t' + ':objectif' +'"'+nom_objectif+'"' + ' .\n'

    file.write(a)
    file.close()

    filewrite = open("generation"+nbr+".ttl", "w")

    filewrite.write("@prefix : <http://dig.isi.edu/> .\n"+
                    "@prefix rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n"+
                    "@prefix owl:   <http://www.w3.org/2002/07/owl#> .\n"+
                    "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n\n")

    filewrite.write(a)
    filewrite.close()

    os.system("python apps/visualisation/ontology_viz.py -o generation"+nbr+".dot generation"+nbr+".ttl -O apps/connaissance/static/ontologie-data/ontology_historique.ttl")
    os.remove("generation"+nbr+".ttl")
    os.system("dot -Tpng -o "+ "apps/connaissance/static/formalismes/historique/generation" +nbr+".png generation"+nbr+".dot")
    os.remove("generation"+nbr+".dot")


def visualisation_domaine(request):

    g = rdflib.Graph()
    g.parse("apps/connaissance/static/viz-onto/viz_domaine.ttl")
    query = """
    SELECT ?domaine
    WHERE {
        ?domaine a :Domaine .
    }"""
    qres = g.query(query)
    domaines = []

    for row in qres:
        domaine = str(row.domaine).replace('http://dig.isi.edu/', '')
        domaines.append(domaine)


    connaissanceNotification = Connaissance.objects.filter(status_vue=False).count()

    context = {
        'domaines': domaines,
        'connaissanceNotification': connaissanceNotification,
    }
    
    
    return render(request, 'visualisation/visualisation_domaine.html', context)