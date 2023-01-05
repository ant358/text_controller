import requests
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable
import logging

logger = logging.getLogger(__name__)

# import ids from the text source database
def get_pageids() -> list[str]:
    """
    Get the pageids from the text database 
    send a GET request to the text database to get the pageids

    Returns:
        list[str]: list of pageids
    """
    try:
        available_pageids = requests.get("http://host.docker.internal:8080/get_pageids").json()
        return available_pageids["pageids: "]
    except requests.exceptions.ConnectionError:
        logger.error("Could not connect to the text database")
        return []

# get the title of a page
def get_title(pageid: str) -> str:
    """
    Get the title of a page
    send a GET request to the text database to get the title of a page

    Args:
        pageid (str): pageid of the page

    Returns:
        str: title of the page
    """
    try:
        article = requests.get(f"http://host.docker.internal:8080/return_article/{pageid}").json()
        return article["title"]
    except requests.exceptions.ConnectionError:
        logger.error("Could not connect to the text database")
        return ""


# query the graph database to get the pageids
def get_pageids_from_graph() -> list[str]:
    """
    Get the pageids from the graph database
    query the graph database to get the pageids

    Returns:
        list[str]: list of pageids
    """
    try:
        driver = GraphDatabase.driver("bolt://localhost:7687")
        with driver.session() as session:
            result = session.run("MATCH (n:Page) RETURN n.pageId")
            return [record['n.pageId'] for record in result]
    except ServiceUnavailable:
        logger.error("Could not connect to the graph database")
        return []

# get the current containers on the network
def get_containers() -> list[str]:
    """
    Get the current containers on the network

    Returns:
        list[str]: list of containers
    """
    pass