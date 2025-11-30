from sentence_transformers import SentenceTransformer
from transformers import AutoImageProcessor, AutoModel
from PIL import Image
import torch
import numpy as np
import logging
from typing import Union, List
import io
from ..core.config import settings

logger = logging.getLogger(__name__)

class EmbeddingService:
    def __init__(self):
        self.device = settings.DEVICE
        logger.info(f"Initializing embedding models on device: {self.device}")
        
        # Initialize text embedding model (BGE)
        try:
            self.text_model = SentenceTransformer(
                settings.TEXT_EMBEDDING_MODEL,
                device=self.device
            )
            logger.info(f"Loaded text model: {settings.TEXT_EMBEDDING_MODEL}")
        except Exception as e:
            logger.error(f"Failed to load text model: {e}")
            self.text_model = None
        
        # Initialize image embedding model (DINO)
        try:
            self.image_processor = AutoImageProcessor.from_pretrained(
                settings.IMAGE_EMBEDDING_MODEL
            )
            self.image_model = AutoModel.from_pretrained(
                settings.IMAGE_EMBEDDING_MODEL
            ).to(self.device)
            self.image_model.eval()
            logger.info(f"Loaded image model: {settings.IMAGE_EMBEDDING_MODEL}")
        except Exception as e:
            logger.error(f"Failed to load image model: {e}")
            self.image_processor = None
            self.image_model = None
    
    async def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for text using BGE
        
        Args:
            text: Input text string
            
        Returns:
            Embedding vector as list of floats
        """
        if self.text_model is None:
            raise RuntimeError("Text embedding model not initialized")
        
        try:
            # Generate embedding
            embedding = self.text_model.encode(
                text,
                normalize_embeddings=True,
                convert_to_numpy=True
            )
            
            # Convert to list and ensure correct dimension
            embedding_list = embedding.tolist()
            
            # Pad or truncate to match expected dimension if needed
            if len(embedding_list) != settings.EMBEDDING_DIMENSION:
                logger.warning(
                    f"Text embedding dimension mismatch: {len(embedding_list)} vs {settings.EMBEDDING_DIMENSION}"
                )
                if len(embedding_list) < settings.EMBEDDING_DIMENSION:
                    embedding_list.extend([0.0] * (settings.EMBEDDING_DIMENSION - len(embedding_list)))
                else:
                    embedding_list = embedding_list[:settings.EMBEDDING_DIMENSION]
            
            return embedding_list
        except Exception as e:
            logger.error(f"Failed to generate text embedding: {e}")
            raise
    
    async def embed_image(self, image_data: bytes) -> List[float]:
        """
        Generate embedding for image using DINO
        
        Args:
            image_data: Image binary data
            
        Returns:
            Embedding vector as list of floats
        """
        if self.image_processor is None or self.image_model is None:
            raise RuntimeError("Image embedding model not initialized")
        
        try:
            # Load image from bytes
            image = Image.open(io.BytesIO(image_data)).convert('RGB')
            
            # Process image
            inputs = self.image_processor(images=image, return_tensors="pt")
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Generate embedding
            with torch.no_grad():
                outputs = self.image_model(**inputs)
                # Use CLS token embedding (first token)
                embedding = outputs.last_hidden_state[:, 0, :].cpu().numpy()[0]
            
            # Normalize embedding
            embedding = embedding / np.linalg.norm(embedding)
            
            # Convert to list and ensure correct dimension
            embedding_list = embedding.tolist()
            
            # Pad or truncate to match expected dimension if needed
            if len(embedding_list) != settings.EMBEDDING_DIMENSION:
                logger.warning(
                    f"Image embedding dimension mismatch: {len(embedding_list)} vs {settings.EMBEDDING_DIMENSION}"
                )
                if len(embedding_list) < settings.EMBEDDING_DIMENSION:
                    embedding_list.extend([0.0] * (settings.EMBEDDING_DIMENSION - len(embedding_list)))
                else:
                    embedding_list = embedding_list[:settings.EMBEDDING_DIMENSION]
            
            return embedding_list
        except Exception as e:
            logger.error(f"Failed to generate image embedding: {e}")
            raise
    
    async def embed_file(self, file_data: bytes, file_type: str, mime_type: str) -> List[float]:
        """
        Generate embedding based on file type
        
        Args:
            file_data: File binary data
            file_type: 'image' or 'text'
            mime_type: MIME type of the file
            
        Returns:
            Embedding vector as list of floats
        """
        try:
            if file_type == "image":
                return await self.embed_image(file_data)
            elif file_type == "text":
                # Decode text content
                try:
                    text = file_data.decode('utf-8')
                except UnicodeDecodeError:
                    # Try other encodings
                    try:
                        text = file_data.decode('latin-1')
                    except:
                        raise ValueError("Unable to decode text file")
                
                return await self.embed_text(text)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
        except Exception as e:
            logger.error(f"Failed to generate embedding for file: {e}")
            raise
    
    def get_model_info(self) -> dict:
        """
        Get information about loaded models
        
        Returns:
            Dictionary with model information
        """
        return {
            "text_model": settings.TEXT_EMBEDDING_MODEL if self.text_model else None,
            "image_model": settings.IMAGE_EMBEDDING_MODEL if self.image_model else None,
            "embedding_dimension": settings.EMBEDDING_DIMENSION,
            "device": self.device,
            "text_model_loaded": self.text_model is not None,
            "image_model_loaded": self.image_model is not None
        }

# Singleton instance
embedding_service = EmbeddingService()

