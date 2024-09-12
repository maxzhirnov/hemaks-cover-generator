import pytest
import os
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_create_image_with_default_template(client):
    response = client.post('/create-image', json={
        'title': 'Test Title'
    })
    assert response.status_code == 200
    assert 'image_path' in response.json
    assert os.path.exists(response.json['image_path'])

def test_create_image_with_specific_template(client):
    response = client.post('/create-image', json={
        'title': 'Test Title',
        'template_name': 'default'
    })
    assert response.status_code == 200
    assert 'image_path' in response.json
    assert os.path.exists(response.json['image_path'])

def test_create_image_with_template_without_extension(client):
    response = client.post('/create-image', json={
        'title': 'Test Title',
        'template_name': 'default'
    })
    assert response.status_code == 200
    assert 'image_path' in response.json
    assert os.path.exists(response.json['image_path'])

def test_create_image_missing_title(client):
    response = client.post('/create-image', json={
        'template_name': 'default'
    })
    assert response.status_code == 400
    assert response.json['error'] == 'Title is required'

def test_create_image_non_existent_template(client):
    response = client.post('/create-image', json={
        'title': 'Test Title',
        'template_name': 'nonexistent'
    })
    assert response.status_code == 500
    assert "Template image 'nonexistent.png' not found" in response.json['error']

def test_create_image_font_not_found(monkeypatch, client):
    # Temporarily change the FONT_PATH to an invalid path
    monkeypatch.setattr('app.FONT_PATH', 'nonexistent-font.ttf')
    response = client.post('/create-image', json={
        'title': 'Test Title',
        'template_name': 'default'
    })
    assert response.status_code == 500
    assert response.json['error'] == 'Font file not found'

def test_list_templates(client):
    response = client.get('/list-templates')
    assert response.status_code == 200
    assert isinstance(response.json['templates'], list)
    # Assuming 'default' is one of the templates
    assert 'default' in response.json['templates']
