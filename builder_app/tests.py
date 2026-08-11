from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from builder_app.models import Portfolio, Project, Education, Experience, Certificate
import json


class ProFolioModelsAndViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client = Client()
        self.client.login(username='testuser', password='password123')
        self.portfolio, _ = Portfolio.objects.get_or_create(user=self.user)

    def test_portfolio_creation_and_defaults(self):
        self.assertEqual(self.portfolio.user.username, 'testuser')
        self.assertTrue(self.portfolio.custom_url.startswith('testuser'))

    def test_add_education_experience_certificate(self):
        # Add Education
        res = self.client.post(reverse('add_education'), {
            'degree': 'B.Tech CS',
            'college': 'IIT Delhi',
            'year': '2020-2024',
            'cgpa': '9.5'
        })
        self.assertEqual(Education.objects.filter(portfolio=self.portfolio).count(), 1)

        # Add Experience
        res = self.client.post(reverse('add_experience'), {
            'company': 'Tech Corp',
            'role': 'Full Stack Developer',
            'duration': '2023 - Present',
            'description': 'Building AI solutions.'
        })
        self.assertEqual(Experience.objects.filter(portfolio=self.portfolio).count(), 1)

        # Add Certificate
        res = self.client.post(reverse('add_certificate'), {
            'name': 'AWS Certified Developer',
            'organization': 'Amazon Web Services',
            'year': '2023',
            'link': 'https://aws.amazon.com'
        })
        self.assertEqual(Certificate.objects.filter(portfolio=self.portfolio).count(), 1)

    def test_add_project(self):
        res = self.client.post(reverse('add_project'), {
            'project_title': 'AI Image Generator',
            'project_description': 'Generates art using deep learning',
            'project_tags': 'Python, PyTorch, React',
            'project_github_link': 'https://github.com/testuser/ai-gen',
            'project_demo_link': 'https://aigen.demo',
            'is_featured': 'on'
        })
        self.assertEqual(Project.objects.filter(portfolio=self.portfolio).count(), 1)
        project = Project.objects.get(portfolio=self.portfolio)
        self.assertTrue(project.is_featured)

    def test_ai_content_generation(self):
        res = self.client.post(
            reverse('generate_ai_content'),
            data=json.dumps({'prompt': 'Created Flutter food delivery app', 'type': 'project_desc'}),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data['status'], 'success')
        self.assertIn('Flutter food delivery app', data['result'])

    def test_export_zip(self):
        res = self.client.get(reverse('export_portfolio_zip'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res['Content-Type'], 'application/zip')

    def test_viewer_portfolio_page(self):
        res = self.client.get(f'/p/{self.portfolio.custom_url}/')
        self.assertEqual(res.status_code, 200)

    def test_all_11_templates_render_successfully(self):
        from builder_app.models import TEMPLATE_CHOICES
        for t_code, t_name in TEMPLATE_CHOICES:
            res = self.client.get(f'/p/{self.portfolio.custom_url}/?preview_template={t_code}')
            self.assertEqual(res.status_code, 200, f"Template {t_code} failed to render")

