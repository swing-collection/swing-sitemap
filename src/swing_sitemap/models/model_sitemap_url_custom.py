class CustomSitemapURL(URL):
    custom_field = models.CharField(max_length=255)
    custom_data = models.JSONField(default=dict)

    def get_absolute_url(self):
        return self.url

    def __str__(self):
        return f"{self.url} - {self.custom_field}"
