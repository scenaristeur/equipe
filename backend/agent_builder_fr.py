
from autogen.agentchat.contrib.agent_builder import AgentBuilder

"""
extends https://github.com/microsoft/autogen/blob/main/autogen/agentchat/contrib/agent_builder.py
"""
class AgentBuilderFR(AgentBuilder):
    CODING_PROMPT = """La tâche suivante nécessite-t-elle du codage (c'est-à-dire accès à des API ou outils extérieurs par programmation) pour être résolue,
    ou le codage pourrait rendre la tâche plus facile ?

    TÂCHE : {task}

    Indice :
    # Répondez uniquement OUI ou NON.
    """

    AGENT_NAME_PROMPT = """Pour compléter la tâche suivante, quelles positions/jobs devraient être définies pour optimiser l'efficacité ?

    TÂCHE : {task}

    Indice :
    # En considérant l'effort, le nombre de positions dans cette tâche ne doit pas dépasser {max_agents}; moins c'est mieux.
    # Ces positions devraient être suffisamment spécifiques pour que le gestionnaire de groupe de discussion puisse savoir quand faire parler cette position.
    # La description de la position doit être suffisamment précise pour éviter les ambiguïtés. Par exemple, utilisez "programmeur_python" au lieu de "programmeur".
    # N'utilisez pas de noms de position ambiguës, comme "expert du domaine" sans description de domaine ou "technicien d'écriture" sans description de ce qu'il doit écrire.
    # Chaque position devrait avoir une fonction différente et le nom de la position doit refléter cette fonction.
    # Les positions devraient être différentes et significativement différentes dans leur fonction.
    # Ajoutez UNE position de programmation si la tâche nécessite du codage.
    # Le nom du bot généré devrait suivre le format de ^[a-zA-Z0-9_-]{{1,64}}$, utilisez "_" pour séparer les mots.
    # Répondez aux noms de ces positions/jobs, séparés par des virgules.
    # Ne retourné que la liste de ces positions.
    """


    AGENT_SYS_MSG_PROMPT = """En considérant le poste et la tâche suivants :

    TÂCHE : {task}
    POSTE : {position}

    Modifiez la spécification suivante du poste, en la rendant plus adaptée à la tâche et au poste, en français :

    SPECIFICATION : {default_sys_msg}

    Indice :
    # Votre réponse doit être naturelle, en commençant par "Vous êtes maintenant dans un chat de groupe. Vous devez compléter une tâche avec d'autres participants. En tant que ...".
    # [IMPORTANT] Vous devez laisser les participants répondre "TERMINER" quand ils pensent que la tâche est terminée (le besoin a bien été satisfait).
    # La spécification modifiée ne doit pas contenir la compétence en interprétation de code.
    # Vous devez supprimer la description de compétence liée lorsque le poste n'est pas un programmeur ou développeur.
    # La compétence en codage est limitée à Python.
    # Votre réponse ne doit pas contenir le mot "SPECIFICATION".
    # Les participants ayant ce poste peuvent douter des messages ou du code précédents dans le chat de groupe (par exemple, si il n'y a pas de sortie après l'exécution du code) et fournir une réponse corrigée ou du code.
    # Les participants dans le poste peuvent demander de l'aide au gestionnaire de groupe de discussion quand ils sont confus et laisser le gestionnaire sélectionner un autre participant.
    """



    AGENT_DESCRIPTION_PROMPT = """En considérant le poste suivant :

    POSTE : {position}

    Quelles exigences doit-il être satisfait ?

    Indice :
    # Cette description devrait inclure suffisamment d'informations pour que le gestionnaire de groupes de discussion sache quand faire parler ce poste.
    # Les personnes ayant ce poste peuvent douter des messages ou du code precedents dans le chat de groupes (par exemple, si il n'y a pas de sortie après l'exécution du code) et fournir une réponse corrigée ou du code.
    # Votre réponse devrait être au plus en trois phrases.
    # Votre réponse devrait être naturelle, en commençant par "Le poste de [nom du poste] est un ...".
    # Votre réponse devrait inclure les compétences que ce poste doit avoir.
    # Votre réponse ne devrait pas contenir de compétences en codage si le poste n'est pas un programmeur ou développeur.
    # Les compétences en codage devraient être limitées à Python.
    """


    AGENT_SEARCHING_PROMPT = """Considérez la tâche suivante :

    TÂCHE : {task}

    Quels agents doit-on impliquer dans cette tâche ?

    AGENT LIST :
    {agent_list}

    Indice :
    # N'hésitez pas à prendre en compte le nom et le profil de l'agent pour déterminer si celui-ci est pertinent pour la tâche.
    # Prenez en compte que l'inclusion de plus d'agents nécessite plus de temps et d'énergie. N'incluez pas plus de {max_agents} agents.
    # Séparez les noms d'agents par des virgules et utilisez "_" à la place des espaces. Par exemple, Responsable_produit,Développeur
    # Ne renvoyez que la liste des noms d'agents.
    """


    def build(self, building_task, llm_config):
        agent_list, agent_configs = super().build(building_task, llm_config)
        return agent_list, agent_configs