import google.generativeai as genai
import streamlit as st

class AiCodeReviewer:
    def __init__(self):
        self.api_key = "AIzaSyB4tK6azgrb_-VQSgsNT2BW29ABjwaxJII"

    def chatbot(self, system_instruction: str = None):
        genai.configure(api_key=self.api_key)
        return genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=system_instruction
        )

    def streamlit_app(self):
        st.title(":email: An AI Code Reviewer")
        st.text("Enter your Python code here...")
        if "chat_history" not in st.session_state:
            st.session_state["chat_history"] = []

        instruction = """
        You are an expert in AI fields. Act as an expert AI code reviewer.
        Analyze the provided code for clarity, efficiency, maintainability, and adherence to best practices.
        Identify potential errors, suggest improvements, and provide clear, actionable feedback.
        Also, provide the corrected code with the necessary fixes.
        """
        model = self.chatbot(system_instruction=instruction)
        chat = model.start_chat(history=st.session_state["chat_history"])

        user_prompt = st.chat_input()

        if user_prompt:
            st.chat_message("user").write(user_prompt)
            response = chat.send_message(user_prompt)

            # Display the Bug Report and Fixed Code sections
            st.markdown("## Bug Report")
            st.write(response.text)  # AI's generated bug report

            # Extract fixed code from AI response (this assumes the AI provides fixed code in a specific format)
            fixed_code = self.extract_fixed_code(response.text)
            if fixed_code:
                st.markdown("## Fixed Code")
                st.code(fixed_code, language='python')

            # Update chat history
            st.session_state["chat_history"] = chat.history

    def extract_fixed_code(self, response_text: str):
        """
        Helper function to extract fixed code from the AI's response text.
        This assumes that the AI's response contains the fixed code after the bug report.
        Adjust the parsing logic as needed based on the actual format of the AI response.
        """
        # Check if the response contains fixed code (this is a simple example, you may need a more robust method)
        if "Fixed Code:" in response_text:
            start_index = response_text.find("Fixed Code:") + len("Fixed Code:")
            return response_text[start_index:].strip()  # Return fixed code after "Fixed Code:"
        return None


if __name__ == "__main__":
    ai = AiCodeReviewer()
    ai.streamlit_app()

