class ImageSitemapURL(URL):
    image_url = models.URLField()
    image_caption = models.CharField(max_length=255, blank=True)
    image_title = models.CharField(max_length=255, blank=True)
    image_license = models.URLField(blank=True)

    def get_absolute_url(self):
        return self.url

    def __str__(self):
        return f"{self.url} - {self.image_url}"