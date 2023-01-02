import requests
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable
import logging


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
        logging.error("Could not connect to the text database")
        return []


# query the graph database to get the pageids
def get_pageids_from_graph() -> list[str]:
    """
    Get the pageids from the graph database
    query the graph database to get the pageids

    Returns:
        list[str]: list of pageids
    """
    try:
        driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))
        with driver.session() as session:
            result = session.run("MATCH (n:Page) RETURN n.pageId")
            return [record['n.pageId'] for record in result]
    except ServiceUnavailable:
        logging.error("Could not connect to the graph database")
        return []
