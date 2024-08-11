from django.contrib.sitemaps import Sitemap
from django.utils.html import escape
from .models import MyModel  # Your model that includes images

class MyModelSitemap(Sitemap):
    def items(self):
        return MyModel.objects.all()

    def location(self, obj):
        return obj.get_absolute_url()  # URL of the object

    def image_urls(self, obj):
        """
        Return a list of image URLs to include in the sitemap for this item.
        """
        return [obj.image.url for obj in obj.images.all()]  # Adjust according to your model

    def _images(self, obj):
        """
        Generate the <image:image> elements for this item.
        """
        return ['<image:image><image:loc>%s</image:loc></image:image>' % escape(url) for url in self.image_urls(obj)]

    def _urls(self, page, protocol, domain):
        urls = super(MyModelSitemap, self)._urls(page, protocol, domain)
        for url in urls:
            item = url['item']
            images = self._images(item)
            if images:
                url['images'] = images
        return urls
