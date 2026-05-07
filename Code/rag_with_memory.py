"""
Enhanced RAG with Conversation Memory
Level 2: Smart RAG Implementation

Features:
- Multi-turn conversation with context awareness
- Tracks conversation history
- Improves answer quality by referencing previous turns
- Ready for production
"""

import os
from collections import deque
from datetime import datetime
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

class ConversationalRAG:
    """
    RAG system with conversation memory.
    
    Remembers previous questions and answers to provide better context
    for follow-up questions.
    """
    
    def __init__(self, vector_store, llm, max_history=5):
        """
        Initialize the conversational RAG system.
        
        Args:
            vector_store: FAISS vector store
            llm: Language model (ChatOpenAI)
            max_history: Maximum number of conversation turns to remember
        """
        self.vector_store = vector_store
        self.llm = llm
        self.max_history = max_history
        
        # Store conversation history
        self.conversation = deque(maxlen=max_history)
        
        # Create retriever
        self.retriever = vector_store.as_retriever(
            search_kwargs={"k": 5}
        )
        
        # System prompt
        self.system_prompt = """You are an expert AI tutor helping someone learn about LLMs, 
machine learning, and AI engineering. You have access to high-quality documentation, 
research papers, and textbooks.

When answering questions:
1. Use ONLY the provided context/documents to answer
2. If the answer isn't in the context, say "I don't have information about this in my knowledge base"
3. Cite which documents/sources you're drawing from
4. Be clear and educational - explain concepts simply
5. For complex topics, break down the answer step-by-step
6. When referring to previous conversation, acknowledge it explicitly
7. Build on previous answers when relevant to the current question

Conversation Guidelines:
- If a user asks a follow-up question (e.g., "How does it compare to X?"), 
  remember what was discussed in the previous turn
- Use pronouns like "it" and "this" naturally, but you have the context from history
- If context seems lost, ask for clarification
"""
    
    def answer_question(self, question: str):
        """
        Answer a question using RAG with conversation context.
        
        Args:
            question: User's question
            
        Returns:
            tuple: (answer_text, retrieved_docs, conversation_history)
        """
        
        # Format conversation history for context
        history_context = self._format_history()
        
        # Retrieve relevant documents
        docs = self.retriever.invoke(question)
        context_str = self._format_context(docs)
        
        # Build the full prompt with history
        full_prompt = self._build_prompt(
            history_context,
            question,
            context_str
        )
        
        # Get response from LLM
        response = self.llm.invoke(full_prompt)
        answer = response.content
        
        # Extract sources
        sources = [
            doc.metadata.get("source", "unknown").split("/")[-1]
            for doc in docs
        ]
        
        # Store in conversation history
        self.conversation.append({
            "timestamp": datetime.now(),
            "question": question,
            "answer": answer,
            "answer_summary": answer[:300],  # Truncate for history display
            "sources": sources
        })
        
        return answer, docs, list(self.conversation)
    
    def _format_history(self):
        """Format conversation history for the LLM prompt."""
        
        if not self.conversation:
            return "(This is the start of the conversation)"
        
        history_text = "CONVERSATION HISTORY (for reference):\n"
        for i, turn in enumerate(self.conversation, 1):
            history_text += f"\n{i}. Q: {turn['question']}\n"
            history_text += f"   A: {turn['answer_summary']}...\n"
            history_text += f"   Sources: {', '.join(turn['sources'])}\n"
        
        return history_text
    
    def _format_context(self, docs):
        """Format retrieved documents as context."""
        
        formatted = []
        for i, doc in enumerate(docs, 1):
            source = doc.metadata.get("source", "unknown").split("/")[-1]
            page = doc.metadata.get("page", "N/A")
            
            formatted.append(
                f"Document {i} ({source}, page {page}):\n{doc.page_content}"
            )
        
        return "\n\n" + "="*60 + "\n".join(formatted)
    
    def _build_prompt(self, history, question, context):
        """Build the complete prompt for the LLM."""
        
        prompt = f"""{self.system_prompt}

{history}

CURRENT QUESTION: {question}

REFERENCE DOCUMENTS:
{context}

Please provide a comprehensive, educational answer to the current question, 
keeping in mind the conversation history above."""
        
        return prompt
    
    def clear_history(self):
        """Clear conversation history."""
        self.conversation.clear()
    
    def get_history(self):
        """Get full conversation history."""
        return list(self.conversation)
    
    def get_summary(self):
        """Get a summary of the conversation so far."""
        if not self.conversation:
            return "No conversation yet"
        
        topics = []
        for turn in self.conversation:
            # Extract key words from question
            words = turn['question'].split()[:5]
            topics.append(" ".join(words))
        
        summary = f"""
Conversation Summary:
- Questions asked: {len(self.conversation)}
- Topics covered: {', '.join(topics)}
- Last question: {self.conversation[-1]['question']}
"""
        return summary


class StreamingRAG(ConversationalRAG):
    """
    Conversational RAG with streaming response support.
    
    Yields response tokens one at a time for real-time display.
    """
    
    def stream_answer(self, question: str):
        """
        Answer a question with streaming response.
        
        Yields:
            str: Response tokens as they arrive from the LLM
        """
        
        # Format conversation history for context
        history_context = self._format_history()
        
        # Retrieve relevant documents
        docs = self.retriever.invoke(question)
        context_str = self._format_context(docs)
        
        # Build the full prompt with history
        full_prompt = self._build_prompt(
            history_context,
            question,
            context_str
        )
        
        # Stream response
        full_response = ""
        for chunk in self.llm.stream(full_prompt):
            token = chunk.content
            full_response += token
            yield token
        
        # Extract sources and store in history
        sources = [
            doc.metadata.get("source", "unknown").split("/")[-1]
            for doc in docs
        ]
        
        self.conversation.append({
            "timestamp": datetime.now(),
            "question": question,
            "answer": full_response,
            "answer_summary": full_response[:300],
            "sources": sources
        })


# -----------------------------------------------------------------------
# Example Usage
# -----------------------------------------------------------------------

if __name__ == "__main__":
    # Load vector store and LLM
    BASE_DIR = "/Users/vidhipitroda/Desktop/Projects/AI tutor"
    FAISS_INDEX_PATH = os.path.join(BASE_DIR, "Data/faiss_index")
    
    print("Loading vector store...")
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vector_store = FAISS.load_local(
        FAISS_INDEX_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )
    
    print("Initializing LLM...")
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
    
    # Create conversational RAG
    print("Setting up conversational RAG...")
    rag = ConversationalRAG(vector_store, llm)
    
    # Example multi-turn conversation
    print("\n" + "="*70)
    print("MULTI-TURN CONVERSATION EXAMPLE")
    print("="*70)
    
    # Turn 1
    print("\n👤 User: What is LoRA?")
    answer1, docs1, history1 = rag.answer_question("What is LoRA?")
    print(f"\n🤖 Tutor: {answer1[:200]}...")
    print(f"\n📚 Sources: {', '.join([d.metadata.get('source', 'unknown').split('/')[-1] for d in docs1])}")
    
    # Turn 2 (Follow-up question that refers to "it")
    print("\n" + "-"*70)
    print("\n👤 User: How does it compare to adapters?")
    answer2, docs2, history2 = rag.answer_question("How does it compare to adapters?")
    print(f"\n🤖 Tutor: {answer2[:200]}...")
    print(f"\n📚 Sources: {', '.join([d.metadata.get('source', 'unknown').split('/')[-1] for d in docs2])}")
    
    # Turn 3 (Another follow-up)
    print("\n" + "-"*70)
    print("\n👤 User: When should I use one over the other?")
    answer3, docs3, history3 = rag.answer_question("When should I use one over the other?")
    print(f"\n🤖 Tutor: {answer3[:200]}...")
    print(f"\n📚 Sources: {', '.join([d.metadata.get('source', 'unknown').split('/')[-1] for d in docs3])}")
    
    # Show conversation summary
    print("\n" + "="*70)
    print("CONVERSATION SUMMARY")
    print("="*70)
    print(rag.get_summary())
    
    print("\n" + "="*70)
    print("✅ Conversational RAG demonstration complete!")
    print("="*70)
