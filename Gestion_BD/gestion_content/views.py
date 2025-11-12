from datetime import timezone
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render,redirect
from Gestion_BD.settings import EMAIL_HOST_USER
from gestion_content.models import *
from gestion_utilisateur.models import *
from .form import NotationForm
from django.db.models import Avg,Q
from django.core.paginator import Paginator
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.template.loader import render_to_string
from django.db.models import Q, Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def auteur(request):
    User = get_user_model()

    auteurs_vedettes_principaux = User.objects.filter(role="auteur", vedette=True, valid_auteur=True)[:6]
    vedettes_ids = [auteur.id for auteur in auteurs_vedettes_principaux]

    auteurs_par_pays = User.objects.filter(role="auteur", valid_auteur=True).exclude(id__in=vedettes_ids).values('pays').annotate(count=Count('id')).order_by('pays')
    auteurs_par_pays_list = []
    for pays_data in auteurs_par_pays:
        auteurs_du_pays = User.objects.filter(role="auteur", pays=pays_data['pays'], valid_auteur=True).exclude(id__in=vedettes_ids).order_by('?')[:2]
        auteurs_par_pays_list.extend(auteurs_du_pays)

    tous_les_auteurs = User.objects.filter(role="auteur", valid_auteur=True).exclude(id__in=vedettes_ids)

    exclude_vedettes = request.GET.get('exclude_vedettes')
    if exclude_vedettes == 'true':
        tous_les_auteurs = tous_les_auteurs.exclude(vedette=True)

    pays_filtre = request.GET.get('pays', '')
    if pays_filtre:
        tous_les_auteurs = tous_les_auteurs.filter(pays=pays_filtre)

    q = request.GET.get('q', '')
    if q:
        tous_les_auteurs = tous_les_auteurs.filter(username__icontains=q) | tous_les_auteurs.filter(email__icontains=q)

    paginator = Paginator(tous_les_auteurs, 30)
    page_number = request.GET.get('page')
    auteurs_paginated = paginator.get_page(page_number)

    genres = Genre.objects.all()
    pays_list = dict(User.PAYS_AFRICAINS)
    usere = request.user
    profil = None
    if usere.is_authenticated:
        try:
            profil = User.objects.get(id=usere.id)
        except User.DoesNotExist:
            profil = None

    context = {
        'auteurs_filtrés': auteurs_paginated,
        'genres': genres,
        'pays_list': pays_list,
        'user_authenticate': request.user.is_authenticated,
        'user': request.user,
        'profil': profil,
        'auteurs_vedettes_principaux': auteurs_vedettes_principaux,
        'auteurs_par_pays_list': auteurs_par_pays_list,
    }

    return render(request, 'gestion_content/auteur.html', context)



def detail_auteur(request, auteur_id):
    edition_choice = Work.choix_edition
    genre_choice =Work.choix_genre
    influence_choice = Work.choix_influence
    totatl_notif = 0
    nb_notif = 0
    user_authenticate = request.user.is_authenticated
    usere = request.user
    try:
     profil = Utilisateur.objects.get(id=usere.id)
    except Utilisateur.DoesNotExist:
     profil = None
     # Récupérer l'auteur
    auteur = get_object_or_404(Utilisateur, id=auteur_id)

    # Récupérer toutes les œuvres de cet auteur avec la moyenne des notations
    oeuvres = Work.objects.filter(author=auteur).annotate(moyenne_note=Avg('notation__rating'))
    auteur_oeuvre = Work.objects.filter(author=auteur)
    print(auteur_oeuvre)
    # Récupérer toutes les notations liées aux œuvres de cet auteur
    notations = Notation.objects.filter(work__in=oeuvres).select_related('user', 'work')
    # notif = Notation.objects.all().count()
    liens_sociaux = Social_link.objects.filter(user=auteur)


    # print(notations.all().count())
    # Gestion du formulaire de notation sans utiliser Django Forms
    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'notation':
            comment = request.POST.get('comment')
            rating = request.POST.get('rating')
            if comment and rating:
                work = oeuvres.first()
                if work:
                    Notation.objects.create(
                        user=request.user,
                        work=work,
                        rating=int(rating),
                        comment=comment
                    )
            return redirect('detail_auteur', auteur_id=auteur_id)
        
        elif form_type == 'ajout_reseaux':
           plateforme = request.POST.get('plateforme')
           url = request.POST.get('url')
           reseau = Social_link.objects.create(
              plateforme = plateforme,
              url = url,
              user = auteur
           )
           reseau.save()
           return redirect('detail_auteur',auteur_id=auteur_id)
           

        elif form_type == 'ajout_oeuvre':
            edition = request.POST.get('edition')
            genre = request.POST.get('genre')
            influence = request.POST.get('influence')
            titre = request.POST.get('titre')
            contenue = request.POST.get('description')  # correspond à "name='description'" dans le HTML
            image = request.FILES.get('image')
            # genre = request.POST.get('genre')  # à adapter si tu l'ajoutes dans le formulaire
            date = request.POST.get('annee')  # correspond à "name='annee'" dans le HTML
            planche1 = request.FILES.get('planche1')
            planche2 = request.FILES.get('planche2')

            # try:
            #     genre_instance = Genre.objects.get(id=genre)
            # except Genre.DoesNotExist:
            #     genre_instance = None

            oeuvre = Work.objects.create(
                title=titre,
                description=contenue,
                author=auteur,
                edition = edition,
                genres = genre,
                influence = influence,
                planche1 = planche1,
                planche2 = planche2,
                # genres=genre_instance,
                cover_image=image,
                publication_date=date
            )
            return redirect('detail_auteur', auteur_id=auteur_id)



    return render(request, 'gestion_content/detail.html', {
        'auteur': auteur,
        'oeuvres': oeuvres,
        'notations': notations,
        # 'social_links':social_links,
        'nb_notif':nb_notif,
        'user_authenticate':user_authenticate,
        'profil':profil,
        'user': request.user,
        'auteur_oeuvre':auteur_oeuvre,
        'liens_sociaux':liens_sociaux,
        "reseau_choice":Social_link.lien,
        "edition":edition_choice,
        'genre':genre_choice,
        'influence':influence_choice
    })

def detail_auteur2(request):
   return render(request,'gestion_content/detail2.html')





def actualite(request):
    actualite = BlogPost.objects.filter(valid=True).all()

    return render(request,'gestion_content/actualite.html',{'actualite':actualite})

def text_affichage(request):
    auteurs = Utilisateur.objects.all().filter(role="auteur")

    # Récupérer les filtres sélectionnés
    genres = request.GET.getlist('genre')  # Liste des genres sélectionnés
    pays = request.GET.getlist('pays')  # Liste des pays sélectionnés

    # Appliquer les filtres si des options sont sélectionnées
    if genres:
        auteurs = auteurs.filter(genre__id__in=genres)  # Filtrer par genres

    if pays:
        auteurs = auteurs.filter(pays__in=pays)  # Filtrer par pays

    # Vérifier si c'est une requête AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'gestion_content/text.html', {'auteurs': auteurs})

    # Si ce n'est pas une requête AJAX, renvoyer la page complète
    return render(request, 'gestion_content/text.html', {'auteurs': auteurs,"genres":genres})


def texte_mail(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        suject = "texte"
        message = "salut c'est juste un texte"
        from_email = EMAIL_HOST_USER
        to_email = [email]
        email = EmailMessage(suject, message, from_email, to_email)
        email.send()
    return render(request,'gestion_content/texte_mail.html')


def profil_auteur(request):
    totatl_notif = 0
    nb_notif = 0
    user_authenticate = request.user.is_authenticated
    genrese = Genre.objects.all()
     # Récupérer l'auteur
    auteur = request.user

    # Récupérer toutes les œuvres de cet auteur avec la moyenne des notations
    oeuvres = Work.objects.filter(author=auteur).annotate(moyenne_note=Avg('notation__rating'))


    # Récupérer toutes les notations liées aux œuvres de cet auteur
    notations = Notation.objects.filter(work__in=oeuvres).select_related('user', 'work')
    # notif = Notation.objects.all().count()
    # social_links = auteur.social_links if auteur.social_links else {}


    # print(notations.all().count())
    # Gestion du formulaire de notation sans utiliser Django Forms


    if notations:
        for each_notif in notations:
          totatl_notif = totatl_notif + each_notif.rating

    notation = Notation.objects.filter(work__in=oeuvres).count()
    print(notation)
    if notation !=0:
       nb_notif = totatl_notif/notation

    if request.method == 'POST':
        titre = request.POST.get('titre')
        contenue = request.POST.get('contenue')
        image = request.FILES.get('image')
        genre = request.POST.get('genre')
        try:
          genre_instance = Genre.objects.get(id=genre)  # Trouver l'objet Genre correspondant
        except Genre.DoesNotExist:
         genre_instance = None
        oeuvre = Work.objects.create(
            title = titre,
            description = contenue,
            author = auteur,
            genres = genre_instance,
            cover_image = image
        )
        oeuvre.save()


    return render(request, 'gestion_content/profil_auteur.html', {
        'auteur': auteur,
        'oeuvres': oeuvres,
        'notations': notations,
        # 'social_links':social_links,
        'nb_notif':nb_notif,
        'user_authenticate':user_authenticate,
        'genres':genrese
    })




def custom_404_view(request, exception):
    # Vous pouvez passer du contexte si nécessaire
    return render(request, 'gestion_content/page404.html', status=404)





def Librairies(request):
    # 1. Récupération des données pour les sections
    librairies_vedettes = Librairie.objects.filter(vedette=True, valide=True)[:6]

    # --- Équivalent du bloc villes pour les tuiles ---
    villes = (Librairie.objects.filter(valide=True)
              .values('ville')
              .annotate(count=Count('id'))
              .order_by('ville'))

    # 2. Logique de Filtrage
    librairies = Librairie.objects.filter(valide=True).order_by('nom') # Tri par défaut

    # Filtre par Pays
    pays_filtre = request.GET.get('pays', '')
    if pays_filtre:
        librairies = librairies.filter(pays=pays_filtre)
    
    # NOUVEAU: Filtre par Ville
    ville_filtre = request.GET.get('ville', '')
    if ville_filtre:
        librairies = librairies.filter(ville__iexact=ville_filtre) # iexact pour insensible à la casse et exact
        
    # Recherche (nom de librairie)
    q = request.GET.get('q', '')
    if q:
        # Recherche dans le nom OU dans la ville
        librairies = librairies.filter(Q(nom__icontains=q) | Q(ville__icontains=q)).distinct()

    # 3. Pagination 
    paginator = Paginator(librairies, 10)
    page_number = request.GET.get('page')
    librairies_paginated = paginator.get_page(page_number)

    # Liste complète des pays africains
    pays_list = dict(Utilisateur.PAYS_AFRICAINS) # Assurez-vous que Utilisateur est importé

    return render(request, "gestion_content/librairie.html", {
        "librairies_filtrees": librairies_paginated,
        "librairies_vedettes": librairies_vedettes,
        "villes": villes,
        "pays_list": pays_list,
        "q_recherche": q, # Renvoyer le terme de recherche pour le conserver dans l'input
        "pays_filtre": pays_filtre, # Renvoyer le filtre pays pour le conserver
        "ville_filtre": ville_filtre, # Renvoyer le filtre ville
        'user_authenticate':request.user.is_authenticated
    })



# vue de detail pour librairie




# NOTE IMPORTANTE: J'assume que PAYS_AFRICAINS est défini quelque part, par exemple dans votre modèle Utilisateur.
# PAYS_AFRICAINS est une liste de tuples (code, nom).

def detail_librairie(request, librairie_id):
    """
    Affiche la page de détail d'une librairie spécifique en utilisant son ID.
    """
    # 1. Récupération de l'objet Librairie (retourne 404 si non trouvé)
    librairie = get_object_or_404(Librairie, pk=librairie_id)

    # 2. Préparation des informations de pays
    # Cette étape nécessite d'accéder à la liste PAYS_AFRICAINS
    # (J'utilise ici une méthode générique pour simuler l'accès aux choix)
    
    # Construction d'un dictionnaire pour la traduction du code pays
    try:
        pays_list = dict(Utilisateur.PAYS_AFRICAINS)
        nom_pays = pays_list.get(librairie.pays, librairie.pays)
    except NameError:
        # Solution de repli si Utilisateur.PAYS_AFRICAINS n'est pas accessible
        nom_pays = librairie.pays

    # 3. Préparation du contexte
    context = {
        "librairie": librairie,
        "nom_pays": nom_pays,
        'user_authenticate':request.user.is_authenticated
    }

    return render(request, "gestion_content/detail_librairie.html", context)

def apropos(request):
    info = ''
    profil_choix = Contact.profil_choice
    if request.method == 'POST':
        profil = request.POST.get('profil')
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        societe = request.POST.get('societe')
        email = request.POST.get('email')
        objet = request.POST.get('objet')
        message = request.POST.get('message')
        new = Contact.objects.create(
            profile = profil,
            nom = nom,
            prenom = prenom,
            societe = societe,
            email = email,
            objet = objet,
            message = message
        )
        new.save()
        info = "Votre message a bien été reçue merci pour votre confiance!"
    context = {
        'info':info,
        'profil':profil_choix,
        'user_authenticate':request.user.is_authenticated
    }

    return render(request,'gestion_content/apropos.html',context)

# def editeur(request):
#     return render(request,'gestion_content/editeur.html')


# N'oubliez pas la route dans urls.py :
# path('librairie/<int:librairie_id>/', views.detail_librairie, name='detail_librairie'),


# vue pour edition

def editeur(request):
    """
    Vue affichant la liste des éditeurs avec options de recherche et de filtrage.
    """
    
    # 1. Préparation des données de base
    editeurs_list = Editeur.objects.all().order_by('nom')
    user_authenticate = request.user.is_authenticated
    
    # Récupérer les options de pays pour le filtre (depuis votre modèle Utilisateur)
    # Assurez-vous que PAYS_AFRICAINS est accessible ici, par exemple en l'important depuis settings
    pays_options = getattr(settings, 'PAYS_AFRICAINS', Editeur.utilisateur.field.related_model.PAYS_AFRICAINS)


    # 2. Gestion de la Recherche (query) et des Filtres (country)
    
    # Recherche par nom
    query = request.GET.get('q')
    if query:
        editeurs_list = editeurs_list.filter(
            Q(nom__icontains=query) |
            Q(description__icontains=query)
        ).distinct()
        
    # Filtrage par pays
    country_code = request.GET.get('country')
    if country_code and country_code != 'all':
        # Le pays est stocké dans le modèle Utilisateur, nous filtrons donc sur le OneToOneField
        editeurs_list = editeurs_list.filter(utilisateur__pays__iexact=country_code)

    # Note : Ajoutons les annotations pour le nombre de livres/auteurs (si les modèles Livre et Auteur existent)
    # editeurs_list = editeurs_list.annotate(
    #     num_livres=Count('livre', distinct=True), 
    #     num_auteurs=Count('auteur', distinct=True)
    # )


    # 3. Gestion de la Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(editeurs_list, 10) # 10 éditeurs par page
    
    try:
        editeurs = paginator.page(page)
    except PageNotAnInteger:
        editeurs = paginator.page(1)
    except EmptyPage:
        editeurs = paginator.page(paginator.num_pages)
        
        
    # 4. Contexte à passer au template
    context = {
        'editeurs': editeurs, # Liste paginée des éditeurs
        'nombre_total': editeurs_list.count(),
        'query_recherche': query if query else '',
        'pays_selectionne': country_code if country_code else 'all',
        'pays_options': pays_options, # La liste complète des pays pour la boucle du sélecteur
        'user_authenticate':request.user.is_authenticated
    }
    
    return render(request, 'gestion_content/editeur.html', context)




# Detail edition

from django.db.models import Prefetch

# Si vous avez un modèle d'événement, vous l'importeriez ici
# from .models import Evenement 

def editeur_detail_view(request, id): # J'utilise 'id' car c'est ce que vous avez dans la fonction, bien que 'slug' soit plus commun
    """
    Vue basée sur une fonction pour afficher les détails d'un éditeur.
    """
    # 1. Récupérer l'objet Editeur (via son ID comme dans votre code)
    editeur = get_object_or_404(Editeur, id=id)

    # 2. Préparation des données complexes (Logique de la vue)
    
    # A. Catalogue de livres
    tous_livres_qs = Livre.objects.filter(editeur=editeur)
    tous_livres_count = tous_livres_qs.count()
    livres_publies = tous_livres_qs.order_by('-date_publication')[:10]

    # B. Auteurs distincts (CORRIGÉ)
    # L'accès de Utilisateur à Auteur se fait via 'details_auteur'
    auteurs_editeur = Utilisateur.objects.filter(
        # On filtre les Utilisateurs dont les détails d'auteur ('details_auteur')
        # ont des livres ('livres_principaux' est le related_name par défaut inversé)
        # qui sont publiés par cet éditeur.
        details_auteur__livres_principaux__editeur=editeur 
        # Si vous vouliez inclure tous les livres (principaux et secondaires) :
        # Q(details_auteur__livres_principaux__editeur=editeur) | Q(details_auteur__livres_secondaires__editeur=editeur) 
    ).distinct().order_by('last_name')[:10]
    
    # C. Événements à venir (Logique supposée)
    # On suppose que vous avez un `Evenement` avec une ForeignKey vers `Editeur`.
    # Si le modèle Evenement n'existe pas, cette partie générera une AttributeError.
    try:
        # Utilisez le related_name par défaut 'evenement_set' si aucun n'est spécifié
        evenements_a_venir = editeur.evenement_set.filter(
            date__gte=timezone.now()
        ).order_by('date')[:3]
    except AttributeError:
        # Gère le cas où le modèle Evenement n'est pas encore créé ou lié
        evenements_a_venir = [] 

    # D. CORRECTION DE L'ERREUR DE TEMPLATE (Liens sociaux)
    # Nous calculons les booléens pour éviter les requêtes complexes dans le template
    # J'assume que `editeur.utilisateur.social_link` est une ManyToMany ou ForeignKey inverse.
    try:
        social_links_qs = editeur.utilisateur.social_link.all()
        # Ces variables sont des booléens simples
        has_facebook_link = social_links_qs.filter(plateforme='Facebook').exists()
        has_instagram_link = social_links_qs.filter(plateforme='Instagram').exists()
    except:
        has_facebook_link = False
        has_instagram_link = False
    
    # ...
    
    # 3. Préparation du Contexte
    context = {
        # ... autres variables
        # Variables de correction pour le template
        'has_facebook_link': has_facebook_link,
        'has_instagram_link': has_instagram_link,
        'editeur':editeur,
        'auteurs_editeur':auteurs_editeur,
        'livres_publies':livres_publies,
        'tous_livres_count':tous_livres_count,
        'user_authenticate':request.user.is_authenticated
    }

    # 4. Rendu du template
    return render(request, 'gestion_content/detail_editeur.html', context)

# N'oubliez pas de lier cette vue dans votre urls.py :
# path('editeur/<slug:slug>/', EditeurDetailView.as_view(), name='editeur_detail'),


# vue pour bdtheque

def bdtheque(request):
    
    
    # 1. Requête de base (QuerySet)
    queryset = Livre.objects.all().select_related('editeur', 'auteur_principal__utilisateur').prefetch_related('genres')
    
    # 2. Récupération des paramètres de requête (Filtres)
    query = request.GET.get('q')
    auteur_id = request.GET.get('auteur')
    editeur_id = request.GET.get('editeur')
    genre_slug = request.GET.get('genre')

    # 3. Application des Filtres
    
    # Recherche rapide (q)
    if query:
        queryset = queryset.filter(
            Q(titre__icontains=query) |
            Q(resumé__icontains=query) |
            Q(isbn__icontains=query) |
            # Recherche dans les noms/prénoms/usernames de l'auteur principal
            Q(auteur_principal__utilisateur__username__icontains=query) |
            Q(auteur_principal__utilisateur__first_name__icontains=query) |
            Q(auteur_principal__utilisateur__last_name__icontains=query) |
            # Recherche dans le nom de l'éditeur
            Q(editeur__nom__icontains=query) 
        ).distinct()

    # Filtre par Auteur
    if auteur_id:
        queryset = queryset.filter(auteur_principal__pk=auteur_id)

    # Filtre par Éditeur
    if editeur_id:
        queryset = queryset.filter(editeur__pk=editeur_id)

    # Filtre par Genre (utilise le champ slug)
    if genre_slug:
        queryset = queryset.filter(genres__slug=genre_slug).distinct()
        
    # Ordonner les résultats (par exemple, du plus récent au plus ancien)
    queryset = queryset.order_by('-date_publication')
    
    # Nombre total de résultats (important pour l'affichage)
    total_results = queryset.count()

    # 4. Pagination
    paginator = Paginator(queryset, 12) # 12 livres par page
    page_number = request.GET.get('page', 1) 

    try:
        livres = paginator.page(page_number)
    except PageNotAnInteger:
        livres = paginator.page(1)
    except EmptyPage:
        livres = paginator.page(paginator.num_pages)


    # 5. Préparation du Contexte
    context = {
        # Données principales
        'livres': livres,
        'total_results': total_results,
        
        # Données pour les filtres (Listes complètes pour les menus déroulants)
        'tous_les_auteurs': Auteur.objects.all().select_related('utilisateur').order_by('utilisateur__last_name'),
        'tous_les_editeurs': Editeur.objects.all().order_by('nom'),
        'tous_les_genres': Genre.objects.all().order_by('nom'),
        
        # Valeurs de filtre actuelles (pour pré-sélectionner les options dans le template)
        'current_q': query if query is not None else '',
        'current_auteur': auteur_id if auteur_id is not None else '',
        'current_editeur': editeur_id if editeur_id is not None else '',
        'current_genre': genre_slug if genre_slug is not None else '',
    }

    # 6. Rendu du template
    return render(request,'gestion_content/bd.html',context)

    

