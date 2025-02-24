class RecommendationExplanationSystem:
    def __init__(self):
        """
        Initializes the explanation system with adaptable templates.
        """
        self.templates = [
            "Based on {user_input}, the {course_title} program at {university} is a great match. {context_match} The compatibility score for this recommendation is {similarity_score:.2f}.",
            "Your aspirations and interests—{user_input}—align strongly with the {course_title} course at {university}. {context_match} It achieved a similarity score of {similarity_score:.2f}.",
            "Given {user_input}, the {course_title} program at {university} is highly recommended. {context_match} It stands out with a compatibility score of {similarity_score:.2f}.",
            "With your goals and interests—{user_input}—the {course_title} at {university} is an excellent fit. {context_match} This recommendation achieved a score of {similarity_score:.2f}."
        ]

    def generate_explanation(self, course_title, university, similarity_score, user_input, context_match):
        """
        Generates a recommendation explanation dynamically for any user input.

        Args:
            course_title (str): The recommended course title.
            university (str): The university offering the course.
            similarity_score (float): The similarity score of the recommendation.
            user_input (str): The user's input describing their interests.
            context_match (str): Specific context aligning the course to user inputs.

        Returns:
            str: A dynamically generated explanation.
        """
        # Validate inputs
        if not user_input.strip():
            return "No user input provided. Unable to generate an explanation."

        if not course_title.strip() or not university.strip():
            return "Course or university details are missing. Unable to generate an explanation."

        # Choose a random template for explanation variety
        import random
        template = random.choice(self.templates)

        # Format the explanation with user input and course details
        explanation = template.format(
            user_input=user_input.strip(),
            course_title=course_title.strip(),
            university=university.strip(),
            similarity_score=similarity_score,
            context_match=context_match.strip()
        )

        return explanation
