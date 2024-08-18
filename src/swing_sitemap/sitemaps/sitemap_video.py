# -*- coding: utf-8 -*-
"""
Video Sitemap Generator
========================

This module provides a `VideoSitemap` class for generating sitemaps that include video content.
It retrieves the model reference from Django settings, allowing for flexible configuration.

Key Points to Remember:
-----------------------
1. **Required Video Tags**: Ensure all required video tags are included in your sitemap.
   At a minimum, include `thumbnail_loc`, `title`, and `description`. You may also add 
   optional tags like `content_loc`, `duration`, `expiration_date`, `rating`, depending 
   on your needs and the specifics of your video content.

2. **Performance Considerations**: For a large number of videos, consider performance implications.
   Generating a sitemap for thousands of videos might be resource-intensive. Consider paginating 
   your sitemap or splitting it into multiple files.

3. **SEO Best Practices**: Ensure the metadata in your video sitemap accurately reflects your video content.
   This improves the chances of your videos appearing in search engine results.

4. **Regular Updates**: Keep your video sitemap up-to-date with new content. Automating this process 
   with Django signals or scheduled tasks can be very efficient.

5. **Accessibility and Quality**: Ensure your videos are of high quality and accessible. Good practices 
   include providing subtitles or transcripts and ensuring that your videos are viewable on various devices.

6. **Submit Your Sitemap**: Submit your video sitemap to search engines through their respective webmaster tools.

Links:
------
- https://github.com/django/django/blob/master/docs/ref/contrib/sitemaps.txt
"""

# =============================================================================
# Imports
# =============================================================================

from typing import Any, Dict, List, Type
from django.apps import apps
from django.conf import settings
from django.utils.html import escape
from swing_sitemap.sitemaps.sitemap_base import BaseSitemap

# =============================================================================
# Video Sitemap Class
# =============================================================================

class VideoSitemap(BaseSitemap):
    """
    VideoSitemap
    ============

    A Django sitemap class for generating video sitemaps. This class is designed to
    generate XML sitemaps that include video content, following search engine guidelines.

    Attributes:
        changefreq (str): The frequency with which the content is expected to change.
        priority (float): The priority of this URL relative to other URLs.
        model (Type): The Django model class that represents videos, retrieved from settings.
    """

    changefreq: str = "weekly"
    priority: float = 0.8

    def __init__(self, items: List[Dict[str, Any]] = None):
        """
        Initialize the VideoSitemap by retrieving the video model from settings.

        Args:
            items (Optional[List[Dict[str, Any]]]): A list of dictionaries where
                each dictionary contains the 'view_name' and optional 'kwargs'
                for reversing URLs. Defaults to an empty list if not provided.
        """
        super().__init__(items=items)
        self.model = self._get_video_model()

    def _get_video_model(self) -> Type[Any]:
        """
        Retrieves the video model class from the Django settings.

        Returns:
            Type[Any]: The video model class.
        """
        model_name = settings.VIDEO_SITEMAP_MODEL
        return apps.get_model(model_name)

    def items(self) -> List[Any]:
        """
        Retrieves all video items from the database to be included in the sitemap.

        Returns:
            List[Any]: A list of all video objects in the database.
        """
        return self.model.objects.all()

    def location(self, obj: Any) -> str:
        """
        Returns the absolute URL for a given video object.

        Args:
            obj (Any): A video object.

        Returns:
            str: The absolute URL of the video page.
        """
        return obj.get_absolute_url()

    def video_urls(self, obj: Any) -> Dict[str, str]:
        """
        Returns a dictionary of video metadata for inclusion in the sitemap.

        Args:
            obj (Any): A video object.

        Returns:
            Dict[str, str]: A dictionary containing the video metadata fields.
        """
        return {
            'thumbnail_loc': obj.thumbnail_url,  # URL of the video thumbnail
            'title': obj.title,
            'description': obj.description,
            'content_loc': obj.video_file.url,  # URL of the video file
            # Additional optional fields can be added here, e.g., 'duration', 'expiration_date', etc.
        }

    def _videos(self, obj: Any) -> str:
        """
        Generates the XML for video tags based on the video metadata.

        Args:
            obj (Any): A video object.

        Returns:
            str: An XML string containing the video tags.
        """
        video_data = self.video_urls(obj)
        video_tag = '<video:video>'
        for key, value in video_data.items():
            video_tag += f'<video:{key}>{escape(value)}</video:{key}>'
        video_tag += '</video:video>'
        return video_tag

    def _urls(self, page: int, protocol: str, domain: str) -> List[Dict[str, Any]]:
        """
        Overrides the base class method to include video tags in the sitemap URLs.

        Args:
            page (int): The page number.
            protocol (str): The protocol used (http or https).
            domain (str): The domain of the website.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries where each dictionary represents a URL and its associated videos.
        """
        urls = super(VideoSitemap, self)._urls(page, protocol, domain)
        for url in urls:
            item = url['item']
            videos = self._videos(item)
            if videos:
                url['videos'] = videos
        return urls

# =============================================================================
# Module Exports
# =============================================================================

__all__ = [
    "VideoSitemap",
]