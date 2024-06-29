import requests

def submit_sitemap():
    sitemap_url = "http://www.example.com/sitemap.xml"  # Replace with your sitemap URL
    google_url = f"http://www.google.com/ping?sitemap={sitemap_url}"
    bing_url = f"http://www.bing.com/ping?sitemap={sitemap_url}"
    
    try:
        requests.get(google_url)
        requests.get(bing_url)
        # You can add logging or notification here
    except requests.exceptions.RequestException as e:
        # Handle exceptions, possibly log them or send notifications
