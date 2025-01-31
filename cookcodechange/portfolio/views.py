from django.shortcuts import render
from django.views.generic import TemplateView

class PortfolioView(TemplateView):
    template_name = "portfolio/portfolio.html"

class GalleryView(TemplateView):
    template_name = "portfolio/gallery.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = [
            {
                'filename': 'bosco.jpg',
                'title': 'Automne dans la forêt',
                'description': 'Cèpes, châtaignes et saveurs d\'automne',
                'category': 'plats'
            },
            {
                'filename': 'ravioli1.JPG',
                'title': 'Ravioli au canard',
                'description': 'Pâtes fraîches maison',
                'category': 'plats'
            },
            {
                'filename': 'ravioli3.JPG',
                'title': 'Ravioli aux herbes',
                'description': 'Beurre noisette et sauge',
                'category': 'plats'
            },
            {
                'filename': 'ricciola.JPG',
                'title': 'Seriola',
                'description': 'Poisson cru mariné aux agrumes',
                'category': 'entrées'
            },            
            {
                'filename': 'open.JPG',
                'title': 'Création Signature',
                'description': 'Gazpacho et crème d\'avocat glacée',
                'category': 'plats'
            },

            {   'filename': 'uovocolante.JPG',
                'title': 'Œuf parfait',
                'description': 'Crème de parmesan',
                'category': 'entrées'
            },

            {
                'filename': 'fragoline.JPG',
                'title': 'Dolce Finale',
                'description': 'Une touche sucrée pour conclure en beauté',
                'category': 'desserts'
            },
            {
                'filename': 'agnello1.JPG',
                'title': 'Agneau fumé au thym',
                'description': 'Haricots verts, oignons de Tropea',
                'category': 'plats'
            },
            {
                'filename': 'anatra.JPG',
                'title': 'Canard aux deux façons',
                'description': 'Magret fumé et cuisse confite au raisin, gelée de café',
                'category': 'plats'
            },
            {
                'filename': 'bavette.jpg',
                'title': 'Bavette de bœuf',
                'description': 'Cuisson parfaite, légumes de saison',
                'category': 'plats'
            },
            {
                'filename': 'bocconcini.JPG',
                'title': 'Friture de seitan',
                'description': 'Petites bouchées de seitan à la sauge',
                'category': 'plats'
            },
            
            {
                'filename': 'cheesecake_fraise.jpg',
                'title': 'Cheesecake aux fraises',
                'description': 'Biscuit spéculoos, fromage frais, fraises fraîches',
                'category': 'desserts'
            },
            {
                'filename': 'coniglio.JPG',
                'title': 'Lapin à la ligure',
                'description': 'Olives taggiasche et romarin',
                'category': 'plats'
            },
            {
                'filename': 'courgette_farcie.jpg',
                'title': 'Fleurs de courgette farcies',
                'description': 'Farce délicate aux herbes',
                'category': 'entrées'
            },
            {
                'filename': 'crémecocosblancs.jpg',
                'title': 'Crème de noix de coco',
                'description': 'Haricots blancs, coco et herbes fraîches',
                'category': 'entrées'
            },
            {
                'filename': 'daube_sanglier.jpg',
                'title': 'Daube de sanglier',
                'description': 'Marinée au vin rouge et aromates',
                'category': 'plats'
            },
            {
                'filename': 'focacciajambon.jpg',
                'title': 'Focaccia au jambon cru',
                'description': 'La tradition italienne revisitée',
                'category': 'entrées'
            },
            {
                'filename': 'foie_de_veau.jpg',
                'title': 'Foie de veau',
                'description': 'Poêlé aux oignons caramélisés',
                'category': 'plats'
            },
            {
                'filename': 'foiedepouletterrine.jpg',
                'title': 'Terrine de foies de volaille',
                'description': 'Parfumée au Cognac',
                'category': 'entrées'
            },
            {
                'filename': 'frittura.jpg',
                'title': 'Friture de la mer',
                'description': 'Poissons et fruits de mer croustillants',
                'category': 'plats'
            },
            {
                'filename': 'lasagnetta1.JPG',
                'title': 'Lasagnetta',
                'description': 'Fine lasagne aux champignons',
                'category': 'plats'
            },
            {
                'filename': 'open.JPG',
                'title': 'Création signature',
                'description': 'Variation autour des textures',
                'category': 'plats'
            },
            {
                'filename': 'opera.jpg',
                'title': 'Opéra',
                'description': 'Gâteau au café et chocolat',
                'category': 'desserts'
            },
            {
                'filename': 'pappardelle.jpg',
                'title': 'Pappardelle maison',
                'description': 'Sauce aux cèpes',
                'category': 'plats'
            },
            {
                'filename': 'poire_vin_rouge.jpg',
                'title': 'Poire pochée au vin rouge',
                'description': 'Épices et agrumes',
                'category': 'desserts'
            },
            {
                'filename': 'poires_pochées.jpg',
                'title': 'Poires pochées',
                'description': 'Au vin blanc et vanille',
                'category': 'desserts'
            },
            {
                'filename': 'porcelet.jpg',
                'title': 'Porcelet croustillant',
                'description': 'Légumes de saison',
                'category': 'plats'
            },
            {
                'filename': 'salmone.JPG',
                'title': 'Saumon confit',
                'description': 'Huile d\'olive et aromates',
                'category': 'plats'
            },
            {
                'filename': 'souffle2.JPG',
                'title': 'Soufflé au Grand Marnier',
                'description': 'Légèreté et gourmandise',
                'category': 'desserts'
            },
            {
                'filename': 'tartare_de_thon.jpg',
                'title': 'Tartare de thon',
                'description': 'Assaisonnement japonais',
                'category': 'entrées'
            },
            {
                'filename': 'tarte_fraises.jpg',
                'title': 'Tarte aux fraises',
                'description': 'Fraises de pays, crème légère',
                'category': 'desserts'
            },
            {
                'filename': 'caffe.JPG',
                'title': 'Pause café gourmande',
                'description': 'Mignardises et café italien',
                'category': 'desserts'
            },
            {
                'filename': 'terrine_foie_poulet.jpg',
                'title': 'Terrine de volaille',
                'description': 'Aux pistaches',
                'category': 'entrées'
            },
            
        ]
        return context

class AboutView(TemplateView):
    template_name = "portfolio/about.html"