class VideoSitemapURL(URL):
    video_title = models.CharField(max_length=255)
    video_description = models.TextField()
    video_thumbnail_url = models.URLField()
    video_content_url = models.URLField()
    video_duration = models.IntegerField(help_text="Duration in seconds")
    video_expiration_date = models.DateTimeField(blank=True, null=True)
    video_publication_date = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return self.url

    def __str__(self):
        return f"{self.url} - {self.video_title}"