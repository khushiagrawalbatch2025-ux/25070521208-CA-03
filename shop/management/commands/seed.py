from django.core.management.base import BaseCommand
from shop.models import Category, Product

DATA = {
    "Shirts": [
        ("Field Shirt", "Indigo twill overshirt with chest pockets and corozo buttons.", "100% organic cotton twill", 2799, "#1d2a5c", "New", True),
        ("Boxy Oxford", "A cropped, roomy oxford washed for softness.", "Cotton oxford, 160 gsm", 2299, "#8fa3c7", "", True),
        ("Madder Camp Shirt", "Short-sleeve camp collar in madder-root red.", "Linen-cotton blend", 2499, "#b3392c", "", False),
    ],
    "Tees": [
        ("Heavy Tee", "270 gsm tee that holds its shape wash after wash.", "Combed cotton jersey", 1199, "#15171f", "Bestseller", True),
        ("Pocket Tee", "Relaxed fit with a patch pocket in undyed cotton.", "Combed cotton jersey", 1299, "#d8d0c0", "", True),
        ("Indigo Long Sleeve", "Hand-dipped tee, every piece is slightly different.", "Combed cotton jersey", 1599, "#26356f", "Limited", False),
    ],
    "Trousers": [
        ("Straight Denim", "Raw 12 oz selvedge denim with a straight leg.", "12 oz selvedge denim", 3499, "#1d2a5c", "", True),
        ("Drawstring Chino", "Easy waist, tapered leg, garment-dyed.", "Cotton twill", 2599, "#c8bfae", "", False),
        ("Wide Linen Pant", "Wide-leg pant that softens with every wash.", "100% linen", 2899, "#6b7a63", "", False),
    ],
    "Layers": [
        ("Chore Jacket", "Boxy canvas jacket with three pockets.", "10 oz cotton canvas", 4299, "#3a4a7a", "", False),
        ("Quilted Liner", "Lightweight liner that works under or over.", "Recycled polyester fill", 3799, "#b3392c", "New", False),
    ],
}

class Command(BaseCommand):
    help = "Load sample categories and products"
    def handle(self, *a, **k):
        from django.utils.text import slugify
        for cname, items in DATA.items():
            cat, _ = Category.objects.get_or_create(slug=slugify(cname), defaults={"name": cname})
            for n, d, f, pr, c, b, ft in items:
                Product.objects.update_or_create(slug=slugify(n), defaults=dict(
                    category=cat, name=n, description=d, fabric=f, price=pr, color=c, badge=b, featured=ft, stock=25))
        self.stdout.write(self.style.SUCCESS("Sample catalogue loaded."))
