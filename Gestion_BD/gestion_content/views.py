from django.shortcuts import get_object_or_404, render,redirect
from gestion_content.models import *
from gestion_utilisateur.models import Auteur
from .form import NotationForm
from django.db.models import Avg,Q


def home(request):
    auteurs = Auteur.objects.all()
    
    # Récupération des paramètres de recherche
    q = request.GET.get('q', '')  # Recherche par nom d'auteur ou username
    genre_id = request.GET.get('genre', '')
    pays = request.GET.get('pays', '')

    # Filtrer les résultats
    if q:
        auteurs = auteurs.filter(Q(user__username__icontains=q) )

    if genre_id:
        auteurs = auteurs.filter(genres__id=genre_id)

    if pays:
        auteurs = auteurs.filter(pays=pays)

    genres = Genre.objects.all()
    pays_list = Auteur.objects.values_list('pays', flat=True).distinct()

    return render(request,'gestion_content/index.html',{
        'auteurs':auteurs,
        'genres':genres,
        'pays_list':pays_list
        
        })


def detail_auteur(request, auteur_id):
     # Récupérer l'auteur
    auteur = get_object_or_404(Auteur, id=auteur_id)

    # Récupérer toutes les œuvres de cet auteur avec la moyenne des notations
    oeuvres = Work.objects.filter(author=auteur).annotate(moyenne_note=Avg('notation__rating'))

    # Récupérer toutes les notations liées aux œuvres de cet auteur
    notations = Notation.objects.filter(work__in=oeuvres).select_related('user', 'work')
    social_links = auteur.social_links if auteur.social_links else {}

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


    return render(request, 'gestion_content/detail.html', {
        'auteur': auteur,
        'oeuvres': oeuvres,
        'notations': notations,
        'social_links':social_links
    })

def detail(request):

 return render(request,'gestion_content/detail_text.html')

