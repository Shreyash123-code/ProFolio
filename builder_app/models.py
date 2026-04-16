from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

TEMPLATE_CHOICES = [
    ('starter', 'Starter'),
    ('gradient_aurora', 'Gradient Aurora'),
    ('minimal_mono', 'Minimal Mono'),
    ('creative_splash', 'Creative Splash'),
    ('elegant', 'Elegant'),
    ('developer', 'Developer'),
]

class Portfolio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default="My Portfolio")
    tagline = models.CharField(max_length=300, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    skills = models.TextField(blank=True, null=True, help_text="Comma-separated skills")
    email = models.EmailField(blank=True, null=True)
    custom_url = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    github_link = models.URLField(blank=True, null=True)
    linkedin_link = models.URLField(blank=True, null=True)
    theme = models.CharField(max_length=20, default='light')
    template = models.CharField(max_length=30, choices=TEMPLATE_CHOICES, default='starter')

    def __str__(self):
        return f"{self.user.username}'s Portfolio"
    
    def save(self, *args, **kwargs):
        if not self.custom_url:
            self.custom_url = slugify(self.user.username)
        super().save(*args, **kwargs)

    def skills_list(self):
        """Returns skills as a list from comma-separated string."""
        if self.skills:
            return [s.strip() for s in self.skills.split(',') if s.strip()]
        return []

class Project(models.Model):
    portfolio = models.ForeignKey(Portfolio, related_name='projects', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='project_images/', blank=True, null=True)
    technology_tags = models.CharField(max_length=300, blank=True, null=True, help_text="Comma-separated tech tags")
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title

    def tags_list(self):
        """Returns tags as a list from comma-separated string."""
        if self.technology_tags:
            return [t.strip() for t in self.technology_tags.split(',') if t.strip()]
        return []
