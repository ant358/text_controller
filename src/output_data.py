from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable
from input_data import get_title
import logging

logger = logging.getLogger(__name__)


# write to the database
def write_document_nodes(pageids: list[str]):
    """
    Write the document nodes to the graph database
    """
    # get the driver
    driver = GraphDatabase.driver("bolt://localhost:7687")
    # create the session
    with driver.session() as session:
        # create the nodes
        for pageid in pageids:
            # get the title
            title = get_title(pageid)
            # create the node
            session.run("MERGE (n:Document {pageId: $pageid, title: $title})", pageid=pageid, title=title)
            # log the creation
            logger.info(f"Created node for {pageid}")
