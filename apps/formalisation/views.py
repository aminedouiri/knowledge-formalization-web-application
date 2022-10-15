from django.shortcuts import render, redirect
from apps.connaissance.models import Connaissance
from apps.commentaire.models import Commentaire
from owlready2 import *   
import rdflib, os
#from apps.visualisation.views import visualisation_tache, visualisation_phenomene, visualisation_activite, visualisation_historique

# Create your views here.

def formalisation(request):

    #Initiation des Ontologies
    # ontologie_tache(request)
    # ontologie_historique(request)
    # ontologie_activite(request)
    # ontologie_phenomene(request)
    # ontologie_strategie(request)
    ###############################

    ajouter_ontologie_tache(request)
    ajouter_ontologie_historique(request)
    ajouter_ontologie_activite(request)
    ajouter_ontologie_phenomene(request)
    ajouter_ontologie_strategie(request)
    ###############################


    connaissance_list = Connaissance.objects.all()
    connaissanceNotification = Connaissance.objects.filter(status_vue=False).count()
    commentaires = Commentaire.objects.all()
    connaissanceNotification += commentaires.count()

    context = {
        'connaissance_list': connaissance_list,
        'connaissanceNotification': connaissanceNotification,
    }

    return render(request, 'formalisation/formalisation.html', context)


def ajouter_ontologie_tache(request):

    if 'tache' in request.POST:

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

        
        #Visualisation 
        nom_tache = request.POST['nom_tache']
        type_tache = request.POST['type_tache']
        type_partage_tache = request.POST['type_partage_tache']
        condition_tache = request.POST['condition_tache']
        
        file = open("apps/connaissance/static/viz-onto/viz_tache.ttl", "a")
            
        a = '\n:tache'+ nbr +' a :Tache ;\n'
        a +='\t' + ':nom ' + '"'+nom_tache+'"' + ' ;\n' + '\t' +':type ' + '"'+type_tache+'"' + " ;\n"
        a +='\t' + ':condition ' + '"'+condition_tache+'"' + ' ;\n'
        a += '\t' + ':type_de_partage ' + '"'+type_partage_tache+'"' + ' .\n'

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

        ##############################################################

def ajouter_ontologie_historique(request):

    if 'historique' in request.POST:

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
            generations.append(generation)

        nbr=len(generations)
        nbr = nbr + 1
        nbr = str(nbr)

        ontologie_historique = get_ontology("file://apps/connaissance/static/ontologie-data/ontologie_historique.owl").load()

        #Classes

        with ontologie_historique:

            class Argumentation(Thing): pass
            class Classe(Thing): pass
            class Element(Thing): pass
            class Generation(Thing): pass

        #ObjectProperty

            class appartient(Element >> Classe): pass
            class possede(ObjectProperty):
                domain = [Generation]
                range = [Argumentation, Element]


        #DatatypeProperty

            class nom_classe(Classe >> str): pass
            class nom_element(Element >> str): pass
            class nom_generation(Generation >> str): pass
            class debut_periode(Generation >> datetime.date): pass
            class fin_periode(Generation >> datetime.date): pass
            class type_de_partage(Generation >> str): pass
            class nom_argumentation(Argumentation >> str): pass
            
            nom_generation = request.POST['nom_generation']
            debut_periode = request.POST['debut_periode']
            fin_periode = request.POST['fin_periode']
            nom_argumentation = request.POST['nom_argumentation']
            nom_element = request.POST['nom_element']
            nom_classe = request.POST['nom_classe']
            nom_objectif = request.POST['nom_objectif']

            type_partage_generation = request.POST['type_partage_generation']
        
            #DataType
            generation = Generation("generation"+nbr)
            generation.nom_generation.append(nom_generation)
            generation.debut_periode.append(debut_periode)
            generation.fin_periode.append(fin_periode)
            generation.type_de_partage.append(type_partage_generation)

            classe = Classe("cls"+nbr)
            classe.nom_classe.append(nom_classe)

            element = Element("ele"+nbr)
            element.nom_element.append(nom_element)

            argumentation = Argumentation("arg"+nbr)
            argumentation.nom_argumentation.append(nom_argumentation)

            #ObjectProperty

            generation.possede = [argumentation, element]
            element.appartient= [classe]

        ontologie_historique.save()

        

        file = open("apps/connaissance/static/viz-onto/viz_historique.ttl", "a")

        a = '\n:generation'+nbr+' a :Generation ;\n'
        a +='\t' + ':nom ' + '"'+nom_generation+'"' + ' ;\n'
        a +='\t' + ':debut_periode ' + '"'+debut_periode+'"' + ' ;\n'
        a +='\t' + ':fin_periode ' + '"'+fin_periode+'"' + ' ;\n'
        a += '\t' + ':possede' + ' :arg'+nbr+', :ele'+nbr+' ;\n' #argumentation --- arg, element---ele
        a +='\t' + ':type_de_partage ' + '"'+type_partage_generation+'"' + ' .\n'

        a += ':arg'+nbr+' a :Argumentation ;\n'
        a +='\t' + ':nom ' + '"'+ nom_argumentation+'"' + ' .\n'

        a += ':ele'+nbr+' a :Element ;\n'
        a +='\t' + ':nom ' + '"'+nom_element+'"' + ' ;\n'
        a += '\t' + ':appartient' + ' :cls'+nbr+' .\n'  

        a += ':cls'+nbr+' a :Classe ;\n' #classse--- cls
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

        
def ajouter_ontologie_activite(request):

    if 'activite' in request.POST:

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

        ontologie_activite = get_ontology("file://apps/connaissance/static/ontologie-data/ontologie_activite.owl").load()

        with ontologie_activite:

            class Activite(Thing): pass
            class Acteur(Thing): pass

            class nom_activite(Activite >> str): pass
            class nom_acteur(Acteur >> str): pass
            class caracteristique_acteur(Acteur >> str): pass
            class nom_ressource(Activite >> str): pass
            class nom_entre(Activite>> str): pass
            class nom_sortie(Activite >> str): pass
            class type_de_partage(Activite >> str): pass

            #instance

            class possede(ObjectProperty):
                domain = [Activite]
                range = [Acteur]

            nom_activite = request.POST['nom_activite']
            nom_acteur = request.POST['nom_acteur']
            caracteristique_acteur = request.POST['caracteristique_acteur']
            nom_entre = request.POST['nom_entre']
            nom_sortie = request.POST['nom_sortie']
            nom_ressource = request.POST['nom_ressource']

            type_partage_activite = request.POST['type_partage_activite']

            activite = Activite("activite"+nbr)
            activite.nom_activite.append(nom_activite)
            activite.nom_entre.append(nom_entre)
            activite.nom_sortie.append(nom_sortie)
            activite.nom_ressource.append(nom_ressource)
            activite.type_de_partage.append(type_partage_activite)
            acteur = Acteur("act"+nbr)
            acteur.nom_acteur.append(nom_acteur)
            acteur.caract_acteur.append(caracteristique_acteur)

            activite.possede = [Acteur]
            
            

        ontologie_activite.save()

        #Visualisation
        

        file = open("apps/connaissance/static/viz-onto/viz_activite.ttl", "a")

        a = '\n:activite'+nbr+' a :Activite ;\n'
        a +='\t' + ':nom ' + '"'+nom_activite+'"' + ' ;\n'
        a +='\t' + ':possede :act'+nbr+' ;\n'
        a += '\t' + ':ressource ' + '"'+nom_ressource+'"' + ' ;\n'
        a += '\t' + ':entre ' + '"'+nom_entre+'"' + ' ;\n'
        a += '\t' + ':sortie ' + '"'+nom_sortie+'"' + ' ;\n'
        a +='\t' + ':type_de_partage ' + '"'+type_partage_activite+'"' + ' .\n'
        a += ':act'+nbr+' a :Acteur ;\n'
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

        ################################
 
def ajouter_ontologie_phenomene(request):
    if 'phenomene' in request.POST:
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
        ontologie_phenomene = get_ontology("file://apps/connaissance/static/ontologie-data/ontologie_phenomene_metier.owl").load()
    #Classes
        with ontologie_phenomene:
            class Environnement_influenceur(Thing): pass
            class Flux(Thing): pass
            class Phenomene_metier(Thing): pass
            class System_cible(Thing): pass
            class System_source(Thing): pass
    #ObjectProperty
            class affecte(Flux >> System_cible): pass
            class genere(ObjectProperty):
                domain = [System_source]
                range = [Flux]
            class possede(ObjectProperty):
                domain = [Phenomene_metier]
                range = [System_source, Environnement_influenceur, Flux, System_cible]
    #DatatypeProperty
            class action_system_source(System_source >> str): pass
            class nom_evenement_initiateur(System_source >> str): pass
            class nom_caracteristique(Environnement_influenceur >> str): pass
            class nom_champ_actif(System_cible >> str): pass
            class nom_consequence(System_cible >> str): pass
            class nom_environnement_influenceur(Environnement_influenceur >> str): pass
            class nom_flux(Flux >> str): pass
            class type_flux(Flux >> str): pass
            class nom_phenomene(Phenomene_metier >> str): pass
            class nom_system_cible(System_cible >> str): pass
            class nom_system_source(System_source >> str): pass
            class type_de_partage(Phenomene_metier >> str): pass
            nom_phenomene = request.POST['nom_phenomene']
            nom_system_source = request.POST['nom_system_source']
            nom_system_cible = request.POST['nom_system_cible']
            action_system_source = request.POST['action_system_source']
            nom_evenement_initiateur = request.POST['nom_evenement_initiateur']
            nom_flux = request.POST['nom_flux']
            type_flux = request.POST['type_flux']
            nom_environnement_influenceur = request.POST['nom_environnement_influenceur']
            nom_caracteristique = request.POST['nom_caracteristique']
            nom_system_cible = request.POST['nom_system_cible']
            nom_champ_actif = request.POST['nom_champ_actif']
            nom_consequence = request.POST['nom_consequence']
            type_partage_phenomene = request.POST['type_partage_phenomene']
            phenomene = Phenomene_metier("phenomene"+nbr)
            system_source = System_source("ss"+nbr)
            evenement_influenceur = Environnement_influenceur("ev"+nbr)
            system_cible = System_cible("sc"+nbr)
            flux = Flux("f"+nbr)
            phenomene.nom_phenomene.append(nom_phenomene)
            phenomene.type_de_partage.append(type_partage_phenomene)
            phenomene.possede = [system_source, evenement_influenceur, flux, system_cible] 
            system_source.nom_system_source.append(nom_system_source)
            system_source.action_system_source.append(action_system_source)
            system_source.nom_evenement_initiateur.append(nom_evenement_initiateur)
            flux.nom_flux.append(nom_flux)
            flux.type_flux.append(type_flux)
            system_source.genere=[flux]
            evenement_influenceur.nom_environnement_influenceur.append(nom_environnement_influenceur)
            evenement_influenceur.nom_caracteristique.append(nom_caracteristique)
            system_cible.nom_system_cible.append(nom_system_cible)
            system_cible.nom_champ_actif.append(nom_champ_actif)
            system_cible.nom_consequence.append(nom_consequence)
            flux.affecte = [system_cible]

            
        ontologie_phenomene.save()

        
        #Visualisation
        
        file = open("apps/connaissance/static/viz-onto/viz_phenomene.ttl", "a")
        a = '\n:phenomene'+nbr+' a :Phenomene_Metier ;\n'
        a +='\t' + ':nom ' + '"'+nom_phenomene+'"' + ' ;\n'
        a += '\t' + ':possede' + ' :f'+nbr+', :ss'+nbr+', :sc'+nbr+', :ev'+nbr+' ;\n'  #flux --- f, system_source --- ss
        a +='\t' + ':type_de_partage ' + '"'+type_partage_phenomene+'"' + ' .\n'
        a += ':ss'+nbr+' a :System_Source ;\n'
        a += '\t' + ':nom ' + '"'+nom_system_source+'"' + ' ;\n'
        a += '\t' + ':action_source ' + '"'+action_system_source+'"' + ' ;\n'
        a += '\t' + ':evenment_initiateur ' + '"'+nom_evenement_initiateur+'"' + ' ;\n'#genere
        a += '\t' + ':genere :f'+nbr+' .\n'
        a += ':f'+nbr+' a :Flux ;\n'
        a += '\t' + ':nom ' + '"'+nom_flux+'"' + ' ;\n'
        a += '\t' + ':type ' + '"'+type_flux+'"' + ' ;\n'
        a += '\t' + ':afecte :sc'+nbr+' .\n'
        a += ':sc'+nbr+' a :System_Cible ;\n'#system_cible --- sc
        a += '\t' + ':nom ' + '"'+nom_system_cible+'"' + ' ;\n'
        a += '\t' + ':champ_actif ' + '"'+nom_champ_actif+'"' + ' ;\n'
        a += '\t' + ':consequence ' + '"'+nom_consequence+'"' + ' .\n'
        a += ':ev'+nbr+' a :Environnement_influenceur ;\n'
        a += '\t' + ':nom ' + '"'+nom_environnement_influenceur+'"' + ' ;\n'
        a += '\t' + ':caracteristique ' + '"'+nom_caracteristique+'"' + ' .\n'
        file.write(a)
        file.close()
        filewrite = open("phenomene"+nbr+".ttl", "w")

        filewrite.write("@prefix : <http://dig.isi.edu/> .\n"+
                        "@prefix rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n"+
                        "@prefix owl:   <http://www.w3.org/2002/07/owl#> .\n"+
                        "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n\n")
        filewrite.write(a)
        filewrite.close()
        os.system("python apps/visualisation/ontology_viz.py -o phenomene"+nbr+".dot phenomene"+nbr+
        ".ttl -O apps/connaissance/static/ontologie-data/ontology_phenomene.ttl")
        os.remove("phenomene"+nbr+".ttl")
        os.system("dot -Tpng -o "+ "apps/connaissance/static/formalismes/phenomene/phenomene" +nbr+".png phenomene"+nbr+".dot")
        os.remove("phenomene"+nbr+".dot")


def ajouter_ontologie_strategie(request):
    """
    ontologie_strategie = get_ontology("file://static/ontologie-data/ontologie_strategie.owl").load()


    with ontologie_strategie:
        class Axe_competence(Thing): pass
        class Axe_processus(Axe_competence): pass
        class Axe_strategique(Thing): pass
        class Orientation_strategique(Axe_strategique): pass
        class Theme_strategique(Orientation_strategique): pass

        class Ceour_metier(Thing): pass
        class Competence(Thing): pass
        class Sous_competence(Competence): pass
        class Facteur_externe(Thing): pass
        class Facteur_interne(Thing): pass
        class Mission(Thing): pass
        class Strategie(Thing): pass


        class composer_de(Axe_strategique >> Competence): pass
        class est_composer(Ceour_metier >> Axe_processus): pass
        class strategie_possede(ObjectProperty):
            domain = [Strategie]
            range = [Facteur_externe, Facteur_interne, Mission, Competence]


        class nom_axe_competence(Axe_competence >> str): pass
        class nom_axe_processus(Axe_processus >> str): pass
        class nom_ceour_metier(Ceour_metier >> str): pass
        class nom_facteur_interne(Facteur_interne >> str): pass
        class nom_facteur_externe(Facteur_externe >> str): pass
        class nom_mission(Mission >> str): pass
        class nom_orientation_strategique(Orientation_strategique >> str): pass
        class nom_strategie(Strategie >> str): pass
        class nom_theme_strategique(Theme_strategique >> str): pass
        class type_facteur_externe(Facteur_externe >> str): pass
        class type_facteur_interne(Facteur_interne >> str): pass

    ontologie_strategie.save()
"""

    if 'strategique' in request.POST:

        nom_strategie = request.POST['nom_strategie']
        nom_mission = request.POST['nom_mission']
        nom_facteur_interne = request.POST['nom_facteur_interne']
        type_facteur_interne = request.POST['type_facteur_interne']
        nom_facteur_externe = request.POST['nom_facteur_externe']
        type_facteur_externe = request.POST['type_facteur_externe']
        nom_competence = request.POST['nom_competence']
        #nom_sous_competence = request.POST['nom_sous_competence']

        #nom_axe_competence = request.POST['nom_axe_competence']
        #nom_processus = request.POST['nom_processus']
        #ceour_metier = request.POST['ceour_metier']

        nom_axe_strategie = request.POST['nom_axe_strategie']
        #orientation_strategique = request.POST['orientation_strategique']
        #theme_strategie = request.POST['theme_strategie']


        type_paratage_strategie=request.POST['type_partage_strategique']


        g = rdflib.Graph()
        g.parse("apps/connaissance/static/viz-onto/viz_strategie.ttl")
        query = """
        SELECT ?strategie
        WHERE {
            ?strategie a :Strategie .
        }"""
        qres = g.query(query)
        strategies = []

        for row in qres:
            strategie = str(row.strategie).replace('http://dig.isi.edu/', '')
            strategies.append(strategie)

        nbr=len(strategies)
        nbr = nbr + 1
        nbr = str(nbr)

        file = open("apps/connaissance/static/viz-onto/viz_strategie.ttl", "a")

        a = '\n:strategie'+nbr+' a :Strategie ;\n'
        a +='\t' + ':nom ' + '"'+nom_strategie+'"' + ' ;\n'
        a += '\t' + ':possede' + ' :mi, :fi, :fe, :com, :axs ;\n'  #flux --- f, system_source --- ss
        a +='\t' + ':type_de_partage ' + '"'+type_paratage_strategie+'"' + ' .\n'
        
        a += ':fe a :Facteur_externe ;\n'
        a += '\t' + ':nom ' + '"'+nom_facteur_externe+'"' + ' ;\n'
        a += '\t' + ':type ' + '"'+type_facteur_externe+'"' + ' .\n'

        a += ':fi a :Facteur_interne ;\n'
        a += '\t' + ':nom ' + '"'+nom_facteur_interne+'"' + ' ;\n'
        a += '\t' + ':type ' + '"'+type_facteur_interne+'"' + ' .\n'

        a += ':mi a :Mission ;\n'#system_cible --- sc
        a += '\t' + ':nom ' + '"'+nom_mission+'"' + ' .\n'

        a += ':com a :Competence ;\n'#system_cible --- sc
        a += '\t' + ':nom ' + '"'+nom_competence+'"' + ' .\n'

        a += ':axs a :Axe_strategique ;\n'#system_cible --- sc
        a += '\t' + ':nom ' + '"'+nom_axe_strategie+'"' + ' .\n'

        file.write(a)
        file.close()

        filewrite = open("strategie"+nbr+".ttl", "w")

        filewrite.write("@prefix : <http://dig.isi.edu/> .\n"+
                        "@prefix rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n"+
                        "@prefix owl:   <http://www.w3.org/2002/07/owl#> .\n"+
                        "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n\n")

        filewrite.write(a)
        filewrite.close()

        os.system("python apps/visualisation/ontology_viz.py -o strategie"+nbr+".dot strategie"+nbr+".ttl -O apps/connaissance/static/ontologie-data/ontology_strategique.ttl")
        os.remove("strategie"+nbr+".ttl")
        os.system("dot -Tpng -o "+ "apps/connaissance/static/formalismes/strategique/strategie" +nbr+".png strategie"+nbr+".dot")
        os.remove("strategie"+nbr+".dot")

def ontologie_tache():
    
    ontologie_tache = get_ontology("file://apps/connaissance/static/ontologie-data/ontologie_tache.owl").load()

    with ontologie_tache:

        class Tache(Thing): pass
        class suit(Tache >> Tache): pass
        class nom_tache(Tache >> str): pass
        class type_tache(Tache >> str): pass
        class type_de_partage(Tache >> str): pass
        class condition_tache(Tache >> str): pass
            
            

    ontologie_tache.save()
