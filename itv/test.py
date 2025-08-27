import pandas as pd
import random
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage, SystemMessage
import os

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
openai_api_key = os.environ["OPENAI_API_KEY"]
model = os.environ["OPENAI_MODEL"]
temperature = os.environ["TEMPERATURE"]

system_template = """
You are an expert evaluator. Your task is to grade the interviewee's answer based on the provided standard answer.

# SCORING GUIDELINES:
- Score range: 0-10 (integer only)
- Focus on correctness, completeness, and conceptual understanding
- Answers do not need to be identical to the standard answer
- Accept alternative wording if the meaning is accurate
- Give partial credit when only part of the answer is correct

# SCORING CRITERIA (flexible with strict penalty for major errors):
- 9-10 points: Answer captures all key ideas, reasoning is clear, demonstrates strong understanding. Minor differences in wording are acceptable.
- 7-8 points: Answer covers most important points; small omissions or slight inaccuracies are acceptable. Expression may differ from standard answer.
- 5-6 points: Answer is generally correct but misses several points or contains minor errors. Partial understanding is evident.
- 3-4 points: Answer shows limited understanding; many points are missing or incorrect. Some correct ideas present.
- 1-2 points: Answer has very few correct elements; major misunderstandings or irrelevant content present. 
- 0 points: Answer is completely wrong, irrelevant, or empty. No understanding demonstrated. Strictly apply maximum penalty.



# INPUT:
STANDARD ANSWER:
{original_answer}

STUDENT'S ANSWER:
{user_answer}

# OUTPUT FORMAT (strictly follow this):
SCORE: [0-10]

DETAILED EVALUATION:
- Strengths: [Correct parts of the student's answer]
- Areas for improvement: [What is wrong or missing]
- Suggestions: [Concrete advice to improve the answer]

SCORE EXPLANATION:
[Clear reasoning for the assigned score, highlighting key differences from the standard answer]

"""

class MLOpsQuizBot:
    def __init__(self, csv_file_path, openai_api_key=None):
        """
        Initialize MLOps quiz chatbot
        
        Args:
            csv_file_path (str): Path to CSV file containing questions and answers
            openai_api_key (str): OpenAI API key (can be set via environment variable)
        """
        # Set up OpenAI API key
        if openai_api_key:
            os.environ["OPENAI_API_KEY"] = openai_api_key
        
        # Initialize LLM
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.3,  # Reduce randomness for consistent scoring
            max_tokens=500
        )
        
        # Load data from CSV
        self.load_data(csv_file_path)
        
        # Create prompt template for scoring
        self.scoring_prompt = PromptTemplate(
            input_variables=["original_answer", "user_answer"],
            template=system_template
        )
    
    def load_data(self, csv_file_path):
        """Load data from CSV file"""
        try:
            self.df = pd.read_csv(csv_file_path)
            print(f"✅ Successfully loaded {len(self.df)} questions from CSV file")
            
            # Check data structure
            if 'question' not in self.df.columns or 'answer' not in self.df.columns:
                raise ValueError("CSV file must have 2 columns: 'question' and 'answer'")
            
            # Clean data
            self.df['question'] = self.df['question'].str.strip()
            self.df['answer'] = self.df['answer'].str.strip()
            
        except Exception as e:
            print(f"❌ Error reading CSV file: {e}")
            raise
    
    def get_random_question(self):
        """Get a random question from dataset"""
        random_index = random.randint(0, len(self.df) - 1)
        question = self.df.iloc[random_index]['question']
        answer = self.df.iloc[random_index]['answer']
        
        return question, answer, random_index
    
    def score_answer(self, original_answer, user_answer):
        """
        Score user's answer against the original answer
        
        Args:
            original_answer (str): Standard answer
            user_answer (str): User's answer
            
        Returns:
            str: Detailed scoring result
        """
        try:
            # Create prompt
            prompt = self.scoring_prompt.format(
                original_answer=original_answer,
                user_answer=user_answer
            )
            
            # Call LLM to score
            messages = [
                SystemMessage(content="You are an MLOps expert and experienced teacher skilled at evaluating technical knowledge."),
                HumanMessage(content=prompt)
            ]
            
            response = self.llm.invoke(messages)
            return response.content
            
        except Exception as e:
            return f"❌ Error during scoring: {e}"
    
    def extract_score(self, scoring_result):
        """Extract score from scoring result"""
        try:
            lines = scoring_result.split('\n')
            for line in lines:
                if 'SCORE:' in line:
                    score_text = line.split(':')[1].strip()
                    # Find number in string
                    import re
                    score_match = re.search(r'\d+', score_text)
                    if score_match:
                        return int(score_match.group())
            return None
        except:
            return None
    
    def start_quiz(self):
        """Start interactive quiz"""
        print("🎯 WELCOME TO MLOPS QUIZ BOT!")
        print("=" * 50)
        print("Instructions:")
        print("- I will ask you a question about MLOps")
        print("- You answer, I will score it (0-10)")
        print("- Type 'quit' to exit\n")
        
        total_score = 0
        question_count = 0
        
        while True:
            try:
                # Get random question
                question, correct_answer, question_index = self.get_random_question()
                
                print(f"📝 QUESTION #{question_count + 1}:")
                print(f"❓ {question}")
                print("\n💭 Your answer:")
                
                # Get user input
                user_answer = input("👉 ").strip()
                
                # Check exit command
                if user_answer.lower() == 'quit':
                    break
                
                if not user_answer:
                    print("⚠️  Please enter an answer!")
                    continue
                
                print("\n⏳ Scoring in progress...")
                
                # Score answer
                scoring_result = self.score_answer(correct_answer, user_answer)
                
                # Extract score
                score = self.extract_score(scoring_result)
                
                # Display results
                print("\n" + "="*60)
                print("📊 SCORING RESULTS:")
                print("="*60)
                print(scoring_result)
                
                if score is not None:
                    total_score += score
                    question_count += 1
                    print(f"\n🎯 CURRENT AVERAGE SCORE: {total_score/question_count:.1f}/10")
                
                print("\n" + "="*60)
                input("\n👉 Press Enter to continue to the next question...")
                print("\n")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ An error occurred: {e}")
                continue
        
        # Display final results
        if question_count > 0:
            avg_score = total_score / question_count
            print(f"\n🏁 FINAL RESULTS:")
            print(f"📈 Questions answered: {question_count}")
            print(f"🎯 Average score: {avg_score:.1f}/10")
            
            # if avg_score >= 8:
            #     print("🏆 Excellent! You have great MLOps knowledge!")
            # elif avg_score >= 6:
            #     print("👍 Good! You understand the basic concepts of MLOps!")
            # elif avg_score >= 4:
            #     print("📚 Average. Please review more about MLOps!")
            # else:
            #     print("💪 Need more effort. Please learn more about MLOps!")


# Usage example
if __name__ == "__main__":
    # Method 1: Set API key directly (not recommended in production)
    # quiz_bot = MLOpsQuizBot("data.csv", openai_api_key="your-api-key-here")
    
    # Method 2: Set API key via environment variable (recommended)
    # export OPENAI_API_KEY="your-api-key-here" (on Linux/Mac)
    # set OPENAI_API_KEY=your-api-key-here (on Windows)
    
    try:
        quiz_bot = MLOpsQuizBot("data.csv")
        quiz_bot.start_quiz()
    except Exception as e:
        print(f"❌ Initialization error: {e}")
        # print("💡 Make sure:")
        # print("   1. File 'data.csv' exists")
        # print("   2. Installed: pip install langchain openai pandas")
        # print("   3. Set OPENAI_API_KEY in environment variables")