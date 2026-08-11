from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

TEMPLATE_CHOICES = [
    ('minimal_developer', 'Minimal Developer'),
    ('software_engineer', 'Software Engineer'),
    ('ai_engineer', 'AI Engineer'),
    ('student_portfolio', 'Student Portfolio'),
    ('creative_portfolio', 'Creative Portfolio'),
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
    professional_title = models.CharField(max_length=200, blank=True, null=True)
    tagline = models.CharField(max_length=300, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    skills = models.TextField(blank=True, null=True, help_text="Comma-separated skills")
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    location = models.CharField(max_length=150, blank=True, null=True)
    custom_url = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    github_link = models.URLField(blank=True, null=True)
    linkedin_link = models.URLField(blank=True, null=True)
    twitter_link = models.URLField(blank=True, null=True)
    instagram_link = models.URLField(blank=True, null=True)
    website_link = models.URLField(blank=True, null=True)
    theme = models.CharField(max_length=20, default='light')
    template = models.CharField(max_length=30, choices=TEMPLATE_CHOICES, default='minimal_developer')
    accent_color = models.CharField(max_length=20, default='#6366f1')
    font_family = models.CharField(max_length=50, default='Inter')
    animation_style = models.CharField(max_length=30, default='fade')
    layout_style = models.CharField(max_length=30, default='modern')
    section_order = models.CharField(max_length=300, default='education,experience,projects,certificates')

    def __str__(self):
        return f"{self.user.username}'s Portfolio"
    
    def save(self, *args, **kwargs):
        if not self.custom_url:
            base_slug = slugify(self.user.username)
            slug = base_slug
            qs = Portfolio.objects.filter(custom_url=slug)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            if qs.exists():
                slug = f"{base_slug}-{self.user.pk}"
            self.custom_url = slug
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
    github_link = models.URLField(blank=True, null=True)
    demo_link = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='project_images/', blank=True, null=True)
    technology_tags = models.CharField(max_length=300, blank=True, null=True, help_text="Comma-separated tech tags")
    is_featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title

    def tags_list(self):
        """Returns tags as a list from comma-separated string."""
        if self.technology_tags:
            return [t.strip() for t in self.technology_tags.split(',') if t.strip()]
        return []

class Education(models.Model):
    portfolio = models.ForeignKey(Portfolio, related_name='educations', on_delete=models.CASCADE)
    degree = models.CharField(max_length=200)
    college = models.CharField(max_length=200)
    year = models.CharField(max_length=100, blank=True, null=True)
    cgpa = models.CharField(max_length=50, blank=True, null=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', '-id']

    def __str__(self):
        return f"{self.degree} - {self.college}"

class Experience(models.Model):
    portfolio = models.ForeignKey(Portfolio, related_name='experiences', on_delete=models.CASCADE)
    company = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    duration = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', '-id']

    def __str__(self):
        return f"{self.role} at {self.company}"

class Certificate(models.Model):
    portfolio = models.ForeignKey(Portfolio, related_name='certificates', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    organization = models.CharField(max_length=200)
    year = models.CharField(max_length=50, blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', '-id']

    def __str__(self):
        return f"{self.name} - {self.organization}"

