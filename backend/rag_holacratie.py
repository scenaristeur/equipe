# https://raw.githubusercontent.com/holacracyone/Holacracy-Constitution-4.1-FRENCH/master/Constitution-Holacracy.md

# https://microsoft.github.io/autogen/docs/notebooks/agentchat_groupchat_RAG/



"""
Première réponse avec igora + LLM_MODEL_NAME="llama-pro-8b-instruct.Q2_K.gguf"


Product_Manager (to chat_manager):

Bien reçu le point de vue du product manager. Il est important d'avoir une organisation résiliente basée sur le système décrit dans la constitution de L'Holacratie. Pour créer cette application, il faudra suivre les étapes suivantes :

1. Trouver un point de tension à résoudre en utilisant le système décrit dans la constitution de L'Holacratie.
2. Créer et gérer les utilisateurs, les cercles, les premiers liens, les tensions, les liens transverses, les liens d’invitation, les liens d’invitation vers le Cercle d’Ancrage... en utilisant le système décrit.
3. Établir un plan d'action étape par étape pour la construction de l'application, en utilisant le système décrit.
4. Commence par les fonctionnalités les plus structurelles, et incrémente les fonctionnalités petit à petit, SEULEMENT lorsque la précédente fonctionnalité est terminée, testée et validée.

Enfin, pour que l'application soit opérationnelle, il faudra également s'assurer que toutes les questions pratiques liées à la création de l'application soient résolues. Par exemple, mettre en place un système de gestion des données, une infrastructure de stockage, une architecture d'accès découpé pour permettre une meilleure sécurité et performance, etc.

Enfin, il faudra également s'assurer que l'application est testée et validée à chaque étape du processus de développement pour garantir que les fonctionnalités soient correctement implémentées et que l'application répond aux besoins des utilisateurs.
"""



# from agent_builder_fr import AgentBuilderFR

from typing_extensions import Annotated
import chromadb

import autogen
from autogen import AssistantAgent,  config_list_from_json
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent

#config_file_or_env = "OAI_CONFIG_LIST"

# config_list = autogen.config_list_from_json(config_file_or_env, filter_dict={"model": ["gpt-4-1106-preview", "gpt-4"]})
config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")


print("LLM models: ", [config_list[i]["model"] for i in range(len(config_list))])

llm_config = {
   # "timeout": 60,
    "temperature": 0,
    "config_list": config_list,
}


def termination_msg(x):
    return isinstance(x, dict) and "TERMINATE" == str(x.get("content", ""))[-9:].upper()


boss = autogen.UserProxyAgent(
    name="Boss",
    is_termination_msg=termination_msg,
    human_input_mode="NEVER",
    code_execution_config=False,  # we don't want to execute code in this case.
    default_auto_reply="Reply `TERMINATE` if the task is done.",
    description="The boss who ask questions and give tasks.",
)

boss_aid = RetrieveUserProxyAgent(
    name="Boss_Assistant",
    is_termination_msg=termination_msg,
    human_input_mode="NEVER",
    max_consecutive_auto_reply=3,
    retrieve_config={
        "task": "code",
        # "docs_path": "https://raw.githubusercontent.com/microsoft/FLAML/main/website/docs/Examples/Integrate%20-%20Spark.md",
        "docs_path": "https://raw.githubusercontent.com/holacracyone/Holacracy-Constitution-4.1-FRENCH/master/Constitution-Holacracy.md",
        "chunk_token_size": 1000,
        "model": config_list[0]["model"],
        "client": chromadb.PersistentClient(path="/tmp/chromadb"),
        "collection_name": "groupchat",
        "get_or_create": True,
    },
    code_execution_config=False,  # we don't want to execute code in this case.
    description="Assistant who has extra content retrieval power for solving difficult problems.",
)


coder_llm_config = llm_config.copy()
coder = AssistantAgent(
    name="Senior_Python_Engineer",
    is_termination_msg=termination_msg,
    system_message="You are a senior python engineer, you provide python code to answer questions. Reply `TERMINATE` in the end when everything is done.",
    llm_config={"config_list": config_list},
    description="Senior Python Engineer who can write code to solve problems and answer questions.",
)

pm_llm_config = llm_config.copy()
pm = autogen.AssistantAgent(
    name="Product_Manager",
    is_termination_msg=termination_msg,
    system_message="You are a product manager. Reply `TERMINATE` in the end when everything is done.",
    llm_config={"config_list": config_list},
    description="Product Manager who can design and plan the project.",
)

reviewer_llm_config = llm_config.copy()
reviewer = autogen.AssistantAgent(
    name="Code_Reviewer",
    is_termination_msg=termination_msg,
    system_message="You are a code reviewer. Reply `TERMINATE` in the end when everything is done.",
    llm_config={"config_list": config_list},
    description="Code Reviewer who can review the code.",
)

PROBLEM = """Je souhaite créer une organisation résiliente se basant sur le système décrit dans la constitution de L'Holacratie. 
Tu dois créer l'application web/Streamlit qui permet aux utilisateur d'interagir avec cette organisation et d'obtenir des informations sur l'organisation.
(Créer et gérer les utilisateurs, les cercles, les premiers liens, les tensions, les liens transverses, les liens d’invitation,
 les liens d’invitation et les liens d’invitation vers le Cercle d’Ancrage... ).
 Etablit un plan d'action étape par étape pour la construction de l'application, en utilisant le système décrit : 
 Trouve une tension, décrit là et continue le processus sur cette tension jusqu'à sa résolution.
 Commence par les fonctionnalités les plus structurelles, et incrémente les fonctionnalités petit à petit, SEULEMENT lorsque la précédente fonctionnalité est terminée, testée et validée.
 !!! CONSTRUIS CETTE APPLICATION !!!"""


def _reset_agents():
    boss.reset()
    boss_aid.reset()
    coder.reset()
    pm.reset()
    reviewer.reset()


def rag_chat():
    _reset_agents()
    groupchat = autogen.GroupChat(
        agents=[boss_aid, pm, coder, reviewer], messages=[], max_round=12, speaker_selection_method="round_robin"
    )
    manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

    # Start chatting with boss_aid as this is the user proxy agent.
    boss_aid.initiate_chat(
        manager,
        message=boss_aid.message_generator,
        problem=PROBLEM,
        n_results=3,
    )


def norag_chat():
    _reset_agents()
    groupchat = autogen.GroupChat(
        agents=[boss, pm, coder, reviewer],
        messages=[],
        max_round=12,
        speaker_selection_method="auto",
        allow_repeat_speaker=False,
    )
    manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

    # Start chatting with the boss as this is the user proxy agent.
    boss.initiate_chat(
        manager,
        message=PROBLEM,
    )


def call_rag_chat():
    _reset_agents()

    # In this case, we will have multiple user proxy agents and we don't initiate the chat
    # with RAG user proxy agent.
    # In order to use RAG user proxy agent, we need to wrap RAG agents in a function and call
    # it from other agents.
    def retrieve_content(
        message: Annotated[
            str,
            "Refined message which keeps the original meaning and can be used to retrieve content for code generation and question answering.",
        ],
        n_results: Annotated[int, "number of results"] = 3,
    ) -> str:
        boss_aid.n_results = n_results  # Set the number of results to be retrieved.
        # Check if we need to update the context.
        update_context_case1, update_context_case2 = boss_aid._check_update_context(message)
        if (update_context_case1 or update_context_case2) and boss_aid.update_context:
            boss_aid.problem = message if not hasattr(boss_aid, "problem") else boss_aid.problem
            _, ret_msg = boss_aid._generate_retrieve_user_reply(message)
        else:
            _context = {"problem": message, "n_results": n_results}
            ret_msg = boss_aid.message_generator(boss_aid, None, _context)
        return ret_msg if ret_msg else message

    boss_aid.human_input_mode = "NEVER"  # Disable human input for boss_aid since it only retrieves content.

    for caller in [pm, coder, reviewer]:
        d_retrieve_content = caller.register_for_llm(
            description="retrieve content for code generation and question answering.", api_style="function"
        )(retrieve_content)

    for executor in [boss, pm]:
        executor.register_for_execution()(d_retrieve_content)

    groupchat = autogen.GroupChat(
        agents=[boss, pm, coder, reviewer],
        messages=[],
        max_round=12,
        speaker_selection_method="auto", #"round_robin",
        allow_repeat_speaker=False,
    )

    manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

    # Start chatting with the boss as this is the user proxy agent.
    boss.initiate_chat(
        manager,
        message=PROBLEM,
    )

norag_chat()