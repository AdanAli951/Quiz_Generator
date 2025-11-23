import re
import random

def simple_quiz():
    print("=== Simple Quiz Generator ===")
    
    # Get paragraph input
    print("Enter your paragraph:")
    paragraph = input().strip()
    
    if not paragraph:
        print("No text entered!")
        return
    
    # Get number of questions
    while True:
        try:
            num_questions = int(input("Enter number of questions to generate (1-10): "))
            if 1 <= num_questions <= 10:
                break
            else:
                print("Please enter a number between 1 and 10")
        except ValueError:
            print("Please enter a valid number")
    
    # Simple sentence splitting
    sentences = re.split(r'[.!?]', paragraph)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    
    # Simple word extraction - get more words for more questions
    words = re.findall(r'\b[a-zA-Z]{5,}\b', paragraph)
    important_words = list(set(words))[:num_questions * 3]  # Get more words for options
    
    questions = []
    
    for i in range(min(num_questions, len(sentences))):
        if not important_words or not sentences:
            break
            
        # Find a sentence with important words
        suitable_sentence = None
        target_word = None
        
        for sentence in sentences:
            sentence_words = [w for w in important_words if w.lower() in sentence.lower()]
            if sentence_words:
                suitable_sentence = sentence
                target_word = random.choice(sentence_words)
                sentences.remove(sentence)  # Remove used sentence
                important_words.remove(target_word)  # Remove used word
                break
        
        if not suitable_sentence:
            break
            
        # Create question
        question_text = suitable_sentence.replace(target_word, "______")
        
        # Create options
        correct = target_word.title()
        wrongs = []
        
        # Get wrong options from remaining important words
        for word in important_words:
            if word != target_word and len(wrongs) < 3:
                wrongs.append(word.title())
        
        # If we don't have enough wrong options, add generic ones
        while len(wrongs) < 3:
            generic_words = ['process', 'system', 'method', 'theory', 'concept', 
                           'principle', 'element', 'structure', 'pattern', 'framework']
            generic = random.choice(generic_words).title()
            if generic not in wrongs and generic != correct:
                wrongs.append(generic)
        
        options = [correct] + wrongs
        random.shuffle(options)
        correct_index = options.index(correct)
        
        questions.append({
            'question': question_text,
            'options': options,
            'answer': correct_index,
            'correct_answer': correct
        })
    
    if not questions:
        print("\nCould not generate questions from the provided text.")
        print("Please try a longer paragraph with more content.")
        return
    
    print(f"\n=== Generated Quiz: {len(questions)} Questions ===")
    print("=" * 50)
    
    # Run the quiz
    score = 0
    for i, q in enumerate(questions, 1):
        print(f"\nQ{i}: {q['question']}")
        print()
        for j, opt in enumerate(q['options']):
            print(f"    {chr(65+j)}) {opt}")
        print()
        
        while True:
            ans = input("Your choice (A/B/C/D): ").upper().strip()
            if ans in ['A','B','C','D']:
                break
            print("Please enter A, B, C, or D")
        
        user_index = ord(ans) - 65
        if user_index == q['answer']:
            print("✅ Correct!")
            score += 1
        else:
            correct_letter = chr(65 + q['answer'])
            print(f"❌ Wrong! The correct answer is {correct_letter}) {q['correct_answer']}")
        
        print("-" * 50)
    
    # Display final results
    print(f"\n{' RESULTS ':=^50}")
    print(f"Final Score: {score}/{len(questions)}")
    percentage = (score / len(questions)) * 100
    print(f"Percentage: {percentage:.1f}%")
    
    # Display answer key
    print(f"\n{' ANSWER KEY ':=^50}")
    for i, q in enumerate(questions, 1):
        correct_letter = chr(65 + q['answer'])
        print(f"Q{i}: {correct_letter}) {q['correct_answer']}")

if __name__ == "__main__":
    simple_quiz()