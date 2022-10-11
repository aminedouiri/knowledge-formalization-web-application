from django.shortcuts import render, redirect
from apps.connaissance.models import Connaissance
from apps.commentaire.models import Commentaire
from apps.userprofile.models import Userprofile
import os, rdflib
from owlready2 import *

# Create your views here.

def models(request):

    if request.user.is_authenticated:

        model = ('tache', 'phenomene', 'activite','strategie', 'historique', 'domaine')

        connaissanceNotification = Connaissance.objects.filter(status_vue=False).count()
        commentaires = Commentaire.objects.all()
        connaissanceNotification += commentaires.count()
        context = {
            'model': model,
            'connaissanceNotification': connaissanceNotification,
        }
        return render(request, 'models/models.html', context)
    else:
        return redirect('login')

def model_element(request, mymodele):

    connaissanceNotification = Connaissance.objects.filter(status_vue=False).count()
    commentaires = Commentaire.objects.all()
    connaissanceNotification += commentaires.count()

    context = {
        'mymodele': mymodele,
        'connaissanceNotification': connaissanceNotification,
    }
    return render(request, 'models/model_element.html', context)


def model_domaine(request):
    if request.user.is_authenticated:
        connaissance_list = Connaissance.objects.all()
        connaissanceNotification = Connaissance.objects.filter(status_vue=False).count()

        context = {
            'connaissance_list': connaissance_list,
            'connaissanceNotification': connaissanceNotification,
        }

        if 'domaine' in request.POST:

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

            nbr=len(domaines)
            nbr = nbr + 1
            nbr = str(nbr)


            ontologie_domaine= get_ontology("file://apps/connaissance/static/ontologie-data/ontologie_domaine.owl").load()


            with ontologie_domaine:

                class Attribute(Thing): pass
                class Attribute_role(Thing): pass
                class Calculation_fonction(Thing): pass
                class Conclusion(Thing): pass
                class Domaine(Thing): pass
                class Object(Thing): pass
                class Permise(Thing): pass
                class Probleme(Thing): pass
                class Probleme_attribute(Thing): pass
                class Resolution(Thing): pass
                class Step(Thing): pass

            #les objects property
                class possede(ObjectProperty):
                    domain = [Domaine, Resolution, Probleme, Object, Probleme_attribute, Attribute_role, Conclusion]
                    range = [Probleme, Object, Step, Probleme_attribute, Attribute, Attribute_role, Conclusion, Calculation_fonction]
                class est_decrit_par(ObjectProperty):
                    domain = [Probleme]
                    range = [Object]
                class est_resolu_par(ObjectProperty):
                    domain = [Probleme]
                    range = [Resolution]
                class est_liee_a(ObjectProperty):
                    domain = [Attribute_role]
                    range = [Permise]
            

            ##########
                class domaine_name(Domaine >> str): pass
                class type_de_partage(Domaine >> str): pass
                class probleme_name(Probleme >> str): pass
                class probleme_status(Probleme >> str): pass
                class object_name(Object >> str): pass
                class attribute_name(Attribute >> str): pass
                class attribute_type(Attribute >> str): pass
                class probleme_attribute_name(Probleme_attribute >> str): pass
                class probleme_attribute_value(Probleme_attribute >> int): pass
                class calculation_fonction_description(Calculation_fonction >> str): pass
                class calculation_fonction_name(Calculation_fonction >> str): pass
                class calculation_fonction_nombre_parametres(Calculation_fonction >> int): pass
                class attribute_role_name(Attribute_role >> str): pass
                class permises_description(Permise >> str): pass
                class resolution_name(Resolution >> str): pass 
                class step_name(Step >> str): pass
                class step_description(Step >> str): pass 


            #Instance

                domaine_name = request.POST['domaine_name']
                object_name = request.POST['object_name']
                attribute_name = request.POST['attribute_name1']
                attribute_type = request.POST['attribute_type1']
                probleme_name = request.POST['probleme_name']
                probleme_status = request.POST['probleme_status']
                probleme_attribute_name = request.POST['probleme_attribute_name1']
                probleme_attribute_value = request.POST['probleme_attribute_value1']
                attribute_role_name = request.POST['attribute_role_name1']
                permises_description = request.POST['permises_description1']
                conclusion_name = request.POST['conclusion_name1']
                resolution_name = request.POST['resolution_name']
                step_name = request.POST['step_name1']
                step_description = request.POST['step_description1']
                calculation_fonction_name = request.POST['calculation_fonction_name']
                calculation_fonction_description = request.POST['calculation_fonction_description']
                nombre_parametre_calculation_fonction = request.POST['nombre_parametre_calculation_fonction']
                type_partage_domaine = request.POST['type_partage_domaine']

                domainee = Domaine("domaine"+nbr)
                probleme = Probleme("pro"+nbr)
                object = Object("obj"+nbr)
                resolution = Resolution("res"+nbr)
                probleme_attribute = Probleme_attribute("proatt"+nbr)
                attribute = Attribute("at"+nbr)
                attribute_role = Attribute_role("att"+nbr)
                step = Step("st"+nbr)
                permise = Permise("per"+nbr)
                conclusion = Conclusion("con"+nbr)
                calculation_fonction = Calculation_fonction("cal"+nbr)

                domainee.domaine_name.append(domaine_name)
                domainee.type_de_partage.append(type_partage_domaine)
                probleme.probleme_name.append(probleme_name)
                probleme.probleme_status.append(probleme_status)
                object.object_name.append(object_name)
                attribute.attribute_name.append(attribute_name)
                attribute.attribute_type.append(attribute_type)
                probleme_attribute.probleme_attribute_name.append(probleme_attribute_name)
                probleme_attribute.probleme_attribute_value.append(probleme_attribute_value)
                calculation_fonction.calculation_fonction_description.append(calculation_fonction_description)
                calculation_fonction.calculation_fonction_name.append(calculation_fonction_name)
                calculation_fonction.calculation_fonction_nombre_parametres.append(nombre_parametre_calculation_fonction)
                attribute_role.attribute_role_name.append(attribute_role_name)
                permise.permises_description.append(permises_description)
                resolution.resolution_name.append(resolution_name)
                step.step_name.append(step_name)
                step.step_description.append(step_description)


                domainee.possede = [probleme]
                probleme.possede = [probleme_attribute]
                probleme.est_decrit_par = [object]
                probleme.possede = [attribute]
                probleme.est_resolu_par = [resolution]
                probleme_attribute.possede = [attribute_role]
                resolution.possede = [step]
                attribute_role.est_liee_a = [permise]
                attribute_role.possede = [conclusion]
                conclusion.possede = [calculation_fonction]

            ontologie_domaine.save()


            file = open("apps/connaissance/static/viz-onto/viz_domaine.ttl", "a")

            a = '\n:domaine'+nbr+' a :Domaine ;\n'
            a +='\t' + ':nom ' + '"'+domaine_name+'"' + ' ;\n'
            a += '\t' + ':possede' + ' :obj'+nbr+', :pro'+nbr+' ;\n' 
            a +='\t' + ':type_de_partage ' + '"'+type_partage_domaine+'"' + ' .\n'

            a += ':att'+nbr+' a :Attribute_role ;\n'
            a +='\t' + ':nom ' + '"'+attribute_role_name+'"' + ' ;\n'
            a += '\t:possede :con'+nbr+' ;\n'
            a += '\t:est_liee_a :per'+nbr+' .\n'

            a += ':per'+nbr+' a :Permise ;\n'
            a += '\t:description ' + '"'+permises_description+'"' + ' .\n'

            a += ':con'+nbr+' a :Conclusion ;\n'
            a +='\t:nom ' + '"'+conclusion_name+'"' + ' ;\n'
            a += '\t:possede :cal'+nbr+' .\n' 

            a += ':cal'+nbr+' a :Calculation_fonction ;\n'
            a += '\t:nom ' + '"'+calculation_fonction_name+'"' + ' ;\n'
            a += '\t:description ' + '"'+calculation_fonction_description+'"' + ' ;\n'
            a += '\t:nombre ' + '"'+nombre_parametre_calculation_fonction+'"' + ' .\n'

            a += ':obj'+nbr+' a :Object ;\n'
            a +='\t:nom ' + '"'+object_name+'"' + ' ;\n'
            a += '\t:possede' + ' :at'+nbr+' .\n' 

            a += ':at'+nbr+' a :Attribute ;\n'
            a +='\t' + ':nom ' + '"'+attribute_name+'"' + ' ;\n'
            a += '\t' + ':type ' + '"'+attribute_type+'"' + ' .\n' 

            a += ':pro'+nbr+' a :Probleme ;\n'
            a +='\t' + ':nom ' + '"'+probleme_name+'"' + ' ;\n'
            a +='\t' + ':status ' + '"'+probleme_status+'"' + ' ;\n' 
            a += '\t:est_decrit_par :obj'+nbr+' ;\n'
            a +='\t' + ':possede :proatt'+nbr+' ;\n'
            a += '\t' + ':est_resolu_par :res'+nbr+' .\n' 

            a += ':res'+nbr+' a :Resolution ;\n'
            a += '\t' + ':nom ' + '"'+resolution_name+'"' + ' ;\n'
            a +='\t' + ':possede :st'+nbr+' .\n'

            a += ':proatt'+nbr+' a :Probleme_attribute ;\n'
            a +='\t' + ':nom ' + '"'+probleme_attribute_name+'"' + ' ;\n'
            a +='\t' + ':value ' + '"'+probleme_attribute_value+'"' + ' ;\n'
            a += '\t' + ':possede :att'+nbr+' .\n'

            a += ':st'+nbr+' a :Step ;\n'
            a +='\t' + ':nom ' + '"'+step_name+'"' + ' ;\n'
            a +='\t' + ':description ' + '"'+step_description+'"' + ' .\n'


            file.write(a)
            file.close()

            filewrite = open("domaine"+nbr+".ttl", "w")

            filewrite.write("@prefix : <http://dig.isi.edu/> .\n"+
                            "@prefix rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n"+
                            "@prefix owl:   <http://www.w3.org/2002/07/owl#> .\n"+
                            "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n\n")

            filewrite.write(a)
            filewrite.close()

            os.system("python apps/visualisation/ontology_viz.py -o domaine"+nbr+".dot domaine"+nbr+".ttl -O apps/connaissance/static/ontologie-data/ontology_domaine.ttl")
            os.remove("domaine"+nbr+".ttl")
            os.system("dot -Tpng -o "+ "apps/connaissance/static/formalismes/domaine/domaine" +nbr+".png domaine"+nbr+".dot")
            os.remove("domaine"+nbr+".dot")

        return render(request, 'domaine/domaine.html', context)

    else:
        return redirect('notFound')



   