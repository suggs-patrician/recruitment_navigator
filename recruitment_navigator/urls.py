from django.conf import settings
from django.urls import include, path
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from search import views as search_views
from jobs import views as jobs_views

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),
    
    # Accounts URLs
    path("accounts/", include("accounts.urls")),
    
    # Jobs API endpoints
    path("api/regions/provinces/", jobs_views.get_provinces, name="api_provinces"),
    path("api/regions/cities/", jobs_views.get_cities, name="api_cities"),
    path("api/regions/counties/", jobs_views.get_counties, name="api_counties"),
    path("api/regions/info/", jobs_views.get_region_info, name="api_region_info"),
    path("api/recent-jobs/", jobs_views.get_recent_jobs, name="api_recent_jobs"),
    path("api/subscribe/", jobs_views.subscribe, name="api_subscribe"),
    
    # Demo page
    path("demo/region-selector/", jobs_views.region_selector_demo, name="region_selector_demo"),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(wagtail_urls)),
    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
]
