from django.shortcuts import get_object_or_404, render,redirect
from gestion_content.models import *
from gestion_utilisateur.models import *
from .form import NotationForm
from django.db.models import Avg,Q
from django.core.paginator import Paginator


def Auteur(request):
    autor = []
    auteurs_list = Utilisateur.objects.filter(role="auteur").all()
    paginator = Paginator(auteurs_list,3)
    page_number = request.GET.get('page')
    auteurs = paginator.get_page(page_number)
    user_authenticate = request.user.is_authenticated
    user = request.user
   
    for autors in auteurs:
        if autors.role == "auteur":
            autor.append(autors)
    
    
    # Récupération des paramètres de recherche
    q = request.GET.get('q', '')  # Recherche par nom d'auteur ou username
    genre_id = request.GET.get('genre', '')
    pays = request.GET.get('pays', '')

    # Filtrer les résultats
    if q:
        auteurs = auteurs.filter(Q(username__icontains=q) )

    if genre_id:
        auteurs = auteurs.filter(genres__id=genre_id)

    if pays:
        auteurs = auteurs.filter(pays=pays)

    genres = Genre.objects.all()
    pays_list = Utilisateur.objects.values_list('pays', flat=True).distinct()

    return render(request,'gestion_content/auteur.html',{
        'auteurs':auteurs,
        'genres':genres,
        'pays_list':pays_list,
        'user_authenticate':user_authenticate,
        "user":user
        
        })


def detail_auteur(request, auteur_id):
    totatl_notif = 0
    nb_notif = 0
    user_authenticate = request.user.is_authenticated
     # Récupérer l'auteur
    auteur = get_object_or_404(Utilisateur, id=auteur_id)

    # Récupérer toutes les œuvres de cet auteur avec la moyenne des notations
    oeuvres = Work.objects.filter(author=auteur).annotate(moyenne_note=Avg('notation__rating'))


    # Récupérer toutes les notations liées aux œuvres de cet auteur
    notations = Notation.objects.filter(work__in=oeuvres).select_related('user', 'work')
    # notif = Notation.objects.all().count()
    # social_links = auteur.social_links if auteur.social_links else {}
    print(notations)
   
    # print(notations.all().count())
    # Gestion du formulaire de notation sans utiliser Django Forms
    if request.method == 'POST':
        comment = request.POST.get('comment')
        rating = request.POST.get('rating')

        if comment and rating:
            # Récupérer une œuvre aléatoire de l'auteur pour l'associer à la notation
            work = oeuvres.first()
            if work:
                Notation.objects.create(
                    user=request.user,
                    work=work,
                    rating=int(rating),
                    comment=comment
                )
        
        return redirect('detail_auteur', auteur_id=auteur_id)
    
    if notations:
        for each_notif in notations:
          totatl_notif = totatl_notif + each_notif.rating
    
    notation = Notation.objects.filter(work__in=oeuvres).count()
    print(notation)
    if notation !=0:
       nb_notif = totatl_notif/notation
    
    
    return render(request, 'gestion_content/detail.html', {
        'auteur': auteur,
        'oeuvres': oeuvres,
        'notations': notations,
        # 'social_links':social_links,
        'nb_notif':nb_notif,
        'user_authenticate':user_authenticate
    })

def detail(request):

 return render(request,'gestion_content/detail_text.html')


def actualite(request):
    actualite = BlogPost.objects.filter(valid=True).all()

    return render(request,'gestion_content/actualite.html',{'actualite':actualite})