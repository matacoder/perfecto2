import pytest
from django.template.loader import get_template

class TestTemplates:
    
    def test_base_template_exists(self):
        """Test that the base template exists and can be loaded"""
        template = get_template('base.html')
        assert template is not None
    
    def test_home_template_exists(self):
        """Test that the home template exists and can be loaded"""
        template = get_template('accounts/home.html')
        assert template is not None
    
    def test_dashboard_template_exists(self):
        """Test that the dashboard template exists and can be loaded"""
        template = get_template('accounts/dashboard.html')
        assert template is not None
    
    def test_required_blocks_in_base_template(self):
        """Test that the base template has all required blocks"""
        template = get_template('base.html')
        template_content = template.template.source
        
        required_blocks = ['title', 'head', 'content', 'scripts']
        
        for block in required_blocks:
            assert f"{{% block {block} %}}" in template_content
