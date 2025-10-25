from google import genai
from dotenv import load_dotenv

load_dotenv()


class ModifyWordDocument:
    def __init__(self,data_dict):
        self.client = genai.Client()
        self.data_dict = data_dict
    
    def modify_document(self,query):
        res = self.client.models.generate_content(
            model='gemini-2.5-flash-lite',
            contents=[
                f"""
                You are given with the document in the format of a list whoose elements are dictionaries, the style key represents the text style and the content key refers to the content of that particular element.

                Your job is to transform the content key of the dictionary to modify the word document and make it more intuitive and readable
                File to be used: {self.data_dict}
                Topic to be transformed on: {query}

                Do not include any triple backticks in the final response.   

                The output must only include a list whoose elements are dictionaries             
"""
            ]
        )
        return res.text

    def modify_formatting(self,query):
        res = self.client.models.generate_content(
            model='gemini-2.5-flash-lite',
            contents=[
                f"""
                Consider the file: ```{self.data_dict}``` and also consider the users input ```{query}``` and return a dictionary with more than 1 key. The first key named content represents the name of the text

                In the passed dictionary: ```{self.data_dict}```, ```Normal``` key represents text which are not headings
                The second key is named formatting with contains another dictionary whoose keys are name of the formatting required, the value will be the option in that formatting

                The first key "content" cannot include headings, title as its key, these must be under the key text_type

                If you don't find specific words or sentences english(text in paragraph) leave it blank
                Consider words which will be eligible for formatting according to the userfrom ```{self.data_dict}``` instead of directly picking from ```{query}```
                
                GUIDELINES FOR RETURNING TEXT FOR FORMATTING
                1. THE KEY MUST BE THE TYPE OF FORMATTING COLOR,BOLD,ITALIC FOLLOWED BY A LIST CONTAINING THE POSSIBLE WORDS TO BE FORMATTED
                2. THESE SHOULD BE A DICTIONARY UNDER THE KEY FORMATTING
                3. IF YOU WANT TO RETURN THE COLOR; THE FORMAT WILL BE "color" FOLLOWED BY THE DICTIONARY WHICH SPECIFIES THE COLOR FOR CHOSEN HEADINGS,PARAGRAPHS  AND SPECIFY THE TEXT PRESENT IN THAT HEADINGS,PARAGRAPH, DONOT USE WORDS LIKE Heading 1,title,normal INSTEAD SPECIFY THE CONTENT OF THOSE HEADINGS

                GUIDELINES FOR RETURNING TEXT FOR ALIGNMENT
                1. THE KEY MUST BE THE SENTENCE WHICH HAS TO BE ALIGNED(CENTER,LEFT,RIGHT,JUSTIFIED) THE VALUE MUST BE THE TYPE OF THE ALIGNMENT
                2. PUT THIS UNDER THE KEY "alignment" WHICH IS UNDER THE KEY "formatting"

                GUIDELINES FOR RETURNING TEXT FOR FONT SIZE
                1. THE KEY MUST BE THE SENTENCE WHOOSE TEXT SIZE MUST BE ADJUSTED THE VALUE MUST BE THE FONTSIZE REQUIRED BY THE USER
                2. PUT THIS UNDER THE KEY "fontsize" WHICH IS UNDER THE KEY "formatting"
                Return that dictionary without any triple backticks at the beginning.

                


                The keys under formatting must not be in uppercase
                Ensure that you don't mess up the number of flower brackets
                """
            ]

        )
        res = res.text.replace('`','').replace('json','')
        res = eval(res)
        d = {}
        try:

            for key in res['formatting'].keys():
                if key == "bold":
                    for ele in res['formatting'][key]:
                        if not ele in d.keys():
                            d[ele] = {"text_style":"bold"}
                        
                        else:
                            d[ele]['text_style'] = "bold"
                
                elif key == "italic":
                    for ele in res['formatting'][key]:
                        if not ele in d.keys():
                            d[ele] = {"text_style":"italic"}
                        
                        else:
                            d[ele]['text_style'] = "italic"
                
                elif key == "underline":
                    for ele in res['formatting'][key]:
                        if not ele in d.keys():
                            d[ele] = {"text_style":"underline"}
                        
                        else:
                            d[ele]['text_style'] = "underline"
                
                elif key == "color":
                    for ele in res['formatting']['color'].keys():
                        if ele not in d:
                            d[ele] = {"color":res['formatting']['color'][ele]} 
                        
                        else:
                            d[ele]["color"] = res['formatting']['color'][ele]
                
                elif key == "alignment":
                    for ele in res['formatting']['alignment'].keys():
                        if ele not in d:
                            d[ele] = {"alignment":res['formatting']['alignment'][ele]}
                        
                        else:
                            d[ele]['alignment'] = res['formatting']['alignment'][ele]
            
            
                elif key == "fontsize":
                    for ele in res['formatting']['fontsize'].keys():
                        if ele not in d:
                            d[ele] = {"fontsize":res['formatting']['fontsize'][ele]}
                        
                        else:
                            d[ele]['fontsize'] = res['formatting']['fontsize'][ele]

        except:
            pass
        return d
doc  = ModifyWordDocument([{"style": "Title", "content": "Bridging the Gap: Reinforcement Learning and Agentic AI"}, {"style": "Heading 1", "content": "Understanding Reinforcement Learning: The Foundation"}, {"style": "Heading 2", "content": "Core Concept: Learning Through Interaction"}, {"style": "Normal", "content": "Reinforcement learning (RL) is a powerful machine learning paradigm where an agent learns optimal decision-making by interacting with an environment. The agent takes actions, observes their consequences (rewards or penalties), and adjusts its strategy to maximize cumulative future rewards."}, {"style": "Heading 2", "content": "Key Components: The RL Ecosystem"}, {"style": "Normal", "content": "At its heart, RL involves an agent, an environment, states (the current situation), actions (choices the agent can make), and rewards (feedback on actions). The agent's goal is to learn a policy—a strategy for choosing actions in different states—that leads to the highest expected long-term reward."}, {"style": "Heading 1", "content": "Introducing Agentic AI: Intelligence in Action"}, {"style": "Heading 2", "content": "Defining Agentic AI"}, {"style": "Normal", "content": "Agentic AI refers to artificial intelligence systems designed to act autonomously and proactively in complex environments. These agents possess capabilities like planning, reasoning, perception, and the ability to pursue goals with a degree of independence."}, {"style": "Heading 2", "content": "Characteristics of Agentic Systems"}, {"style": "Normal", "content": "Agentic AI systems are characterized by their ability to perceive their surroundings, make decisions, and execute actions to achieve objectives. They often operate with limited human oversight and can adapt to dynamic and unpredictable situations."}, {"style": "Heading 1", "content": "The Synergy: How RL and LLMs Power Agentic AI"}, {"style": "Heading 2", "content": "RL as the Learning Engine for Agentic AI"}, {"style": "Normal", "content": "Reinforcement learning provides a robust framework for agentic AI to learn how to operate effectively. By training agents using RL, we can imbue them with the ability to discover optimal strategies through experience, rather than explicit programming for every possible scenario."}, {"style": "Heading 2", "content": "The Role of Large Language Models (LLMs) in Agentic AI"}, {"style": "Normal", "content": "Large Language Models (LLMs) are revolutionizing agentic AI by providing sophisticated language understanding, generation, and reasoning capabilities. LLMs can act as the \"brain\" of an agent, enabling it to interpret complex instructions, plan multi-step tasks, and communicate its intentions effectively. They allow agents to process and act upon unstructured text data, a capability crucial for many real-world applications."}, {"style": "Heading 2", "content": "LLMs Enhancing Agentic Capabilities: Planning, Reasoning, and Tool Use"}, {"style": "Normal", "content": "LLMs enhance agentic AI by facilitating advanced planning, where agents can break down complex goals into actionable sub-tasks. Their reasoning abilities allow them to infer context and make informed decisions, while their capacity for tool use enables them to interact with external systems and APIs, expanding their operational scope significantly."}, {"style": "Heading 2", "content": "From Trial-and-Error to Goal Achievement with LLMs and RL"}, {"style": "Normal", "content": "The trial-and-error learning inherent in RL is crucial for agentic AI. When combined with LLMs, this process becomes more intelligent. LLMs can help agents understand the success or failure of an action by interpreting feedback, leading to more efficient learning. This synergy allows agents to explore the consequences of their actions, gradually refining their behavior to achieve complex goals, such as navigating a city, managing a complex system, or performing delicate robotic tasks, with a deeper understanding of the task at hand."}, {"style": "Heading 2", "content": "Navigating Exploration-Exploitation in LLM-Powered Agentic AI"}, {"style": "Normal", "content": "A key challenge in agentic AI is balancing exploration (trying new strategies) with exploitation (using known successful strategies). LLMs can aid in this by generating diverse and coherent exploration strategies based on their understanding of the environment and goals. RL algorithms then help refine these strategies, enabling LLM-powered agentic systems to continuously improve and adapt."}, {"style": "Heading 1", "content": "Applications and Future Frontiers of LLMs in Agentic AI"}, {"style": "Heading 2", "content": "Real-World Impact of LLM-Powered Agentic AI"}, {"style": "Normal", "content": "The convergence of LLMs and agentic AI is driving innovation in conversational agents that can perform complex tasks, automated content creation, sophisticated personal assistants, intelligent customer service bots, and AI systems that can autonomously manage and optimize digital workflows. These agents leverage LLMs for understanding user intent and generating human-like responses, while RL fine-tunes their behavior for optimal task completion."}, {"style": "Heading 2", "content": "Advancing Towards General Intelligence with LLMs and RL"}, {"style": "Normal", "content": "The integration of LLMs with RL represents a significant leap towards developing more general-purpose AI agents. These agents can handle a wider range of tasks and environments due to the LLMs' broad knowledge and reasoning abilities, augmented by RL's capacity for adaptive learning. Future research focuses on enhancing the sample efficiency of RL, improving the generalization capabilities of LLM-based agents, and ensuring the safety, reliability, and explainability of these increasingly intelligent systems."}])
res = doc.modify_formatting(input("Enter something..."))

print(res)