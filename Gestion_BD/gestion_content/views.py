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

def Auteur(request):
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
            titre = request.POST.get('titre')
            contenue = request.POST.get('description')  # correspond à "name='description'" dans le HTML
            image = request.FILES.get('image')
            # genre = request.POST.get('genre')  # à adapter si tu l'ajoutes dans le formulaire
            date = request.POST.get('annee')  # correspond à "name='annee'" dans le HTML

            # try:
            #     genre_instance = Genre.objects.get(id=genre)
            # except Genre.DoesNotExist:
            #     genre_instance = None

            oeuvre = Work.objects.create(
                title=titre,
                description=contenue,
                author=auteur,
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
        "reseau_choice":Social_link.lien
    })

def detail_auteur2(request):
   return render(request,'gestion_content/detail2.html')


def detail(request):

 return render(request,'gestion_content/detail_text.html')


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


def apropos(request):
    return render(request,'gestion_content/apropos.html')

def custom_404_view(request, exception):
    # Vous pouvez passer du contexte si nécessaire
    return render(request, 'gestion_content/page404.html', status=404)

