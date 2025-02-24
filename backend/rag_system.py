"""
Recipe RAG System - A retrieval-augmented generation system for recipes
Author: [Your Name]
Date: February 2025

This system combines vector search with language model generation to provide
contextually relevant recipe information based on user queries.
"""

from llama_index.core import VectorStoreIndex, Document, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from datasets import load_dataset
from transformers import pipeline
import torch
import logging
from typing import List, Dict, Any, Optional
import os
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class RecipeRAGSystem:
    """
    A Retrieval-Augmented Generation system specialized for recipe queries.
    
    This class handles both the retrieval of relevant recipe documents from a vector store
    and the generation of helpful responses using a language model.
    """
    
    def __init__(
        self, 
        embedding_model: str = "BAAI/bge-small-en-v1.5",
        llm_model: str = "microsoft/Phi-3-mini-4k-instruct",
        dataset_name: str = "m3hrdadfi/recipe_nlg_lite",
        temperature: float = 0.7,
        top_k: int = 3
    ):
        """
        Initialize the RAG system with specified models and parameters.
        
        Args:
            embedding_model: Name of the HuggingFace embedding model
            llm_model: Name of the language model for generation
            dataset_name: Name of the HuggingFace dataset containing recipes
            temperature: Sampling temperature for text generation
            top_k: Default number of documents to retrieve
        """
        logger.info(f"Initializing RecipeRAGSystem with {embedding_model} and {llm_model}")
        
        # Configure embedding model
        Settings.llm = None
        Settings.embed_model = HuggingFaceEmbedding(model_name=embedding_model)
        
        # Configure LLM
        self.generator = pipeline(
            "text-generation",
            model=llm_model,
            torch_dtype=torch.float32,
            device_map="auto" if torch.cuda.is_available() else "cpu",
            do_sample=True,
            temperature=temperature
        )
        
        self.default_top_k = top_k
        self.dataset_name = dataset_name
        self.index = None
        
        # Build index
        self._build_index()
    
    def _build_index(self) -> None:
        """
        Build the vector index from the recipe dataset.
        
        This method loads the recipe dataset and converts entries to documents
        suitable for indexing with LlamaIndex.
        """
        logger.info(f"Building index from dataset: {self.dataset_name}")
        try:
            dataset = load_dataset(self.dataset_name, trust_remote_code=True)
            
            # Build documents with structured content
            documents = []
            for item in dataset["train"]:
                text = (
                    f"Recipe: {item['name']}\n"
                    f"Ingredients: {item['ingredients']}\n"
                    f"Steps: {item['steps']}"
                )
                documents.append(Document(text=text, metadata={"name": item["name"]}))
            
            logger.info(f"Created {len(documents)} recipe documents")
            self.index = VectorStoreIndex.from_documents(documents)
            
        except Exception as e:
            logger.error(f"Error building index: {str(e)}")
            raise
    
    def retrieve(self, query: str, top_k: Optional[int] = None) -> Dict[str, Any]:
        """
        Retrieve relevant recipe documents for a user query.
        
        Args:
            query: The user's recipe-related query
            top_k: Number of documents to retrieve (overrides default)
            
        Returns:
            A dictionary containing query results and metadata
        """
        k = top_k or self.default_top_k
        logger.info(f"Retrieving top {k} documents for query: '{query}'")
        
        try:
            query_engine = self.index.as_query_engine(similarity_top_k=k)
            result = query_engine.query(query)
            
            # Extract source nodes and metadata
            sources = [n.node.get_content() for n in result.source_nodes]
            metadata = [n.node.metadata for n in result.source_nodes]
            
            return {
                "result": result,
                "sources": sources,
                "metadata": metadata
            }
        except Exception as e:
            logger.error(f"Retrieval error: {str(e)}")
            raise
    
    def generate_answer(self, question: str, context: List[str]) -> str:
        """
        Generate a helpful response based on the retrieved recipe context.
        
        Args:
            question: The user's original question
            context: List of retrieved recipe documents as context
            
        Returns:
            The generated response
        """
        logger.info(f"Generating answer for: '{question}'")
        
        try:
            # Build a detailed prompt with system context and retrieved information
            prompt = f"""
            [INST] <<SYS>>
            You are a professional recipe assistant. Answer the user's question based on the following recipes:
            
            {"".join(context)}
            <</SYS>>
            
            Question: {question} [/INST]
            """
            
            result = self.generator(
                prompt,
                max_new_tokens=256,
                temperature=0.7
            )[0]['generated_text']
            
            # Extract just the model's response part
            response = result.split("[/INST]")[-1].strip()
            return response
            
        except Exception as e:
            logger.error(f"Generation error: {str(e)}")
            raise