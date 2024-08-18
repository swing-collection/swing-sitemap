class NewsSitemapURL(URL):
    publication_name = models.CharField(max_length=255)
    publication_language = models.CharField(max_length=10)
    title = models.CharField(max_length=255)
    publication_date = models.DateTimeField()

    def get_absolute_url(self):
        return self.url

    def __str__(self):
        return f"{self.title} - {self.publication_name}"