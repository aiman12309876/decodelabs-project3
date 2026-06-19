class RecommendationSystem:
    def __init__(self):
        self.items = {
            'movie': {
                'Inception': ['Sci-Fi', 'Thriller', 'Action'],
                'The Matrix': ['Sci-Fi', 'Action', 'Adventure'],
                'The Godfather': ['Drama', 'Crime'],
                'Interstellar': ['Sci-Fi', 'Drama', 'Adventure'],
                'The Dark Knight': ['Action', 'Thriller', 'Drama'],
                'Pulp Fiction': ['Crime', 'Drama'],
                'Avatar': ['Sci-Fi', 'Action', 'Adventure'],
                'Titanic': ['Romance', 'Drama'],
                'The Shawshank Redemption': ['Drama'],
                'Gladiator': ['Action', 'Drama', 'Adventure']
            },
            'book': {
                '1984': ['Dystopian', 'Sci-Fi', 'Classic'],
                'The Hobbit': ['Fantasy', 'Adventure'],
                'To Kill a Mockingbird': ['Classic', 'Drama'],
                'Dune': ['Sci-Fi', 'Adventure', 'Fantasy'],
                'Pride and Prejudice': ['Romance', 'Classic'],
                'The Alchemist': ['Adventure', 'Inspirational'],
                'Sapiens': ['Non-Fiction', 'History'],
                'Atomic Habits': ['Non-Fiction', 'Self-Help'],
                'The Great Gatsby': ['Classic', 'Drama'],
                'The Catcher in the Rye': ['Classic', 'Drama']
            },
            'course': {
                'Python for Beginners': ['Programming', 'Python', 'Beginner'],
                'Data Science 101': ['Data Science', 'Python', 'Statistics'],
                'Machine Learning A-Z': ['AI', 'Machine Learning', 'Python'],
                'Deep Learning Specialization': ['AI', 'Deep Learning', 'Neural Networks'],
                'Web Development Bootcamp': ['Web', 'HTML', 'CSS', 'JavaScript'],
                'Java Programming': ['Programming', 'Java', 'Beginner'],
                'Database Management': ['SQL', 'Database', 'Backend'],
                'DevOps Fundamentals': ['DevOps', 'Cloud', 'CI/CD'],
                'Cybersecurity Basics': ['Security', 'Network', 'Ethical Hacking'],
                'Blockchain Essentials': ['Blockchain', 'Cryptocurrency', 'Web3']
            }
        }

    def get_user_preferences(self):
        print("\n" + "=" * 60)
        print("   AI RECOMMENDATION SYSTEM")
        print("=" * 60)
        
        print("\nChoose a category:")
        print("1. Movies")
        print("2. Books")
        print("3. Courses")
        
        choice = input("\nEnter your choice (1/2/3): ")
        
        if choice == '1':
            category = 'movie'
            category_name = 'Movies'
        elif choice == '2':
            category = 'book'
            category_name = 'Books'
        elif choice == '3':
            category = 'course'
            category_name = 'Courses'
        else:
            print("Invalid choice! Defaulting to Movies.")
            category = 'movie'
            category_name = 'Movies'
        
        print(f"\nYou selected: {category_name}")
        
        print(f"\nAvailable {category_name}:")
        items_list = list(self.items[category].keys())
        for i, item in enumerate(items_list, 1):
            print(f"{i}. {item}")
        
        print("\nEnter your preferences (comma-separated numbers):")
        print("Example: 1,3,5")
        
        preference_input = input("Your choices: ")
        
        try:
            indices = [int(x.strip()) - 1 for x in preference_input.split(',')]
            selected_items = [items_list[i] for i in indices if 0 <= i < len(items_list)]
        except:
            selected_items = []
        
        return category, selected_items

    def get_item_tags(self, category, item_name):
        return self.items[category].get(item_name, [])

    def calculate_similarity(self, category, selected_items):
        if not selected_items:
            return []
        
        selected_tags = []
        for item in selected_items:
            tags = self.get_item_tags(category, item)
            selected_tags.extend(tags)
        
        selected_tags = list(set(selected_tags))
        
        if not selected_tags:
            return []
        
        scores = {}
        all_items = self.items[category]
        
        for item_name, tags in all_items.items():
            if item_name in selected_items:
                continue
            
            common_tags = set(tags) & set(selected_tags)
            score = len(common_tags)
            scores[item_name] = score
        
        sorted_items = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        return sorted_items[:5]

    def display_recommendations(self, category, selected_items, recommendations):
        category_names = {
            'movie': 'Movies',
            'book': 'Books',
            'course': 'Courses'
        }
        
        print("\n" + "=" * 60)
        print("   YOUR RECOMMENDATIONS")
        print("=" * 60)
        
        print(f"\nYou liked: {', '.join(selected_items)}")
        
        if not recommendations:
            print("\nNo recommendations found. Try selecting different items.")
            return
        
        print(f"\nRecommended {category_names[category]} for you:")
        print("-" * 40)
        
        for i, (item, score) in enumerate(recommendations, 1):
            tags = self.get_item_tags(category, item)
            print(f"{i}. {item}")
            print(f"   Tags: {', '.join(tags)}")
            print(f"   Similarity Score: {score}")
            print()

def main():
    system = RecommendationSystem()
    
    print("\n" + "=" * 60)
    print("   AI RECOMMENDATION SYSTEM")
    print("=" * 60)
    print("\nThis system recommends items based on your preferences.")
    print("It matches the tags of items you like with other items.\n")
    
    category, selected_items = system.get_user_preferences()
    
    if selected_items:
        recommendations = system.calculate_similarity(category, selected_items)
        system.display_recommendations(category, selected_items, recommendations)
    else:
        print("\nNo valid selections made. Please try again.")
    
    print("\n" + "=" * 60)
    print("   RECOMMENDATION COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()