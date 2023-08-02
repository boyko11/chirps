"""Models for the embedding app"""
from django.contrib.auth.models import User
from django.db import models
from embedding.providers.cohere import CohereEmbeddingProvider

from .providers.base import BaseEmbeddingProvider
from .providers.openai import OpenAIEmbeddingProvider


class Embedding(models.Model):
    """A model to store embeddings generated by an asset."""

    class Service(models.TextChoices):
        """Enumerations to define services available for generating embeddings."""

        COHERE = 'cohere', 'cohere'
        LOCAL = 'localhost', 'Locally Hosted: NOT IMPLEMENTED'
        OPEN_AI = 'OpenAI', 'OpenAI'

        @classmethod
        def get_provider_from_service_name(cls, name: str) -> BaseEmbeddingProvider:
            """Get the provider for the service."""
            embedding_service_providers = {
                Embedding.Service.OPEN_AI: OpenAIEmbeddingProvider,
                Embedding.Service.COHERE: CohereEmbeddingProvider,
            }
            if name not in embedding_service_providers:
                raise NotImplementedError

            return embedding_service_providers[name]

    created_at = models.DateTimeField(auto_now_add=True)

    # Name of the model used to generate the embedding
    model = models.CharField(max_length=256)

    # The service used to generate the embedding
    service = models.CharField(max_length=256, choices=Service.choices)

    # The text used to generate the embedding
    text = models.TextField()

    # The result of the embedding operation
    vectors = models.JSONField()

    # Which user does this embedding belong to?
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def to_dict(self) -> dict:
        """Convert the model to a dictionary."""
        return {
            'id': self.id,
            'created_at': self.created_at,
            'model': self.model,
            'service': self.service,
            'text': self.text,
            'vectors': self.vectors,
        }

    @staticmethod
    def get_models_for_service(service):
        """Get available embedding models based on selected service"""
        embedding_service_models = {
            Embedding.Service.OPEN_AI: [('text-embedding-ada-002', 'text-embedding-ada-002')],
            Embedding.Service.COHERE: [
                ('embed-english-light-v2.0', 'embed-english-light-v2.0'),
                ('embed-english-v2.0', 'embed-english-v2.0'),
                ('embed-multilingual-v2.0', 'embed-multilingual-v2.0'),
            ],
        }
        if service not in embedding_service_models:
            return []

        return embedding_service_models[service]
