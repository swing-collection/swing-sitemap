"""


Key Points to Remember:
Required Video Tags: Ensure that you include all the required video tags in your sitemap. At a minimum, most search engines require thumbnail_loc, title, and description. You can add more tags like content_loc, duration, expiration_date, rating, etc., depending on your needs and the specifics of your video content.

Performance Considerations: If you have a large number of videos, consider the performance implications. Generating a sitemap for thousands of videos might be resource-intensive. In such cases, think about paginating your sitemap or splitting it into multiple files.

SEO Best Practices: Make sure that the metadata you provide in your video sitemap accurately reflects the content of your videos. This improves the chances of your videos appearing in search engine results.

Regular Updates: Keep your video sitemap up-to-date with new content. Automating this process with Django signals or scheduled tasks can be very efficient.

Accessibility and Quality: Just like with regular content, ensure that your videos are of high quality and accessible. Good practices include providing subtitles or transcripts and ensuring that your videos are viewable on various devices.

Submit Your Sitemap: Don’t forget to submit your new video sitemap to search engines. This can usually be done through their respective webmaster tools.
"""




from django.contrib.sitemaps import Sitemap
from django.utils.html import escape
from .models import VideoModel  # Your video model

class VideoSitemap(Sitemap):
    def items(self):
        return VideoModel.objects.all()  # Assuming each item corresponds to a video

    def location(self, obj):
        return obj.get_absolute_url()  # URL of the video page

    def video_urls(self, obj):
        """
        Return a dictionary of video data for each video.
        """
        # Adjust the dictionary below according to your model's fields
        return {
            'thumbnail_loc': obj.thumbnail_url,  # URL of the video thumbnail
            'title': obj.title,
            'description': obj.description,
            'content_loc': obj.video_file.url,  # URL of the video file
            # Additional optional fields: duration, expiration_date, etc.
        }

    def _videos(self, obj):
        video_data = self.video_urls(obj)
        video_tag = '<video:video>'
        for key, value in video_data.items():
            video_tag += f'<video:{key}>{escape(value)}</video:{key}>'
        video_tag += '</video:video>'
        return video_tag

    def _urls(self, page, protocol, domain):
        urls = super(VideoSitemap, self)._urls(page, protocol, domain)
        for url in urls:
            item = url['item']
            videos = self._videos(item)
            if videos:
                url['videos'] = videos
        return urls
