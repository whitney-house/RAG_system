from llama_index.core import VectorStoreIndex, Document, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.faiss import FaissVectorStore
from llama_index.core import StorageContext
from datasets import load_dataset
from transformers import pipeline
import faiss
import torch
import logging
import os
from dotenv import load_dotenv
from typing import List, Dict, Any, Optional


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class RecipeRAGSystem:
    """
    Retrieval-Augmented Generation (RAG) system for recipe queries.
    Uses Llama 2 for response generation and an optimized embedding model for retrieval.
    """
    
    def __init__(
        self, 
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
        llm_model: str = "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        dataset_name: str = "m3hrdadfi/recipe_nlg_lite",
        temperature: float = 0.7,
        top_k: int = 3
    ):
        """
        Initialize the RAG system with specified models and parameters.
        """
        logger.info(f"Initializing RAGSystem with {embedding_model} and {llm_model}")
        
        
        Settings.llm = None # To shut down openai error 
        self.embedding_model = HuggingFaceEmbedding(model_name=embedding_model)
        Settings.embed_model = self.embedding_model
        
        # Configure LLM
        self.generator = pipeline(
            "text-generation",
            model=llm_model,
            torch_dtype=torch.float16,
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
        """
        logger.info(f"Building index from dataset: {self.dataset_name}")
        try:
            dataset = load_dataset(self.dataset_name, trust_remote_code=True)
            
            documents = [
                Document(
                    text=f"Recipe: {item['name']}\nIngredients: {item['ingredients']}\nSteps: {item['steps']}",
                    metadata={"name": item["name"]}
                )
                for item in dataset["train"]
            ]
            
            logger.info(f"Created {len(documents)} recipe documents")

            embeddings = self.embedding_model.get_text_embedding_batch(
                [doc.text for doc in documents]
            )
            dimension = len(embeddings[0])
            faiss_index = faiss.IndexFlatL2(dimension)

            vector_store = FaissVectorStore(faiss_index=faiss_index)
            storage_context = StorageContext.from_defaults(vector_store=vector_store)
        
            #self.index = VectorStoreIndex.from_documents(documents)
            self.index = VectorStoreIndex.from_documents(documents, 
                                                        storage_context=storage_context
                                                        )
            
        except Exception as e:
            logger.error(f"Error building index: {str(e)}")
            raise
    
    def retrieve(self, query: str, top_k: Optional[int] = None) -> Dict[str, Any]:
        """
        Retrieve relevant recipe documents for a user query.
        """
        k = top_k or self.default_top_k
        logger.info(f"Retrieving top {k} documents for query: '{query}'")
        
        try:
            query_engine = self.index.as_query_engine(similarity_top_k=k)
            result = query_engine.query(query)
            
            sources = [n.node.get_content() for n in result.source_nodes]
            metadata = [n.node.metadata for n in result.source_nodes]
            
            return {"result": result, "sources": sources, "metadata": metadata}
        except Exception as e:
            logger.error(f"Retrieval error: {str(e)}")
            raise
    
    def generate_answer(self, question: str, context: List[str]) -> str:
        """
        Generate a response based on retrieved context.
        """
        logger.info(f"Generating answer for: '{question}'")
        
        try:
            prompt = f"""
            [INST] <<SYS>>
            You are a helpful recipe assistant. Use the following recipes to answer:
            
            {"".join(context)}
            <</SYS>>
            
            Question: {question} [/INST]
            """
            
            result = self.generator(
                prompt,
                max_new_tokens=1000,
                temperature=0.7
            )[0]['generated_text']
            
            response = result.split("[/INST]")[-1].strip()
            return response
            
        except Exception as e:
            logger.error(f"Generation error: {str(e)}")
            raise