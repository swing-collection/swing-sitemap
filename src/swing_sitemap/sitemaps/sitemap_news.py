"""


### 4. **Test Your News Sitemap**

After setting up the news sitemap, access `/sitemap_news.xml` on your website to ensure that it's correctly formatted and includes all the necessary news-specific tags.

### Key Points to Consider:

1. **News-Specific Tags**: Ensure your sitemap includes news-specific tags like `news:news`, `news:publication`, `news:publication_date`, `news:title`, and any other relevant tags as per Google's guidelines.

2. **Article Freshness**: Google News sitemaps typically consider articles published in the last two days. Adjust your `items` method to filter articles accordingly.

3. **Article Selection**: Be selective about the articles you include. Google News prefers high-quality, original news content. Avoid promotional articles or non-news content.

4. **SEO Best Practices for News**: Make sure your news articles have SEO-friendly URLs, use proper heading tags, and include meta descriptions to improve their discoverability.

5. **Regular Updates**: Keep your news sitemap updated. Automate the update process as much as possible to ensure that new articles are quickly included in the sitemap.

6. **Google News Publisher Center**: If you haven't already, register your website with the Google News Publisher Center. This step is crucial for getting your content recognized and indexed by Google News.

7. **Performance Considerations**: If you have a large volume of news articles being published, consider the performance implications of generating your sitemap. You might need to implement caching or optimize database queries.

8. **Testing and Validation**: Regularly test your sitemap for errors and validate it against Google's guidelines to ensure it's being correctly indexed.

By implementing a Google News Sitemap in your Django app, you can significantly improve the speed and efficiency with which Google indexes your news articles, potentially increasing your visibility and traffic from Google News.

"""




from django.contrib.sitemaps import Sitemap
from django.utils.html import escape
from .models import NewsArticle  # Your news article model

class NewsSitemap(Sitemap):
    def items(self):
        # Return the recent news articles, Google News generally considers the last two days
        return NewsArticle.objects.filter(publish_date__gte=datetime.now()-timedelta(days=2))

    def location(self, obj):
        return obj.get_absolute_url()

    def news_tags(self, obj):
        """
        Return the news-specific tags for each article.
        """
        return {
            'publication_name': escape(obj.publication.name),
            'publication_language': obj.publication.language,
            'title': escape(obj.title),
            'genres': obj.genres,  # e.g., "PressRelease, Blog"
            'publication_date': obj.publish_date.strftime('%Y-%m-%d'),
            'keywords': ','.join([escape(keyword) for keyword in obj.keywords.split(',')]),
        }

    def _news(self, obj):
        news_data = self.news_tags(obj)
        news_tag = '<news:news>'
        for key, value in news_data.items():
            news_tag += f'<news:{key}>{value}</news:{key}>'
        news_tag += '</news:news>'
        return news_tag

    def _urls(self, page, protocol, domain):
        urls = super(NewsSitemap, self)._urls(page, protocol, domain)
        for url in urls:
            item = url['item']
            news = self._news(item)
            if news:
                url['news'] = news
        return urls
