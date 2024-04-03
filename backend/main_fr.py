from autogen import GroupChat, GroupChatManager, UserProxyAgent, ConversableAgent, config_list_from_json

from agent_builder_fr import AgentBuilderFR

config_file_or_env = "OAI_CONFIG_LIST"
llm_config = {"temperature": 0.3}
# config_list = autogen.config_list_from_json(config_file_or_env, filter_dict={"model": ["gpt-4-1106-preview", "gpt-4"]})
config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")


    

def start_task(execution_task: str, agent_list: list):
    group_chat = GroupChat(agents=agent_list, messages=[], max_round=12)
    manager = GroupChatManager(groupchat=group_chat, llm_config={"config_list": config_list, **llm_config})
    agent_list[0].initiate_chat(manager, message=execution_task)

builder = AgentBuilderFR(
    # config_file_or_env=config_file_or_env, builder_model="gpt-4-1106-preview", agent_model="gpt-4-1106-preview"
    config_file_or_env=config_file_or_env
)

building_task = """Générer des agents capable de trouver des écoles de surf et des hébergements à proximité 
en programmant et en analysant les sites internet en relation avec le surf et l'hébergement dans les landes."""

agent_list, agent_configs = builder.build(building_task, llm_config)

start_task(
    execution_task="""Trouve moi un spot sympa dans Les Landes, pour le mois d'août 2024, entre Mimizan (Landes) et Moliets-et-Mâa (Landes) pour apprendre le surf avec mon fils de 13 ans, on aimerait effectuer un satge de 3 ou 4 jours pour commencer.
    Trouve nous également un hébergement à moins de 30€ la nuit pour deux à proximité du spot de surf. N'hésite pas à proposer des solution originales.""",
    agent_list=agent_list,
)
