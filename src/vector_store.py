from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, VectorParams, Distance
from .models import StructuredItem
from typing import List, Dict, Any
import uuid

class VectorStore:
    def __init__(self, host: str = "localhost", port: int = 6333, collection_name: str = "thoughts"):
        self.client = QdrantClient(host=host, port=port)
        self.collection_name = collection_name
        self._ensure_collection_exists()

    def _ensure_collection_exists(self):
        collections = self.client.get_collections()
        exists = any(c.name == self.collection_name for c in collections.collections)
        
        if not exists:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
            )

    def upsert_item(self, item: StructuredItem, vector: List[float]):
        """
        Stores the structured item and its vector embedding.
        """
        point_id = str(uuid.uuid4())
        
        # Convert enums to strings for storage
        payload = item.model_dump(mode='json')
        
        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                PointStruct(
                    id=point_id,
                    vector=vector,
                    payload=payload
                )
            ]
        )

    def search_similar(self, vector: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        """
        Searches for similar items using the query vector.
        """
        results = self.client.query_points(
            collection_name=self.collection_name,
            query=vector,
            limit=limit
        ).points
        return [hit.payload for hit in results]
