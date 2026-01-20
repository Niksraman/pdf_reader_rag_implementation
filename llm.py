
"""
LLM integration module - handles different LLM providers
"""
from typing import List
from abc import ABC, abstractmethod
from config import LLM_TYPE, OLLAMA_BASE_URL, OLLAMA_MODEL, OPENAI_API_KEY, OPENAI_MODEL
from logger import setup_logger

logger = setup_logger(__name__)

class LLMProvider(ABC):
    """Abstract base class for LLM providers"""
    
    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Generate response from prompt"""
        pass

class OllamaProvider(LLMProvider):
    """Ollama LLM provider"""
    
    def __init__(self, base_url: str = OLLAMA_BASE_URL, model: str = OLLAMA_MODEL):
        """
        Initialize Ollama provider
        
        Args:
            base_url: Base URL for Ollama
            model: Model name
        """
        self.base_url = base_url
        self.model = model
        self.api_url = f"{base_url}/api/generate"
        logger.info(f"Initialized OllamaProvider with model: {model}")
    
    def generate(self, prompt: str) -> str:
        """
        Generate response using Ollama
        
        Args:
            prompt: Input prompt
            
        Returns:
            Generated response
        """
        try:
            import requests
            
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }
            
            response = requests.post(self.api_url, json=payload, timeout=300)
            response.raise_for_status()
            
            result = response.json().get("response", "")
            logger.info(f"Generated response from Ollama ({len(result)} chars)")
            return result
        except Exception as e:
            logger.error(f"Error generating response from Ollama: {str(e)}")
            raise

class OpenAIProvider(LLMProvider):
    """OpenAI LLM provider"""
    
    def __init__(self, api_key: str = OPENAI_API_KEY, model: str = OPENAI_MODEL):
        """
        Initialize OpenAI provider
        
        Args:
            api_key: OpenAI API key
            model: Model name
        """
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set")
        
        self.api_key = api_key
        self.model = model
        logger.info(f"Initialized OpenAIProvider with model: {model}")
    
    def generate(self, prompt: str) -> str:
        """
        Generate response using OpenAI
        
        Args:
            prompt: Input prompt
            
        Returns:
            Generated response
        """
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=self.api_key)
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=1000
            )
            
            result = response.choices[0].message.content
            logger.info(f"Generated response from OpenAI ({len(result)} chars)")
            return result
        except Exception as e:
            logger.error(f"Error generating response from OpenAI: {str(e)}")
            raise

class HuggingFaceProvider(LLMProvider):
    """HuggingFace LLM provider"""
    
    def __init__(self, model: str = "meta-llama/Llama-2-7b-chat-hf"):
        """
        Initialize HuggingFace provider
        
        Args:
            model: Model name from HuggingFace
        """
        from transformers import pipeline
        
        try:
            self.model = model
            self.pipeline = pipeline("text-generation", model=model, device=0)
            logger.info(f"Initialized HuggingFaceProvider with model: {model}")
        except Exception as e:
            logger.error(f"Error initializing HuggingFace: {str(e)}")
            raise
    
    def generate(self, prompt: str) -> str:
        """
        Generate response using HuggingFace
        
        Args:
            prompt: Input prompt
            
        Returns:
            Generated response
        """
        try:
            response = self.pipeline(prompt, max_length=500, do_sample=True)[0]
            result = response.get("generated_text", "")
            logger.info(f"Generated response from HuggingFace ({len(result)} chars)")
            return result
        except Exception as e:
            logger.error(f"Error generating response from HuggingFace: {str(e)}")
            raise

def get_llm_provider(provider_type: str = LLM_TYPE) -> LLMProvider:
    """
    Get LLM provider based on configuration
    
    Args:
        provider_type: Type of LLM provider (ollama, openai, huggingface)
        
    Returns:
        LLMProvider instance
    """
    if provider_type.lower() == "ollama":
        return OllamaProvider()
    elif provider_type.lower() == "openai":
        return OpenAIProvider()
    elif provider_type.lower() == "huggingface":
        return HuggingFaceProvider()
    else:
        raise ValueError(f"Unknown LLM provider: {provider_type}")


def generate_answer(question: str, documents: List[dict]) -> str:
    """
    Generate an answer using the configured LLM, grounded in provided documents.
    
    Args:
        question: User question
        documents: List of relevant documents with 'content' field
        
    Returns:
        Generated answer
    """
    try:
        llm = get_llm_provider()
        context = "\n\n".join([doc.get("content", doc) for doc in documents])
        prompt = f"""You are an expert assistant. Use ONLY the following context to answer the question.

Context:
{context}

Question: {question}
Answer:"""
        answer = llm.generate(prompt)
        return answer.strip()
    except Exception as e:
        logger.error(f"Error generating answer: {str(e)}")
        return "[Error: LLM unavailable]"
